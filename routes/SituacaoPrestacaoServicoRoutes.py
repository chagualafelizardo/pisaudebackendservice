from flask import Blueprint
from controllers.SituacaoPrestacaoServicoController import SituacaoPrestacaoServicoController

situacao_prestacao_servico_bp = Blueprint('situacao_servico', __name__)

@situacao_prestacao_servico_bp.route('/situacaoprestacaoservico', methods=['GET'])
def get_all():
    return SituacaoPrestacaoServicoController.get_all()

@situacao_prestacao_servico_bp.route('/situacaoprestacaoservico/<int:id>', methods=['GET'])
def get_by_id(id):
    return SituacaoPrestacaoServicoController.get_by_id(id)

@situacao_prestacao_servico_bp.route('/situacaoprestacaoservico', methods=['POST'])
def create():
    return SituacaoPrestacaoServicoController.create()

@situacao_prestacao_servico_bp.route('/situacaoprestacaoservico/<int:id>', methods=['PUT'])
def update(id):
    return SituacaoPrestacaoServicoController.update(id)

@situacao_prestacao_servico_bp.route('/situacaoprestacaoservico/<int:id>', methods=['DELETE'])
def delete(id):
    return SituacaoPrestacaoServicoController.delete(id)
