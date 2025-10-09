from flask import Blueprint
from controllers.FormaPrestacaoServicoController import FormaPrestacaoServicoController

forma_prestacao_servico_bp = Blueprint('forma_prestacao_servico', __name__)

@forma_prestacao_servico_bp.route('/serviceform', methods=['GET'])
def get_service_forms():
    return FormaPrestacaoServicoController.get_all()

@forma_prestacao_servico_bp.route('/serviceform/<int:id>', methods=['GET'])
def get_service_form(id):
    return FormaPrestacaoServicoController.get_by_id(id)

@forma_prestacao_servico_bp.route('/serviceform', methods=['POST'])
def create_service_form():
    return FormaPrestacaoServicoController.create()

@forma_prestacao_servico_bp.route('/serviceform/<int:id>', methods=['PUT'])
def update_service_form(id):
    return FormaPrestacaoServicoController.update(id)

@forma_prestacao_servico_bp.route('/serviceform/<int:id>', methods=['DELETE'])
def delete_service_form(id):
    return FormaPrestacaoServicoController.delete(id)
