from flask import jsonify, request
from models import db, State
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

class StateController:
    @staticmethod
    def get_all():
        try:
            states = State.query.all()
            return jsonify([{
                'id': state.id,
                'description': state.description,
                'createAt': state.createAt,
                'updateAt': state.updateAt
            } for state in states]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            state = State.query.get(id)
            if state:
                return jsonify({
                    'id': state.id,
                    'description': state.description,
                    'createAt': state.createAt,
                    'updateAt': state.updateAt
                }), 200
            return jsonify({'message': 'State not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            if not data or 'description' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            # Verifica se o state já existe
            if State.query.filter_by(description=data['description']).first():
                return jsonify({'message': 'State already exists'}), 400

            novo_state = State(
                description=data['description']
            )

            db.session.add(novo_state)
            db.session.commit()

            return jsonify({
                'id': novo_state.id,
                'description': novo_state.description,
                'createAt': novo_state.createAt,
                'updateAt': novo_state.updateAt
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            state = State.query.get(id)
            if not state:
                return jsonify({'message': 'State not found'}), 404

            data = request.get_json()
            if not data or 'description' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            # Verifica se a nova descrição já existe em outro registro
            existing = State.query.filter(
                State.description == data['description'],
                State.id != id
            ).first()
            if existing:
                return jsonify({'message': 'State with this description already exists'}), 400

            state.description = data['description']
            state.updateAt = datetime.utcnow()

            db.session.commit()

            return jsonify({
                'id': state.id,
                'description': state.description,
                'createAt': state.createAt,
                'updateAt': state.updateAt
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            state = State.query.get(id)
            if not state:
                return jsonify({'message': 'State not found'}), 404

            db.session.delete(state)
            db.session.commit()

            return jsonify({'message': 'State deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500