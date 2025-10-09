from flask import Blueprint
from controllers.TransferenciaController import TransferenciaController

transferencia_bp = Blueprint('transferencia', __name__)

@transferencia_bp.route('/transferencia', methods=['GET'])
def get_transferencias():
    return TransferenciaController.get_all()

@transferencia_bp.route('/transferencia/<int:id>', methods=['GET'])
def get_transferencia(id):
    return TransferenciaController.get_by_id(id)

@transferencia_bp.route('/transferencia', methods=['POST'])
def create_transferencia():
    return TransferenciaController.create()

@transferencia_bp.route('/transferencia/<int:id>', methods=['PUT'])
def update_transferencia(id):
    return TransferenciaController.update(id)

@transferencia_bp.route('/transferencia/<int:id>', methods=['DELETE'])
def delete_transferencia(id):
    return TransferenciaController.delete(id)
