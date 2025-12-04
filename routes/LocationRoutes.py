from flask import Blueprint
from controllers.LocationController import LocationController

location_bp = Blueprint('location', __name__)

# Rotas principais de Location
@location_bp.route('/location', methods=['GET'])
def get_locations():
    return LocationController.get_all()

@location_bp.route('/location/<int:id>', methods=['GET'])
def get_location(id):
    return LocationController.get_by_id(id)

@location_bp.route('/location', methods=['POST'])
def create_location():
    return LocationController.create()

@location_bp.route('/location/<int:id>', methods=['PUT'])
def update_location(id):
    return LocationController.update(id)

@location_bp.route('/location/<int:id>', methods=['DELETE'])
def delete_location(id):
    return LocationController.delete(id)

# 🔹 NOVAS ROTAS PARA RESPONSÁVEIS
@location_bp.route('/location/responsaveis', methods=['GET'])
def get_responsaveis():
    return LocationController.get_responsaveis()

# 🔹 NOVAS ROTAS PARA GERIR RECURSOS INDIVIDUAIS DENTRO DE UMA LOCATION
@location_bp.route('/location/<int:location_id>/resource/<int:resource_id>', methods=['PUT'])
def update_location_resource(location_id, resource_id):
    return LocationController.update_resource(location_id, resource_id)

@location_bp.route('/location/<int:location_id>/resource/<int:resource_id>', methods=['DELETE'])
def delete_location_resource(location_id, resource_id):
    return LocationController.delete_resource(location_id, resource_id)