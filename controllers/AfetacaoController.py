from flask import jsonify, request
from models import db
from models.Afetacao import Afetacao, SyncStatusEnum
from datetime import datetime
import logging
import base64  # no topo, se ainda não estiver

logger = logging.getLogger(__name__)

class AfetacaoController:

    @staticmethod
    def get_all():
        try:
            logger.info("[GET ALL] Fetching all afetacoes")
            afetacoes = Afetacao.query.all()
            result = []
            for a in afetacoes:
                result.append({
                    'id': a.id,
                    # Adiciona objeto person com imagem
                    'person': {
                        'fullname': a.person.fullname if a.person else None,
                        'image': base64.b64encode(a.person.image).decode('utf-8') if a.person and a.person.image else None
                    },
                    'personId': a.personId,
                    'personFullname': a.person.fullname if a.person else None,
                    'ramoId': a.ramoId,
                    'ramoDescription': a.ramo.description if a.ramo else None,
                    'unidadeMilitarId': a.unidadeMilitarId,
                    'unidadeMilitarDescription': a.unidadeMilitar.name if a.unidadeMilitar else None,
                    'subunidadeId': a.subunidadeId,
                    'subunidadeDescription': a.subunidade.name if a.subunidade else None,
                    'especialidadeId': a.especialidadeId,
                    'especialidadeDescription': a.especialidade.description if a.especialidade else None,
                    'subespecialidadeId': a.subespecialidadeId,
                    'subespecialidadeDescription': a.subespecialidade.description if a.subespecialidade else None,
                    'funcaoId': a.funcaoId,
                    'funcaoDescription': a.funcao.description if a.funcao else None,
                    'situacaoGeralId': a.situacaoGeralId,
                    'situacaoGeralDescription': a.situacaoGeral.description if a.situacaoGeral else None,
                    'situacaoPrestacaoServicoId': a.situacaoPrestacaoServicoId,
                    'situacaoPrestacaoServicoDescription': a.situacaoPrestacaoServico.description if a.situacaoPrestacaoServico else None,
                    'ultimoAnoPromocao': a.ultimoAnoPromocao.isoformat() if a.ultimoAnoPromocao else None,
                    'ordemServicoPromocao': a.ordemServicoPromocao,
                    'syncStatus': a.syncStatus.value,
                    'syncStatusDate': a.syncStatusDate.isoformat() if a.syncStatusDate else None,
                    'createdAt': a.createdAt.isoformat() if a.createdAt else None,
                    'updatedAt': a.updatedAt.isoformat() if a.updatedAt else None
                })
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"[GET ALL] Failed to fetch afetacoes: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()

            new_afetacao = Afetacao(
                personId=data['personId'],
                ramoId=data['ramoId'],
                unidadeMilitarId=data['unidadeMilitarId'],
                subunidadeId=data['subunidadeId'],
                especialidadeId=data['especialidadeId'],
                subespecialidadeId=data['subespecialidadeId'],
                funcaoId=data['funcaoId'],
                situacaoGeralId=data['situacaoGeralId'],
                situacaoPrestacaoServicoId=data['situacaoPrestacaoServicoId'],
                ultimoAnoPromocao=datetime.fromisoformat(data['ultimoAnoPromocao']).date() if data.get('ultimoAnoPromocao') else None,
                ordemServicoPromocao=data.get('ordemServicoPromocao'),
                syncStatus=SyncStatusEnum.NotSyncronized,
                syncStatusDate=None
            )

            db.session.add(new_afetacao)
            db.session.commit()
            return jsonify({'message': 'Afetacao created successfully', 'id': new_afetacao.id}), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"[CREATE] Failed to create afetacao: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            a = Afetacao.query.get(id)
            if not a:
                return jsonify({'message': 'Afetacao not found'}), 404

            data = request.get_json()
            a.personId = data['personId']
            a.ramoId = data['ramoId']
            a.unidadeMilitarId = data['unidadeMilitarId']
            a.subunidadeId = data['subunidadeId']
            a.especialidadeId = data['especialidadeId']
            a.subespecialidadeId = data['subespecialidadeId']
            a.funcaoId = data['funcaoId']
            a.situacaoGeralId = data['situacaoGeralId']
            a.situacaoPrestacaoServicoId = data['situacaoPrestacaoServicoId']
            a.ultimoAnoPromocao = datetime.fromisoformat(data['ultimoAnoPromocao']).date() if data.get('ultimoAnoPromocao') else None
            a.ordemServicoPromocao = data.get('ordemServicoPromocao')
            a.updatedAt = datetime.utcnow()

            db.session.commit()
            return jsonify({'message': 'Afetacao updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"[UPDATE] Failed to update afetacao ID {id}: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            a = Afetacao.query.get(id)
            if not a:
                return jsonify({'message': 'Afetacao not found'}), 404

            db.session.delete(a)
            db.session.commit()
            return jsonify({'message': 'Afetacao deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"[DELETE] Failed to delete afetacao ID {id}: {e}")
            return jsonify({'error': str(e)}), 500
