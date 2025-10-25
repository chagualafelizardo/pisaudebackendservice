from flask import jsonify, request
from models import db, UserComponente, User, Componente
from datetime import datetime

class UserComponenteController:

    @staticmethod
    def get_all():
        """Listar todos os UserComponente"""
        try:
            user_componentes = UserComponente.query.all()
            result = []
            for uc in user_componentes:
                result.append({
                    'id': uc.id,
                    'user_id': uc.user_id,
                    'username': uc.user.fullname if uc.user else None,
                    'componente_id': uc.componente_id,
                    'componente': uc.componente.descricao if uc.componente else None,
                    'can_access': uc.can_access,
                    'createAt': uc.createAt,
                    'updateAt': uc.updateAt
                })
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        """Buscar UserComponente por ID"""
        try:
            uc = UserComponente.query.get(id)
            if not uc:
                return jsonify({'message': 'UserComponente not found'}), 404

            return jsonify({
                'id': uc.id,
                'user_id': uc.user_id,
                'username': uc.user.fullname if uc.user else None,
                'componente_id': uc.componente_id,
                'componente': uc.componente.descricao if uc.componente else None,
                'can_access': uc.can_access,
                'createAt': uc.createAt,
                'updateAt': uc.updateAt
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        """Criar novo UserComponente"""
        try:
            data = request.get_json()
            required_fields = ['user_id', 'componente_id']
            if not all(field in data for field in required_fields):
                return jsonify({'message': 'Missing required data'}), 400

            # Evitar duplicação
            if UserComponente.query.filter_by(user_id=data['user_id'], componente_id=data['componente_id']).first():
                return jsonify({'message': 'This user already has this componente'}), 400

            new_uc = UserComponente(
                user_id=data['user_id'],
                componente_id=data['componente_id'],
                can_access=data.get('can_access', True)
            )

            db.session.add(new_uc)
            db.session.commit()

            return jsonify({'message': 'UserComponente created', 'id': new_uc.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        """Atualizar UserComponente existente"""
        try:
            uc = UserComponente.query.get(id)
            if not uc:
                return jsonify({'message': 'UserComponente not found'}), 404

            data = request.get_json()
            if 'can_access' in data:
                uc.can_access = bool(data['can_access'])
            if 'user_id' in data:
                uc.user_id = data['user_id']
            if 'componente_id' in data:
                uc.componente_id = data['componente_id']

            uc.updateAt = datetime.utcnow()
            db.session.commit()

            return jsonify({'message': 'UserComponente updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        """Remover UserComponente"""
        try:
            uc = UserComponente.query.get(id)
            if not uc:
                return jsonify({'message': 'UserComponente not found'}), 404

            db.session.delete(uc)
            db.session.commit()
            return jsonify({'message': 'UserComponente deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_user(user_id):
        try:
            ucs = UserComponente.query.filter_by(user_id=user_id).all()
            result = []
            for uc in ucs:
                result.append({
                    'id': uc.id,
                    'user_id': uc.user_id,
                    'username': uc.user.fullname if uc.user else None,
                    'componente_id': uc.componente_id,
                    'componente': uc.componente.descricao if uc.componente else None,
                    'can_access': uc.can_access,
                    'createAt': uc.createAt,
                    'updateAt': uc.updateAt
                })
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod    
    def get_user_componentes():
        user_id = request.args.get('userId')
        if user_id:
            return UserComponenteController.get_by_user(int(user_id))
        return UserComponenteController.get_all()