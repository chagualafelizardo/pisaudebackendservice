from flask import jsonify, request
from models import db, Role
from datetime import datetime

class RoleController:
    @staticmethod
    def get_all():
        try:
            roles = Role.query.all()
            return jsonify([r.to_dict() for r in roles]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            role = Role.query.get(id)
            if not role:
                return jsonify({'message': 'Role not found'}), 404
            return jsonify(role.to_dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            if not data or 'description' not in data:
                return jsonify({'message': 'Missing description'}), 400

            if Role.query.filter_by(description=data['description']).first():
                return jsonify({'message': 'Role already exists'}), 400

            new_role = Role(
                description=data['description'],
                can_create=data.get('can_create', False),
                can_read=data.get('can_read', True),
                can_update=data.get('can_update', False),
                can_delete=data.get('can_delete', False)
            )

            db.session.add(new_role)
            db.session.commit()
            return jsonify(new_role.to_dict()), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            role = Role.query.get(id)
            if not role:
                return jsonify({'message': 'Role not found'}), 404

            data = request.get_json()
            if not data or 'description' not in data:
                return jsonify({'message': 'Missing description'}), 400

            existing = Role.query.filter(
                Role.description == data['description'],
                Role.id != id
            ).first()
            if existing:
                return jsonify({'message': 'Role with this description already exists'}), 400

            # Atualizar campos
            role.description = data['description']
            role.can_create = data.get('can_create', role.can_create)
            role.can_read = data.get('can_read', role.can_read)
            role.can_update = data.get('can_update', role.can_update)
            role.can_delete = data.get('can_delete', role.can_delete)
            role.updateAt = datetime.utcnow()

            db.session.commit()
            return jsonify(role.to_dict()), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            role = Role.query.get(id)
            if not role:
                return jsonify({'message': 'Role not found'}), 404

            db.session.delete(role)
            db.session.commit()
            return jsonify({'message': 'Role deleted successfully'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
