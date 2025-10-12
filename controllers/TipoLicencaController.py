import logging
from flask import jsonify, request
from models import db, TipoLicenca, SyncStatusEnum
from datetime import datetime

# Configuração básica de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TipoLicencaController:

    @staticmethod
    def get_all():
        logger.info("[GET ALL] Request received to fetch all tipos de licença.")
        try:
            tipos = TipoLicenca.query.all()
            logger.info(f"[GET ALL] Found {len(tipos)} tipos de licença.")
            
            result = []
            for t in tipos:
                logger.debug(f"[GET ALL] Tipo: id={t.id}, description={t.description}")
                result.append({
                    'id': t.id,
                    'description': t.description,
                    'syncStatus': t.syncStatus.value if t.syncStatus else None,
                    'syncStatusDate': t.syncStatusDate.isoformat() if t.syncStatusDate else None,
                    'createAt': t.createAt.isoformat() if t.createAt else None,
                    'updateAt': t.updateAt.isoformat() if t.updateAt else None,
                })

            logger.info(f"[GET ALL] Returning {len(result)} tipos de licença as JSON.")
            response = jsonify(result)
            logger.info(f"[GET ALL] Response type: {type(response)}")
            return response, 200

        except Exception as e:
            logger.exception("[GET ALL] Failed to fetch tipos de licença.")
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def get_by_id(id):
        logger.info(f"[GET BY ID] Request received for tipo de licença ID {id}.")
        try:
            t = TipoLicenca.query.get(id)
            if not t:
                logger.warning(f"[GET BY ID] Tipo de Licença with ID {id} not found.")
                return jsonify({'message': 'Tipo de Licença not found'}), 404

            logger.info(f"[GET BY ID] Returning tipo de licença: {t.description}")
            return jsonify({
                'id': t.id,
                'description': t.description,
                'syncStatus': t.syncStatus.value,
                'syncStatusDate': t.syncStatusDate.isoformat() if t.syncStatusDate else None,
                'createAt': t.createAt.isoformat() if t.createAt else None,
                'updateAt': t.updateAt.isoformat() if t.updateAt else None,
            }), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch tipo de licença ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        logger.info("[CREATE] Request received to create new tipo de licença.")
        try:
            data = request.get_json(force=True)
            logger.info(f"[CREATE] Received data: {data}")

            description = data.get('description')
            if not description:
                logger.warning("[CREATE] Missing description field.")
                return jsonify({'message': 'Description is required'}), 400

            if TipoLicenca.query.filter_by(description=description).first():
                logger.warning(f"[CREATE] Tipo de Licença '{description}' already exists.")
                return jsonify({'message': 'Tipo de Licença already exists'}), 400

            new_tipo = TipoLicenca(description=description)
            db.session.add(new_tipo)
            db.session.commit()

            logger.info(f"[CREATE] Tipo de Licença '{description}' created successfully with ID {new_tipo.id}.")
            return jsonify({
                'message': 'Tipo de Licença created successfully',
                'id': new_tipo.id,
                'description': new_tipo.description
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create tipo de licença.")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        logger.info(f"[UPDATE] Request received to update tipo de licença ID {id}.")
        try:
            t = TipoLicenca.query.get(id)
            if not t:
                logger.warning(f"[UPDATE] Tipo de Licença with ID {id} not found.")
                return jsonify({'message': 'Tipo de Licença not found'}), 404

            data = request.get_json(force=True)
            logger.info(f"[UPDATE] Received data: {data}")

            description = data.get('description')
            if not description:
                logger.warning("[UPDATE] Missing description field.")
                return jsonify({'message': 'Description is required'}), 400

            existing = TipoLicenca.query.filter(
                TipoLicenca.description == description,
                TipoLicenca.id != id
            ).first()

            if existing:
                logger.warning(f"[UPDATE] Description '{description}' already in use by ID {existing.id}.")
                return jsonify({'message': 'Description already in use'}), 400

            t.description = description
            t.updateAt = datetime.utcnow()
            db.session.commit()

            logger.info(f"[UPDATE] Tipo de Licença ID {id} updated successfully.")
            return jsonify({
                'message': 'Tipo de Licença updated successfully',
                'id': t.id,
                'description': t.description
            }), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update tipo de licença ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        logger.info(f"[DELETE] Request received to delete tipo de licença ID {id}.")
        try:
            t = TipoLicenca.query.get(id)
            if not t:
                logger.warning(f"[DELETE] Tipo de Licença with ID {id} not found.")
                return jsonify({'message': 'Tipo de Licença not found'}), 404

            db.session.delete(t)
            db.session.commit()
            logger.info(f"[DELETE] Tipo de Licença ID {id} deleted successfully.")
            return jsonify({'message': 'Tipo de Licença deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete tipo de licença ID {id}")
            return jsonify({'error': str(e)}), 500
