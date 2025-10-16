from flask import Blueprint
from controllers.LicencaController import LicencaController

licenca_bp = Blueprint('licenca', __name__)

@licenca_bp.route('/licenca', methods=['GET'])
def get_licencas():
    return LicencaController.get_all()

@licenca_bp.route('/licenca/<int:id>', methods=['GET'])
def get_licenca(id):
    return LicencaController.get_by_id(id)

@licenca_bp.route('/licenca', methods=['POST'])
def create_licenca():
    return LicencaController.create()

@licenca_bp.route('/licenca/<int:id>', methods=['PUT'])
def update_licenca(id):
    return LicencaController.update(id)

@licenca_bp.route('/licenca/<int:id>', methods=['DELETE'])
def delete_licenca(id):
    return LicencaController.delete(id)
