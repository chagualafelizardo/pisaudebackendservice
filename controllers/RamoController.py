import logging
from flask import jsonify, request
from models import db, Ramo, SyncStatusEnum
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class RamoController:

    @staticmethod
    def get_all():
        try:
            ramos = Ramo.query.all()
            result = []
            for r in ramos:
                result.append({
                    'id': r.id,
                    'description': r.description,
                    'syncStatus': r.syncStatus.value,
                    'syncStatusDate': r.syncStatusDate.isoformat() if r.syncStatusDate else None,
                    'createAt': r.createAt.isoformat() if r.createAt else None,
                    'updateAt': r.updateAt.isoformat() if r.updateAt else None,
                    # 'persons': [{'id': per.id, 'fullname': per.fullname} for per in r.persons]  # caso implemente relacionamento
                })
            return jsonify(result), 200
        except Exception as e:
            logger.exception("[GET ALL] Failed to fetch ramos")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            r = Ramo.query.get(id)
            if not r:
                return jsonify({'message': 'Ramo not found'}), 404

            return jsonify({
                'id': r.id,
                'description': r.description,
                'syncStatus': r.syncStatus.value,
                'syncStatusDate': r.syncStatusDate.isoformat() if r.syncStatusDate else None,
                'createAt': r.createAt.isoformat() if r.createAt else None,
                'updateAt': r.updateAt.isoformat() if r.updateAt else None,
                # 'persons': [{'id': per.id, 'fullname': per.fullname} for per in r.persons]
            }), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch ramo ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            description = data.get('description')
            if not description:
                return jsonify({'message': 'Description is required'}), 400

            if Ramo.query.filter_by(description=description).first():
                return jsonify({'message': 'Ramo already exists'}), 400

            new_ramo = Ramo(description=description)
            db.session.add(new_ramo)
            db.session.commit()

            return jsonify({
                'message': 'Ramo created successfully',
                'id': new_ramo.id,
                'description': new_ramo.description
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create ramo")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            r = Ramo.query.get(id)
            if not r:
                return jsonify({'message': 'Ramo not found'}), 404

            data = request.get_json()
            description = data.get('description')
            if not description:
                return jsonify({'message': 'Description is required'}), 400

            existing_ramo = Ramo.query.filter(Ramo.description == description, Ramo.id != id).first()
            if existing_ramo:
                return jsonify({'message': 'Description already in use'}), 400

            r.description = description
            r.updateAt = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Ramo updated successfully',
                'id': r.id,
                'description': r.description
            }), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update ramo ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            r = Ramo.query.get(id)
            if not r:
                return jsonify({'message': 'Ramo not found'}), 404

            db.session.delete(r)
            db.session.commit()
            return jsonify({'message': 'Ramo deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete ramo ID {id}")
            return jsonify({'error': str(e)}), 500
