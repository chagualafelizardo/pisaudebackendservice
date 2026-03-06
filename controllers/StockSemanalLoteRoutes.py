from flask import Blueprint
from controllers.StockSemanalLoteController import StockSemanalLoteController

stock_semanal_lote_bp = Blueprint('stock_semanal_lote', __name__)

@stock_semanal_lote_bp.route('/stock_semanal_lote', methods=['GET'])
def get_all_lotes():
    """Lista todos os lotes de stock semanal. Suporta filtro opcional ?id_stock_semanal=..."""
    return StockSemanalLoteController.get_all()

@stock_semanal_lote_bp.route('/stock_semanal_lote/<int:id>', methods=['GET'])
def get_lote(id):
    """Obtém um lote específico pelo ID"""
    return StockSemanalLoteController.get_by_id(id)

@stock_semanal_lote_bp.route('/stock_semanal_lote', methods=['POST'])
def create_lote():
    """Cria um novo lote associado a um registo de stock semanal existente"""
    return StockSemanalLoteController.create()

@stock_semanal_lote_bp.route('/stock_semanal_lote/<int:id>', methods=['PUT'])
def update_lote(id):
    """Atualiza um lote existente"""
    return StockSemanalLoteController.update(id)

@stock_semanal_lote_bp.route('/stock_semanal_lote/<int:id>', methods=['DELETE'])
def delete_lote(id):
    """Remove um lote"""
    return StockSemanalLoteController.delete(id)