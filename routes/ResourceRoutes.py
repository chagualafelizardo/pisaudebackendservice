from flask import Blueprint
from controllers.ResourceController import ResourceController

resource_bp = Blueprint('resource', __name__)

@resource_bp.route('/resource', methods=['GET'])
def get_resources():
    return ResourceController.get_all()

@resource_bp.route('/resource/<int:id>', methods=['GET'])
def get_resource(id):
    return ResourceController.get_by_id(id)

@resource_bp.route('/resource', methods=['POST'])
def create_resource():
    return ResourceController.create()

@resource_bp.route('/resource/<int:id>', methods=['PUT'])
def update_resource(id):
    return ResourceController.update(id)

@resource_bp.route('/resource/<int:id>', methods=['DELETE'])
def delete_resource(id):
    return ResourceController.delete(id)
