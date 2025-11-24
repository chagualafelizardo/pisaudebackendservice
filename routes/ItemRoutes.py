from flask import Blueprint
from controllers.ItemController import ItemController
from controllers.ItemLocationNecessidadeController import ItemLocationNecessidadeController

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

@item_bp.route('/item/<int:id>/historico', methods=['GET'])
def get_historico_item(id):
    return ItemController.get_historico(id)

# 🔹 Nova rota para entrada de stock do item
@item_bp.route('/item/<int:id>/entrada', methods=['POST'])
def adicionar_entrada_stock(id):
    return ItemController.adicionar_entrada_stock(id)

# 🔹 Necessidades relacionadas a um Item
@item_bp.route('/item/<int:id>/necessidades', methods=['GET'])
def get_necessidades_item(id):
    """Lista todas as necessidades associadas a um item"""
    return ItemLocationNecessidadeController.get_by_item(id)

@item_bp.route('/item/<int:id>/necessidades', methods=['POST'])
def create_necessidade_item(id):
    """Cria uma nova necessidade associada a um item"""
    return ItemLocationNecessidadeController.create()

# 🔹 Distribuir item
@item_bp.route('/item/<int:item_id>/distribuir', methods=['POST'])
def distribuir_item(item_id):
    return ItemController.distribuir_item(item_id)

# 🔹 Nova rota global para listar TODAS as necessidades com nome do item
@item_bp.route('/item/necessidades', methods=['GET'])
def get_necessidades_por_item():
    """Lista todas as necessidades agrupadas por item (join com Item)"""
    return ItemController.get_necessidades_por_item()

# 🔹 Confirmar recepção de item
@item_bp.route('/item/<int:id>/confirmarrecepcao', methods=['PUT'])
def confirmar_recepcao_item(id):
    """Confirma a recepção de um item (guia assinada, data, recebedor)"""
    return ItemController.confirmar_recepcao(id)
