import logging
from flask import jsonify, request, send_file
from io import BytesIO
from datetime import datetime
from models import db, Despacho, EstadoDespachoEnum, Person
import base64

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class DespachoController:

    @staticmethod
    def serialize_person(person: Person):
        if not person:
            return None
        return {
            'id': person.id,
            'fullname': person.fullname,
            'nim': person.nim,
            'gender': person.gender,
            'dateofbirth': person.dateofbirth.isoformat() if person.dateofbirth else None,
            'dataIncorporacao': person.incorporationdata.isoformat() if person.incorporationdata else None,
            'image': base64.b64encode(person.image).decode('utf-8') if person.image else None
        }

    @staticmethod
    def serialize_despacho(d: Despacho):
        return {
            'id': d.id,
            'person_id': d.person_id,
            'person': DespachoController.serialize_person(d.person),
            'person_image': base64.b64encode(d.person.image).decode('utf-8') if d.person and d.person.image else None,
            'titulo': d.titulo,
            'descricao': d.descricao,
            'data_despacho': d.data_despacho.isoformat() if d.data_despacho else None,
            'estado': d.estado.value if d.estado else None,
            'observacao': d.observacao,
            'anexo_nome': d.anexo_nome,
            'anexo_tipo': d.anexo_tipo,
            'criado_em': d.criado_em.isoformat() if d.criado_em else None,
            'atualizado_em': d.atualizado_em.isoformat() if d.atualizado_em else None
        }

    @staticmethod
    def get_all():
        try:
            logger.info("[GET ALL] Iniciando busca de todos os despachos")
            despachos = Despacho.query.all()
            result = [DespachoController.serialize_despacho(d) for d in despachos]
            logger.info(f"[GET ALL] Encontrados {len(result)} despachos")
            return jsonify(result), 200
        except Exception as e:
            logger.exception(f"[GET ALL] ERRO CRÍTICO ao listar despachos: {str(e)}")
            return jsonify({'error': 'Erro interno do servidor ao buscar despachos'}), 500

    @staticmethod
    def get_by_id(id):
        try:
            logger.info(f"[GET BY ID] Buscando despacho ID: {id}")
            d = Despacho.query.get(id)
            if not d:
                logger.warning(f"[GET BY ID] Despacho não encontrado: {id}")
                return jsonify({'message': 'Despacho não encontrado'}), 404

            result = DespachoController.serialize_despacho(d)
            logger.info(f"[GET BY ID] Despacho encontrado: {d.titulo}")
            return jsonify(result), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] ERRO ao buscar despacho {id}: {str(e)}")
            return jsonify({'error': f'Erro ao buscar despacho: {str(e)}'}), 500

    @staticmethod
    def create():
        try:
            if not request.content_type or 'multipart/form-data' not in request.content_type:
                logger.warning("[CREATE] Content-Type não é multipart/form-data")
                return jsonify({'error': 'Content-Type deve ser multipart/form-data'}), 400

            data = request.form.to_dict()
            file = request.files.get('anexo')
            
            logger.info(f"[CREATE] Iniciando criação de despacho. Dados recebidos: {list(data.keys())}")
            logger.info(f"[CREATE] Ficheiro anexo: {'Sim' if file else 'Não'}")

            titulo = data.get('titulo', '').strip()
            if not titulo:
                return jsonify({'error': 'O campo título é obrigatório'}), 400

            data_despacho_str = data.get('data_despacho')
            data_despacho = datetime.strptime(data_despacho_str, '%Y-%m-%d').date() if data_despacho_str else datetime.now().date()

            estado_str = data.get('estado', 'PENDENTE')
            estado = EstadoDespachoEnum[estado_str] if estado_str in EstadoDespachoEnum.__members__ else EstadoDespachoEnum.PENDENTE

            person_id = None
            if 'person_id' in data and data['person_id']:
                try:
                    person_id = int(data['person_id'])
                    if not Person.query.get(person_id):
                        return jsonify({'error': f'Militar com ID {person_id} não encontrado'}), 400
                except (ValueError, TypeError):
                    person_id = None

            novo_despacho = Despacho(
                titulo=titulo,
                descricao=data.get('descricao', '').strip(),
                data_despacho=data_despacho,
                estado=estado,
                observacao=data.get('observacao', '').strip(),
                person_id=person_id
            )

            if file and file.filename:
                if file.content_length and file.content_length > 10 * 1024 * 1024:
                    return jsonify({'error': 'Ficheiro muito grande. Máximo 10MB permitido.'}), 400
                novo_despacho.anexo_nome = file.filename
                novo_despacho.anexo_tipo = file.mimetype
                novo_despacho.anexo_dados = file.read()

            db.session.add(novo_despacho)
            db.session.commit()
            
            return jsonify({
                'message': 'Despacho criado com sucesso', 
                'id': novo_despacho.id,
                'titulo': novo_despacho.titulo
            }), 201
            
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[CREATE] ERRO CRÍTICO ao criar despacho: {str(e)}")
            return jsonify({'error': 'Erro interno do servidor ao criar despacho'}), 500

    @staticmethod
    def update(id):
        try:
            if not request.content_type or 'multipart/form-data' not in request.content_type:
                return jsonify({'error': 'Content-Type deve ser multipart/form-data'}), 400

            despacho = Despacho.query.get(id)
            if not despacho:
                return jsonify({'error': 'Despacho não encontrado'}), 404

            data = request.form.to_dict()
            file = request.files.get('anexo')

            if 'titulo' in data and data['titulo'].strip():
                despacho.titulo = data['titulo'].strip()
            if 'descricao' in data:
                despacho.descricao = data['descricao'].strip()
            if 'data_despacho' in data and data['data_despacho']:
                try:
                    despacho.data_despacho = datetime.strptime(data['data_despacho'], '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({'error': 'Data inválida'}), 400
            if 'estado' in data and data['estado'] in EstadoDespachoEnum.__members__:
                despacho.estado = EstadoDespachoEnum[data['estado']]
            if 'observacao' in data:
                despacho.observacao = data['observacao'].strip()
            if 'person_id' in data:
                try:
                    person_id = int(data['person_id'])
                    if not Person.query.get(person_id):
                        return jsonify({'error': f'Militar com ID {person_id} não encontrado'}), 400
                    despacho.person_id = person_id
                except (ValueError, TypeError):
                    despacho.person_id = None

            if file and file.filename:
                if file.content_length and file.content_length > 10 * 1024 * 1024:
                    return jsonify({'error': 'Ficheiro muito grande. Máximo 10MB permitido.'}), 400
                despacho.anexo_nome = file.filename
                despacho.anexo_tipo = file.mimetype
                despacho.anexo_dados = file.read()

            db.session.commit()
            return jsonify({'message': 'Despacho atualizado com sucesso', 'id': despacho.id}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] ERRO ao atualizar despacho {id}: {str(e)}")
            return jsonify({'error': 'Erro interno do servidor ao atualizar despacho'}), 500

    @staticmethod
    def delete(id):
        try:
            despacho = Despacho.query.get(id)
            if not despacho:
                return jsonify({'error': 'Despacho não encontrado'}), 404

            db.session.delete(despacho)
            db.session.commit()
            return jsonify({'message': 'Despacho excluído com sucesso'}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] ERRO ao excluir despacho {id}: {str(e)}")
            return jsonify({'error': 'Erro interno do servidor ao excluir despacho'}), 500

    @staticmethod
    def download_anexo(id):
        try:
            despacho = Despacho.query.get(id)
            if not despacho or not despacho.anexo_dados:
                return jsonify({'error': 'Anexo não encontrado'}), 404

            return send_file(
                BytesIO(despacho.anexo_dados),
                as_attachment=True,
                download_name=despacho.anexo_nome,
                mimetype=despacho.anexo_tipo or 'application/octet-stream'
            )

        except Exception as e:
            logger.exception(f"[DOWNLOAD ANEXO] ERRO ao baixar anexo {id}: {str(e)}")
            return jsonify({'error': 'Erro interno do servidor ao baixar anexo'}), 500


