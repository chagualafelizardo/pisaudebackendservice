from flask import Blueprint
from controllers.ItemHistoricoController import ItemHistoricoController

historico_bp = Blueprint('historico', __name__)

# Listar todos os históricos
@historico_bp.route('/historico', methods=['GET'])
def get_historicos():
    return ItemHistoricoController.get_all()

# Listar históricos de um item específico
@historico_bp.route('/item/<int:item_id>/historico', methods=['GET'])
def get_historicos_por_item(item_id):
    return ItemHistoricoController.get_all(item_id=item_id)

# Buscar histórico por ID
@historico_bp.route('/historico/<int:id>', methods=['GET'])
def get_historico(id):
    return ItemHistoricoController.get_by_id(id)

# Criar novo histórico
@historico_bp.route('/historico', methods=['POST'])
def create_historico():
    return ItemHistoricoController.create()

# Atualizar histórico existente
@historico_bp.route('/historico/<int:id>', methods=['PUT'])
def update_historico(id):
    return ItemHistoricoController.update(id)

# Remover histórico
@historico_bp.route('/historico/<int:id>', methods=['DELETE'])
def delete_historico(id):
    return ItemHistoricoController.delete(id)
