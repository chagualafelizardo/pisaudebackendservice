from flask import Blueprint
from controllers.FuncaoController import FuncaoController

funcao_bp = Blueprint('funcao', __name__)

@funcao_bp.route('/funcao', methods=['GET'])
def get_funcoes():
    return FuncaoController.get_all()

@funcao_bp.route('/funcao/<int:id>', methods=['GET'])
def get_funcao(id):
    return FuncaoController.get_by_id(id)

@funcao_bp.route('/funcao', methods=['POST'])
def create_funcao():
    return FuncaoController.create()

@funcao_bp.route('/funcao/<int:id>', methods=['PUT'])
def update_funcao(id):
    return FuncaoController.update(id)

@funcao_bp.route('/funcao/<int:id>', methods=['DELETE'])
def delete_funcao(id):
    return FuncaoController.delete(id)
