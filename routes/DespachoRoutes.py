from flask import Blueprint
from controllers.DespachoController import DespachoController

despacho_bp = Blueprint('despacho', __name__)

@despacho_bp.route('/despacho', methods=['GET'])
def get_despachos():
    return DespachoController.get_all()

@despacho_bp.route('/despacho/<int:id>', methods=['GET'])
def get_despacho(id):
    return DespachoController.get_by_id(id)

@despacho_bp.route('/despacho', methods=['POST'])
def create_despacho():
    return DespachoController.create()

@despacho_bp.route('/despacho/<int:id>', methods=['PUT'])
def update_despacho(id):
    return DespachoController.update(id)

@despacho_bp.route('/despacho/<int:id>', methods=['DELETE'])
def delete_despacho(id):
    return DespachoController.delete(id)
