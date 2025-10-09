from flask import Blueprint
from controllers.EspecialidadeController import EspecialidadeController

especialidade_bp = Blueprint('especialidade', __name__)

@especialidade_bp.route('/especialidade', methods=['GET'])
def get_especialidades():
    return EspecialidadeController.get_all()

@especialidade_bp.route('/especialidade/<int:id>', methods=['GET'])
def get_especialidade(id):
    return EspecialidadeController.get_by_id(id)

@especialidade_bp.route('/especialidade', methods=['POST'])
def create_especialidade():
    return EspecialidadeController.create()

@especialidade_bp.route('/especialidade/<int:id>', methods=['PUT'])
def update_especialidade(id):
    return EspecialidadeController.update(id)

@especialidade_bp.route('/especialidade/<int:id>', methods=['DELETE'])
def delete_especialidade(id):
    return EspecialidadeController.delete(id)
