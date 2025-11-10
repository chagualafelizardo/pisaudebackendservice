import logging
import base64
from flask import jsonify, request
from datetime import datetime

from models import (
    db,
    NotaEnvio,
    NotaEnvioItem,
    NotaEnvioDocument,
    TipoItem,
    Item,
    SyncStatusEnum
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

VALID_SYNC_STATUS = [e.value for e in SyncStatusEnum]

# ======================================================
# 🔹 Configuração de Logging Global
# ======================================================
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] - %(message)s"
)
logger = logging.getLogger("NotaEnvioController")

VALID_SYNC_STATUS = [e.value for e in SyncStatusEnum]


class NotaEnvioController:

   
    # ======================================================
    # 🔹 Serialização COMPLETA
    # ======================================================
    @staticmethod
    def serialize(n: NotaEnvio):
        return {
            'id': n.id,
            'numero_nota': n.numero_nota,
            'tipo_item_id': n.tipo_item_id,
            'tipo_item_nome': n.tipo_item.nome if n.tipo_item else None,  # ✅ Nome do tipo de item
            'data_envio': n.data_envio.isoformat() if n.data_envio else None,  # ✅ Data de envio
            'origem': n.origem,
            'destino': n.destino,
            'observacoes': n.observacoes,
            'user': n.user,
            'syncStatus': n.syncStatus.value if n.syncStatus else None,
            'syncStatusDate': n.syncStatusDate.isoformat() if n.syncStatusDate else None,
            'createAt': n.createAt.isoformat() if n.createAt else None,
            'updateAt': n.updateAt.isoformat() if n.updateAt else None,
            'itens': [
                {
                    'id': i.id,
                    'item_id': i.item_id,
                    'item_nome': i.item.designacao if i.item else None,
                    'quantidade_enviada': i.quantidade_enviada
                } for i in n.itens
            ],
            'documentos': [  # ✅ Lista COMPLETA de documentos
                {
                    'id': d.id,
                    'nome_arquivo': d.nome_arquivo,
                    'tipo_mime': d.tipo_mime,
                    'dados_arquivo': base64.b64encode(d.dados_arquivo).decode('utf-8')
                        if d.dados_arquivo else None,
                    'tamanho_bytes': len(d.dados_arquivo) if d.dados_arquivo else 0
                } for d in n.documentos
            ]
        }

    # ======================================================
    # 🔹 Listar todas - VERSÃO CORRIGIDA
    # ======================================================
    @staticmethod
    def get_all():
        try:
            # Carrega todos os relacionamentos necessários
            notas = NotaEnvio.query.options(
                db.joinedload(NotaEnvio.tipo_item),
                db.joinedload(NotaEnvio.itens).joinedload(NotaEnvioItem.item),
                db.joinedload(NotaEnvio.documentos)
            ).all()
            
            logger.info(f"📋 Encontradas {len(notas)} notas de envio")
            
            # Usa a serialização completa
            resultado = [NotaEnvioController.serialize(n) for n in notas]
            
            return jsonify(resultado), 200
            
        except Exception as e:
            logger.exception("❌ Erro ao buscar notas de envio")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 Buscar por ID - VERSÃO CORRIGIDA
    # ======================================================
    @staticmethod
    def get_by_id(id):
        try:
            # Carrega todos os relacionamentos necessários
            nota = NotaEnvio.query.options(
                db.joinedload(NotaEnvio.tipo_item),
                db.joinedload(NotaEnvio.itens).joinedload(NotaEnvioItem.item),
                db.joinedload(NotaEnvio.documentos)
            ).get(id)
            
            if not nota:
                logger.warning(f"❌ NotaEnvio ID={id} não encontrada")
                return jsonify({'message': 'NotaEnvio not found'}), 404

            # Usa a serialização completa
            return jsonify(NotaEnvioController.serialize(nota)), 200

        except Exception as e:
            logger.exception(f"❌ Erro ao buscar NotaEnvio ID={id}")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 Método adicional: Buscar com filtros
    # ======================================================
    @staticmethod
    def get_filtered():
        try:
            query = NotaEnvio.query.options(
                db.joinedload(NotaEnvio.tipo_item),
                db.joinedload(NotaEnvio.itens).joinedload(NotaEnvioItem.item),
                db.joinedload(NotaEnvio.documentos)
            )
            
            # Aplica filtros se fornecidos
            numero_nota = request.args.get('numero_nota')
            if numero_nota:
                query = query.filter(NotaEnvio.numero_nota.ilike(f'%{numero_nota}%'))
            
            tipo_item_id = request.args.get('tipo_item_id')
            if tipo_item_id:
                query = query.filter(NotaEnvio.tipo_item_id == tipo_item_id)
            
            data_inicio = request.args.get('data_inicio')
            data_fim = request.args.get('data_fim')
            if data_inicio and data_fim:
                query = query.filter(
                    NotaEnvio.data_envio.between(
                        datetime.fromisoformat(data_inicio),
                        datetime.fromisoformat(data_fim)
                    )
                )
            
            notas = query.all()
            resultado = [NotaEnvioController.serialize(n) for n in notas]
            
            return jsonify({
                'total': len(resultado),
                'notas': resultado
            }), 200
            
        except Exception as e:
            logger.exception("❌ Erro ao buscar notas filtradas")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 Método adicional: Download de documento
    # ======================================================
    @staticmethod
    def download_documento(nota_id, documento_id):
        try:
            nota = NotaEnvio.query.get(nota_id)
            if not nota:
                return jsonify({'message': 'NotaEnvio not found'}), 404
            
            documento = next((d for d in nota.documentos if d.id == documento_id), None)
            if not documento:
                return jsonify({'message': 'Documento not found'}), 404
            
            from flask import send_file
            import io
            
            return send_file(
                io.BytesIO(documento.dados_arquivo),
                as_attachment=True,
                download_name=documento.nome_arquivo,
                mimetype=documento.tipo_mime
            )
            
        except Exception as e:
            logger.exception(f"❌ Erro ao baixar documento {documento_id} da nota {nota_id}")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 Criar nova
    # ======================================================
    @staticmethod
    def create():
        logger.info("➡️ [CREATE] Requisição recebida para criar NotaEnvio")
        try:
            # Detecta se é JSON ou multipart/form-data
            if request.content_type and request.content_type.startswith("application/json"):
                data = request.get_json(force=True)
            else:
                data = request.form.to_dict()
                # Convertendo campos JSON (itens/documentos) se vierem como string
                documentos = {}
                for key, value in data.items():
                    if key.startswith("documentos["):
                        # Ex.: documentos[0][nome_arquivo]
                        idx = key.split("[")[1].split("]")[0]
                        campo = key.split("[")[2].split("]")[0]
                        documentos.setdefault(idx, {})[campo] = value
                # Converte em lista ordenada
                data["documentos"] = [documentos[i] for i in sorted(documentos.keys(), key=int)] if documentos else []
                logger.info(f"📎 Documentos reconstruídos do form: {data.get('documentos')}")

                import json
                if 'itens' in data:
                    try:
                        data['itens'] = json.loads(data['itens'])
                    except Exception:
                        logger.warning("⚠️ Campo 'itens' não é JSON válido — ignorado.")
                        data['itens'] = []

            logger.info(f"📦 Dados recebidos: {data}")

            # ======================================================
            # 🔹 Capturar USER automaticamente - VERSÃO FINAL
            # ======================================================
            user_value = None

            # 1️⃣ Do JSON ou form (prioridade máxima - vem do frontend)
            if isinstance(data, dict):
                user_value = data.get('user') or data.get('username')

            # 2️⃣ Da sessão Flask (segunda opção)
            if not user_value:
                try:
                    from flask import session
                    user_value = session.get('username') or session.get('user')
                except Exception:
                    pass

            # 3️⃣ Headers HTTP (terceira opção)
            if not user_value:
                user_value = request.headers.get('X-User') or request.headers.get('X-Username')

            # 4️⃣ Cookies (quarta opção)
            if not user_value:
                user_value = request.cookies.get('username')

            # 5️⃣ Final fallback
            if not user_value:
                user_value = 'Usuário não identificado'
                logger.warning("⚠️ Usuário não pôde ser determinado")

            logger.info(f"👤 User determinado: {user_value}")

            # 5️⃣ Do flask-login (se o app usar login)
            if not user_value:
                try:
                    from flask_login import current_user
                    if current_user and getattr(current_user, 'is_authenticated', False):
                        user_value = getattr(current_user, 'username', None)
                except Exception:
                    pass

            logger.info(f"👤 User determinado: {user_value or 'Anônimo / não informado'}")

            # ======================================================
            # 🔹 Validação de campos obrigatórios
            # ======================================================
            required_fields = ['numero_nota', 'tipo_item_id', 'origem', 'destino']
            missing = [f for f in required_fields if not data.get(f)]
            if missing:
                logger.warning(f"❌ Campos obrigatórios ausentes: {missing}")
                return jsonify({'error': f"Campos obrigatórios ausentes: {missing}"}), 400

            # ======================================================
            # 🔹 Status de sincronização
            # ======================================================
            sync_status_str = data.get('syncStatus', 'Not Syncronized')
            sync_status = (
                SyncStatusEnum(sync_status_str)
                if sync_status_str in VALID_SYNC_STATUS
                else SyncStatusEnum.NotSyncronized
            )

            # ======================================================
            # 🔹 Criar NotaEnvio
            # ======================================================
            nota = NotaEnvio(
                numero_nota=data['numero_nota'],
                tipo_item_id=data['tipo_item_id'],
                origem=data['origem'],
                destino=data['destino'],
                observacoes=data.get('observacoes'),
                user=user_value,  # ✅ agora definido automaticamente
                syncStatus=sync_status,
                syncStatusDate=datetime.fromisoformat(data['syncStatusDate'])
                    if data.get('syncStatusDate') else None,
                data_envio=datetime.fromisoformat(data['data_envio'])
                    if data.get('data_envio') else datetime.utcnow()
            )

            db.session.add(nota)
            db.session.flush()  # Gera ID antes de adicionar itens/documentos
            logger.info(f"🆕 NotaEnvio criada (id={nota.id}) — adicionando itens e documentos")

            # ======================================================
            # 🔹 Itens
            # ======================================================
            itens = data.get('itens', [])
            itens_adicionados = 0
            for i in itens:
                if not i.get('item_id') or not i.get('quantidade_enviada'):
                    logger.warning(f"⚠️ Item inválido ignorado: {i}")
                    continue
                nota_item = NotaEnvioItem(
                    nota_envio_id=nota.id,
                    item_id=i['item_id'],
                    quantidade_enviada=i['quantidade_enviada']
                )
                db.session.add(nota_item)
                itens_adicionados += 1
            logger.info(f"📦 {itens_adicionados} itens adicionados")

            # ======================================================
            # 🔹 Documentos
            # ======================================================
            documentos_adicionados = 0
            if 'file' in request.files:
                files = request.files.getlist('file')
                for file in files:
                    doc = NotaEnvioDocument(
                        nota_envio_id=nota.id,
                        nome_arquivo=file.filename,
                        tipo_mime=file.mimetype,
                        dados_arquivo=file.read()
                    )
                    nota.documentos.append(doc)
                    documentos_adicionados += 1

            elif 'documentos' in data:
                for d in data.get('documentos', []):
                    if 'dados_arquivo' in d:
                        try:
                            dados_bin = base64.b64decode(d['dados_arquivo'])
                            doc = NotaEnvioDocument(
                                nota_envio_id=nota.id,
                                nome_arquivo=d['nome_arquivo'],
                                tipo_mime=d.get('tipo_mime'),
                                dados_arquivo=dados_bin
                            )
                            nota.documentos.append(doc)
                            documentos_adicionados += 1
                        except Exception as e:
                            logger.error(f"❌ Erro ao decodificar documento {d.get('nome_arquivo')}: {e}")
                            continue

            logger.info(f"📎 {documentos_adicionados} documentos vinculados à nota")

            # ======================================================
            # 🔹 Commit final
            # ======================================================
            db.session.commit()
            logger.info(f"✅ NotaEnvio salva com sucesso (id={nota.id})")
            return jsonify({
                'message': 'NotaEnvio criada com sucesso',
                'id': nota.id,
                'itens_adicionados': itens_adicionados,
                'documentos_adicionados': documentos_adicionados
            }), 201

        except Exception as e:
            db.session.rollback()
            logger.exception("❌ Erro inesperado ao criar NotaEnvio")
            return jsonify({'error': str(e)}), 500

        finally:
            db.session.close()
            logger.info("🧹 Sessão fechada após operação de criação")

    # ======================================================
    # 🔹 Atualizar - VERSÃO CORRIGIDA
    # ======================================================
    @staticmethod
    def update(id):
        logger.info(f"➡️ [UPDATE] Atualizando NotaEnvio ID={id}")
        try:
            nota = NotaEnvio.query.get(id)
            if not nota:
                logger.warning(f"❌ NotaEnvio ID={id} não encontrada")
                return jsonify({'message': 'NotaEnvio not found'}), 404

            # Detecta se é JSON ou multipart/form-data (IGUAL AO CREATE)
            if request.content_type and request.content_type.startswith("application/json"):
                data = request.get_json(force=True)
            else:
                data = request.form.to_dict()
                # Convertendo campos JSON (itens/documentos) se vierem como string
                documentos = {}
                for key, value in data.items():
                    if key.startswith("documentos["):
                        # Ex.: documentos[0][nome_arquivo]
                        idx = key.split("[")[1].split("]")[0]
                        campo = key.split("[")[2].split("]")[0]
                        documentos.setdefault(idx, {})[campo] = value
                # Converte em lista ordenada
                data["documentos"] = [documentos[i] for i in sorted(documentos.keys(), key=int)] if documentos else []
                logger.info(f"📎 Documentos reconstruídos do form: {data.get('documentos')}")

                import json
                if 'itens' in data:
                    try:
                        data['itens'] = json.loads(data['itens'])
                    except Exception:
                        logger.warning("⚠️ Campo 'itens' não é JSON válido — ignorado.")
                        data['itens'] = []

            logger.info(f"📦 Dados recebidos: {data}")

            # ======================================================
            # 🔹 Capturar USER automaticamente (IGUAL AO CREATE)
            # ======================================================
            user_value = None

            # 1️⃣ Do JSON ou form (prioridade máxima - vem do frontend)
            if isinstance(data, dict):
                user_value = data.get('user') or data.get('username')

            # 2️⃣ Da sessão Flask (segunda opção)
            if not user_value:
                try:
                    from flask import session
                    user_value = session.get('username') or session.get('user')
                except Exception:
                    pass

            # 3️⃣ Headers HTTP (terceira opção)
            if not user_value:
                user_value = request.headers.get('X-User') or request.headers.get('X-Username')

            # 4️⃣ Cookies (quarta opção)
            if not user_value:
                user_value = request.cookies.get('username')

            # 5️⃣ Final fallback
            if not user_value:
                user_value = 'Usuário não identificado'
                logger.warning("⚠️ Usuário não pôde ser determinado")

            logger.info(f"👤 User determinado: {user_value}")

            # ======================================================
            # 🔹 Atualiza campos básicos
            # ======================================================
            for field in ['numero_nota', 'tipo_item_id', 'origem', 'destino', 'observacoes', 'user']:
                if field in data:
                    setattr(nota, field, data[field])

            if 'data_envio' in data and data['data_envio']:
                nota.data_envio = datetime.fromisoformat(data['data_envio'])
            if 'syncStatus' in data and data['syncStatus'] in VALID_SYNC_STATUS:
                nota.syncStatus = SyncStatusEnum(data['syncStatus'])
            if 'syncStatusDate' in data and data['syncStatusDate']:
                nota.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])

            # ======================================================
            # 🔹 INICIALIZA VARIÁVEIS DE CONTAGEM
            # ======================================================
            itens_adicionados = 0  # ✅ INICIALIZA A VARIÁVEL
            documentos_adicionados = 0  # ✅ INICIALIZA A VARIÁVEL

            # ======================================================
            # 🔹 Atualiza itens (MESMA LÓGICA DO CREATE)
            # ======================================================
            if 'itens' in data:
                # Remove itens antigos
                NotaEnvioItem.query.filter_by(nota_envio_id=nota.id).delete()
                for i in data['itens']:
                    if not i.get('item_id') or not i.get('quantidade_enviada'):
                        logger.warning(f"⚠️ Item inválido ignorado: {i}")
                        continue
                    nota_item = NotaEnvioItem(
                        nota_envio_id=nota.id,
                        item_id=i['item_id'],
                        quantidade_enviada=i['quantidade_enviada']
                    )
                    db.session.add(nota_item)
                    itens_adicionados += 1
                logger.info(f"📦 {itens_adicionados} itens atualizados")
            else:
                logger.info("📦 Nenhum item para atualizar")

            # ======================================================
            # 🔹 Atualiza documentos (MESMA LÓGICA DO CREATE)
            # ======================================================
            
            # ✅ CORREÇÃO: Suporte a upload de arquivos (igual ao create)
            if 'file' in request.files:
                files = request.files.getlist('file')
                for file in files:
                    if file and file.filename:  # Só processa se tem arquivo
                        doc = NotaEnvioDocument(
                            nota_envio_id=nota.id,
                            nome_arquivo=file.filename,
                            tipo_mime=file.mimetype,
                            dados_arquivo=file.read()
                        )
                        db.session.add(doc)
                        documentos_adicionados += 1
                        logger.info(f"📎 Documento adicionado via upload: {file.filename}")

            # ✅ CORREÇÃO: Suporte a documentos via base64 (igual ao create)
            elif 'documentos' in data:
                for d in data.get('documentos', []):
                    if 'dados_arquivo' in d:
                        try:
                            dados_bin = base64.b64decode(d['dados_arquivo'])
                            doc = NotaEnvioDocument(
                                nota_envio_id=nota.id,
                                nome_arquivo=d['nome_arquivo'],
                                tipo_mime=d.get('tipo_mime'),
                                dados_arquivo=dados_bin
                            )
                            db.session.add(doc)
                            documentos_adicionados += 1
                            logger.info(f"📎 Documento adicionado via base64: {d.get('nome_arquivo')}")
                        except Exception as e:
                            logger.error(f"❌ Erro ao decodificar documento {d.get('nome_arquivo')}: {e}")
                            continue
            else:
                logger.info("📎 Nenhum novo documento para adicionar")

            logger.info(f"📎 {documentos_adicionados} novos documentos adicionados à nota")

            # ======================================================
            # 🔹 Commit final
            # ======================================================
            db.session.commit()
            logger.info(f"✅ NotaEnvio ID={id} atualizada com sucesso")
            return jsonify({
                'message': 'NotaEnvio atualizada com sucesso',
                'itens_atualizados': itens_adicionados,  # ✅ AGORA VARIÁVEL SEMPRE DEFINIDA
                'documentos_adicionados': documentos_adicionados  # ✅ AGORA VARIÁVEL SEMPRE DEFINIDA
            }), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"❌ Erro ao atualizar NotaEnvio ID={id}")
            return jsonify({'error': str(e)}), 500

        finally:
            db.session.close()
            logger.info("🧹 Sessão fechada após atualização")


    # ======================================================
    # 🔹 Deletar
    # ======================================================
    @staticmethod
    def delete(id):
        logger.info(f"➡️ [DELETE] Solicitada exclusão da NotaEnvio ID={id}")
        try:
            nota = NotaEnvio.query.get(id)
            if not nota:
                logger.warning(f"❌ NotaEnvio ID={id} não encontrada")
                return jsonify({'message': 'NotaEnvio not found'}), 404

            # Deleta itens e documentos antes da nota
            NotaEnvioItem.query.filter_by(nota_envio_id=nota.id).delete()
            NotaEnvioDocument.query.filter_by(nota_envio_id=nota.id).delete()
            db.session.delete(nota)
            db.session.commit()
            logger.info(f"✅ NotaEnvio ID={id} excluída com sucesso")
            return jsonify({'message': 'NotaEnvio excluída com sucesso'}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"❌ Erro ao excluir NotaEnvio ID={id}")
            return jsonify({'error': str(e)}), 500

        finally:
            db.session.close()
            logger.info("🧹 Sessão fechada após exclusão")


