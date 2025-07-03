from flask import Blueprint
from controllers.UserController import UserController

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['GET'])
def get_users():
    return UserController.get_all()

@user_bp.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    return UserController.get_by_id(id)

@user_bp.route('/user', methods=['POST'])
def create_user():
    return UserController.create()

@user_bp.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    return UserController.update(id)

@user_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    return UserController.delete(id)
