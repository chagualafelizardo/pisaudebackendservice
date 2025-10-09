from flask import Blueprint
from controllers.PatentController import PatentController

patent_bp = Blueprint('patent', __name__)

@patent_bp.route('/patent', methods=['GET'])
def get_patents():
    return PatentController.get_all()

@patent_bp.route('/patent/<int:id>', methods=['GET'])
def get_patent(id):
    return PatentController.get_by_id(id)

@patent_bp.route('/patent', methods=['POST'])
def create_patent():
    return PatentController.create()

@patent_bp.route('/patent/<int:id>', methods=['PUT'])
def update_patent(id):
    return PatentController.update(id)

@patent_bp.route('/patent/<int:id>', methods=['DELETE'])
def delete_patent(id):
    return PatentController.delete(id)
