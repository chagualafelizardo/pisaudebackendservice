import logging
from flask import jsonify, request
from models import db, Especialidade, SyncStatusEnum
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EspecialidadeController:

    @staticmethod
    def get_all():
        try:
            especialidades = Especialidade.query.all()
            result = []
            for e in especialidades:
                result.append({
                    'id': e.id,
                    'description': e.description,
                    'syncStatus': e.syncStatus.value,
                    'syncStatusDate': e.syncStatusDate.isoformat() if e.syncStatusDate else None,
                    'createAt': e.createAt.isoformat() if e.createAt else None,
                    'updateAt': e.updateAt.isoformat() if e.updateAt else None,
                })
            return jsonify(result), 200
        except Exception as e:
            logger.exception("[GET ALL] Failed to fetch especialidades")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            e = Especialidade.query.get(id)
            if not e:
                return jsonify({'message': 'Especialidade not found'}), 404

            return jsonify({
                'id': e.id,
                'description': e.description,
                'syncStatus': e.syncStatus.value,
                'syncStatusDate': e.syncStatusDate.isoformat() if e.syncStatusDate else None,
                'createAt': e.createAt.isoformat() if e.createAt else None,
                'updateAt': e.updateAt.isoformat() if e.updateAt else None,
            }), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch especialidade ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            description = data.get('description')
            if not description:
                return jsonify({'message': 'Description is required'}), 400

            if Especialidade.query.filter_by(description=description).first():
                return jsonify({'message': 'Especialidade already exists'}), 400

            new_especialidade = Especialidade(description=description)
            db.session.add(new_especialidade)
            db.session.commit()

            return jsonify({
                'message': 'Especialidade created successfully',
                'id': new_especialidade.id,
                'description': new_especialidade.description
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create especialidade")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            e = Especialidade.query.get(id)
            if not e:
                return jsonify({'message': 'Especialidade not found'}), 404

            data = request.get_json()
            description = data.get('description')
            if not description:
                return jsonify({'message': 'Description is required'}), 400

            existing = Especialidade.query.filter(Especialidade.description == description, Especialidade.id != id).first()
            if existing:
                return jsonify({'message': 'Description already in use'}), 400

            e.description = description
            e.updateAt = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Especialidade updated successfully',
                'id': e.id,
                'description': e.description
            }), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update especialidade ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            e = Especialidade.query.get(id)
            if not e:
                return jsonify({'message': 'Especialidade not found'}), 404

            db.session.delete(e)
            db.session.commit()
            return jsonify({'message': 'Especialidade deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete especialidade ID {id}")
            return jsonify({'error': str(e)}), 500
