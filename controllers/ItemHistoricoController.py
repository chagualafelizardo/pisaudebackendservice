from flask import request, jsonify
from models import db, ItemHistorico
from datetime import datetime

class ItemHistoricoController:
    @staticmethod
    def get_all(item_id=None):
        """Listar todos os registros de histórico ou por item"""
        try:
            if item_id:
                historicos = ItemHistorico.query.filter_by(item_id=item_id).all()
            else:
                historicos = ItemHistorico.query.all()

            return jsonify([
                {
                    'id': h.id,
                    'item_id': h.item_id,
                    'tipo_movimento': h.tipo_movimento,
                    'quantidade': h.quantidade,
                    'observacoes': h.observacoes,
                    'user': h.user,  # ✅ Incluir usuário
                    'data_movimento': h.data_movimento.isoformat() if h.data_movimento else None
                } for h in historicos
            ]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        """Buscar registro de histórico por ID"""
        try:
            historico = ItemHistorico.query.get(id)
            if not historico:
                return jsonify({'message': 'Histórico not found'}), 404

            return jsonify({
                'id': historico.id,
                'item_id': historico.item_id,
                'tipo_movimento': historico.tipo_movimento,
                'quantidade': historico.quantidade,
                'observacoes': historico.observacoes,
                'data_movimento': historico.data_movimento.isoformat() if historico.data_movimento else None
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        """Criar novo registro de histórico"""
        try:
            data = request.get_json()
            required_fields = ['item_id', 'tipo_movimento', 'quantidade']
            if not all(field in data for field in required_fields):
                return jsonify({'message': 'Missing required data'}), 400

            new_historico = ItemHistorico(
                item_id=data['item_id'],
                tipo_movimento=data['tipo_movimento'],
                quantidade=data['quantidade'],
                observacoes=data.get('observacoes', ''),
                data_movimento=datetime.utcnow()
            )

            db.session.add(new_historico)
            db.session.commit()

            return jsonify({
                'id': new_historico.id,
                'item_id': new_historico.item_id,
                'tipo_movimento': new_historico.tipo_movimento,
                'quantidade': new_historico.quantidade,
                'observacoes': new_historico.observacoes,
                'data_movimento': new_historico.data_movimento.isoformat()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        """Atualizar registro de histórico existente"""
        try:
            historico = ItemHistorico.query.get(id)
            if not historico:
                return jsonify({'message': 'Histórico not found'}), 404

            data = request.get_json()
            if 'tipo_movimento' in data:
                historico.tipo_movimento = data['tipo_movimento']
            if 'quantidade' in data:
                historico.quantidade = data['quantidade']
            if 'observacoes' in data:
                historico.observacoes = data['observacoes']
            if 'data_movimento' in data:
                historico.data_movimento = datetime.fromisoformat(data['data_movimento'])

            db.session.commit()
            return jsonify({'message': 'Histórico updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        """Remover registro de histórico"""
        try:
            historico = ItemHistorico.query.get(id)
            if not historico:
                return jsonify({'message': 'Histórico not found'}), 404

            db.session.delete(historico)
            db.session.commit()
            return jsonify({'message': 'Histórico deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
