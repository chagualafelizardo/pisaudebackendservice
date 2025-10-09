import logging
from flask import jsonify, request
from models import db, Patent
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class PatentController:

    @staticmethod
    def get_all():
        try:
            patents = Patent.query.all()
            result = []
            for p in patents:
                result.append({
                    'id': p.id,
                    'description': p.description,
                    'createAt': p.createAt.isoformat() if p.createAt else None,
                    'updateAt': p.updateAt.isoformat() if p.updateAt else None,
                    'persons': [{'id': per.id, 'fullname': per.fullname} for per in p.persons]
                })
            return jsonify(result), 200
        except Exception as e:
            logger.exception("[GET ALL] Failed to fetch patents")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            p = Patent.query.get(id)
            if not p:
                return jsonify({'message': 'Patent not found'}), 404

            return jsonify({
                'id': p.id,
                'description': p.description,
                'createAt': p.createAt.isoformat() if p.createAt else None,
                'updateAt': p.updateAt.isoformat() if p.updateAt else None,
                'persons': [{'id': per.id, 'fullname': per.fullname} for per in p.persons]
            }), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch patent ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            description = data.get('description')
            if not description:
                return jsonify({'message': 'Description is required'}), 400

            if Patent.query.filter_by(description=description).first():
                return jsonify({'message': 'Patent already exists'}), 400

            new_patent = Patent(description=description)
            db.session.add(new_patent)
            db.session.commit()

            return jsonify({
                'message': 'Patent created successfully',
                'id': new_patent.id,
                'description': new_patent.description
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create patent")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            p = Patent.query.get(id)
            if not p:
                return jsonify({'message': 'Patent not found'}), 404

            data = request.get_json()
            description = data.get('description')
            if not description:
                return jsonify({'message': 'Description is required'}), 400

            existing_patent = Patent.query.filter(Patent.description == description, Patent.id != id).first()
            if existing_patent:
                return jsonify({'message': 'Description already in use'}), 400

            p.description = description
            p.updateAt = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Patent updated successfully',
                'id': p.id,
                'description': p.description
            }), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update patent ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            p = Patent.query.get(id)
            if not p:
                return jsonify({'message': 'Patent not found'}), 404

            db.session.delete(p)
            db.session.commit()
            return jsonify({'message': 'Patent deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete patent ID {id}")
            return jsonify({'error': str(e)}), 500
