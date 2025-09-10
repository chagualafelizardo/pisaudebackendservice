from flask import Blueprint
from controllers.RoleController import RoleController

role_bp = Blueprint('role', __name__)

@role_bp.route('/role', methods=['GET'])
def get_roles():
    return RoleController.get_all()

@role_bp.route('/role/<int:id>', methods=['GET'])
def get_role(id):
    return RoleController.get_by_id(id)

@role_bp.route('/role', methods=['POST'])
def create_role():
    return RoleController.create()

@role_bp.route('/role/<int:id>', methods=['PUT'])
def update_role(id):
    return RoleController.update(id)

@role_bp.route('/role/<int:id>', methods=['DELETE'])
def delete_role(id):
    return RoleController.delete(id)
