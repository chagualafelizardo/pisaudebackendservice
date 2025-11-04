import logging
from flask import jsonify, request
from models import db, Distribuicao, Item, Armazem, Location
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DistribuicaoController:

    @staticmethod
    def serialize(d: Distribuicao):
        return {
            'id': d.id,
            'item_id': d.item_id,
            'item_nome': d.item.designacao if d.item else None,
            'armazem_id': d.armazem_id,
            'armazem_nome': d.armazem.nome if d.armazem else None,
            'location_id': d.location_id,
            'location_nome': d.location.name if d.location else None,
            'quantidade': d.quantidade,
            'data_distribuicao': d.data_distribuicao.isoformat() if d.data_distribuicao else None,
            'observacao': d.observacao
        }

    @staticmethod
    def get_all():
        try:
            distribuicoes = Distribuicao.query.all()
            return jsonify([DistribuicaoController.serialize(d) for d in distribuicoes]), 200
        except Exception as e:
            logger.exception("[GET ALL] Distribuicao failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            distribuicao = Distribuicao.query.get(id)
            if not distribuicao:
                return jsonify({'message': 'Distribuicao not found'}), 404
            return jsonify(DistribuicaoController.serialize(distribuicao)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Distribuicao {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            distribuicao = Distribuicao(
                item_id=data['item_id'],
                armazem_id=data['armazem_id'],
                location_id=data['location_id'],
                quantidade=data['quantidade'],
                data_distribuicao=datetime.fromisoformat(data['data_distribuicao']) if data.get('data_distribuicao') else datetime.utcnow(),
                observacao=data.get('observacao')
            )
            db.session.add(distribuicao)
            db.session.commit()
            return jsonify({'message': 'Distribuicao created successfully', 'id': distribuicao.id}), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Distribuicao failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            distribuicao = Distribuicao.query.get(id)
            if not distribuicao:
                return jsonify({'message': 'Distribuicao not found'}), 404

            data = request.get_json()
            distribuicao.item_id = data.get('item_id', distribuicao.item_id)
            distribuicao.armazem_id = data.get('armazem_id', distribuicao.armazem_id)
            distribuicao.location_id = data.get('location_id', distribuicao.location_id)
            distribuicao.quantidade = data.get('quantidade', distribuicao.quantidade)
            if 'data_distribuicao' in data and data['data_distribuicao']:
                distribuicao.data_distribuicao = datetime.fromisoformat(data['data_distribuicao'])
            distribuicao.observacao = data.get('observacao', distribuicao.observacao)

            db.session.commit()
            return jsonify({'message': 'Distribuicao updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Distribuicao {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            distribuicao = Distribuicao.query.get(id)
            if not distribuicao:
                return jsonify({'message': 'Distribuicao not found'}), 404
            db.session.delete(distribuicao)
            db.session.commit()
            return jsonify({'message': 'Distribuicao deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Distribuicao {id}")
            return jsonify({'error': str(e)}), 500
