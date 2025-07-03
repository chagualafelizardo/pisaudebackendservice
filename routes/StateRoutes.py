from flask import Blueprint
from controllers.StateController import StateController

state_bp = Blueprint('state', __name__)

@state_bp.route('/state', methods=['GET'])
def get_estados():
    return StateController.get_all()

@state_bp.route('/state/<int:id>', methods=['GET'])
def get_estado(id):
    return StateController.get_by_id(id)

@state_bp.route('/state', methods=['POST'])
def create_estado():
    return StateController.create()

@state_bp.route('/state/<int:id>', methods=['PUT'])
def update_estado(id):
    return StateController.update(id)

@state_bp.route('/state/<int:id>', methods=['DELETE'])
def delete_estado(id):
    return StateController.delete(id)