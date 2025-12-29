from flask import Blueprint
from controllers.ObservationController import ObservationController
from controllers.DashboardController import DashboardController

observation_bp = Blueprint('observation', __name__)

@observation_bp.route('/observation', methods=['GET'])
def get_observations():
    return ObservationController.get_all()

@observation_bp.route('/observation/<int:id>', methods=['GET'])
def get_observation(id):
    return ObservationController.get_by_id(id)

@observation_bp.route('/observation', methods=['POST'])
def create_observation():
    return ObservationController.create()

@observation_bp.route('/observation/<int:id>', methods=['PUT'])
def update_observation(id):
    return ObservationController.update(id)

@observation_bp.route('/observation/<int:id>', methods=['DELETE'])
def delete_observation(id):
    return ObservationController.delete(id)

@observation_bp.route('/observation/confirm/<int:id>', methods=['PUT'])
def confirm_action(id):
    return ObservationController.confirm_action(id)

@observation_bp.route('/observation/smsstatus/<int:id>', methods=['PUT'])
def update_status(id):
    return ObservationController.update_message_status_simplified(id)

# Nova rota para atualizar groupId + textmessageId
@observation_bp.route('/observation/updategroup/<int:id>', methods=['PUT'])
def update_group(id):
    return ObservationController.update_group(id)

@observation_bp.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    return DashboardController.get_dashboard_data()