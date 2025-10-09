from flask import Blueprint
from controllers.AfetacaoController import AfetacaoController

afetacao_bp = Blueprint('afetacao', __name__)

@afetacao_bp.route('/afetacao', methods=['GET'])
def get_afetacoes():
    return AfetacaoController.get_all()

@afetacao_bp.route('/afetacao/<int:id>', methods=['GET'])
def get_afetacao(id):
    return AfetacaoController.get_by_id(id)

@afetacao_bp.route('/afetacao', methods=['POST'])
def create_afetacao():
    return AfetacaoController.create()

@afetacao_bp.route('/afetacao/<int:id>', methods=['PUT'])
def update_afetacao(id):
    return AfetacaoController.update(id)

@afetacao_bp.route('/afetacao/<int:id>', methods=['DELETE'])
def delete_afetacao(id):
    return AfetacaoController.delete(id)
