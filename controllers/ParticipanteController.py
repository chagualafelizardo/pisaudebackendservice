import logging
from flask import jsonify, request
from datetime import datetime
from models import db, Participante, FormacaoItem

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ParticipanteController:

    # ======================================================
    # 🔹 SERIALIZER
    # ======================================================
    @staticmethod
    def serialize(p: Participante):
        return {
            'id': p.id,
            'nome': p.nome,
            'contacto': p.contacto,
            'presente': p.presente,
            'formacao_id': p.formacao_id,
            'formacao_nome': p.formacao.nome_formacao if p.formacao else None,
            'syncStatus': p.syncStatus,
            'syncStatusDate': p.syncStatusDate.isoformat() if p.syncStatusDate else None,
            'createAt': p.createAt.isoformat() if p.createAt else None,
            'updateAt': p.updateAt.isoformat() if p.updateAt else None
        }

    # ======================================================
    # 🔹 LISTAR TODOS
    # ======================================================
    @staticmethod
    def get_all():
        try:
            participantes = Participante.query.all()
            return jsonify([ParticipanteController.serialize(p) for p in participantes]), 200
        except Exception as e:
            logger.exception("[GET ALL] Falha ao listar participantes")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 OBTER POR ID
    # ======================================================
    @staticmethod
    def get_by_id(id):
        try:
            participante = Participante.query.get(id)
            if not participante:
                return jsonify({'message': 'Participante não encontrado'}), 404
            return jsonify(ParticipanteController.serialize(participante)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Falha ao obter participante ID={id}")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 CRIAR PARTICIPANTE
    # ======================================================
    @staticmethod
    def create():
        try:
            logger.info("➡️ [CREATE PARTICIPANTE] Requisição recebida")
            data = request.get_json() if request.is_json else request.form.to_dict()

            if not data.get('nome'):
                return jsonify({'error': 'O nome do participante é obrigatório'}), 400
            if not data.get('formacao_id'):
                return jsonify({'error': 'O campo formacao_id é obrigatório'}), 400

            formacao = FormacaoItem.query.get(data['formacao_id'])
            if not formacao:
                return jsonify({'error': 'Formação associada não encontrada'}), 404

            participante = Participante(
                nome=data['nome'],
                contacto=data.get('contacto'),
                presente=data.get('presente', 'no'),
                formacao_id=data['formacao_id'],
                syncStatus=data.get('syncStatus', 'NotSyncronized'),
                syncStatusDate=datetime.utcnow()
            )

            db.session.add(participante)
            db.session.commit()

            logger.info(f"✅ Participante criado com sucesso (id={participante.id}) na formação {formacao.nome_formacao}")
            return jsonify({'message': 'Participante criado com sucesso', 'id': participante.id}), 201

        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Falha ao criar participante")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 ATUALIZAR PARTICIPANTE
    # ======================================================
    @staticmethod
    def update(id):
        try:
            logger.info(f"➡️ [UPDATE PARTICIPANTE] Atualizando participante ID={id}")
            participante = Participante.query.get(id)
            if not participante:
                return jsonify({'message': 'Participante não encontrado'}), 404

            data = request.get_json() if request.is_json else request.form.to_dict()

            participante.nome = data.get('nome', participante.nome)
            participante.contacto = data.get('contacto', participante.contacto)
            participante.presente = data.get('presente', participante.presente)
            participante.syncStatus = data.get('syncStatus', participante.syncStatus)
            participante.syncStatusDate = datetime.utcnow()

            db.session.commit()
            logger.info(f"✅ Participante atualizado com sucesso (id={id})")
            return jsonify({'message': 'Participante atualizado com sucesso'}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Falha ao atualizar participante ID={id}")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 DELETAR PARTICIPANTE
    # ======================================================
    @staticmethod
    def delete(id):
        try:
            participante = Participante.query.get(id)
            if not participante:
                return jsonify({'message': 'Participante não encontrado'}), 404

            db.session.delete(participante)
            db.session.commit()

            logger.info(f"✅ Participante deletado com sucesso (id={id})")
            return jsonify({'message': 'Participante deletado com sucesso'}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Falha ao deletar participante ID={id}")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 LISTAR PARTICIPANTES DE UMA FORMAÇÃO
    # ======================================================
    @staticmethod
    def get_by_formacao(formacao_id):
        try:
            formacao = FormacaoItem.query.get(formacao_id)
            if not formacao:
                return jsonify({'message': 'Formação não encontrada'}), 404

            participantes = Participante.query.filter_by(formacao_id=formacao_id).all()
            return jsonify([ParticipanteController.serialize(p) for p in participantes]), 200

        except Exception as e:
            logger.exception(f"[GET BY FORMAÇÃO] Falha ao listar participantes da formação ID={formacao_id}")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 MARCAR PRESENÇA
    # ======================================================
    @staticmethod
    def marcar_presenca(id):
        try:
            participante = Participante.query.get(id)
            if not participante:
                return jsonify({'message': 'Participante não encontrado'}), 404

            participante.presente = 'yes'
            participante.syncStatus = 'Updated'
            participante.syncStatusDate = datetime.utcnow()

            db.session.commit()

            logger.info(f"✅ Presença marcada para participante ID={id}")
            return jsonify({'message': 'Presença marcada com sucesso'}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[MARCAR PRESENÇA] Falha ao marcar presença ID={id}")
            return jsonify({'error': str(e)}), 500
