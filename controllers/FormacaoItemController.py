import logging
from flask import jsonify, request
from datetime import datetime
from models import db, FormacaoItem, Participante

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class FormacaoItemController:

    # ======================================================
    # 🔹 SERIALIZER
    # ======================================================
    @staticmethod
    def serialize(formacao: FormacaoItem):
        return {
            'id': formacao.id,
            'nome_formacao': formacao.nome_formacao,
            'data_formacao': formacao.data_formacao.isoformat() if formacao.data_formacao else None,
            'observacao': formacao.observacao,
            'user': formacao.user,
            'syncStatus': formacao.syncStatus,
            'syncStatusDate': formacao.syncStatusDate.isoformat() if formacao.syncStatusDate else None,
            'createAt': formacao.createAt.isoformat() if formacao.createAt else None,
            'updateAt': formacao.updateAt.isoformat() if formacao.updateAt else None,
            'participantes': [
                {
                    'id': p.id,
                    'nome': p.nome,
                    'contacto': p.contacto,
                    'presente': p.presente,
                    'syncStatus': p.syncStatus,
                    'createAt': p.createAt.isoformat() if p.createAt else None
                } for p in formacao.participantes
            ]
        }

    # ======================================================
    # 🔹 CAPTURAR USUÁRIO AUTOMATICAMENTE
    # ======================================================
    @staticmethod
    def _get_user_from_request():
        user_value = None
        if request.is_json:
            data = request.get_json(silent=True) or {}
            user_value = data.get('user') or data.get('username')
        else:
            data = request.form.to_dict()
            user_value = data.get('user') or data.get('username')

        if not user_value:
            try:
                from flask import session
                user_value = session.get('username') or session.get('user')
            except Exception:
                pass

        if not user_value:
            user_value = request.headers.get('X-User') or request.headers.get('X-Username')
        if not user_value:
            user_value = request.cookies.get('username')

        if not user_value:
            try:
                from flask_login import current_user
                if current_user and getattr(current_user, 'is_authenticated', False):
                    user_value = getattr(current_user, 'username', None) or \
                                 getattr(current_user, 'email', None) or \
                                 getattr(current_user, 'name', None)
            except Exception:
                pass

        if not user_value:
            user_value = 'Usuário não identificado'
            logger.warning("⚠️ Usuário não pôde ser determinado no FormacaoItemController")

        logger.info(f"👤 User determinado: {user_value}")
        return user_value

    # ======================================================
    # 🔹 LISTAR TODAS AS FORMAÇÕES
    # ======================================================
    @staticmethod
    def get_all():
        try:
            formacoes = FormacaoItem.query.all()
            return jsonify([FormacaoItemController.serialize(f) for f in formacoes]), 200
        except Exception as e:
            logger.exception("[GET ALL] Formação falhou")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 OBTER FORMAÇÃO POR ID
    # ======================================================
    @staticmethod
    def get_by_id(id):
        try:
            formacao = FormacaoItem.query.get(id)
            if not formacao:
                return jsonify({'message': 'Formação não encontrada'}), 404
            return jsonify(FormacaoItemController.serialize(formacao)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Formação {id} falhou")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 CRIAR FORMAÇÃO
    # ======================================================
    @staticmethod
    def create():
        try:
            logger.info("➡️ [CREATE FORMAÇÃO] Requisição recebida")
            data = request.get_json() if request.is_json else request.form.to_dict()

            user_value = FormacaoItemController._get_user_from_request()

            if not data.get('nome_formacao'):
                return jsonify({'error': 'O nome da formação é obrigatório'}), 400

            formacao = FormacaoItem(
                nome_formacao=data['nome_formacao'],
                data_formacao=datetime.fromisoformat(data['data_formacao']) if data.get('data_formacao') else datetime.utcnow(),
                observacao=data.get('observacao'),
                user=user_value,
                syncStatus=data.get('syncStatus', 'NotSyncronized'),
                syncStatusDate=datetime.utcnow()
            )

            db.session.add(formacao)
            db.session.commit()

            logger.info(f"✅ Formação criada com sucesso (id={formacao.id}) por {user_value}")
            return jsonify({'message': 'Formação criada com sucesso', 'id': formacao.id}), 201

        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Formação falhou")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 ATUALIZAR FORMAÇÃO
    # ======================================================
    @staticmethod
    def update(id):
        try:
            logger.info(f"➡️ [UPDATE FORMAÇÃO] Atualizando Formação ID={id}")

            formacao = FormacaoItem.query.get(id)
            if not formacao:
                return jsonify({'message': 'Formação não encontrada'}), 404

            data = request.get_json() if request.is_json else request.form.to_dict()
            user_value = FormacaoItemController._get_user_from_request()

            formacao.nome_formacao = data.get('nome_formacao', formacao.nome_formacao)
            formacao.observacao = data.get('observacao', formacao.observacao)
            if data.get('data_formacao'):
                formacao.data_formacao = datetime.fromisoformat(data['data_formacao'])

            formacao.user = user_value
            formacao.syncStatus = data.get('syncStatus', formacao.syncStatus)
            formacao.syncStatusDate = datetime.utcnow()

            db.session.commit()
            logger.info(f"✅ Formação atualizada (id={formacao.id}) por {user_value}")
            return jsonify({'message': 'Formação atualizada com sucesso'}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Formação {id} falhou")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 DELETAR FORMAÇÃO
    # ======================================================
    @staticmethod
    def delete(id):
        try:
            formacao = FormacaoItem.query.get(id)
            if not formacao:
                return jsonify({'message': 'Formação não encontrada'}), 404

            db.session.delete(formacao)
            db.session.commit()

            logger.info(f"✅ Formação deletada com sucesso (id={id})")
            return jsonify({'message': 'Formação deletada com sucesso'}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Formação {id} falhou")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 ADICIONAR PARTICIPANTE À FORMAÇÃO
    # ======================================================
    @staticmethod
    def adicionar_participante(formacao_id):
        try:
            logger.info(f"➡️ [ADD PARTICIPANTE] Formação ID={formacao_id}")

            formacao = FormacaoItem.query.get(formacao_id)
            if not formacao:
                return jsonify({'message': 'Formação não encontrada'}), 404

            data = request.get_json()
            if not data or not data.get('nome'):
                return jsonify({'error': 'Nome do participante é obrigatório'}), 400

            participante = Participante(
                nome=data['nome'],
                contacto=data.get('contacto'),
                presente=data.get('presente', 'no'),
                formacao_id=formacao_id,
                syncStatus='NotSyncronized',
                syncStatusDate=datetime.utcnow()
            )

            db.session.add(participante)
            db.session.commit()

            logger.info(f"✅ Participante '{participante.nome}' adicionado à formação ID={formacao_id}")
            return jsonify({'message': 'Participante adicionado com sucesso', 'id': participante.id}), 201

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[ADD PARTICIPANTE] Falhou para formação {formacao_id}")
            return jsonify({'error': str(e)}), 500
