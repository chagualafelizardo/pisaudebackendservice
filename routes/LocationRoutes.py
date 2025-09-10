from flask import Blueprint
from controllers.LocationController import LocationController

location_bp = Blueprint('location', __name__)

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