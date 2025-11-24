from flask import Blueprint
from controllers.GroupController import GroupController

group_bp = Blueprint('group', __name__)

@group_bp.route('/group', methods=['GET'])
def get_grupos():
    return GroupController.get_all()

@group_bp.route('/group/<int:id>', methods=['GET'])
def get_grupo(id):
    return GroupController.get_by_id(id)

@group_bp.route('/group', methods=['POST'])
def create_grupo():
    return GroupController.create()

@group_bp.route('/group/<int:id>', methods=['PUT'])
def update_grupo(id):
    return GroupController.update(id)

@group_bp.route('/group/<int:id>', methods=['DELETE'])
def delete_grupo(id):
    return GroupController.delete(id)

# 🔥 NOVA ROTA PARA INSERIR PACIENTES NO GRUPO
@group_bp.route('/group/addmembersingrup', methods=['POST'])
def add_members():
    return GroupController.add_members()
