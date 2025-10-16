import logging
from flask import jsonify, request, send_file
from io import BytesIO
from datetime import datetime
from models import db, Licenca, TipoLicenca, EstadoLicencaEnum, Person, Despacho  # ✅ inclui Despacho

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LicencaController:

    @staticmethod
    def get_all():
        try:
            licencas = Licenca.query.all()
            result = []
            for l in licencas:
                result.append({
                    'id': l.id,
                    'person_id': l.person_id,
                    'person_name': l.person.fullname if l.person else None,
                    'tipo_id': l.tipo_id,
                    'tipo_description': l.tipo.description if l.tipo else None,
                    'despacho_id': l.despacho_id,
                    'despacho_numero': l.despacho.numero if l.despacho else None,  # ✅
                    'motivo': l.motivo,
                    'data_inicio': l.data_inicio.isoformat(),
                    'data_fim': l.data_fim.isoformat(),
                    'estado': l.estado.value,
                    'observacao': l.observacao,
                    'anexo_nome': l.anexo_nome,
                    'criado_em': l.criado_em.isoformat() if l.criado_em else None
                })
            return jsonify(result), 200
        except Exception as e:
            logger.exception("[GET ALL] Erro ao listar licenças")
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def get_by_id(id):
        try:
            l = Licenca.query.get(id)
            if not l:
                return jsonify({'message': 'Licença não encontrada'}), 404

            return jsonify({
                'id': l.id,
                'person_id': l.person_id,
                'person_name': l.person.fullname if l.person else None,
                'tipo_id': l.tipo_id,
                'tipo_description': l.tipo.description if l.tipo else None,
                'despacho_id': l.despacho_id,
                'despacho_numero': l.despacho.numero if l.despacho else None,  # ✅
                'motivo': l.motivo,
                'data_inicio': l.data_inicio.isoformat(),
                'data_fim': l.data_fim.isoformat(),
                'estado': l.estado.value,
                'observacao': l.observacao,
                'anexo_nome': l.anexo_nome,
                'criado_em': l.criado_em.isoformat() if l.criado_em else None
            }), 200
        except Exception as e:
            logger.exception("[GET BY ID] Erro ao buscar licença")
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def create():
        try:
            data = request.form.to_dict()
            file = request.files.get('anexo')

            person_id = data.get('person_id')
            tipo_id = data.get('tipo_id')
            despacho_id = data.get('despacho_id')  # ✅ opcional
            data_inicio = data.get('data_inicio')
            data_fim = data.get('data_fim')

            if not person_id or not tipo_id or not data_inicio or not data_fim:
                return jsonify({'message': 'Campos obrigatórios: person_id, tipo_id, data_inicio, data_fim'}), 400

            if not Person.query.get(person_id):
                return jsonify({'message': 'Pessoa não encontrada'}), 404
            if not TipoLicenca.query.get(tipo_id):
                return jsonify({'message': 'Tipo de licença não encontrado'}), 404
            if despacho_id and not Despacho.query.get(despacho_id):
                return jsonify({'message': 'Despacho não encontrado'}), 404

            nova_licenca = Licenca(
                person_id=person_id,
                tipo_id=tipo_id,
                despacho_id=despacho_id if despacho_id else None,
                motivo=data.get('motivo'),
                data_inicio=datetime.fromisoformat(data_inicio).date(),
                data_fim=datetime.fromisoformat(data_fim).date(),
                observacao=data.get('observacao')
            )

            if file:
                nova_licenca.anexo_nome = file.filename
                nova_licenca.anexo_tipo = file.mimetype
                nova_licenca.anexo_dados = file.read()

            db.session.add(nova_licenca)
            db.session.commit()
            return jsonify({'message': 'Licença criada com sucesso', 'id': nova_licenca.id}), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Erro ao criar licença")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def download_anexo(id):
        """Permite baixar o ficheiro anexo."""
        try:
            licenca = Licenca.query.get(id)
            if not licenca or not licenca.anexo_dados:
                return jsonify({'message': 'Anexo não encontrado'}), 404

            return send_file(
                BytesIO(licenca.anexo_dados),
                as_attachment=True,
                download_name=licenca.anexo_nome,
                mimetype=licenca.anexo_tipo or 'application/octet-stream'
            )
        except Exception as e:
            logger.exception("[DOWNLOAD] Erro ao baixar anexo")
            return jsonify({'error': str(e)}), 500
