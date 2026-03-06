from flask import Blueprint
from controllers.MedicamentoController import MedicamentoController

medicamento_bp = Blueprint('medicamento', __name__)

@medicamento_bp.route('/medicamentos', methods=['GET'])
def get_medicamentos():
    """Lista todos os medicamentos"""
    return MedicamentoController.get_all()

@medicamento_bp.route('/medicamentos/<int:id>', methods=['GET'])
def get_medicamento(id):
    """Obtém um medicamento específico pelo ID"""
    return MedicamentoController.get_by_id(id)

@medicamento_bp.route('/medicamentos', methods=['POST'])
def create_medicamento():
    """Cria um novo medicamento"""
    return MedicamentoController.create()

@medicamento_bp.route('/medicamentos/<int:id>', methods=['PUT'])
def update_medicamento(id):
    """Atualiza um medicamento existente"""
    return MedicamentoController.update(id)

@medicamento_bp.route('/medicamentos/<int:id>', methods=['DELETE'])
def delete_medicamento(id):
    """Remove um medicamento (apenas administrador)"""
    return MedicamentoController.delete(id)