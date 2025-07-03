from flask import Blueprint
from controllers.ObservationController import ObservationController

observation_bp = Blueprint('observation', __name__)

@observation_bp.route('/observations', methods=['GET'])
def get_observations():
    return ObservationController.get_all()

@observation_bp.route('/observations/<int:id>', methods=['GET'])
def get_observation(id):
    return ObservationController.get_by_id(id)

@observation_bp.route('/observations', methods=['POST'])
def create_observation():
    return ObservationController.create()

@observation_bp.route('/observations/<int:id>', methods=['PUT'])
def update_observation(id):
    return ObservationController.update(id)

@observation_bp.route('/observations/<int:id>', methods=['DELETE'])
def delete_observation(id):
    return ObservationController.delete(id)