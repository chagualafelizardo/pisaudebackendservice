from flask import Blueprint
from controllers.ItemLocationNecessidadeController import ItemLocationNecessidadeController

necessidade_bp = Blueprint('necessidade', __name__)

# 🔹 Rotas CRUD básicas
@necessidade_bp.route('/necessidade', methods=['GET'])
def get_necessidades():
    return ItemLocationNecessidadeController.get_all()

@necessidade_bp.route('/necessidade/<int:id>', methods=['GET'])
def get_necessidade(id):
    return ItemLocationNecessidadeController.get_by_id(id)

@necessidade_bp.route('/necessidade', methods=['POST'])
def create_necessidade():
    return ItemLocationNecessidadeController.create()

@necessidade_bp.route('/necessidade/<int:id>', methods=['PUT'])
def update_necessidade(id):
    return ItemLocationNecessidadeController.update(id)

@necessidade_bp.route('/necessidade/<int:id>', methods=['DELETE'])
def delete_necessidade(id):
    return ItemLocationNecessidadeController.delete(id)

# 🔹 Nova rota para listar necessidades de um item específico
@necessidade_bp.route('/necessidade/item/<int:item_id>', methods=['GET'])
def get_necessidades_por_item(item_id):
    return ItemLocationNecessidadeController.get_by_item(item_id)
