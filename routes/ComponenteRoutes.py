from flask import Blueprint
from controllers.ComponenteController import ComponenteController

componente_bp = Blueprint('componente', __name__)

@componente_bp.route('/componente', methods=['GET'])
def get_componentes():
    return ComponenteController.get_all()

@componente_bp.route('/componente/<int:id>', methods=['GET'])
def get_componente(id):
    return ComponenteController.get_by_id(id)

@componente_bp.route('/componente', methods=['POST'])
def create_componente():
    return ComponenteController.create()

@componente_bp.route('/componente/<int:id>', methods=['PUT'])
def update_componente(id):
    return ComponenteController.update(id)

@componente_bp.route('/componente/<int:id>', methods=['DELETE'])
def delete_componente(id):
    return ComponenteController.delete(id)
