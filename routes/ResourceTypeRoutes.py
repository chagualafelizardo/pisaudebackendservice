from flask import Blueprint
from controllers.ResourceTypeController import ResourceTypeController

resourcetype_bp = Blueprint('resourcetype', __name__)

@resourcetype_bp.route('/resourcetype', methods=['GET'])
def get_resourcetypes():
    return ResourceTypeController.get_all()

@resourcetype_bp.route('/resourcetype/<int:id>', methods=['GET'])
def get_resourcetype(id):
    return ResourceTypeController.get_by_id(id)

@resourcetype_bp.route('/resourcetype', methods=['POST'])
def create_resourcetype():
    return ResourceTypeController.create()

@resourcetype_bp.route('/resourcetype/<int:id>', methods=['PUT'])
def update_resourcetype(id):
    return ResourceTypeController.update(id)

@resourcetype_bp.route('/resourcetype/<int:id>', methods=['DELETE'])
def delete_resourcetype(id):
    return ResourceTypeController.delete(id)
