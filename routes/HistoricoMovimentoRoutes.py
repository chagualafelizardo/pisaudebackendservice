from flask import Blueprint
from controllers.HistoricoMovimentoController import HistoricoMovimentoController

historico_movimento_bp = Blueprint('historico_movimento', __name__)

@historico_movimento_bp.route('/historico_movimento', methods=['GET'])
def get_all_movimentos():
    """Lista todos os movimentos históricos com suporte a filtros (unidade, medicamento, datas, tipo)"""
    return HistoricoMovimentoController.get_all()

@historico_movimento_bp.route('/historico_movimento/<int:id>', methods=['GET'])
def get_movimento(id):
    """Obtém um movimento histórico específico pelo ID"""
    return HistoricoMovimentoController.get_by_id(id)

@historico_movimento_bp.route('/historico_movimento', methods=['POST'])
def create_movimento():
    """Regista um novo movimento histórico (entrada, saída ou ajuste)"""
    return HistoricoMovimentoController.create()

@historico_movimento_bp.route('/historico_movimento/<int:id>', methods=['PUT'])
def update_movimento(id):
    """Atualiza um movimento histórico existente"""
    return HistoricoMovimentoController.update(id)

@historico_movimento_bp.route('/historico_movimento/<int:id>', methods=['DELETE'])
def delete_movimento(id):
    """Remove um movimento histórico (apenas administrador)"""
    return HistoricoMovimentoController.delete(id)