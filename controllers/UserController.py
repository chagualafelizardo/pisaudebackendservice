from flask import request, jsonify
from models import db, User, Location
from datetime import datetime

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
                'password': user.password,
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
            required_fields = ['fullname', 'username', 'password','gender', 'email', 'profile', 'contact', 'locationId']  # ← locationId com I maiúsculo
            if not all(field in data for field in required_fields):
                return jsonify({'message': 'Missing required data'}), 400

            # Verifica se já existe um usuário com os mesmos campos únicos
            if User.query.filter_by(username=data['username']).first():
                return jsonify({'message': 'Username already exists'}), 400

            if User.query.filter_by(email=data['email']).first():
                return jsonify({'message': 'Email already exists'}), 400

            if User.query.filter_by(contact=data['contact']).first():
                return jsonify({'message': 'Contact already exists'}), 400

            new_user = User(
                fullname=data['fullname'],
                username=data['username'],
                password=data['password'],
                gender=data['gender'],
                email=data['email'],
                profile=data['profile'],
                contact=data['contact'],
                locationId=data['locationId']  # ← Alterado para locationId
            )

            db.session.add(new_user)
            db.session.commit()

            return jsonify({
                'id': new_user.id,
                'fullname': new_user.fullname,
                'locationId': new_user.locationId  # ← Adicionado na resposta
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            user = User.query.get(id)
            if not user:
                return jsonify({'message': 'User not found'}), 404

            data = request.get_json()
            for field in ['fullname', 'username', 'password','gender', 'email', 'profile', 'contact', 'locationId']:  # ← locationId com I maiúsculo
                if field in data:
                    setattr(user, field, data[field])
            user.updateAt = datetime.utcnow()

            db.session.commit()

            return jsonify({'message': 'User updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
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
            db.session.rollback()
            return jsonify({'error': str(e)}), 500