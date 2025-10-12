from flask import Blueprint
from controllers.EspecialidadeSaudeController import EspecialidadeSaudeController

especialidade_saude_bp = Blueprint('especialidade_saude', __name__)

# GET all especialidades de saúde
@especialidade_saude_bp.route('/especialidadesaude', methods=['GET'])
def get_especialidades_saude():
    return EspecialidadeSaudeController.get_all()

# GET especialidade de saúde by ID
@especialidade_saude_bp.route('/especialidadesaude/<int:id>', methods=['GET'])
def get_especialidade_saude(id):
    return EspecialidadeSaudeController.get_by_id(id)

# POST create new especialidade de saúde
@especialidade_saude_bp.route('/especialidadesaude', methods=['POST'])
def create_especialidade_saude():
    return EspecialidadeSaudeController.create()

# PUT update existing especialidade de saúde
@especialidade_saude_bp.route('/especialidadesaude/<int:id>', methods=['PUT'])
def update_especialidade_saude(id):
    return EspecialidadeSaudeController.update(id)

# DELETE remove especialidade de saúde
@especialidade_saude_bp.route('/especialidadesaude/<int:id>', methods=['DELETE'])
def delete_especialidade_saude(id):
    return EspecialidadeSaudeController.delete(id)
