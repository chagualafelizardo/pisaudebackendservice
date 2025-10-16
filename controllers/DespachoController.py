import logging
from flask import jsonify, request, send_file
from io import BytesIO
from datetime import datetime
from models import db, Despacho, EstadoDespachoEnum, Person

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DespachoController:

    @staticmethod
    def get_all():
        try:
            despachos = Despacho.query.all()
            result = []
            for d in despachos:
                result.append({
                    'id': d.id,
                    'person_id': d.person_id,
                    'person_name': d.person.fullname if d.person else None,
                    'titulo': d.titulo,
                    'descricao': d.descricao,
                    'data_despacho': d.data_despacho.isoformat(),
                    'estado': d.estado.value,
                    'observacao': d.observacao,
                    'anexo_nome': d.anexo_nome,
                    'criado_em': d.criado_em.isoformat() if d.criado_em else None
                })
            return jsonify(result), 200
        except Exception as e:
            logger.exception("[GET ALL] Erro ao listar despachos")
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def get_by_id(id):
        try:
            d = Despacho.query.get(id)
            if not d:
                return jsonify({'message': 'Despacho não encontrado'}), 404

            return jsonify({
                'id': d.id,
                'person_id': d.person_id,
                'person_name': d.person.fullname if d.person else None,
                'titulo': d.titulo,
                'descricao': d.descricao,
                'data_despacho': d.data_despacho.isoformat(),
                'estado': d.estado.value,
                'observacao': d.observacao,
                'anexo_nome': d.anexo_nome,
                'criado_em': d.criado_em.isoformat() if d.criado_em else None
            }), 200
        except Exception as e:
            logger.exception("[GET BY ID] Erro ao buscar despacho")
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def create():
        try:
            data = request.form.to_dict()
            file = request.files.get('anexo')

            titulo = data.get('titulo')
            if not titulo:
                return jsonify({'message': 'O campo título é obrigatório'}), 400

            novo_despacho = Despacho(
                titulo=titulo,
                descricao=data.get('descricao'),
                data_despacho=datetime.now().date(),
                estado=EstadoDespachoEnum.PENDENTE,
                observacao=data.get('observacao'),
                person_id=data.get('person_id')
            )

            if file:
                novo_despacho.anexo_nome = file.filename
                novo_despacho.anexo_tipo = file.mimetype
                novo_despacho.anexo_dados = file.read()

            db.session.add(novo_despacho)
            db.session.commit()

            return jsonify({'message': 'Despacho criado com sucesso', 'id': novo_despacho.id}), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Erro ao criar despacho")
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def download_anexo(id):
        """Permite baixar o ficheiro anexo."""
        try:
            despacho = Despacho.query.get(id)
            if not despacho or not despacho.anexo_dados:
                return jsonify({'message': 'Anexo não encontrado'}), 404

            return send_file(
                BytesIO(despacho.anexo_dados),
                as_attachment=True,
                download_name=despacho.anexo_nome,
                mimetype=despacho.anexo_tipo or 'application/octet-stream'
            )
        except Exception as e:
            logger.exception("[DOWNLOAD] Erro ao baixar anexo")
            return jsonify({'error': str(e)}), 500
