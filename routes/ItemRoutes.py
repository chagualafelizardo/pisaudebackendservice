from flask import Blueprint
from controllers.ItemController import ItemController

item_bp = Blueprint('item', __name__)

@item_bp.route('/item', methods=['GET'])
def get_itens():
    return ItemController.get_all()

@item_bp.route('/item/<int:id>', methods=['GET'])
def get_item(id):
    return ItemController.get_by_id(id)

@item_bp.route('/item', methods=['POST'])
def create_item():
    return ItemController.create()

@item_bp.route('/item/<int:id>', methods=['PUT'])
def update_item(id):
    return ItemController.update(id)

@item_bp.route('/item/<int:id>', methods=['DELETE'])
def delete_item(id):
    return ItemController.delete(id)
