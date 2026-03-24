import logging
from flask import jsonify, request, send_file
from io import BytesIO
from datetime import datetime
from models import db, Licenca, TipoLicenca, EstadoLicencaEnum, Person, Despacho
import base64
import unicodedata

# Configurar logger mais detalhado
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)

class LicencaController:

    @staticmethod
    def get_all():
        try:
            logger.info("🔍 [GET ALL LICENÇAS] Iniciando busca de todas as licenças")
            
            licencas = Licenca.query.all()
            logger.info(f"📊 [GET ALL LICENÇAS] Encontradas {len(licencas)} licenças no banco de dados")
            
            result = []
            for l in licencas:
                result.append({
                    'id': l.id,
                    'person_id': l.person_id,
                    'person_name': l.person.fullname if l.person else None,
                    
                    # Tipo da licença
                    'tipo_id': l.tipo_id,
                    'tipo_description': l.tipo.description if l.tipo else None,
                    
                    # Despacho e beneficiário
                    'despacho_id': l.despacho_id,
                    'despacho_titulo': (
                        f"{l.despacho.titulo} - {l.despacho.person.fullname}"
                        if l.despacho and l.despacho.person else 
                        (l.despacho.titulo if l.despacho else None)
                    ),
                    "person_image": (
                        base64.b64encode(l.despacho.person.image).decode('utf-8')
                        if l.despacho and l.despacho.person and l.despacho.person.image else None
                    ),
                    'motivo': l.motivo,
                    'data_inicio': l.data_inicio.isoformat() if l.data_inicio else None,
                    'data_fim': l.data_fim.isoformat() if l.data_fim else None,
                    'estado': l.estado.value,
                    'observacao': l.observacao,
                    'anexo_nome': l.anexo_nome,
                    'criado_em': l.criado_em.isoformat() if l.criado_em else None
                })
            
            logger.info(f"✅ [GET ALL LICENÇAS] Retornando {len(result)} licenças com sucesso")
            return jsonify(result), 200
            
        except Exception as e:
            logger.exception(f"💥 [GET ALL LICENÇAS] ERRO CRÍTICO ao listar licenças: {str(e)}")
            return jsonify({'error': 'Erro interno do servidor ao buscar licenças'}), 500

    @staticmethod
    def get_by_id(id):
        try:
            logger.info(f"🔍 [GET BY ID LICENÇA] Buscando licença ID: {id}")
            
            l = Licenca.query.get(id)
            if not l:
                logger.warning(f"⚠️ [GET BY ID LICENÇA] Licença não encontrada: {id}")
                return jsonify({'message': 'Licença não encontrada'}), 404

            logger.info(f"✅ [GET BY ID LICENÇA] Licença encontrada: ID {l.id} - {l.person.fullname if l.person else 'Sem pessoa'}")
            
            return jsonify({
                'id': l.id,
                'person_id': l.person_id,
                'person_name': l.person.fullname if l.person else None,
                'tipo_id': l.tipo_id,
                'tipo_description': l.tipo.description if l.tipo else None,
                'despacho_id': l.despacho_id,
                'despacho_numero': l.despacho.numero if l.despacho else None,
                'motivo': l.motivo,
                'data_inicio': l.data_inicio.isoformat(),
                'data_fim': l.data_fim.isoformat(),
                'estado': l.estado.value,
                'observacao': l.observacao,
                'anexo_nome': l.anexo_nome,
                'criado_em': l.criado_em.isoformat() if l.criado_em else None
            }), 200
            
        except Exception as e:
            logger.exception(f"💥 [GET BY ID LICENÇA] ERRO ao buscar licença {id}: {str(e)}")
            return jsonify({'error': f'Erro ao buscar licença: {str(e)}'}), 500

    @staticmethod
    def create():
        try:
            # Log do request
            logger.info(f"🆕 [CREATE LICENÇA] Iniciando criação de nova licença")
            logger.info(f"📨 [CREATE LICENÇA] Content-Type: {request.content_type}")
            logger.info(f"📨 [CREATE LICENÇA] Método: {request.method}")
            logger.info(f"📨 [CREATE LICENÇA] Headers: {dict(request.headers)}")

            data = request.form.to_dict()
            file = request.files.get('anexo')

            logger.info(f"📝 [CREATE LICENÇA] Dados recebidos no form: {data}")
            logger.info(f"📎 [CREATE LICENÇA] Ficheiro anexo: {'Sim' if file else 'Não'}")

            # Validação de campos obrigatórios
            person_id = data.get('person_id')
            tipo_id = data.get('tipo_id')
            despacho_id = data.get('despacho_id')
            data_inicio = data.get('data_inicio')
            data_fim = data.get('data_fim')

            logger.info(f"🔍 [CREATE LICENÇA] Validando campos - Person: {person_id}, Tipo: {tipo_id}, Início: {data_inicio}, Fim: {data_fim}")

            if not person_id or not tipo_id or not data_inicio or not data_fim:
                logger.warning("⚠️ [CREATE LICENÇA] Campos obrigatórios faltando")
                return jsonify({'message': 'Campos obrigatórios: person_id, tipo_id, data_inicio, data_fim'}), 400

            # Verificar se as entidades relacionadas existem
            logger.info(f"🔍 [CREATE LICENÇA] Verificando existência das entidades relacionadas")
            
            if not Person.query.get(person_id):
                logger.warning(f"⚠️ [CREATE LICENÇA] Pessoa não encontrada: ID {person_id}")
                return jsonify({'message': 'Pessoa não encontrada'}), 404
            
            if not TipoLicenca.query.get(tipo_id):
                logger.warning(f"⚠️ [CREATE LICENÇA] Tipo de licença não encontrado: ID {tipo_id}")
                return jsonify({'message': 'Tipo de licença não encontrado'}), 404
            
            if despacho_id and not Despacho.query.get(despacho_id):
                logger.warning(f"⚠️ [CREATE LICENÇA] Despacho não encontrado: ID {despacho_id}")
                return jsonify({'message': 'Despacho não encontrado'}), 404

            logger.info("✅ [CREATE LICENÇA] Todas as validações passaram")

            # Criar nova licença
            nova_licenca = Licenca(
                person_id=person_id,
                tipo_id=tipo_id,
                despacho_id=despacho_id if despacho_id else None,
                motivo=data.get('motivo'),
                data_inicio=datetime.fromisoformat(data_inicio).date(),
                data_fim=datetime.fromisoformat(data_fim).date(),
                observacao=data.get('observacao'),
                estado=EstadoLicencaEnum[data.get('estado', 'PENDENTE').upper()] if data.get('estado') else EstadoLicencaEnum.PENDENTE
            )

            logger.info(f"📋 [CREATE LICENÇA] Nova licença criada em memória: Person {person_id}, Tipo {tipo_id}")

            # Processar anexo se existir
            if file:
                logger.info(f"📎 [CREATE LICENÇA] Processando anexo: {file.filename} ({file.mimetype})")
                if file.content_length and file.content_length > 10 * 1024 * 1024:  # 10MB limit
                    logger.warning(f"⚠️ [CREATE LICENÇA] Ficheiro muito grande: {file.content_length} bytes")
                    return jsonify({'error': 'Ficheiro muito grande. Máximo 10MB permitido.'}), 400
                
                nova_licenca.anexo_nome = file.filename
                nova_licenca.anexo_tipo = file.mimetype
                nova_licenca.anexo_dados = file.read()
                logger.info(f"✅ [CREATE LICENÇA] Anexo processado - Tamanho: {len(nova_licenca.anexo_dados)} bytes")

            # Salvar no banco de dados
            db.session.add(nova_licenca)
            db.session.commit()
            
            logger.info(f"✅ [CREATE LICENÇA] Licença criada com sucesso. ID: {nova_licenca.id}")
            
            return jsonify({
                'message': 'Licença criada com sucesso', 
                'id': nova_licenca.id,
                'person_id': nova_licenca.person_id,
                'tipo_id': nova_licenca.tipo_id
            }), 201
            
        except Exception as e:
            db.session.rollback()
            logger.exception(f"💥 [CREATE LICENÇA] ERRO CRÍTICO ao criar licença: {str(e)}")
            return jsonify({'error': 'Erro interno do servidor ao criar licença'}), 500

    @staticmethod
    def update(id):
        try:
            logger.info(f"✏️ [UPDATE LICENÇA] Iniciando atualização da licença ID: {id}")
            
            licenca = Licenca.query.get(id)
            if not licenca:
                logger.warning(f"⚠️ [UPDATE LICENÇA] Licença não encontrada: {id}")
                return jsonify({'error': 'Licença não encontrada'}), 404

            data = request.form.to_dict()
            file = request.files.get('anexo')

            logger.info(f"📝 [UPDATE LICENÇA] Dados recebidos: {data}")
            logger.info(f"📎 [UPDATE LICENÇA] Ficheiro anexo: {'Sim' if file else 'Não'}")

            campos_atualizados = []

            # Atualizar campos básicos
            if 'person_id' in data:
                licenca.person_id = data['person_id']
                campos_atualizados.append('person_id')

            if 'tipo_id' in data:
                licenca.tipo_id = data['tipo_id']
                campos_atualizados.append('tipo_id')

            if 'despacho_id' in data:
                licenca.despacho_id = data['despacho_id'] or None
                campos_atualizados.append('despacho_id')

            if 'motivo' in data:
                licenca.motivo = data['motivo']
                campos_atualizados.append('motivo')

            if 'data_inicio' in data and data['data_inicio']:
                licenca.data_inicio = datetime.fromisoformat(data['data_inicio']).date()
                campos_atualizados.append('data_inicio')

            if 'data_fim' in data and data['data_fim']:
                licenca.data_fim = datetime.fromisoformat(data['data_fim']).date()
                campos_atualizados.append('data_fim')

            if 'observacao' in data:
                licenca.observacao = data['observacao']
                campos_atualizados.append('observacao')

            # 🆕 Atualizar estado da licença (novo bloco)
            if 'estado' in data and data['estado']:
                estado_input = data['estado'].upper()
                try:
                    # Tenta primeiro pelo NAME
                    licenca.estado = EstadoLicencaEnum[estado_input]
                except KeyError:
                    # Tenta pelo VALUE (caso front-end envie "Concluído", "Pendente", etc.)
                    for e in EstadoLicencaEnum:
                        if e.value.upper() == estado_input:
                            licenca.estado = e
                            break
                    else:
                        logger.warning(f"⚠️ [UPDATE LICENÇA] Estado inválido: {data['estado']}")


            # 📎 Atualizar anexo se fornecido
            if file and file.filename:
                logger.info(f"📎 [UPDATE LICENÇA] Atualizando anexo: {file.filename}")
                if file.content_length and file.content_length > 10 * 1024 * 1024:
                    logger.warning(f"⚠️ [UPDATE LICENÇA] Ficheiro muito grande: {file.content_length} bytes")
                    return jsonify({'error': 'Ficheiro muito grande. Máximo 10MB permitido.'}), 400
                    
                licenca.anexo_nome = file.filename
                licenca.anexo_tipo = file.mimetype
                licenca.anexo_dados = file.read()
                campos_atualizados.append('anexo')

            db.session.commit()
            
            logger.info(f"✅ [UPDATE LICENÇA] Licença {id} atualizada com sucesso. Campos modificados: {campos_atualizados}")
            
            return jsonify({
                'message': 'Licença atualizada com sucesso',
                'id': licenca.id,
                'campos_atualizados': campos_atualizados
            }), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"💥 [UPDATE LICENÇA] ERRO ao atualizar licença {id}: {str(e)}")
            return jsonify({'error': 'Erro interno do servidor ao atualizar licença'}), 500


    @staticmethod
    def delete(id):
        try:
            logger.info(f"🗑️ [DELETE LICENÇA] Iniciando exclusão da licença ID: {id}")
            
            licenca = Licenca.query.get(id)
            if not licenca:
                logger.warning(f"⚠️ [DELETE LICENÇA] Licença não encontrada: {id}")
                return jsonify({'error': 'Licença não encontrada'}), 404

            db.session.delete(licenca)
            db.session.commit()
            
            logger.info(f"✅ [DELETE LICENÇA] Licença excluída com sucesso: {id}")
            return jsonify({'message': 'Licença excluída com sucesso'}), 200
            
        except Exception as e:
            db.session.rollback()
            logger.exception(f"💥 [DELETE LICENÇA] ERRO ao excluir licença {id}: {str(e)}")
            return jsonify({'error': 'Erro interno do servidor ao excluir licença'}), 500

    @staticmethod
    def download_anexo(id):
        try:
            licenca = Licenca.query.get(id)
            if not licenca:
                return jsonify({'error': 'Licença não encontrada'}), 404

            if not licenca.anexo_dados:
                return jsonify({'error': 'Anexo não encontrado'}), 404

            # Garantir que o nome do arquivo seja seguro para download
            nome_arquivo = licenca.anexo_nome or 'anexo'
            mimetype = licenca.anexo_tipo or 'application/octet-stream'

            return send_file(
                BytesIO(licenca.anexo_dados),
                as_attachment=True,
                download_name=nome_arquivo,
                mimetype=mimetype
            )
        except Exception as e:
            logger.exception(f"Erro ao baixar anexo {id}: {str(e)}")
            return jsonify({'error': 'Erro interno ao baixar anexo'}), 500