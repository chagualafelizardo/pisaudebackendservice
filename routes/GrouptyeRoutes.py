from flask import Blueprint
from controllers.GrouptypeController import GrouptypeController

grouptype_bp = Blueprint('grouptype', __name__)

@grouptype_bp.route('/grouptypes', methods=['GET'])
def get_grouptypes():
    return GrouptypeController.get_all()

@grouptype_bp.route('/grouptypes/<int:id>', methods=['GET'])
def get_grouptype(id):
    return GrouptypeController.get_by_id(id)

@grouptype_bp.route('/grouptypes', methods=['POST'])
def create_grouptype():
    return GrouptypeController.create()

@grouptype_bp.route('/grouptypes/<int:id>', methods=['PUT'])
def update_grouptype(id):
    return GrouptypeController.update(id)

@grouptype_bp.route('/grouptypes/<int:id>', methods=['DELETE'])
def delete_grouptype(id):
    return GrouptypeController.delete(id)