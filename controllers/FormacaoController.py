# controllers/FormacaoController.py
import logging
from flask import jsonify, request, send_file
from io import BytesIO
from datetime import datetime
from models import db, Formacao, Person, Pais, TipoLicenca, Licenca, Despacho
import base64

logger = logging.getLogger(__name__)

class FormacaoController:

    @staticmethod
    def serialize_formacao(f):
        return {
            'id': f.id,
            'person_id': f.person_id,
            'person': {
                'id': f.person.id,
                'fullname': f.person.fullname,
                'nim': f.person.nim,
                'gender': f.person.gender,
                'dateofbirth': f.person.dateofbirth.isoformat() if f.person.dateofbirth else None,
                'incorporationdata': f.person.incorporationdata.isoformat() if f.person.incorporationdata else None,
                'image': base64.b64encode(f.person.image).decode('utf-8') if f.person.image else None
            } if f.person else None,
            'inicio': f.inicio.isoformat() if f.inicio else None,
            'duracao': f.duracao,
            'anoacademico': f.anoacademico,
            'despachoautorizacao': f.despachoautorizacao,
            'pais_id': f.pais_id,
            'pais': {'id': f.pais.id, 'description': f.pais.description} if f.pais else None,
            'tipo_licenca_id': f.tipo_licenca_id,
            'tipo_licenca': {'id': f.tipo_licenca.id, 'description': f.tipo_licenca.description} if f.tipo_licenca else None,
            'licenca_id': f.licenca_id,
            'licenca': {
                'id': f.licenca.id,
                'motivo': f.licenca.motivo,
                'data_inicio': f.licenca.data_inicio.isoformat() if f.licenca.data_inicio else None,
                'data_fim': f.licenca.data_fim.isoformat() if f.licenca.data_fim else None,
                'anexo_nome': f.licenca.anexo_nome
            } if f.licenca else None,
            'despacho_id': f.despacho_id,
            'despacho': {
                'id': f.despacho.id,
                'titulo': f.despacho.titulo,
                'data_despacho': f.despacho.data_despacho.isoformat() if f.despacho.data_despacho else None,
                'anexo_nome': f.despacho.anexo_nome
            } if f.despacho else None,
            'syncStatus': f.syncStatus,
            'syncStatusDate': f.syncStatusDate.isoformat() if f.syncStatusDate else None,
            'createAt': f.createAt.isoformat() if f.createAt else None,
            'updateAt': f.updateAt.isoformat() if f.updateAt else None
        }

    @staticmethod
    def get_all():
        try:
            formacoes = Formacao.query.all()
            return jsonify([FormacaoController.serialize_formacao(f) for f in formacoes]), 200
        except Exception as e:
            logger.exception("[GET ALL] Erro ao listar formações")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            f = Formacao.query.get(id)
            if not f:
                return jsonify({'message': 'Formação não encontrada'}), 404
            return jsonify(FormacaoController.serialize_formacao(f)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Erro ao buscar formação {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            # Verificar se é multipart/form-data (mas aqui não esperamos arquivos diretos, apenas referências a licenças/despachos)
            # Se for JSON, use request.json, senão request.form
            if request.content_type and 'application/json' in request.content_type:
                data = request.get_json()
                is_multipart = False
            else:
                data = request.form.to_dict()
                is_multipart = True

            # Validar campos obrigatórios
            required = ['person_id', 'pais_id', 'tipo_licenca_id', 'inicio', 'duracao', 'anoacademico']
            for field in required:
                if not data.get(field):
                    return jsonify({'error': f'O campo {field} é obrigatório'}), 400

            # Converter dados
            try:
                inicio = datetime.fromisoformat(data['inicio'])
            except ValueError:
                return jsonify({'error': 'Formato de data/hora inválido para início'}), 400

            # Verificar existência das entidades
            person = Person.query.get(data['person_id'])
            if not person:
                return jsonify({'error': 'Pessoa não encontrada'}), 404

            pais = Pais.query.get(data['pais_id'])
            if not pais:
                return jsonify({'error': 'País não encontrado'}), 404

            tipo = TipoLicenca.query.get(data['tipo_licenca_id'])
            if not tipo:
                return jsonify({'error': 'Tipo de licença não encontrado'}), 404

            nova_formacao = Formacao(
                person_id=data['person_id'],
                pais_id=data['pais_id'],
                tipo_licenca_id=data['tipo_licenca_id'],
                inicio=inicio,
                duracao=data['duracao'],
                anoacademico=data['anoacademico'],
                despachoautorizacao=data.get('despachoautorizacao', ''),
                syncStatus=data.get('syncStatus', 'Not Syncronized'),
                syncStatusDate=datetime.fromisoformat(data['syncStatusDate']) if data.get('syncStatusDate') else None
            )

            # Relacionamentos opcionais com Licenca e Despacho
            licenca_id = data.get('licenca_id')
            if licenca_id:
                licenca = Licenca.query.get(licenca_id)
                if not licenca:
                    return jsonify({'error': 'Licença não encontrada'}), 404
                nova_formacao.licenca_id = licenca_id

            despacho_id = data.get('despacho_id')
            if despacho_id:
                despacho = Despacho.query.get(despacho_id)
                if not despacho:
                    return jsonify({'error': 'Despacho não encontrado'}), 404
                nova_formacao.despacho_id = despacho_id

            db.session.add(nova_formacao)
            db.session.commit()
            return jsonify({'message': 'Formação criada com sucesso', 'id': nova_formacao.id}), 201

        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Erro ao criar formação")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            formacao = Formacao.query.get(id)
            if not formacao:
                return jsonify({'message': 'Formação não encontrada'}), 404

            # Suporta JSON ou form-data
            if request.content_type and 'application/json' in request.content_type:
                data = request.get_json()
            else:
                data = request.form.to_dict()

            # Atualizar campos
            if 'person_id' in data:
                if not Person.query.get(data['person_id']):
                    return jsonify({'error': 'Pessoa não encontrada'}), 404
                formacao.person_id = data['person_id']
            if 'pais_id' in data:
                if not Pais.query.get(data['pais_id']):
                    return jsonify({'error': 'País não encontrado'}), 404
                formacao.pais_id = data['pais_id']
            if 'tipo_licenca_id' in data:
                if not TipoLicenca.query.get(data['tipo_licenca_id']):
                    return jsonify({'error': 'Tipo de licença não encontrado'}), 404
                formacao.tipo_licenca_id = data['tipo_licenca_id']
            if 'inicio' in data:
                try:
                    formacao.inicio = datetime.fromisoformat(data['inicio'])
                except ValueError:
                    return jsonify({'error': 'Formato de data/hora inválido'}), 400
            if 'duracao' in data:
                formacao.duracao = data['duracao']
            if 'anoacademico' in data:
                formacao.anoacademico = data['anoacademico']
            if 'despachoautorizacao' in data:
                formacao.despachoautorizacao = data['despachoautorizacao']
            if 'syncStatus' in data:
                formacao.syncStatus = data['syncStatus']
            if 'syncStatusDate' in data and data['syncStatusDate']:
                formacao.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])

            # Atualizar licenca_id
            if 'licenca_id' in data:
                licenca_id = data['licenca_id']
                if licenca_id:
                    if not Licenca.query.get(licenca_id):
                        return jsonify({'error': 'Licença não encontrada'}), 404
                formacao.licenca_id = licenca_id if licenca_id else None

            # Atualizar despacho_id
            if 'despacho_id' in data:
                despacho_id = data['despacho_id']
                if despacho_id:
                    if not Despacho.query.get(despacho_id):
                        return jsonify({'error': 'Despacho não encontrado'}), 404
                formacao.despacho_id = despacho_id if despacho_id else None

            db.session.commit()
            return jsonify({'message': 'Formação atualizada com sucesso', 'id': formacao.id}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Erro ao atualizar formação {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            formacao = Formacao.query.get(id)
            if not formacao:
                return jsonify({'message': 'Formação não encontrada'}), 404
            db.session.delete(formacao)
            db.session.commit()
            return jsonify({'message': 'Formação excluída com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Erro ao excluir formação {id}")
            return jsonify({'error': str(e)}), 500