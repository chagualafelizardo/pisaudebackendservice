from flask import Blueprint
from controllers.StockController import StockController

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/stock', methods=['GET'])
def get_stocks():
    return StockController.get_all()

@stock_bp.route('/stock/<int:id>', methods=['GET'])
def get_stock(id):
    return StockController.get_historico(id)

@stock_bp.route('/stock', methods=['POST'])
def create_stock():
    return StockController.create()

@stock_bp.route('/stock/<int:id>', methods=['PUT'])
def update_stock(id):
    return StockController.update(id)

@stock_bp.route('/stock/<int:id>', methods=['DELETE'])
def delete_stock(id):
    return StockController.delete(id)
