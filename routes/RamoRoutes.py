from flask import Blueprint
from controllers.RamoController import RamoController

ramo_bp = Blueprint('ramo', __name__)

@ramo_bp.route('/ramo', methods=['GET'])
def get_ramos():
    return RamoController.get_all()

@ramo_bp.route('/ramo/<int:id>', methods=['GET'])
def get_ramo(id):
    return RamoController.get_by_id(id)

@ramo_bp.route('/ramo', methods=['POST'])
def create_ramo():
    return RamoController.create()

@ramo_bp.route('/ramo/<int:id>', methods=['PUT'])
def update_ramo(id):
    return RamoController.update(id)

@ramo_bp.route('/ramo/<int:id>', methods=['DELETE'])
def delete_ramo(id):
    return RamoController.delete(id)
