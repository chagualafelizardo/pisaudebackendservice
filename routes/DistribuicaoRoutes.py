from flask import Blueprint
from controllers.DistribuicaoController import DistribuicaoController

distribuicao_bp = Blueprint('distribuicao', __name__)

@distribuicao_bp.route('/distribuicao', methods=['GET'])
def get_distribuicoes():
    return DistribuicaoController.get_all()

@distribuicao_bp.route('/distribuicao/<int:id>', methods=['GET'])
def get_distribuicao(id):
    return DistribuicaoController.get_by_id(id)

@distribuicao_bp.route('/distribuicao', methods=['POST'])
def create_distribuicao():
    return DistribuicaoController.create()

@distribuicao_bp.route('/distribuicao/<int:id>', methods=['PUT'])
def update_distribuicao(id):
    return DistribuicaoController.update(id)

@distribuicao_bp.route('/distribuicao/<int:id>', methods=['DELETE'])
def delete_distribuicao(id):
    return DistribuicaoController.delete(id)
