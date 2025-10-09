import logging
from flask import jsonify, request
from models import db, SituacaoGeral, SyncStatusEnum
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class SituacaoGeralController:

    @staticmethod
    def get_all():
        try:
            situacoes = SituacaoGeral.query.all()
            result = []
            for s in situacoes:
                result.append({
                    'id': s.id,
                    'description': s.description,
                    'syncStatus': s.syncStatus.value,
                    'syncStatusDate': s.syncStatusDate.isoformat() if s.syncStatusDate else None,
                    'createAt': s.createAt.isoformat() if s.createAt else None,
                    'updateAt': s.updateAt.isoformat() if s.updateAt else None,
                })
            return jsonify(result), 200
        except Exception as e:
            logger.exception("[GET ALL] Failed to fetch situações gerais")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            s = SituacaoGeral.query.get(id)
            if not s:
                return jsonify({'message': 'Situação Geral not found'}), 404

            return jsonify({
                'id': s.id,
                'description': s.description,
                'syncStatus': s.syncStatus.value,
                'syncStatusDate': s.syncStatusDate.isoformat() if s.syncStatusDate else None,
                'createAt': s.createAt.isoformat() if s.createAt else None,
                'updateAt': s.updateAt.isoformat() if s.updateAt else None,
            }), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch situação geral ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            description = data.get('description')
            if not description:
                return jsonify({'message': 'Description is required'}), 400

            if SituacaoGeral.query.filter_by(description=description).first():
                return jsonify({'message': 'Situação Geral already exists'}), 400

            new_situacao = SituacaoGeral(description=description)
            db.session.add(new_situacao)
            db.session.commit()

            return jsonify({
                'message': 'Situação Geral created successfully',
                'id': new_situacao.id,
                'description': new_situacao.description
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create situação geral")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            s = SituacaoGeral.query.get(id)
            if not s:
                return jsonify({'message': 'Situação Geral not found'}), 404

            data = request.get_json()
            description = data.get('description')
            if not description:
                return jsonify({'message': 'Description is required'}), 400

            existing = SituacaoGeral.query.filter(SituacaoGeral.description == description, SituacaoGeral.id != id).first()
            if existing:
                return jsonify({'message': 'Description already in use'}), 400

            s.description = description
            s.updateAt = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Situação Geral updated successfully',
                'id': s.id,
                'description': s.description
            }), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update situação geral ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            s = SituacaoGeral.query.get(id)
            if not s:
                return jsonify({'message': 'Situação Geral not found'}), 404

            db.session.delete(s)
            db.session.commit()
            return jsonify({'message': 'Situação Geral deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete situação geral ID {id}")
            return jsonify({'error': str(e)}), 500
