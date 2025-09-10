from flask import Blueprint
from controllers.KeyPopulationController import KeyPopulationController

keypopulation_bp = Blueprint('keypopulation', __name__)

@keypopulation_bp.route('/keypopulation', methods=['GET'])
def get_all_key_populations():
    return KeyPopulationController.get_all()

@keypopulation_bp.route('/keypopulation/<int:id>', methods=['GET'])
def get_key_population(id):
    return KeyPopulationController.get_by_id(id)

@keypopulation_bp.route('/keypopulation', methods=['POST'])
def create_key_population():
    return KeyPopulationController.create()

@keypopulation_bp.route('/keypopulation/<int:id>', methods=['PUT'])
def update_key_population(id):
    return KeyPopulationController.update(id)

@keypopulation_bp.route('/keypopulation/<int:id>', methods=['DELETE'])
def delete_key_population(id):
    return KeyPopulationController.delete(id)