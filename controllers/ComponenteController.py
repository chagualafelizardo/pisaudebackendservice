from flask import request, jsonify
from models import db, Componente
from datetime import datetime

class ComponenteController:
    @staticmethod
    def get_all():
        """Listar todos os componentes"""
        try:
            componentes = Componente.query.all()
            return jsonify([
                {
                    'id': c.id,
                    'componente_id': c.componente_id,
                    'descricao': c.descricao,
                    'is_active': c.is_active,
                    'createAt': c.createAt,
                    'updateAt': c.updateAt
                } for c in componentes
            ]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        """Buscar componente por ID"""
        try:
            componente = Componente.query.get(id)
            if not componente:
                return jsonify({'message': 'Componente not found'}), 404

            return jsonify({
                'id': componente.id,
                'componente_id': componente.componente_id,
                'descricao': componente.descricao,
                'is_active': componente.is_active,
                'createAt': componente.createAt,
                'updateAt': componente.updateAt
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        """Criar novo componente"""
        try:
            data = request.get_json()
            required_fields = ['componente_id', 'descricao']
            if not all(field in data for field in required_fields):
                return jsonify({'message': 'Missing required data'}), 400

            # Evitar duplicação de componente_id ou descricao
            if Componente.query.filter_by(componente_id=data['componente_id']).first():
                return jsonify({'message': 'Componente ID already exists'}), 400
            if Componente.query.filter_by(descricao=data['descricao']).first():
                return jsonify({'message': 'Componente description already exists'}), 400

            new_componente = Componente(
                componente_id=data['componente_id'],
                descricao=data['descricao'],
                is_active=data.get('is_active', True)
            )

            db.session.add(new_componente)
            db.session.commit()

            return jsonify({
                'id': new_componente.id,
                'componente_id': new_componente.componente_id,
                'descricao': new_componente.descricao,
                'is_active': new_componente.is_active
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        """Atualizar componente existente"""
        try:
            componente = Componente.query.get(id)
            if not componente:
                return jsonify({'message': 'Componente not found'}), 404

            data = request.get_json()
            if 'componente_id' in data:
                existing = Componente.query.filter(
                    Componente.componente_id == data['componente_id'],
                    Componente.id != id
                ).first()
                if existing:
                    return jsonify({'message': 'Componente ID already exists'}), 400
                componente.componente_id = data['componente_id']

            if 'descricao' in data:
                existing_desc = Componente.query.filter(
                    Componente.descricao == data['descricao'],
                    Componente.id != id
                ).first()
                if existing_desc:
                    return jsonify({'message': 'Componente description already exists'}), 400
                componente.descricao = data['descricao']

            if 'is_active' in data:
                componente.is_active = bool(data['is_active'])

            componente.updateAt = datetime.utcnow()
            db.session.commit()

            return jsonify({'message': 'Componente updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        """Remover componente"""
        try:
            componente = Componente.query.get(id)
            if not componente:
                return jsonify({'message': 'Componente not found'}), 404

            db.session.delete(componente)
            db.session.commit()
            return jsonify({'message': 'Componente deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
