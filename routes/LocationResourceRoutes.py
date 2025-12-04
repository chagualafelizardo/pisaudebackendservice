from flask import Blueprint
from controllers.LocationResourceController import LocationResourceController

location_resource_bp = Blueprint('location_resource', __name__)

# 🔹 GET ALL
@location_resource_bp.route('/locationresources', methods=['GET'])
def get_location_resources():
    return LocationResourceController.get_all()

# 🔹 GET BY ID
@location_resource_bp.route('/locationresources/<int:id>', methods=['GET'])
def get_location_resource(id):
    return LocationResourceController.get_by_id(id)

# 🔹 CREATE
@location_resource_bp.route('/locationresources', methods=['POST'])
def create_location_resource():
    return LocationResourceController.create()

# 🔹 UPDATE
@location_resource_bp.route('/locationresources/<int:id>', methods=['PUT'])
def update_location_resource(id):
    return LocationResourceController.update(id)

# 🔹 DELETE
@location_resource_bp.route('/locationresources/<int:id>', methods=['DELETE'])
def delete_location_resource(id):
    return LocationResourceController.delete(id)
