import logging
from flask import jsonify, request
from models import db, FormaPrestacaoServico
from datetime import datetime

logger = logging.getLogger(__name__)

class FormaPrestacaoServicoController:
    @staticmethod
    def get_all():
        try:
            logger.info("[GET ALL] Fetching all service forms")
            forms = FormaPrestacaoServico.query.all()
            result = []
            for f in forms:
                result.append({
                    'id': f.id,
                    'description': f.description,
                    'createAt': f.createAt.isoformat() if f.createAt else None,
                    'updateAt': f.updateAt.isoformat() if f.updateAt else None
                })
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"[GET ALL] Failed to fetch service forms: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            logger.info(f"[GET BY ID] Fetching service form ID: {id}")
            f = FormaPrestacaoServico.query.get(id)
            if not f:
                logger.warning(f"[GET BY ID] Service form ID {id} not found")
                return jsonify({'message': 'Service form not found'}), 404

            return jsonify({
                'id': f.id,
                'description': f.description,
                'createAt': f.createAt.isoformat() if f.createAt else None,
                'updateAt': f.updateAt.isoformat() if f.updateAt else None
            }), 200
        except Exception as e:
            logger.error(f"[GET BY ID] Error fetching service form ID {id}: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            description = data.get('description')

            if not description:
                logger.warning("[CREATE] Missing description")
                return jsonify({'message': 'Missing required data'}), 400

            if FormaPrestacaoServico.query.filter_by(description=description).first():
                logger.warning(f"[CREATE] Service form '{description}' already exists")
                return jsonify({'message': 'Service form already exists'}), 400

            new_form = FormaPrestacaoServico(description=description)
            db.session.add(new_form)
            db.session.commit()

            logger.info(f"[CREATE] Service form '{description}' created successfully with ID {new_form.id}")
            return jsonify({
                'message': 'Service form created successfully',
                'id': new_form.id,
                'description': new_form.description,
                'createAt': new_form.createAt.isoformat() if new_form.createAt else None,
                'updateAt': new_form.updateAt.isoformat() if new_form.updateAt else None
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"[CREATE] Failed to create service form: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            f = FormaPrestacaoServico.query.get(id)
            if not f:
                logger.warning(f"[UPDATE] Service form ID {id} not found")
                return jsonify({'message': 'Service form not found'}), 404

            data = request.get_json()
            description = data.get('description')

            if not description:
                logger.warning(f"[UPDATE] Missing data for service form ID {id}")
                return jsonify({'message': 'Missing required data'}), 400

            if FormaPrestacaoServico.query.filter(FormaPrestacaoServico.description == description, FormaPrestacaoServico.id != id).first():
                logger.warning(f"[UPDATE] Service form description '{description}' already in use")
                return jsonify({'message': 'Description already in use'}), 400

            f.description = description
            f.updateAt = datetime.utcnow()
            db.session.commit()

            logger.info(f"[UPDATE] Service form ID {id} updated successfully")
            return jsonify({
                'message': 'Service form updated successfully',
                'id': f.id,
                'description': f.description,
                'createAt': f.createAt.isoformat() if f.createAt else None,
                'updateAt': f.updateAt.isoformat() if f.updateAt else None
            }), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"[UPDATE] Failed to update service form ID {id}: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            f = FormaPrestacaoServico.query.get(id)
            if not f:
                logger.warning(f"[DELETE] Service form ID {id} not found")
                return jsonify({'message': 'Service form not found'}), 404

            db.session.delete(f)
            db.session.commit()
            logger.info(f"[DELETE] Service form ID {id} deleted successfully")
            return jsonify({'message': 'Service form deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"[DELETE] Failed to delete service form ID {id}: {e}")
            return jsonify({'error': str(e)}), 500
