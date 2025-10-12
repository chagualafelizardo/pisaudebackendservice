from flask import Blueprint
from controllers.FormacaoController import FormacaoController

formacao_bp = Blueprint('formacao', __name__)

@formacao_bp.route('/formacao', methods=['GET'])
def get_formacoes():
    return FormacaoController.get_all()

@formacao_bp.route('/formacao/<int:id>', methods=['GET'])
def get_formacao(id):
    return FormacaoController.get_by_id(id)

@formacao_bp.route('/formacao', methods=['POST'])
def create_formacao():
    return FormacaoController.create()

@formacao_bp.route('/formacao/<int:id>', methods=['PUT'])
def update_formacao(id):
    return FormacaoController.update(id)

@formacao_bp.route('/formacao/<int:id>', methods=['DELETE'])
def delete_formacao(id):
    return FormacaoController.delete(id)
