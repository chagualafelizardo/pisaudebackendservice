from flask import Blueprint
from controllers.StockSemanalController import StockSemanalController

stock_semanal_bp = Blueprint('stock_semanal', __name__)

@stock_semanal_bp.route('/stock_semanal', methods=['GET'])
def get_all_stock_semanal():
    return StockSemanalController.get_all()

@stock_semanal_bp.route('/stock_semanal/<int:id>', methods=['GET'])
def get_stock_semanal(id):
    return StockSemanalController.get_by_id(id)

@stock_semanal_bp.route('/stock_semanal', methods=['POST'])
def create_stock_semanal():
    return StockSemanalController.create()

@stock_semanal_bp.route('/stock_semanal/<int:id>', methods=['PUT'])
def update_stock_semanal(id):
    return StockSemanalController.update(id)

@stock_semanal_bp.route('/stock_semanal/<int:id>', methods=['DELETE'])
def delete_stock_semanal(id):
    return StockSemanalController.delete(id)