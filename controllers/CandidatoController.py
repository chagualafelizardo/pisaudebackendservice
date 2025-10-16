import logging
from flask import jsonify, request
from models import db, Candidato, CandidatoEdicao, Person
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class CandidatoController:

    @staticmethod
    def get_all():
        try:
            candidatos = Candidato.query.all()
            result = []
            for c in candidatos:
                ultima_edicao = c.edicoes[-1] if c.edicoes else None
                result.append({
                    'id': c.id,
                    'personId': c.personId,
                    'personFullname': c.person.fullname if c.person else None,
                    'curso': c.curso,
                    'instituicao': c.instituicao,
                    'numero_da_edicao': ultima_edicao.numeroedicao if ultima_edicao else None,
                    'data_edicao': ultima_edicao.dataedicao.isoformat() if ultima_edicao else None,
                    'syncStatus': c.syncStatus,
                    'syncStatusDate': c.syncStatusDate.isoformat() if c.syncStatusDate else None,
                    'createAt': c.createAt.isoformat() if c.createAt else None,
                    'updateAt': c.updateAt.isoformat() if c.updateAt else None
                })
            return jsonify(result), 200
        except Exception as e:
            logger.exception("[GET ALL] Failed to fetch candidatos")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            c = Candidato.query.get(id)
            if not c:
                return jsonify({'message': 'Candidato not found'}), 404

            ultima_edicao = c.edicoes[-1] if c.edicoes else None
            return jsonify({
                'id': c.id,
                'personId': c.personId,
                'personFullname': c.person.fullname if c.person else None,
                'curso': c.curso,
                'instituicao': c.instituicao,
                'numero_da_edicao': ultima_edicao.numeroedicao if ultima_edicao else None,
                'data_edicao': ultima_edicao.dataedicao.isoformat() if ultima_edicao else None,
                'syncStatus': c.syncStatus,
                'syncStatusDate': c.syncStatusDate.isoformat() if c.syncStatusDate else None,
                'createAt': c.createAt.isoformat() if c.createAt else None,
                'updateAt': c.updateAt.isoformat() if c.updateAt else None
            }), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch candidato ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            person_id = data.get('personId')
            curso = data.get('curso')
            instituicao = data.get('instituicao')
            numeroedicao = data.get('numero_da_edicao')
            dataedicao = data.get('data_edicao')
            sync_status = data.get('syncStatus', 'Not Syncronized')
            sync_status_date = data.get('syncStatusDate')

            if not person_id or not curso:
                return jsonify({'message': 'personId and curso are required'}), 400

            person = Person.query.get(person_id)
            if not person:
                return jsonify({'message': 'Person not found'}), 404

            new_candidato = Candidato(
                personId=person_id,
                curso=curso,
                instituicao=instituicao,
                syncStatus=sync_status,
                syncStatusDate=datetime.fromisoformat(sync_status_date) if sync_status_date else None
            )
            db.session.add(new_candidato)
            db.session.flush()

            if numeroedicao or dataedicao:
                new_edicao = CandidatoEdicao(
                    candidatoId=new_candidato.id,
                    numeroedicao=numeroedicao,
                    dataedicao=datetime.fromisoformat(dataedicao).date() if dataedicao else datetime.utcnow().date()
                )
                db.session.add(new_edicao)

            db.session.commit()
            return jsonify({'message': 'Candidato created successfully', 'id': new_candidato.id}), 201

        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create candidato")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            c = Candidato.query.get(id)
            if not c:
                return jsonify({'message': 'Candidato not found'}), 404

            data = request.get_json()
            person_id = data.get('personId', c.personId)
            curso = data.get('curso', c.curso)
            instituicao = data.get('instituicao', c.instituicao)
            numeroedicao = data.get('numero_da_edicao')
            dataedicao = data.get('data_edicao')
            sync_status = data.get('syncStatus')
            sync_status_date = data.get('syncStatusDate')

            if person_id != c.personId:
                person = Person.query.get(person_id)
                if not person:
                    return jsonify({'message': 'Person not found'}), 404
                c.personId = person_id

            c.curso = curso
            c.instituicao = instituicao
            if sync_status:
                c.syncStatus = sync_status
            if sync_status_date:
                c.syncStatusDate = datetime.fromisoformat(sync_status_date)

            c.updateAt = datetime.utcnow()

            if numeroedicao or dataedicao:
                ultima_edicao = c.edicoes[-1] if c.edicoes else None
                if ultima_edicao:
                    ultima_edicao.numeroedicao = numeroedicao or ultima_edicao.numeroedicao
                    if dataedicao:
                        ultima_edicao.dataedicao = datetime.fromisoformat(dataedicao).date()
                else:
                    new_edicao = CandidatoEdicao(
                        candidatoId=c.id,
                        numeroedicao=numeroedicao,
                        dataedicao=datetime.fromisoformat(dataedicao).date() if dataedicao else datetime.utcnow().date()
                    )
                    db.session.add(new_edicao)

            db.session.commit()
            return jsonify({'message': 'Candidato updated successfully'}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update candidato ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            c = Candidato.query.get(id)
            if not c:
                return jsonify({'message': 'Candidato not found'}), 404

            db.session.delete(c)
            db.session.commit()
            return jsonify({'message': 'Candidato deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete candidato ID {id}")
            return jsonify({'error': str(e)}), 500
