import logging
from flask import jsonify, request
from models import db, ItemPendente
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ItensPendentesController:

    # 🔹 SERIALIZAR DADOS
    @staticmethod
    def serialize(item: ItemPendente):
        return {
            'id': item.id,
            'nome_item': item.nome_item,
            'quantidade_esperada': item.quantidade_esperada,
            'prioridade': item.prioridade,
            'data_esperada_entrega': item.data_esperada_entrega.isoformat() if item.data_esperada_entrega else None,
            'categoria': item.categoria,
            'observacoes': item.observacoes,
            'fornecedor_origem': item.fornecedor_origem,
            'data_registro': item.data_registro.isoformat() if item.data_registro else None
        }

    # 🔹 LISTAR TODOS
    @staticmethod
    def get_all():
        try:
            itens = ItemPendente.query.all()
            return jsonify([ItensPendentesController.serialize(i) for i in itens]), 200
        except Exception as e:
            logger.exception("[GET ALL] ItensPendentes failed")
            return jsonify({'error': str(e)}), 500

    # 🔹 OBTER POR ID
    @staticmethod
    def get_by_id(id):
        try:
            item = ItemPendente.query.get(id)
            if not item:
                return jsonify({'message': 'Item pendente não encontrado'}), 404
            return jsonify(ItensPendentesController.serialize(item)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] ItensPendentes {id} failed")
            return jsonify({'error': str(e)}), 500

    # 🔹 CRIAR NOVO
    @staticmethod
    def create():
        try:
            data = request.get_json()
            item = ItemPendente(
                nome_item=data.get('nome_item'),
                quantidade_esperada=data.get('quantidade_esperada'),
                prioridade=data.get('prioridade'),
                data_esperada_entrega=datetime.fromisoformat(data['data_esperada_entrega'])
                if data.get('data_esperada_entrega') else None,
                categoria=data.get('categoria'),
                observacoes=data.get('observacoes'),
                fornecedor_origem=data.get('fornecedor_origem')
            )
            db.session.add(item)
            db.session.commit()
            logger.info(f"[CREATE] Item pendente criado: {item.nome_item}")
            return jsonify({'message': 'Item pendente criado com sucesso', 'id': item.id}), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] ItensPendentes failed")
            return jsonify({'error': str(e)}), 500

    # 🔹 ATUALIZAR EXISTENTE
    @staticmethod
    def update(id):
        try:
            item = ItemPendente.query.get(id)
            if not item:
                return jsonify({'message': 'Item pendente não encontrado'}), 404

            data = request.get_json()
            item.nome_item = data.get('nome_item', item.nome_item)
            item.quantidade_esperada = data.get('quantidade_esperada', item.quantidade_esperada)
            item.prioridade = data.get('prioridade', item.prioridade)
            if data.get('data_esperada_entrega'):
                item.data_esperada_entrega = datetime.fromisoformat(data['data_esperada_entrega'])
            item.categoria = data.get('categoria', item.categoria)
            item.observacoes = data.get('observacoes', item.observacoes)
            item.fornecedor_origem = data.get('fornecedor_origem', item.fornecedor_origem)

            db.session.commit()
            logger.info(f"[UPDATE] Item pendente atualizado: ID={id}")
            return jsonify({'message': 'Item pendente atualizado com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] ItensPendentes {id} failed")
            return jsonify({'error': str(e)}), 500

    # 🔹 EXCLUIR ITEM
    @staticmethod
    def delete(id):
        try:
            item = ItemPendente.query.get(id)
            if not item:
                return jsonify({'message': 'Item pendente não encontrado'}), 404
            db.session.delete(item)
            db.session.commit()
            logger.info(f"[DELETE] Item pendente removido: ID={id}")
            return jsonify({'message': 'Item pendente removido com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] ItensPendentes {id} failed")
            return jsonify({'error': str(e)}), 500
