from flask import Blueprint, request, jsonify
from models import db, MedicamentoLocation

medicamento_location_bp = Blueprint('medicamento_location', __name__)

@medicamento_location_bp.route('/medicamento-location/medicamento/<int:medicamento_id>', methods=['GET'])
def get_by_medicamento(medicamento_id):
    """Retorna todas as configurações de stock para um medicamento"""
    configs = MedicamentoLocation.query.filter_by(medicamento_id=medicamento_id).all()
    return jsonify([{
        'id': c.id,
        'location_id': c.location_id,
        'stock_minimo': c.stock_minimo,
        'stock_maximo': c.stock_maximo
    } for c in configs])

@medicamento_location_bp.route('/medicamento-location/medicamento/<int:medicamento_id>', methods=['POST'])
def save_for_medicamento(medicamento_id):
    """Recebe uma lista de configurações e cria/atualiza os registos"""
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({'error': 'Esperada uma lista de configurações'}), 400

    for item in data:
        location_id = item.get('location_id')
        stock_minimo = item.get('stock_minimo', 0)
        stock_maximo = item.get('stock_maximo', 0)

        if not location_id:
            continue

        config = MedicamentoLocation.query.filter_by(
            medicamento_id=medicamento_id,
            location_id=location_id
        ).first()

        if config:
            config.stock_minimo = stock_minimo
            config.stock_maximo = stock_maximo
        else:
            config = MedicamentoLocation(
                medicamento_id=medicamento_id,
                location_id=location_id,
                stock_minimo=stock_minimo,
                stock_maximo=stock_maximo
            )
            db.session.add(config)

    db.session.commit()
    return jsonify({'message': 'Configurações salvas com sucesso'}), 200

@medicamento_location_bp.route('/medicamento-location', methods=['GET'])
def get_all():
    """Retorna todas as configurações de stock mínimo/máximo (todos os medicamentos e localizações)"""
    configs = MedicamentoLocation.query.all()
    return jsonify([{
        'id': c.id,
        'medicamento_id': c.medicamento_id,
        'location_id': c.location_id,
        'stock_minimo': c.stock_minimo,
        'stock_maximo': c.stock_maximo
    } for c in configs])

@medicamento_location_bp.route('/medicamento-location/<int:id>', methods=['DELETE'])
def delete(id):
    """Remove uma configuração específica (se necessário)"""
    config = MedicamentoLocation.query.get_or_404(id)
    db.session.delete(config)
    db.session.commit()
    return jsonify({'message': 'Configuração removida'}), 200