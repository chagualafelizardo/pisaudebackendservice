from flask import Blueprint
from controllers.SubunidadeController import SubunidadeController

subunidade_bp = Blueprint('subunidade', __name__)

@subunidade_bp.route('/subunidade', methods=['GET'])
def get_subunidades():
    return SubunidadeController.get_all()

@subunidade_bp.route('/subunidade/<int:id>', methods=['GET'])
def get_subunidade(id):
    return SubunidadeController.get_by_id(id)

@subunidade_bp.route('/subunidade', methods=['POST'])
def create_subunidade():
    return SubunidadeController.create()

@subunidade_bp.route('/subunidade/<int:id>', methods=['PUT'])
def update_subunidade(id):
    return SubunidadeController.update(id)

@subunidade_bp.route('/subunidade/<int:id>', methods=['DELETE'])
def delete_subunidade(id):
    return SubunidadeController.delete(id)
