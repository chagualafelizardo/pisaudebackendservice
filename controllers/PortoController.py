import logging
from flask import jsonify, request
from models import db, Porto, Provincia
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

VALID_SYNC_STATUS = ['Not Syncronized', 'Syncronized', 'Updated']

class PortoController:

    @staticmethod
    def serialize(p: Porto):
        # Buscar o nome da provincia de forma explícita
        provincia_nome = None
        if p.provincia_id:
            provincia = Provincia.query.get(p.provincia_id)
            provincia_nome = provincia.nome if provincia else None

        return {
            'id': p.id,
            'nome': p.nome,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'provincia_id': p.provincia_id,
            'provincia_nome': provincia_nome,
            'syncStatus': p.syncStatus,
            'syncStatusDate': p.syncStatusDate.isoformat() if p.syncStatusDate else None,
            'createAt': p.createAt.isoformat() if p.createAt else None,
            'updateAt': p.updateAt.isoformat() if p.updateAt else None
        }

    # -------------------------
    # GET ALL
    # -------------------------
    @staticmethod
    def get_all():
        try:
            portos = Porto.query.all()
            return jsonify([PortoController.serialize(p) for p in portos]), 200
        except Exception as e:
            logger.exception("[GET ALL] Porto failed")
            return jsonify({'error': str(e)}), 500

    # -------------------------
    # GET BY ID
    # -------------------------
    @staticmethod
    def get_by_id(id):
        try:
            porto = Porto.query.get(id)
            if not porto:
                return jsonify({'message': 'Porto not found'}), 404
            return jsonify(PortoController.serialize(porto)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Porto {id}")
            return jsonify({'error': str(e)}), 500

    # -------------------------
    # CREATE
    # -------------------------
    @staticmethod
    def create():
        try:
            data = request.get_json()
            sync_status = data.get('syncStatus')
            if sync_status not in VALID_SYNC_STATUS:
                sync_status = 'Not Syncronized'

            porto = Porto(
                nome=data['nome'],
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                provincia_id=data['provincia_id'],
                syncStatus=sync_status,
                syncStatusDate=datetime.fromisoformat(data['syncStatusDate']) if data.get('syncStatusDate') else None
            )
            db.session.add(porto)
            db.session.commit()
            return jsonify({'message': 'Porto created successfully', 'id': porto.id}), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Porto failed")
            return jsonify({'error': str(e)}), 500

    # -------------------------
    # UPDATE
    # -------------------------
    @staticmethod
    def update(id):
        try:
            porto = Porto.query.get(id)
            if not porto:
                return jsonify({'message': 'Porto not found'}), 404

            data = request.get_json()
            porto.nome = data.get('nome', porto.nome)
            porto.latitude = data.get('latitude', porto.latitude)
            porto.longitude = data.get('longitude', porto.longitude)
            porto.provincia_id = data.get('provincia_id', porto.provincia_id)
            if 'syncStatus' in data and data['syncStatus'] in VALID_SYNC_STATUS:
                porto.syncStatus = data['syncStatus']
            if 'syncStatusDate' in data and data['syncStatusDate']:
                porto.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])

            db.session.commit()
            return jsonify({'message': 'Porto updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Porto {id}")
            return jsonify({'error': str(e)}), 500

    # -------------------------
    # DELETE
    # -------------------------
    @staticmethod
    def delete(id):
        try:
            porto = Porto.query.get(id)
            if not porto:
                return jsonify({'message': 'Porto not found'}), 404
            db.session.delete(porto)
            db.session.commit()
            return jsonify({'message': 'Porto deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Porto {id}")
            return jsonify({'error': str(e)}), 500
