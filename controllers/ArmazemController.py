import logging
from flask import jsonify, request
from models import db, Armazem, Provincia
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

VALID_SYNC_STATUS = ['Not Syncronized', 'Syncronized', 'Updated']


class ArmazemController:

    @staticmethod
    def serialize(a: Armazem):
        return {
            'id': a.id,
            'nome': a.nome,
            'latitude': a.latitude,
            'longitude': a.longitude,
            'provincia_id': a.provincia_id,
            'provincia_nome': a.provincia.nome if a.provincia else None,
            'syncStatus': a.syncStatus.value if hasattr(a.syncStatus, 'value') else a.syncStatus,
            'syncStatusDate': a.syncStatusDate.isoformat() if a.syncStatusDate else None,
            'createAt': a.createAt.isoformat() if a.createAt else None,
            'updateAt': a.updateAt.isoformat() if a.updateAt else None
        }

    @staticmethod
    def get_all():
        try:
            armazens = Armazem.query.all()
            return jsonify([ArmazemController.serialize(a) for a in armazens]), 200
        except Exception as e:
            logger.exception("[GET ALL] Armazem failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            armazem = Armazem.query.get(id)
            if not armazem:
                return jsonify({'message': 'Armazem not found'}), 404
            return jsonify(ArmazemController.serialize(armazem)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Armazem {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            sync_status = data.get('syncStatus')
            if sync_status not in VALID_SYNC_STATUS:
                sync_status = 'Not Syncronized'

            armazem = Armazem(
                nome=data['nome'],
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                provincia_id=data['provincia_id'],
                syncStatus=sync_status,
                syncStatusDate=datetime.fromisoformat(data['syncStatusDate']) if data.get('syncStatusDate') else None
            )
            db.session.add(armazem)
            db.session.commit()
            return jsonify({'message': 'Armazem created successfully', 'id': armazem.id}), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Armazem failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            armazem = Armazem.query.get(id)
            if not armazem:
                return jsonify({'message': 'Armazem not found'}), 404

            data = request.get_json()
            armazem.nome = data.get('nome', armazem.nome)
            armazem.latitude = data.get('latitude', armazem.latitude)
            armazem.longitude = data.get('longitude', armazem.longitude)
            armazem.provincia_id = data.get('provincia_id', armazem.provincia_id)
            if 'syncStatus' in data and data['syncStatus'] in VALID_SYNC_STATUS:
                armazem.syncStatus = data['syncStatus']
            if 'syncStatusDate' in data and data['syncStatusDate']:
                armazem.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])

            db.session.commit()
            return jsonify({'message': 'Armazem updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Armazem {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            armazem = Armazem.query.get(id)
            if not armazem:
                return jsonify({'message': 'Armazem not found'}), 404
            db.session.delete(armazem)
            db.session.commit()
            return jsonify({'message': 'Armazem deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Armazem {id}")
            return jsonify({'error': str(e)}), 500
