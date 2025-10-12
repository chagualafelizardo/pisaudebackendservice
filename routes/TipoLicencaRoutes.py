from flask import Blueprint
from controllers.TipoLicencaController import TipoLicencaController

tipo_licenca_bp = Blueprint('tipo_licenca', __name__)

@tipo_licenca_bp.route('/tipolicenca', methods=['GET'])
def get_tipos_licenca():
    return TipoLicencaController.get_all()

@tipo_licenca_bp.route('/tipolicenca/<int:id>', methods=['GET'])
def get_tipo_licenca(id):
    return TipoLicencaController.get_by_id(id)

@tipo_licenca_bp.route('/tipolicenca', methods=['POST'])
def create_tipo_licenca():
    return TipoLicencaController.create()

@tipo_licenca_bp.route('/tipolicenca/<int:id>', methods=['PUT'])
def update_tipo_licenca(id):
    return TipoLicencaController.update(id)

@tipo_licenca_bp.route('/tipolicenca/<int:id>', methods=['DELETE'])
def delete_tipo_licenca(id):
    return TipoLicencaController.delete(id)
