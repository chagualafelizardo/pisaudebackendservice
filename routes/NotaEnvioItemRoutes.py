from flask import Blueprint
from controllers.NotaEnvioItemController import NotaEnvioItemController

# 🔹 Criação do Blueprint
nota_envio_item_bp = Blueprint('nota_envio_item', __name__)

# ===============================================================
# 🔹 ROTAS PADRÃO CRUD
# ===============================================================

@nota_envio_item_bp.route('/notaenvioitem', methods=['GET'])
def get_nota_envio_itens():
    """Listar todos os registros de NotaEnvioItem"""
    return NotaEnvioItemController.get_all()


@nota_envio_item_bp.route('/notaenvioitem/<int:id>', methods=['GET'])
def get_nota_envio_item(id):
    """Buscar NotaEnvioItem por ID"""
    return NotaEnvioItemController.get_by_id(id)


@nota_envio_item_bp.route('/notaenvioitem', methods=['POST'])
def create_nota_envio_item():
    """Criar novo NotaEnvioItem"""
    return NotaEnvioItemController.create()


@nota_envio_item_bp.route('/notaenvioitem/<int:id>', methods=['PUT'])
def update_nota_envio_item(id):
    """Atualizar NotaEnvioItem existente"""
    return NotaEnvioItemController.update(id)


@nota_envio_item_bp.route('/notaenvioitem/<int:id>', methods=['DELETE'])
def delete_nota_envio_item(id):
    """Excluir NotaEnvioItem"""
    return NotaEnvioItemController.delete(id)


# ===============================================================
# 🔹 ROTA EXTRA — Buscar itens de uma Nota específica
# ===============================================================

@nota_envio_item_bp.route('/notaenvio/<int:nota_envio_id>/itens', methods=['GET'])
def get_itens_by_nota(nota_envio_id):
    """Listar todos os itens associados a uma NotaEnvio"""
    return NotaEnvioItemController.get_by_nota(nota_envio_id)
