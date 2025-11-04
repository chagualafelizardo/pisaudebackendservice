from flask import jsonify, request
from models import db, Group, ItemHistorico, Item
from datetime import datetime

class StockController:

    @staticmethod
    def adicionar_entrada(item_id, quantidade, observacoes=None):
        try:
            item = Item.query.get(item_id)
            if not item:
                return jsonify({'message': 'Item não encontrado'}), 404

            # Atualizar quantidade atual
            item.quantidade = (item.quantidade or 0) + quantidade

            # Criar registro histórico
            hist = ItemHistorico(
                item_id=item.id,
                quantidade=quantidade,
                tipo_movimento='entrada',
                observacoes=observacoes
            )
            db.session.add(hist)
            db.session.commit()
            return jsonify({'message': 'Entrada de stock registrada com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_historico(item_id):
        try:
            historico = ItemHistorico.query.filter_by(item_id=item_id).order_by(ItemHistorico.data_movimento.desc()).all()
            return jsonify([{
                'id': h.id,
                'quantidade': h.quantidade,
                'tipo_movimento': h.tipo_movimento,
                'data_movimento': h.data_movimento.isoformat(),
                'observacoes': h.observacoes
            } for h in historico]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
