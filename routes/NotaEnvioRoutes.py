from flask import Blueprint
from controllers.NotaEnvioController import NotaEnvioController

nota_envio_bp = Blueprint('nota_envio', __name__)

@nota_envio_bp.route('/notaenvio', methods=['GET'])
def get_notas_envio():
    return NotaEnvioController.get_all()

@nota_envio_bp.route('/notaenvio/<int:id>', methods=['GET'])
def get_nota_envio(id):
    return NotaEnvioController.get_by_id(id)

@nota_envio_bp.route('/notaenvio', methods=['POST'])
def create_nota_envio():
    return NotaEnvioController.create()

@nota_envio_bp.route('/notaenvio/<int:id>', methods=['PUT'])
def update_nota_envio(id):
    return NotaEnvioController.update(id)

@nota_envio_bp.route('/notaenvio/<int:id>', methods=['DELETE'])
def delete_nota_envio(id):
    return NotaEnvioController.delete(id)