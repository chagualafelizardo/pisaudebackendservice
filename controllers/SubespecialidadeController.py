import logging
from flask import jsonify, request
from models import db
from models.Subespecialidade import Subespecialidade
from models.Especialidade import Especialidade
from datetime import datetime

logger = logging.getLogger(__name__)

class SubespecialidadeController:

    @staticmethod
    def get_all():
        try:
            logger.info("[GET ALL] Fetching all subespecialidades")
            subespecialidades = Subespecialidade.query.all()
            result = []
            for sub in subespecialidades:
                result.append({
                    'id': sub.id,
                    'description': sub.description,
                    'especialidadeId': sub.especialidadeId,
                    'especialidadeDescription': sub.especialidade.description if sub.especialidade else None,
                    'syncStatus': sub.syncStatus.value,
                    'syncStatusDate': sub.syncStatusDate.isoformat() if sub.syncStatusDate else None,
                    'createAt': sub.createAt.isoformat() if sub.createAt else None,
                    'updateAt': sub.updateAt.isoformat() if sub.updateAt else None
                })
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"[GET ALL] Failed to fetch subespecialidades: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            logger.info(f"[GET BY ID] Fetching subespecialidade ID: {id}")
            sub = Subespecialidade.query.get(id)
            if not sub:
                return jsonify({'message': 'Subespecialidade not found'}), 404

            return jsonify({
                'id': sub.id,
                'description': sub.description,
                'especialidadeId': sub.especialidadeId,
                'especialidadeDescription': sub.especialidade.description if sub.especialidade else None,
                'syncStatus': sub.syncStatus.value,
                'syncStatusDate': sub.syncStatusDate.isoformat() if sub.syncStatusDate else None,
                'createAt': sub.createAt.isoformat() if sub.createAt else None,
                'updateAt': sub.updateAt.isoformat() if sub.updateAt else None
            }), 200
        except Exception as e:
            logger.error(f"[GET BY ID] Error fetching subespecialidade ID {id}: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_especialidade(especialidade_id):
        try:
            logger.info(f"[GET BY ESPECIALIDADE] Fetching subespecialidades for Especialidade ID: {especialidade_id}")
            subespecialidades = Subespecialidade.query.filter_by(especialidadeId=especialidade_id).all()
            
            result = []
            for sub in subespecialidades:
                result.append({
                    'id': sub.id,
                    'description': sub.description,
                    'especialidadeId': sub.especialidadeId,
                    'especialidadeDescription': sub.especialidade.description if sub.especialidade else None,
                    'syncStatus': sub.syncStatus.value,
                    'syncStatusDate': sub.syncStatusDate.isoformat() if sub.syncStatusDate else None,
                    'createAt': sub.createAt.isoformat() if sub.createAt else None,
                    'updateAt': sub.updateAt.isoformat() if sub.updateAt else None
                })
            
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"[GET BY ESPECIALIDADE] Failed: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            description = data.get('description')
            especialidadeId = data.get('especialidadeId')

            if not description or not especialidadeId:
                return jsonify({'message': 'Description and Especialidade ID are required'}), 400

            if Subespecialidade.query.filter_by(description=description).first():
                return jsonify({'message': 'Subespecialidade already exists'}), 400

            especialidade = Especialidade.query.get(especialidadeId)
            if not especialidade:
                return jsonify({'message': 'Especialidade not found'}), 404

            new_sub = Subespecialidade(
                description=description,
                especialidadeId=especialidadeId
            )
            db.session.add(new_sub)
            db.session.commit()
            logger.info(f"[CREATE] Subespecialidade '{description}' created successfully")

            return jsonify({
                'message': 'Subespecialidade created successfully',
                'id': new_sub.id
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"[CREATE] Failed to create subespecialidade: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            sub = Subespecialidade.query.get(id)
            if not sub:
                return jsonify({'message': 'Subespecialidade not found'}), 404

            data = request.get_json()
            description = data.get('description')
            especialidadeId = data.get('especialidadeId')

            if not description or not especialidadeId:
                return jsonify({'message': 'Description and Especialidade ID are required'}), 400

            if Subespecialidade.query.filter(Subespecialidade.description == description, Subespecialidade.id != id).first():
                return jsonify({'message': 'Description already in use'}), 400

            especialidade = Especialidade.query.get(especialidadeId)
            if not especialidade:
                return jsonify({'message': 'Especialidade not found'}), 404

            sub.description = description
            sub.especialidadeId = especialidadeId
            sub.updateAt = datetime.utcnow()
            db.session.commit()
            logger.info(f"[UPDATE] Subespecialidade ID {id} updated")

            return jsonify({'message': 'Subespecialidade updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"[UPDATE] Failed to update subespecialidade ID {id}: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            sub = Subespecialidade.query.get(id)
            if not sub:
                return jsonify({'message': 'Subespecialidade not found'}), 404

            db.session.delete(sub)
            db.session.commit()
            logger.info(f"[DELETE] Subespecialidade ID {id} deleted")
            return jsonify({'message': 'Subespecialidade deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"[DELETE] Failed to delete subespecialidade ID {id}: {e}")
            return jsonify({'error': str(e)}), 500
