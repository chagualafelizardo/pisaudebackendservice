import logging
from flask import jsonify, request
from models import db, Pais, SyncStatusEnum
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PaisController:

    @staticmethod
    def get_all():
        try:
            paises = Pais.query.all()
            result = [{
                'id': p.id,
                'description': p.description,
                'syncStatus': p.syncStatus.value,
                'syncStatusDate': p.syncStatusDate.isoformat() if p.syncStatusDate else None,
                'createAt': p.createAt.isoformat() if p.createAt else None,
                'updateAt': p.updateAt.isoformat() if p.updateAt else None,
            } for p in paises]
            return jsonify(result), 200
        except Exception as e:
            logger.exception("Failed to fetch countries")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            p = Pais.query.get(id)
            if not p:
                return jsonify({'message': 'Pais not found'}), 404
            return jsonify({
                'id': p.id,
                'description': p.description,
                'syncStatus': p.syncStatus.value,
                'syncStatusDate': p.syncStatusDate.isoformat() if p.syncStatusDate else None,
                'createAt': p.createAt.isoformat() if p.createAt else None,
                'updateAt': p.updateAt.isoformat() if p.updateAt else None,
            }), 200
        except Exception as e:
            logger.exception(f"Failed to fetch Pais ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json(force=True)
            description = data.get('description')
            if not description:
                return jsonify({'message': 'Description is required'}), 400

            if Pais.query.filter_by(description=description).first():
                return jsonify({'message': 'Pais already exists'}), 400

            new_pais = Pais(description=description)
            db.session.add(new_pais)
            db.session.commit()
            return jsonify({
                'message': 'Pais created successfully',
                'id': new_pais.id,
                'description': new_pais.description
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("Failed to create Pais")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            p = Pais.query.get(id)
            if not p:
                return jsonify({'message': 'Pais not found'}), 404

            data = request.get_json(force=True)
            description = data.get('description')
            if not description:
                return jsonify({'message': 'Description is required'}), 400

            existing = Pais.query.filter(Pais.description==description, Pais.id!=id).first()
            if existing:
                return jsonify({'message': 'Description already in use'}), 400

            p.description = description
            p.updateAt = datetime.utcnow()
            db.session.commit()
            return jsonify({
                'message': 'Pais updated successfully',
                'id': p.id,
                'description': p.description
            }), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Failed to update Pais ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            p = Pais.query.get(id)
            if not p:
                return jsonify({'message': 'Pais not found'}), 404
            db.session.delete(p)
            db.session.commit()
            return jsonify({'message': 'Pais deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Failed to delete Pais ID {id}")
            return jsonify({'error': str(e)}), 500
