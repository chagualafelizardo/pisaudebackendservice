from flask import jsonify, request
from models import db, UserRole, User, Role
from datetime import datetime

class UserRoleController:
    @staticmethod
    def assign_role_to_user():
        try:
            data = request.get_json()
            required_fields = ['user_id', 'role_id']
            
            if not all(field in data for field in required_fields):
                return jsonify({'message': 'Missing required fields'}), 400

            # Verifica se user e role existem
            user = User.query.get(data['user_id'])
            role = Role.query.get(data['role_id'])
            
            if not user:
                return jsonify({'message': 'User not found'}), 404
            if not role:
                return jsonify({'message': 'Role not found'}), 404

            # Verifica se a associação já existe
            existing = UserRole.query.filter_by(
                user_id=data['user_id'],
                role_id=data['role_id']
            ).first()
            
            if existing:
                return jsonify({'message': 'Role already assigned to this user'}), 400

            new_assignment = UserRole(
                user_id=data['user_id'],
                role_id=data['role_id']
            )

            db.session.add(new_assignment)
            db.session.commit()

            return jsonify({
                'id': new_assignment.id,
                'message': 'Role assigned to user successfully',
                'user_id': new_assignment.user_id,
                'role_id': new_assignment.role_id
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_user_roles(user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'message': 'User not found'}), 404

            roles = [{
                'role_id': ur.role.id,
                'description': ur.role.descriton,
                'assigned_at': ur.createAt.isoformat()
            } for ur in user.user_roles]

            return jsonify({
                'user_id': user.id,
                'fullname': user.fullname,
                'roles': roles
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def remove_role_from_user(user_role_id):
        try:
            assignment = UserRole.query.get(user_role_id)
            if not assignment:
                return jsonify({'message': 'Assignment not found'}), 404

            db.session.delete(assignment)
            db.session.commit()

            return jsonify({'message': 'Role removed from user successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_users_by_role(role_id):
        try:
            role = Role.query.get(role_id)
            if not role:
                return jsonify({'message': 'Role not found'}), 404

            users = [{
                'user_id': ur.user.id,
                'fullname': ur.user.fullname,
                'username': ur.user.username,
                'assigned_at': ur.createAt.isoformat()
            } for ur in role.user_roles]

            return jsonify({
                'role_id': role.id,
                'description': role.descriton,
                'users': users
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500