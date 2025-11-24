import logging
from flask import jsonify, request
from models import db, Armazem, Provincia
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

VALID_SYNC_STATUS = ['Not Syncronized', 'Syncronized', 'Updated']


class ArmazemController:
    @staticmethod
    def serialize(a):
        """Serializa um armazém, incluindo província, itens, observação e status."""
        return {
            'id': a.id,
            'nome': a.nome,
            'latitude': a.latitude,
            'longitude': a.longitude,
            'observacao': a.observacao,
            'provincia_id': a.provincia_id,
            'provincia_nome': a.provincia.nome if a.provincia else None,
            'syncStatus': a.syncStatus,
            'syncStatusDate': a.syncStatusDate.isoformat() if a.syncStatusDate else None,
            # 🔹 Inclui os itens do armazém
            'itens': [
                {
                    'id': i.id,
                    'codigo': i.codigo,
                    'designacao': i.designacao,
                    'quantidade': i.quantidade,
                    'user': i.user,
                    'recebeu': i.recebeu
                }
                for i in a.itens
            ] if hasattr(a, 'itens') else []
        }

    @staticmethod
    def get_all():
        """Listar todos os armazéns"""
        armazens = Armazem.query.all()
        return jsonify([ArmazemController.serialize(a) for a in armazens])

    @staticmethod
    def get_by_id(id):
        """Obter um armazém específico"""
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
        """Criar um novo armazém"""
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
                observacao=data.get('observacao'),
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
        """Atualizar um armazém existente"""
        try:
            armazem = Armazem.query.get(id)
            if not armazem:
                return jsonify({'message': 'Armazem not found'}), 404

            data = request.get_json()
            armazem.nome = data.get('nome', armazem.nome)
            armazem.latitude = data.get('latitude', armazem.latitude)
            armazem.longitude = data.get('longitude', armazem.longitude)
            armazem.provincia_id = data.get('provincia_id', armazem.provincia_id)
            armazem.observacao = data.get('observacao', armazem.observacao)

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
        """Eliminar um armazém"""
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
