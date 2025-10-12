import logging
from flask import jsonify, request
from models import db, Formacao, Pais, TipoLicenca, Person, SyncStatusEnum
from datetime import datetime

# Configuração básica de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class FormacaoController:

    @staticmethod
    def get_all():
        logger.info("[GET ALL] Request received to fetch all formacoes.")
        try:
            formacoes = Formacao.query.all()
            result = []
            for f in formacoes:
                result.append({
                    'id': f.id,
                    'inicio': f.inicio.isoformat() if f.inicio else None,
                    'duracao': f.duracao,
                    'anoacademico': f.anoacademico,
                    'despachoautorizacao': f.despachoautorizacao,
                    'person': {
                        'id': f.person.id,
                        'fullname': f.person.fullname
                    } if f.person else None,
                    'pais': {
                        'id': f.pais.id,
                        'description': f.pais.description
                    } if f.pais else None,
                    'tipo_licenca': {
                        'id': f.tipo_licenca.id,
                        'description': f.tipo_licenca.description
                    } if f.tipo_licenca else None,
                    'syncStatus': f.syncStatus.value if f.syncStatus else None,
                    'syncStatusDate': f.syncStatusDate.isoformat() if f.syncStatusDate else None,
                    'createAt': f.createAt.isoformat() if f.createAt else None,
                    'updateAt': f.updateAt.isoformat() if f.updateAt else None,
                })
            return jsonify(result), 200
        except Exception as e:
            logger.exception("[GET ALL] Failed to fetch formacoes.")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        logger.info(f"[GET BY ID] Request received for formacao ID {id}.")
        try:
            f = Formacao.query.get(id)
            if not f:
                return jsonify({'message': 'Formacao not found'}), 404
            result = {
                'id': f.id,
                'inicio': f.inicio.isoformat() if f.inicio else None,
                'duracao': f.duracao,
                'anoacademico': f.anoacademico,
                'despachoautorizacao': f.despachoautorizacao,
                'person': {
                    'id': f.person.id,
                    'fullname': f.person.fullname
                } if f.person else None,
                'pais': {
                    'id': f.pais.id,
                    'description': f.pais.description
                } if f.pais else None,
                'tipo_licenca': {
                    'id': f.tipo_licenca.id,
                    'description': f.tipo_licenca.description
                } if f.tipo_licenca else None,
                'syncStatus': f.syncStatus.value if f.syncStatus else None,
                'syncStatusDate': f.syncStatusDate.isoformat() if f.syncStatusDate else None,
                'createAt': f.createAt.isoformat() if f.createAt else None,
                'updateAt': f.updateAt.isoformat() if f.updateAt else None,
            }
            return jsonify(result), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch formacao ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        logger.info("[CREATE] Request received to create new formacao.")
        try:
            data = request.get_json(force=True)
            inicio = data.get('inicio')
            duracao = data.get('duracao')
            anoacademico = data.get('anoacademico')
            despachoautorizacao = data.get('despachoautorizacao')
            person_id = data.get('person_id')
            pais_id = data.get('pais_id')
            tipo_licenca_id = data.get('tipo_licenca_id')

            # Validações básicas
            if not all([inicio, duracao, anoacademico, despachoautorizacao, person_id, pais_id, tipo_licenca_id]):
                return jsonify({'message': 'All fields are required'}), 400

            person = Person.query.get(person_id)
            pais = Pais.query.get(pais_id)
            tipo_licenca = TipoLicenca.query.get(tipo_licenca_id)
            if not person:
                return jsonify({'message': 'Person not found'}), 404
            if not pais:
                return jsonify({'message': 'Pais not found'}), 404
            if not tipo_licenca:
                return jsonify({'message': 'TipoLicenca not found'}), 404

            formacao = Formacao(
                inicio=datetime.fromisoformat(inicio),
                duracao=duracao,
                anoacademico=anoacademico,
                despachoautorizacao=despachoautorizacao,
                person=person,
                pais=pais,
                tipo_licenca=tipo_licenca,
                syncStatus=SyncStatusEnum(data.get('syncStatus', 'Not Syncronized')),
                syncStatusDate=datetime.fromisoformat(data['syncStatusDate']) if data.get('syncStatusDate') else None
            )
            db.session.add(formacao)
            db.session.commit()
            return jsonify({
                'message': 'Formacao created successfully',
                'id': formacao.id
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create formacao.")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        logger.info(f"[UPDATE] Request received to update formacao ID {id}.")
        try:
            f = Formacao.query.get(id)
            if not f:
                return jsonify({'message': 'Formacao not found'}), 404

            data = request.get_json(force=True)
            inicio = data.get('inicio')
            duracao = data.get('duracao')
            anoacademico = data.get('anoacademico')
            despachoautorizacao = data.get('despachoautorizacao')
            person_id = data.get('person_id')
            pais_id = data.get('pais_id')
            tipo_licenca_id = data.get('tipo_licenca_id')

            if not all([inicio, duracao, anoacademico, despachoautorizacao, person_id, pais_id, tipo_licenca_id]):
                return jsonify({'message': 'All fields are required'}), 400

            person = Person.query.get(person_id)
            pais = Pais.query.get(pais_id)
            tipo_licenca = TipoLicenca.query.get(tipo_licenca_id)
            if not person:
                return jsonify({'message': 'Person not found'}), 404
            if not pais:
                return jsonify({'message': 'Pais not found'}), 404
            if not tipo_licenca:
                return jsonify({'message': 'TipoLicenca not found'}), 404

            f.inicio = datetime.fromisoformat(inicio)
            f.duracao = duracao
            f.anoacademico = anoacademico
            f.despachoautorizacao = despachoautorizacao
            f.person = person
            f.pais = pais
            f.tipo_licenca = tipo_licenca
            f.updateAt = datetime.utcnow()

            db.session.commit()
            return jsonify({'message': 'Formacao updated successfully', 'id': f.id}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update formacao ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        logger.info(f"[DELETE] Request received to delete formacao ID {id}.")
        try:
            f = Formacao.query.get(id)
            if not f:
                return jsonify({'message': 'Formacao not found'}), 404

            db.session.delete(f)
            db.session.commit()
            return jsonify({'message': 'Formacao deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete formacao ID {id}")
            return jsonify({'error': str(e)}), 500
