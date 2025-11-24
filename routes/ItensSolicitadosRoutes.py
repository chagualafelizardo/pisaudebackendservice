from flask import Blueprint
from controllers.ItemsSolicitadosController import ItemsSolicitadosController

items_solicitados_bp = Blueprint('items_solicitados', __name__)

@items_solicitados_bp.route('/items_solicitados', methods=['GET'])
def get_items_solicitados():
    return ItemsSolicitadosController.get_all()

@items_solicitados_bp.route('/items_solicitados/<int:id>', methods=['GET'])
def get_item_solicitado(id):
    return ItemsSolicitadosController.get_by_id(id)

@items_solicitados_bp.route('/items_solicitados', methods=['POST'])
def create_item_solicitado():
    return ItemsSolicitadosController.create()

@items_solicitados_bp.route('/items_solicitados/<int:id>', methods=['PUT'])
def update_item_solicitado(id):
    return ItemsSolicitadosController.update(id)

@items_solicitados_bp.route('/items_solicitados/<int:id>', methods=['DELETE'])
def delete_item_solicitado(id):
    return ItemsSolicitadosController.delete(id)
