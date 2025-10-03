from flask import jsonify, request
from models import db, ResourceType
from datetime import datetime
import logging  # <-- IMPORTANTE

class ResourceTypeController:
    @staticmethod
    def get_all():
        try:
            types = ResourceType.query.all()
            return jsonify([
                {
                    'id': t.id,
                    'name': t.name,
                    'description': t.description,
                    'createAt': t.createAt,
                    'updateAt': t.updateAt
                } for t in types
            ]), 200
        except Exception as e:
            logging.error(f"[GET ALL] Failed to load ResourceTypes: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            t = ResourceType.query.get(id)
            if t:
                return jsonify({
                    'id': t.id,
                    'name': t.name,
                    'description': t.description,
                    'createAt': t.createAt,
                    'updateAt': t.updateAt
                }), 200
            return jsonify({'message': 'Resource type not found'}), 404
        except Exception as e:
            logging.error(f"[GET BY ID] Error for ResourceType {id}: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            name = data.get('name')
            description = data.get('description', '')

            if not name:
                return jsonify({'message': 'Missing required name'}), 400

            if ResourceType.query.filter_by(name=name).first():
                return jsonify({'message': 'Resource type already exists'}), 400

            new_type = ResourceType(
                name=name,
                description=description
            )

            db.session.add(new_type)
            db.session.commit()

            logging.info(f"[CREATE] ResourceType '{name}' created successfully.")
            return jsonify({'message': 'Resource type created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"[CREATE] Error creating ResourceType: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            t = ResourceType.query.get(id)
            if not t:
                return jsonify({'message': 'Resource type not found'}), 404

            data = request.get_json()
            old_name = t.name
            t.name = data.get('name', t.name)
            t.description = data.get('description', t.description)
            t.updateAt = datetime.utcnow()

            db.session.commit()

            logging.info(f"[UPDATE] ResourceType ID {id} ('{old_name}' → '{t.name}') updated successfully.")
            return jsonify({'message': 'Resource type updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logging.error(f"[UPDATE] Error updating ResourceType {id}: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            t = ResourceType.query.get(id)
            if not t:
                return jsonify({'message': 'Resource type not found'}), 404

            db.session.delete(t)
            db.session.commit()

            logging.info(f"[DELETE] ResourceType ID {id} ('{t.name}') deleted successfully.")
            return jsonify({'message': 'Resource type deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logging.error(f"[DELETE] Error deleting ResourceType {id}: {str(e)}")
            return jsonify({'error': str(e)}), 500