# ======================================================
# 🔹 Visualizar documento (SIMPLES - como antes)
# ======================================================
@staticmethod
def view_documento(nota_id, documento_id):
    try:
        nota = NotaEnvio.query.get(nota_id)
        if not nota:
            logger.warning(f"❌ NotaEnvio ID={nota_id} não encontrada")
            return jsonify({'message': 'NotaEnvio not found'}), 404
        
        documento = next((d for d in nota.documentos if d.id == documento_id), None)
        if not documento:
            logger.warning(f"❌ Documento ID={documento_id} não encontrado na nota {nota_id}")
            return jsonify({'message': 'Documento not found'}), 404
        
        from flask import send_file
        import io
        
        logger.info(f"👁️ Visualizando documento: {documento.nome_arquivo} ({documento.tipo_mime})")
        
        # ✅ SIMPLES: Envia o arquivo para visualização no browser
        return send_file(
            io.BytesIO(documento.dados_arquivo),
            mimetype=documento.tipo_mime,
            as_attachment=False,  # Não força download - abre no browser
            download_name=documento.nome_arquivo
        )
            
    except Exception as e:
        logger.exception(f"❌ Erro ao visualizar documento {documento_id} da nota {nota_id}")
        return jsonify({'error': str(e)}), 500

# ======================================================
# 🔹 Listar documentos de uma nota
# ======================================================
@staticmethod
def get_documentos(nota_id):
    try:
        nota = NotaEnvio.query.get(nota_id)
        if not nota:
            return jsonify({'message': 'NotaEnvio not found'}), 404
        
        documentos = [
            {
                'id': d.id,
                'nome_arquivo': d.nome_arquivo,
                'tipo_mime': d.tipo_mime,
                'tamanho_bytes': len(d.dados_arquivo) if d.dados_arquivo else 0,
                'createAt': d.createAt.isoformat() if d.createAt else None
            }
            for d in nota.documentos
        ]
        
        return jsonify(documentos), 200
        
    except Exception as e:
        logger.exception(f"❌ Erro ao listar documentos da nota {nota_id}")
        return jsonify({'error': str(e)}), 500
    

    # ======================================================
# 🔹 Listar documentos de uma nota específica
# ======================================================
@staticmethod
def get_documentos(nota_id):
    try:
        nota = NotaEnvio.query.get(nota_id)
        if not nota:
            logger.warning(f"❌ NotaEnvio ID={nota_id} não encontrada")
            return jsonify({'message': 'NotaEnvio not found'}), 404
        
        documentos = [
            {
                'id': d.id,
                'nome_arquivo': d.nome_arquivo,
                'tipo_mime': d.tipo_mime,
                'tamanho_bytes': len(d.dados_arquivo) if d.dados_arquivo else 0,
                'createAt': d.createAt.isoformat() if d.createAt else None
            }
            for d in nota.documentos
        ]
        
        logger.info(f"📄 Listados {len(documentos)} documentos da nota {nota_id}")
        return jsonify(documentos), 200
        
    except Exception as e:
        logger.exception(f"❌ Erro ao listar documentos da nota {nota_id}")
        return jsonify({'error': str(e)}), 500

