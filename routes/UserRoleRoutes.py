from flask import Blueprint
from controllers.UserRoleController import UserRoleController

user_role_bp = Blueprint('user_role', __name__)

@user_role_bp.route('/user-roles', methods=['POST'])
def assign_role():
    return UserRoleController.assign_role_to_user()

@user_role_bp.route('/users/<int:user_id>/roles', methods=['GET'])
def get_user_roles(user_id):
    return UserRoleController.get_user_roles(user_id)

@user_role_bp.route('/user-roles/<int:user_role_id>', methods=['DELETE'])
def remove_role(user_role_id):
    return UserRoleController.remove_role_from_user(user_role_id)

@user_role_bp.route('/roles/<int:role_id>/users', methods=['GET'])
def get_role_users(role_id):
    return UserRoleController.get_users_by_role(role_id)