import logging
from flask import jsonify, request
from models import db, NotaEnvioItem

# 🔹 Configuração global de logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)


class NotaEnvioItemController:

    @staticmethod
    def serialize(n: NotaEnvioItem):
        return {
            'id': n.id,
            'nota_envio_id': n.nota_envio_id,
            'item_id': n.item_id,
            'quantidade_enviada': n.quantidade_enviada
        }

    # 🔹 Listar todos
    @staticmethod
    def get_all():
        logger.info("[GET ALL] Iniciando busca de todos os NotaEnvioItem")
        try:
            itens = NotaEnvioItem.query.all()
            logger.info(f"[GET ALL] Encontrados {len(itens)} registros de NotaEnvioItem")
            return jsonify([NotaEnvioItemController.serialize(i) for i in itens]), 200
        except Exception as e:
            logger.exception("[GET ALL] Erro ao buscar NotaEnvioItem")
            return jsonify({'error': str(e)}), 500

    # 🔹 Buscar por ID
    @staticmethod
    def get_by_id(id):
        logger.info(f"[GET BY ID] Solicitado NotaEnvioItem ID={id}")
        try:
            item = NotaEnvioItem.query.get(id)
            if not item:
                logger.warning(f"[GET BY ID] NotaEnvioItem ID={id} não encontrado")
                return jsonify({'message': 'NotaEnvioItem não encontrado'}), 404

            logger.info(f"[GET BY ID] NotaEnvioItem ID={id} encontrado")
            return jsonify(NotaEnvioItemController.serialize(item)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Erro ao buscar NotaEnvioItem ID={id}")
            return jsonify({'error': str(e)}), 500

    # 🔹 Buscar por NotaEnvio (para listar todos os itens de uma nota)
    @staticmethod
    def get_by_nota(nota_envio_id):
        logger.info(f"[GET BY NOTA] Itens associados à NotaEnvio ID={nota_envio_id}")
        try:
            itens = NotaEnvioItem.query.filter_by(nota_envio_id=nota_envio_id).all()
            if not itens:
                logger.warning(f"[GET BY NOTA] Nenhum item encontrado para NotaEnvio ID={nota_envio_id}")
                return jsonify({'message': 'Nenhum item encontrado para esta nota'}), 404

            logger.info(f"[GET BY NOTA] Encontrados {len(itens)} itens para NotaEnvio ID={nota_envio_id}")
            return jsonify([NotaEnvioItemController.serialize(i) for i in itens]), 200
        except Exception as e:
            logger.exception(f"[GET BY NOTA] Erro ao buscar itens da NotaEnvio ID={nota_envio_id}")
            return jsonify({'error': str(e)}), 500

    # 🔹 Criar novo
    @staticmethod
    def create():
        logger.info("[CREATE] Solicitada criação de novo NotaEnvioItem")
        try:
            data = request.get_json(force=True, silent=True)
            logger.info(f"[CREATE] Dados recebidos: {data}")

            if not data or not data.get('nota_envio_id') or not data.get('item_id') or not data.get('quantidade_enviada'):
                logger.warning("[CREATE] Campos obrigatórios ausentes")
                return jsonify({'message': 'nota_envio_id, item_id e quantidade_enviada são obrigatórios'}), 400

            novo_item = NotaEnvioItem(
                nota_envio_id=data['nota_envio_id'],
                item_id=data['item_id'],
                quantidade_enviada=data['quantidade_enviada']
            )

            db.session.add(novo_item)
            db.session.commit()

            logger.info(f"[CREATE] NotaEnvioItem criado com sucesso ID={novo_item.id}")
            return jsonify({'message': 'NotaEnvioItem criado com sucesso', 'id': novo_item.id}), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Erro ao criar NotaEnvioItem")
            return jsonify({'error': str(e)}), 500

    # 🔹 Atualizar
    @staticmethod
    def update(id):
        logger.info(f"[UPDATE] Solicitada atualização do NotaEnvioItem ID={id}")
        try:
            item = NotaEnvioItem.query.get(id)
            if not item:
                logger.warning(f"[UPDATE] NotaEnvioItem ID={id} não encontrado")
                return jsonify({'message': 'NotaEnvioItem não encontrado'}), 404

            data = request.get_json(force=True, silent=True)
            logger.info(f"[UPDATE] Dados recebidos: {data}")

            item.nota_envio_id = data.get('nota_envio_id', item.nota_envio_id)
            item.item_id = data.get('item_id', item.item_id)
            item.quantidade_enviada = data.get('quantidade_enviada', item.quantidade_enviada)

            db.session.commit()
            logger.info(f"[UPDATE] NotaEnvioItem ID={id} atualizado com sucesso")
            return jsonify({'message': 'NotaEnvioItem atualizado com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Erro ao atualizar NotaEnvioItem ID={id}")
            return jsonify({'error': str(e)}), 500

    # 🔹 Deletar
    @staticmethod
    def delete(id):
        logger.info(f"[DELETE] Solicitada exclusão de NotaEnvioItem ID={id}")
        try:
            item = NotaEnvioItem.query.get(id)
            if not item:
                logger.warning(f"[DELETE] NotaEnvioItem ID={id} não encontrado")
                return jsonify({'message': 'NotaEnvioItem não encontrado'}), 404

            db.session.delete(item)
            db.session.commit()

            logger.info(f"[DELETE] NotaEnvioItem ID={id} excluído com sucesso")
            return jsonify({'message': 'NotaEnvioItem excluído com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Erro ao excluir NotaEnvioItem ID={id}")
            return jsonify({'error': str(e)}), 500
