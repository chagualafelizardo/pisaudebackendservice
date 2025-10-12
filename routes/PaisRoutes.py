from flask import Blueprint
from controllers.PaisController import PaisController

pais_bp = Blueprint('pais', __name__)

@pais_bp.route('/pais', methods=['GET'])
def get_paises():
    return PaisController.get_all()

@pais_bp.route('/pais/<int:id>', methods=['GET'])
def get_pais(id):
    return PaisController.get_by_id(id)

@pais_bp.route('/pais', methods=['POST'])
def create_pais():
    return PaisController.create()

@pais_bp.route('/pais/<int:id>', methods=['PUT'])
def update_pais(id):
    return PaisController.update(id)

@pais_bp.route('/pais/<int:id>', methods=['DELETE'])
def delete_pais(id):
    return PaisController.delete(id)
