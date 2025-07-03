# controllers/portatestagem_controller.py
from datetime import datetime
from flask import jsonify, request
from models import db
from models.PortaTestagem import PortaTestagem


class PortaTestagemController:
    # GET /portatestagens
    @staticmethod
    def get_all():
        try:
            portas = PortaTestagem.query.all()
            return jsonify([{
                'id': porta.id,
                'description': porta.description,
                'created_at': porta.created_at,
                'updated_at': porta.updated_at
            } for porta in portas]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # GET /portatestagens/<id>
    @staticmethod
    def get_by_id(id):
        try:
            porta = PortaTestagem.query.get(id)
            if porta:
                return jsonify({
                    'id': porta.id,
                    'description': porta.description,
                    'created_at': porta.created_at,
                    'updated_at': porta.updated_at
                }), 200
            return jsonify({'message': 'PortaTestagem not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # POST /portatestagens
    @staticmethod
    def create():
        try:
            data = request.get_json()
            if not data or 'description' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            # Verifica duplicidade
            if PortaTestagem.query.filter_by(description=data['description']).first():
                return jsonify({'message': 'PortaTestagem already exists'}), 400

            nova_porta = PortaTestagem(description=data['description'])

            db.session.add(nova_porta)
            db.session.commit()

            return jsonify({
                'id': nova_porta.id,
                'description': nova_porta.description,
                'created_at': nova_porta.created_at,
                'updated_at': nova_porta.updated_at
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # PUT /portatestagens/<id>
    @staticmethod
    def update(id):
        try:
            porta = PortaTestagem.query.get(id)
            if not porta:
                return jsonify({'message': 'PortaTestagem not found'}), 404

            data = request.get_json()
            if not data or 'description' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            # Verifica se já existe outra porta com a mesma descrição
            if PortaTestagem.query.filter(
                PortaTestagem.description == data['description'],
                PortaTestagem.id != id
            ).first():
                return jsonify({'message': 'Another PortaTestagem with this description already exists'}), 400

            porta.description = data['description']
            porta.updated_at = datetime.utcnow()

            db.session.commit()

            return jsonify({
                'id': porta.id,
                'description': porta.description,
                'created_at': porta.created_at,
                'updated_at': porta.updated_at
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # DELETE /portatestagens/<id>
    @staticmethod
    def delete(id):
        try:
            porta = PortaTestagem.query.get(id)
            if not porta:
                return jsonify({'message': 'PortaTestagem not found'}), 404

            db.session.delete(porta)
            db.session.commit()

            return jsonify({'message': 'PortaTestagem deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
