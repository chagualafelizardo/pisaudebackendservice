from flask import Blueprint
from controllers.SubespecialidadeController import SubespecialidadeController

subespecialidade_bp = Blueprint('subespecialidade', __name__)

@subespecialidade_bp.route('/subespecialidade', methods=['GET'])
def get_subespecialidades():
    return SubespecialidadeController.get_all()

@subespecialidade_bp.route('/subespecialidade/<int:id>', methods=['GET'])
def get_subespecialidade(id):
    return SubespecialidadeController.get_by_id(id)

@subespecialidade_bp.route('/subespecialidade', methods=['POST'])
def create_subespecialidade():
    return SubespecialidadeController.create()

@subespecialidade_bp.route('/subespecialidade/<int:id>', methods=['PUT'])
def update_subespecialidade(id):
    return SubespecialidadeController.update(id)

@subespecialidade_bp.route('/subespecialidade/<int:id>', methods=['DELETE'])
def delete_subespecialidade(id):
    return SubespecialidadeController.delete(id)

# ✅ Nova rota para filtrar por especialidade
@subespecialidade_bp.route('/subespecialidade/byespecialidade/<int:especialidade_id>', methods=['GET'])
def get_subespecialidades_by_especialidade(especialidade_id):
    return SubespecialidadeController.get_by_especialidade(especialidade_id)