import logging
from flask import jsonify, request
from models import db, SyncStatusEnum
from models.Funcao import Funcao
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class FuncaoController:

    @staticmethod
    def get_all():
        try:
            funcoes = Funcao.query.all()
            result = []
            for f in funcoes:
                result.append({
                    'id': f.id,
                    'description': f.description,
                    'syncStatus': f.syncStatus.value,
                    'syncStatusDate': f.syncStatusDate.isoformat() if f.syncStatusDate else None,
                    'createAt': f.createAt.isoformat() if f.createAt else None,
                    'updateAt': f.updateAt.isoformat() if f.updateAt else None,
                })
            logger.info("[GET ALL] Retrieved all funções")
            return jsonify(result), 200
        except Exception as e:
            logger.exception("[GET ALL] Failed to fetch funções")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            f = Funcao.query.get(id)
            if not f:
                logger.warning(f"[GET BY ID] Função ID {id} not found")
                return jsonify({'message': 'Função not found'}), 404

            logger.info(f"[GET BY ID] Retrieved função ID {id}")
            return jsonify({
                'id': f.id,
                'description': f.description,
                'syncStatus': f.syncStatus.value,
                'syncStatusDate': f.syncStatusDate.isoformat() if f.syncStatusDate else None,
                'createAt': f.createAt.isoformat() if f.createAt else None,
                'updateAt': f.updateAt.isoformat() if f.updateAt else None,
            }), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch função ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            description = data.get('description')

            if not description:
                logger.warning("[CREATE] Missing description")
                return jsonify({'message': 'Description is required'}), 400

            if Funcao.query.filter_by(description=description).first():
                logger.warning(f"[CREATE] Função '{description}' already exists")
                return jsonify({'message': 'Função already exists'}), 400

            new_funcao = Funcao(description=description)
            db.session.add(new_funcao)
            db.session.commit()

            logger.info(f"[CREATE] Função '{description}' created successfully")
            return jsonify({
                'message': 'Função created successfully',
                'id': new_funcao.id,
                'description': new_funcao.description
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create função")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            f = Funcao.query.get(id)
            if not f:
                logger.warning(f"[UPDATE] Função ID {id} not found")
                return jsonify({'message': 'Função not found'}), 404

            data = request.get_json()
            description = data.get('description')

            if not description:
                logger.warning("[UPDATE] Missing description")
                return jsonify({'message': 'Description is required'}), 400

            existing = Funcao.query.filter(Funcao.description == description, Funcao.id != id).first()
            if existing:
                logger.warning(f"[UPDATE] Description '{description}' already in use")
                return jsonify({'message': 'Description already in use'}), 400

            f.description = description
            f.updateAt = datetime.utcnow()
            db.session.commit()

            logger.info(f"[UPDATE] Função ID {id} updated successfully")
            return jsonify({
                'message': 'Função updated successfully',
                'id': f.id,
                'description': f.description
            }), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update função ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            f = Funcao.query.get(id)
            if not f:
                logger.warning(f"[DELETE] Função ID {id} not found")
                return jsonify({'message': 'Função not found'}), 404

            db.session.delete(f)
            db.session.commit()

            logger.info(f"[DELETE] Função ID {id} deleted successfully")
            return jsonify({'message': 'Função deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete função ID {id}")
            return jsonify({'error': str(e)}), 500
