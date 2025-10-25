from flask import Blueprint
from controllers.ArmazemController import ArmazemController

armazem_bp = Blueprint('armazem', __name__)

@armazem_bp.route('/armazem', methods=['GET'])
def get_armazens():
    return ArmazemController.get_all()

@armazem_bp.route('/armazem/<int:id>', methods=['GET'])
def get_armazem(id):
    return ArmazemController.get_by_id(id)

@armazem_bp.route('/armazem', methods=['POST'])
def create_armazem():
    return ArmazemController.create()

@armazem_bp.route('/armazem/<int:id>', methods=['PUT'])
def update_armazem(id):
    return ArmazemController.update(id)

@armazem_bp.route('/armazem/<int:id>', methods=['DELETE'])
def delete_armazem(id):
    return ArmazemController.delete(id)
