import logging
from flask import jsonify, request
from models import db, Provincia
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

VALID_SYNC_STATUS = ['Not Syncronized', 'Syncronized', 'Updated']


class ProvinciaController:

    @staticmethod
    def serialize(provincia: Provincia):
        return {
            'id': provincia.id,
            'nome': provincia.nome,
            'syncStatus': provincia.syncStatus.value if hasattr(provincia.syncStatus, 'value') else provincia.syncStatus,
            'syncStatusDate': provincia.syncStatusDate.isoformat() if provincia.syncStatusDate else None,
            'createAt': provincia.createAt.isoformat() if provincia.createAt else None,
            'updateAt': provincia.updateAt.isoformat() if provincia.updateAt else None
        }

    @staticmethod
    def get_all():
        try:
            provincias = Provincia.query.all()
            return jsonify([ProvinciaController.serialize(p) for p in provincias]), 200
        except Exception as e:
            logger.exception("[GET ALL] Provincia failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            provincia = Provincia.query.get(id)
            if not provincia:
                return jsonify({'message': 'Provincia not found'}), 404
            return jsonify(ProvinciaController.serialize(provincia)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Provincia {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            sync_status = data.get('syncStatus')
            if sync_status not in VALID_SYNC_STATUS:
                sync_status = 'Not Syncronized'

            provincia = Provincia(
                nome=data['nome'],
                syncStatus=sync_status,
                syncStatusDate=datetime.fromisoformat(data['syncStatusDate']) if data.get('syncStatusDate') else None
            )
            db.session.add(provincia)
            db.session.commit()
            return jsonify({'message': 'Provincia created successfully', 'id': provincia.id}), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Provincia failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            provincia = Provincia.query.get(id)
            if not provincia:
                return jsonify({'message': 'Provincia not found'}), 404

            data = request.get_json()
            provincia.nome = data.get('nome', provincia.nome)
            if 'syncStatus' in data and data['syncStatus'] in VALID_SYNC_STATUS:
                provincia.syncStatus = data['syncStatus']
            if 'syncStatusDate' in data and data['syncStatusDate']:
                provincia.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])

            db.session.commit()
            return jsonify({'message': 'Provincia updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Provincia {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            provincia = Provincia.query.get(id)
            if not provincia:
                return jsonify({'message': 'Provincia not found'}), 404
            db.session.delete(provincia)
            db.session.commit()
            return jsonify({'message': 'Provincia deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Provincia {id}")
            return jsonify({'error': str(e)}), 500
