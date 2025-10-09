import logging
from flask import jsonify, request
from models import db, SituacaoPrestacaoServico, SyncStatusEnum
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class SituacaoPrestacaoServicoController:

    @staticmethod
    def get_all():
        try:
            items = SituacaoPrestacaoServico.query.all()
            result = []
            for i in items:
                result.append({
                    'id': i.id,
                    'description': i.description,
                    'syncStatus': i.syncStatus.value,
                    'syncStatusDate': i.syncStatusDate.isoformat() if i.syncStatusDate else None,
                    'createAt': i.createAt.isoformat() if i.createAt else None,
                    'updateAt': i.updateAt.isoformat() if i.updateAt else None,
                })
            return jsonify(result), 200
        except Exception as e:
            logger.exception("[GET ALL] Failed to fetch situacoes")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            item = SituacaoPrestacaoServico.query.get(id)
            if not item:
                return jsonify({'message': 'Item not found'}), 404

            return jsonify({
                'id': item.id,
                'description': item.description,
                'syncStatus': item.syncStatus.value,
                'syncStatusDate': item.syncStatusDate.isoformat() if item.syncStatusDate else None,
                'createAt': item.createAt.isoformat() if item.createAt else None,
                'updateAt': item.updateAt.isoformat() if item.updateAt else None,
            }), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch item ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            description = data.get('description')
            if not description:
                return jsonify({'message': 'Description is required'}), 400

            if SituacaoPrestacaoServico.query.filter_by(description=description).first():
                return jsonify({'message': 'Already exists'}), 400

            new_item = SituacaoPrestacaoServico(description=description)
            db.session.add(new_item)
            db.session.commit()

            return jsonify({
                'message': 'Created successfully',
                'id': new_item.id,
                'description': new_item.description
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create item")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            item = SituacaoPrestacaoServico.query.get(id)
            if not item:
                return jsonify({'message': 'Item not found'}), 404

            data = request.get_json()
            description = data.get('description')
            if not description:
                return jsonify({'message': 'Description is required'}), 400

            existing = SituacaoPrestacaoServico.query.filter(SituacaoPrestacaoServico.description == description, SituacaoPrestacaoServico.id != id).first()
            if existing:
                return jsonify({'message': 'Description already in use'}), 400

            item.description = description
            item.updateAt = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Updated successfully',
                'id': item.id,
                'description': item.description
            }), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update item ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            item = SituacaoPrestacaoServico.query.get(id)
            if not item:
                return jsonify({'message': 'Item not found'}), 404

            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': 'Deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete item ID {id}")
            return jsonify({'error': str(e)}), 500
