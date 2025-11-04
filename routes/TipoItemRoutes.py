from flask import Blueprint
from controllers.TipoItemController import TipoItemController

tipo_item_bp = Blueprint('tipo_item', __name__)

@tipo_item_bp.route('/tipo_item', methods=['GET'])
def get_tipo_itens():
    return TipoItemController.get_all()

@tipo_item_bp.route('/tipo_item/<int:id>', methods=['GET'])
def get_tipo_item(id):
    return TipoItemController.get_by_id(id)

@tipo_item_bp.route('/tipo_item', methods=['POST'])
def create_tipo_item():
    return TipoItemController.create()

@tipo_item_bp.route('/tipo_item/<int:id>', methods=['PUT'])
def update_tipo_item(id):
    return TipoItemController.update(id)

@tipo_item_bp.route('/tipo_item/<int:id>', methods=['DELETE'])
def delete_tipo_item(id):
    return TipoItemController.delete(id)
