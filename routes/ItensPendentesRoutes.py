from flask import Blueprint
from controllers.ItensPendentesController import ItensPendentesController

# 🔹 Blueprint principal
itens_pendentes_bp = Blueprint('itens_pendentes', __name__)

# ===============================================================
# 🔹 ROTAS CRUD BÁSICAS
# ===============================================================

@itens_pendentes_bp.route('/itenspendentes', methods=['GET'])
def get_itens_pendentes():
    return ItensPendentesController.get_all()

@itens_pendentes_bp.route('/itenspendentes/<int:id>', methods=['GET'])
def get_item_pendente(id):
    return ItensPendentesController.get_by_id(id)

@itens_pendentes_bp.route('/itenspendentes', methods=['POST'])
def create_item_pendente():
    return ItensPendentesController.create()

@itens_pendentes_bp.route('/itenspendentes/<int:id>', methods=['PUT'])
def update_item_pendente(id):
    return ItensPendentesController.update(id)

@itens_pendentes_bp.route('/itenspendentes/<int:id>', methods=['DELETE'])
def delete_item_pendente(id):
    return ItensPendentesController.delete(id)
