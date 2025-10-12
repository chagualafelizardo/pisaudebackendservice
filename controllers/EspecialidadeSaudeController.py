import logging
from flask import jsonify, request
from models import db, EspecialidadeSaude
from datetime import datetime

logger = logging.getLogger(__name__)

class EspecialidadeSaudeController:
    @staticmethod
    def get_all():
        """Fetch all Especialidades de Saúde"""
        try:
            logger.info("[GET ALL] Fetching all Especialidades de Saúde")
            especialidades = EspecialidadeSaude.query.all()
            result = []

            for esp in especialidades:
                result.append({
                    'id': esp.id,
                    'curso': esp.curso,
                    'anoFormacao': esp.anoFormacao,
                    'instituicaoFormacao': esp.instituicaoFormacao,
                    'observation': esp.observation,
                    'syncStatus': esp.syncStatus.value if esp.syncStatus else None,
                    'syncStatusDate': esp.syncStatusDate,
                    'createAt': esp.createAt,
                    'updateAt': esp.updateAt
                })

            return jsonify(result), 200
        except Exception as e:
            logger.error(f"[GET ALL] Failed to fetch Especialidades de Saúde: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        """Fetch a single EspecialidadeSaude by ID"""
        try:
            logger.info(f"[GET BY ID] Fetching EspecialidadeSaude ID: {id}")
            esp = EspecialidadeSaude.query.get(id)

            if not esp:
                logger.warning(f"[GET BY ID] EspecialidadeSaude ID {id} not found")
                return jsonify({'message': 'Especialidade de Saúde not found'}), 404

            return jsonify({
                'id': esp.id,
                'curso': esp.curso,
                'anoFormacao': esp.anoFormacao,
                'instituicaoFormacao': esp.instituicaoFormacao,
                'observation': esp.observation,
                'syncStatus': esp.syncStatus.value if esp.syncStatus else None,
                'syncStatusDate': esp.syncStatusDate,
                'createAt': esp.createAt,
                'updateAt': esp.updateAt
            }), 200
        except Exception as e:
            logger.error(f"[GET BY ID] Error fetching EspecialidadeSaude ID {id}: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        """Create a new EspecialidadeSaude"""
        try:
            data = request.get_json()
            curso = data.get('curso')
            anoFormacao = data.get('anoFormacao')
            instituicaoFormacao = data.get('instituicaoFormacao')
            observation = data.get('observation')

            if not curso:
                logger.warning("[CREATE] Missing 'curso' field")
                return jsonify({'message': 'Course name is required'}), 400

            if EspecialidadeSaude.query.filter_by(curso=curso).first():
                logger.warning(f"[CREATE] EspecialidadeSaude '{curso}' already exists")
                return jsonify({'message': 'Especialidade de Saúde already exists'}), 400

            new_esp = EspecialidadeSaude(
                curso=curso,
                anoFormacao=anoFormacao,
                instituicaoFormacao=instituicaoFormacao,
                observation=observation
            )

            db.session.add(new_esp)
            db.session.commit()

            logger.info(f"[CREATE] EspecialidadeSaude '{curso}' created successfully")
            return jsonify({'message': 'Especialidade de Saúde created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"[CREATE] Failed to create EspecialidadeSaude: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        """Update an existing EspecialidadeSaude"""
        try:
            esp = EspecialidadeSaude.query.get(id)
            if not esp:
                logger.warning(f"[UPDATE] EspecialidadeSaude ID {id} not found")
                return jsonify({'message': 'Especialidade de Saúde not found'}), 404

            data = request.get_json()
            curso = data.get('curso')
            anoFormacao = data.get('anoFormacao')
            instituicaoFormacao = data.get('instituicaoFormacao')
            observation = data.get('observation')

            if not curso:
                logger.warning("[UPDATE] Missing 'curso' field")
                return jsonify({'message': 'Course name is required'}), 400

            if EspecialidadeSaude.query.filter(EspecialidadeSaude.curso == curso, EspecialidadeSaude.id != id).first():
                logger.warning(f"[UPDATE] EspecialidadeSaude name '{curso}' already used by another record")
                return jsonify({'message': 'Course name already in use'}), 400

            esp.curso = curso
            esp.anoFormacao = anoFormacao
            esp.instituicaoFormacao = instituicaoFormacao
            esp.observation = observation
            esp.updateAt = datetime.utcnow()

            db.session.commit()
            logger.info(f"[UPDATE] EspecialidadeSaude ID {id} updated successfully")
            return jsonify({'message': 'Especialidade de Saúde updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"[UPDATE] Failed to update EspecialidadeSaude ID {id}: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        """Delete an EspecialidadeSaude"""
        try:
            esp = EspecialidadeSaude.query.get(id)
            if not esp:
                logger.warning(f"[DELETE] EspecialidadeSaude ID {id} not found")
                return jsonify({'message': 'Especialidade de Saúde not found'}), 404

            db.session.delete(esp)
            db.session.commit()

            logger.info(f"[DELETE] EspecialidadeSaude ID {id} deleted successfully")
            return jsonify({'message': 'Especialidade de Saúde deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"[DELETE] Failed to delete EspecialidadeSaude ID {id}: {e}")
            return jsonify({'error': str(e)}), 500
