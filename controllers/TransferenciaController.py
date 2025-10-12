import logging
from flask import jsonify, request
from models import db, Transferencia, SyncStatusEnum, Location, Person
from datetime import datetime
from models.Afetacao import Afetacao

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class TransferenciaController:

    @staticmethod
    def get_all():
        try:
            transferencias = Transferencia.query.all()
            result = []
            for t in transferencias:
                result.append({
                    'id': t.id,
                    'dataUmOrigem': t.dataUmOrigem.isoformat() if t.dataUmOrigem else None,
                    'unidadeMilitarOrigemId': t.unidadeMilitarOrigemId,
                    'unidadeMilitarOrigemName': t.unidadeMilitarOrigem.name if t.unidadeMilitarOrigem else None,
                    'dataUmAtual': t.dataUmAtual.isoformat() if t.dataUmAtual else None,
                    'unidadeMilitarAtualId': t.unidadeMilitarAtualId,
                    'unidadeMilitarAtualName': t.unidadeMilitarAtual.name if t.unidadeMilitarAtual else None,
                    'observation': t.observation,
                    'persons': [{'id': p.id, 'fullname': p.fullname} for p in t.persons],
                    'syncStatus': t.syncStatus.value if t.syncStatus else None,
                    'syncStatusDate': t.syncStatusDate.isoformat() if t.syncStatusDate else None,
                    'createdAt': t.createdAt.isoformat() if t.createdAt else None,
                    'updatedAt': t.updatedAt.isoformat() if t.updatedAt else None,
                })
            return jsonify(result), 200
        except Exception as e:
            logger.exception("[GET ALL] Failed to fetch transferencias")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            t = Transferencia.query.get(id)
            if not t:
                return jsonify({'message': 'Transferencia not found'}), 404

            return jsonify({
                'id': t.id,
                'dataUmOrigem': t.dataUmOrigem.isoformat() if t.dataUmOrigem else None,
                'unidadeMilitarOrigemId': t.unidadeMilitarOrigemId,
                'unidadeMilitarOrigemName': t.unidadeMilitarOrigem.name if t.unidadeMilitarOrigem else None,
                'dataUmAtual': t.dataUmAtual.isoformat() if t.dataUmAtual else None,
                'unidadeMilitarAtualId': t.unidadeMilitarAtualId,
                'unidadeMilitarAtualName': t.unidadeMilitarAtual.name if t.unidadeMilitarAtual else None,
                'observation': t.observation,
                'persons': [{'id': p.id, 'fullname': p.fullname} for p in t.persons],
                'syncStatus': t.syncStatus.value if t.syncStatus else None,
                'syncStatusDate': t.syncStatusDate.isoformat() if t.syncStatusDate else None,
                'createdAt': t.createdAt.isoformat() if t.createdAt else None,
                'updatedAt': t.updatedAt.isoformat() if t.updatedAt else None,
            }), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch transferencia ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            person_ids = data.get('personIds', [])

            t = Transferencia(
                dataUmOrigem=datetime.fromisoformat(data['dataUmOrigem']).date() if data.get('dataUmOrigem') else None,
                unidadeMilitarOrigemId=data.get('unidadeMilitarOrigemId'),
                dataUmAtual=datetime.fromisoformat(data['dataUmAtual']).date() if data.get('dataUmAtual') else None,
                unidadeMilitarAtualId=data.get('unidadeMilitarAtualId'),
                observation=data.get('observation'),
                syncStatus=SyncStatusEnum[data['syncStatus']] if data.get('syncStatus') in SyncStatusEnum.__members__ else SyncStatusEnum.NotSyncronized,
                syncStatusDate=datetime.fromisoformat(data['syncStatusDate']) if data.get('syncStatusDate') else None,
            )

            for pid in person_ids:
                person = Person.query.get(pid)
                if person:
                    t.persons.append(person)

                    # 🟡 Atualiza Afetacao com nova localização
                    afetacao = Afetacao.query.filter_by(personId=pid).order_by(Afetacao.id.desc()).first()
                    if afetacao:
                        afetacao.unidadeMilitarId = data.get('unidadeMilitarAtualId')
                        afetacao.updatedAt = datetime.utcnow()

            db.session.add(t)
            db.session.commit()

            return jsonify({
                'message': 'Transferencia created and afetacao updated successfully',
                'id': t.id
            }), 201

        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create transferencia and update afetacao")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            t = Transferencia.query.get(id)
            if not t:
                return jsonify({'message': 'Transferencia not found'}), 404

            data = request.get_json()

            t.dataUmOrigem = datetime.fromisoformat(data['dataUmOrigem']).date() if data.get('dataUmOrigem') else t.dataUmOrigem
            t.unidadeMilitarOrigemId = data.get('unidadeMilitarOrigemId', t.unidadeMilitarOrigemId)
            t.dataUmAtual = datetime.fromisoformat(data['dataUmAtual']).date() if data.get('dataUmAtual') else t.dataUmAtual
            t.unidadeMilitarAtualId = data.get('unidadeMilitarAtualId', t.unidadeMilitarAtualId)
            t.observation = data.get('observation', t.observation)
            if data.get('syncStatus') in SyncStatusEnum.__members__:
                t.syncStatus = SyncStatusEnum[data['syncStatus']]
            if data.get('syncStatusDate'):
                t.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])

            # Atualizar persons
            if 'personIds' in data:
                t.persons = []
                for pid in data['personIds']:
                    person = Person.query.get(pid)
                    if person:
                        t.persons.append(person)

            t.updatedAt = datetime.utcnow()
            db.session.commit()

            return jsonify({'message': 'Transferencia updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update transferencia ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            t = Transferencia.query.get(id)
            if not t:
                return jsonify({'message': 'Transferencia not found'}), 404

            db.session.delete(t)
            db.session.commit()
            return jsonify({'message': 'Transferencia deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete transferencia ID {id}")
            return jsonify({'error': str(e)}), 500
