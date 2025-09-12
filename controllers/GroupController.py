from flask import jsonify, request
from models import db, Group
from datetime import datetime

class GroupController:
    @staticmethod
    def get_all():
        try:
            groups = Group.query.all()
            return jsonify([{
                'id': group.id,
                'description': group.description,
                'createAt': group.createAt,
                'updateAt': group.updateAt
            } for group in groups]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            group = Group.query.get(id)  # Corrigido: Group com G maiúsculo
            if group:
                return jsonify({
                    'id': group.id,
                    'description': group.description,
                    'createAt': group.createAt,
                    'updateAt': group.updateAt
                }), 200
            return jsonify({'message': 'group not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            if not data or 'description' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            if Group.query.filter_by(description=data['description']).first():
                return jsonify({'message': 'Grupo already exists'}), 400

            novo_group = Group(  # Corrigido: Group com G maiúsculo
                description=data['description']
            )

            db.session.add(novo_group)
            db.session.commit()

            return jsonify({
                'id': novo_group.id,
                'description': novo_group.description,
                'createAt': novo_group.createAt,
                'updateAt': novo_group.updateAt
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            group = Group.query.get(id)
            if not group:
                return jsonify({'message': 'group not found'}), 404

            data = request.get_json()
            if not data or 'description' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            existing = Group.query.filter(  # Corrigido: Group com G maiúsculo
                Group.description == data['description'],
                Group.id != id
            ).first()
            if existing:
                return jsonify({'message': 'group with this description already exists'}), 400

            group.description = data['description']
            group.updateAt = datetime.utcnow()

            db.session.commit()

            return jsonify({
                'id': group.id,
                'description': group.description,
                'createAt': group.createAt,  # Corrigido: group em vez de grupo
                'updateAt': group.updateAt   # Corrigido: group em vez de grupo
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            group = Group.query.get(id)  # Corrigido: Group com G maiúsculo
            if not group:
                return jsonify({'message': 'group not found'}), 404

            db.session.delete(group)
            db.session.commit()

            return jsonify({'message': 'group deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500