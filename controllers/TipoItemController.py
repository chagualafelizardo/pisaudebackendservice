import logging
from flask import jsonify, request
from models import db, TipoItem

# 🔹 Configuração global de logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)


class TipoItemController:

    @staticmethod
    def serialize(t: TipoItem):
        return {
            'id': t.id,
            'nome': t.nome
        }

    # 🔹 Listar todos
    @staticmethod
    def get_all():
        logger.info("[GET ALL] Iniciando busca de todos os TipoItem")
        try:
            tipos = TipoItem.query.all()
            logger.info(f"[GET ALL] Encontrados {len(tipos)} registros de TipoItem")
            return jsonify([TipoItemController.serialize(t) for t in tipos]), 200
        except Exception as e:
            logger.exception("[GET ALL] Erro ao buscar TipoItem")
            return jsonify({'error': str(e)}), 500

    # 🔹 Buscar por ID
    @staticmethod
    def get_by_id(id):
        logger.info(f"[GET BY ID] Solicitado TipoItem ID={id}")
        try:
            tipo = TipoItem.query.get(id)
            if not tipo:
                logger.warning(f"[GET BY ID] TipoItem ID={id} não encontrado")
                return jsonify({'message': 'TipoItem não encontrado'}), 404
            logger.info(f"[GET BY ID] TipoItem ID={id} encontrado")
            return jsonify(TipoItemController.serialize(tipo)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Erro ao buscar TipoItem ID={id}")
            return jsonify({'error': str(e)}), 500

    # 🔹 Criar novo
    @staticmethod
    def create():
        logger.info("[CREATE] Solicitada criação de novo TipoItem")
        try:
            data = request.get_json(force=True, silent=True)
            logger.info(f"[CREATE] Dados recebidos: {data}")

            if not data or not data.get('nome'):
                logger.warning("[CREATE] Campo 'nome' ausente ou vazio")
                return jsonify({'message': 'Nome é obrigatório'}), 400

            tipo = TipoItem(nome=data['nome'])
            db.session.add(tipo)
            db.session.commit()

            logger.info(f"[CREATE] TipoItem criado com sucesso ID={tipo.id}")
            return jsonify({'message': 'TipoItem criado com sucesso', 'id': tipo.id}), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Erro ao criar TipoItem")
            return jsonify({'error': str(e)}), 500

    # 🔹 Atualizar
    @staticmethod
    def update(id):
        logger.info(f"[UPDATE] Solicitada atualização do TipoItem ID={id}")
        try:
            tipo = TipoItem.query.get(id)
            if not tipo:
                logger.warning(f"[UPDATE] TipoItem ID={id} não encontrado")
                return jsonify({'message': 'TipoItem não encontrado'}), 404

            data = request.get_json(force=True, silent=True)
            logger.info(f"[UPDATE] Dados recebidos: {data}")
            tipo.nome = data.get('nome', tipo.nome)

            db.session.commit()
            logger.info(f"[UPDATE] TipoItem ID={id} atualizado com sucesso")
            return jsonify({'message': 'TipoItem atualizado com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Erro ao atualizar TipoItem ID={id}")
            return jsonify({'error': str(e)}), 500

    # 🔹 Deletar
    @staticmethod
    def delete(id):
        logger.info(f"[DELETE] Solicitada exclusão de TipoItem ID={id}")
        try:
            tipo = TipoItem.query.get(id)
            if not tipo:
                logger.warning(f"[DELETE] TipoItem ID={id} não encontrado")
                return jsonify({'message': 'TipoItem não encontrado'}), 404

            db.session.delete(tipo)
            db.session.commit()

            logger.info(f"[DELETE] TipoItem ID={id} excluído com sucesso")
            return jsonify({'message': 'TipoItem excluído com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Erro ao excluir TipoItem ID={id}")
            return jsonify({'error': str(e)}), 500
