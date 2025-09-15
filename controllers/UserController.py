from flask import request, jsonify
from models import db, User, Location
from datetime import datetime
from werkzeug.security import generate_password_hash

class UserController:
    @staticmethod
    def get_all():
        try:
            users = User.query.all()
            return jsonify([
                {
                    'id': user.id,
                    'fullname': user.fullname,
                    'username': user.username,
                    'gender': user.gender,
                    'email': user.email,
                    'profile': user.profile,
                    'contact': user.contact,
                    'locationId': user.locationId,  # ← Alterado para locationId
                    'location': user.location.name if user.location else None,
                    'createAt': user.createAt,
                    'updateAt': user.updateAt
                } for user in users
            ]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            user = User.query.get(id)
            if not user:
                return jsonify({'message': 'User not found'}), 404

            return jsonify({
                'id': user.id,
                'fullname': user.fullname,
                'username': user.username,
                'password': '',
                'gender': user.gender,
                'email': user.email,
                'profile': user.profile,
                'contact': user.contact,
                'locationId': user.locationId,  # ← Alterado para locationId
                'location': user.location.name if user.location else None,
                'createAt': user.createAt,
                'updateAt': user.updateAt
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            required_fields = ['fullname', 'username', 'password', 'gender', 'email', 'profile', 'contact', 'locationId']
            if not all(field in data for field in required_fields):
                return jsonify({'message': 'Missing required data'}), 400

            # Verificar duplicatas
            if User.query.filter_by(username=data['username']).first():
                return jsonify({'message': 'Username already exists'}), 400
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'message': 'Email already exists'}), 400
            if User.query.filter_by(contact=data['contact']).first():
                return jsonify({'message': 'Contact already exists'}), 400

            # Hashear a senha
            hashed_password = generate_password_hash(data['password'])

            new_user = User(
                fullname=data['fullname'],
                username=data['username'],
                password=hashed_password,
                gender=data['gender'],
                email=data['email'],
                profile=data['profile'],
                contact=data['contact'],
                locationId=int(data['locationId'])  # ← conversão garantida
            )

            db.session.add(new_user)
            db.session.commit()

            return jsonify({
                'id': new_user.id,
                'fullname': new_user.fullname,
                'locationId': new_user.locationId
            }), 201
        except Exception as e:
            print(f"Erro ao salvar usuário: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            user = User.query.get(id)
            if not user:
                return jsonify({'message': 'User not found'}), 404

            data = request.get_json()

            if 'fullname' in data:
                user.fullname = data['fullname']
            if 'username' in data:
                user.username = data['username']
            if 'gender' in data:
                user.gender = data['gender']
            if 'email' in data:
                user.email = data['email']
            if 'profile' in data:
                user.profile = data['profile']
            if 'contact' in data:
                user.contact = data['contact']
            if 'locationId' in data:
                user.locationId = int(data['locationId'])  # ✅ Conversão aqui

            if 'password' in data and data['password'].strip():
                user.password = generate_password_hash(data['password'])

            user.updateAt = datetime.utcnow()
            db.session.commit()

            return jsonify({'message': 'User updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar usuário: {e}")
            return jsonify({'error': str(e)}), 500
        
    @staticmethod
    def delete(id):
        try:
            user = User.query.get(id)
            if not user:
                return jsonify({'message': 'User not found'}), 404

            db.session.delete(user)
            db.session.commit()

            return jsonify({'message': 'User deleted successfully'}), 200
        except Exception as e:
            print(f"Erro ao salvar usuário: {e}")
            return jsonify({'error': str(e)}), 500