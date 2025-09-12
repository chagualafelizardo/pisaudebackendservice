from flask import jsonify, request
from models import db, UserRole, User, Role
from datetime import datetime

class UserRoleController:

    @staticmethod
    def get_all():
        try:
            user_roles = UserRole.query.all()
            result = []
            for ur in user_roles:
                result.append({
                    'id': ur.id,
                    'userId': ur.userId,
                    'username': ur.user.username if ur.user else None,
                    'roleId': ur.roleId,
                    'role': ur.role.description if ur.role else None,
                    'createAt': ur.createAt,
                    'updateAt': ur.updateAt
                })
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            new_user_role = UserRole(
                userId=data['userId'],
                roleId=data['roleId'],
            )
            db.session.add(new_user_role)
            db.session.commit()
            return jsonify({'message': 'UserRole created', 'id': new_user_role.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            ur = UserRole.query.get(id)
            if not ur:
                return jsonify({'message': 'UserRole not found'}), 404

            db.session.delete(ur)
            db.session.commit()
            return jsonify({'message': 'UserRole deleted'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
