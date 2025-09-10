from flask import Blueprint
from controllers.PortaTestagemController import PortaTestagemController

portatestagem_bp = Blueprint('portatestagem', __name__)

@portatestagem_bp.route('/portatestagem', methods=['GET'])
def get_all_portas_testagem():
    return PortaTestagemController.get_all()

@portatestagem_bp.route('/portatestagem/<int:id>', methods=['GET'])
def get_porta_testagem(id):
    return PortaTestagemController.get_by_id(id)

@portatestagem_bp.route('/portatestagem', methods=['POST'])
def create_porta_testagem():
    return PortaTestagemController.create()

@portatestagem_bp.route('/portatestagem/<int:id>', methods=['PUT'])
def update_porta_testagem(id):
    return PortaTestagemController.update(id)

@portatestagem_bp.route('/portatestagem/<int:id>', methods=['DELETE'])
def delete_porta_testagem(id):
    return PortaTestagemController.delete(id)