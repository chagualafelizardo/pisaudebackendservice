from flask import Blueprint
from controllers.PortoController import PortoController

porto_bp = Blueprint('porto', __name__)

@porto_bp.route('/porto', methods=['GET'])
def get_portos():
    return PortoController.get_all()

@porto_bp.route('/porto/<int:id>', methods=['GET'])
def get_porto(id):
    return PortoController.get_by_id(id)

@porto_bp.route('/porto', methods=['POST'])
def create_porto():
    return PortoController.create()

@porto_bp.route('/porto/<int:id>', methods=['PUT'])
def update_porto(id):
    return PortoController.update(id)

@porto_bp.route('/porto/<int:id>', methods=['DELETE'])
def delete_porto(id):
    return PortoController.delete(id)
