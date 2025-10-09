from flask import Blueprint
from controllers.SituacaoGeralController import SituacaoGeralController

situacao_geral_bp = Blueprint('situacao_geral', __name__)

@situacao_geral_bp.route('/situacaogeral', methods=['GET'])
def get_situacoes():
    return SituacaoGeralController.get_all()

@situacao_geral_bp.route('/situacaogeral/<int:id>', methods=['GET'])
def get_situacao_by_id(id):
    return SituacaoGeralController.get_by_id(id)

@situacao_geral_bp.route('/situacaogeral', methods=['POST'])
def create_situacao():
    return SituacaoGeralController.create()

@situacao_geral_bp.route('/situacaogeral/<int:id>', methods=['PUT'])
def update_situacao(id):
    return SituacaoGeralController.update(id)

@situacao_geral_bp.route('/situacaogeral/<int:id>', methods=['DELETE'])
def delete_situacao(id):
    return SituacaoGeralController.delete(id)
