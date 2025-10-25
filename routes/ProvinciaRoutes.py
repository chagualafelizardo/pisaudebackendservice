from flask import Blueprint
from controllers.ProvinciaController import ProvinciaController

provincia_bp = Blueprint('provincia', __name__)

@provincia_bp.route('/provincia', methods=['GET'])
def get_provincias():
    return ProvinciaController.get_all()

@provincia_bp.route('/provincia/<int:id>', methods=['GET'])
def get_provincia(id):
    return ProvinciaController.get_by_id(id)

@provincia_bp.route('/provincia', methods=['POST'])
def create_provincia():
    return ProvinciaController.create()

@provincia_bp.route('/provincia/<int:id>', methods=['PUT'])
def update_provincia(id):
    return ProvinciaController.update(id)

@provincia_bp.route('/provincia/<int:id>', methods=['DELETE'])
def delete_provincia(id):
    return ProvinciaController.delete(id)
