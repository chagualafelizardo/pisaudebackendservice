from flask import jsonify, request
from models import db, Role
from datetime import datetime

class RoleController:
    @staticmethod
    def get_all():
        try:
            roles = Role.query.all()
            return jsonify([{
                'id': role.id,
                'descriton': role.descriton,
                'createAt': role.createAt,
                'updateAt': role.updateAt
            } for role in roles]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            role = Role.query.get(id)
            if role:
                return jsonify({
                    'id': role.id,
                    'descriton': role.descriton,
                    'createAt': role.createAt,
                    'updateAt': role.updateAt
                }), 200
            return jsonify({'message': 'Role not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            if not data or 'descriton' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            if Role.query.filter_by(descriton=data['descriton']).first():
                return jsonify({'message': 'Role already exists'}), 400

            new_role = Role(descriton=data['descriton'])

            db.session.add(new_role)
            db.session.commit()

            return jsonify({
                'id': new_role.id,
                'descriton': new_role.descriton,
                'createAt': new_role.createAt,
                'updateAt': new_role.updateAt
            }), 201
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
            if not data or 'descriton' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            existing = Role.query.filter(
                Role.descriton == data['descriton'],
                Role.id != id
            ).first()
            if existing:
                return jsonify({'message': 'Role with this description already exists'}), 400

            role.descriton = data['descriton']
            role.updateAt = datetime.utcnow()

            db.session.commit()

            return jsonify({
                'id': role.id,
                'descriton': role.descriton,
                'createAt': role.createAt,
                'updateAt': role.updateAt
            }), 200
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
