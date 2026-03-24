import logging
import base64
from flask import jsonify, request, send_file
from models import db, Person, Patent, FormaPrestacaoServico, PersonDocument
from datetime import datetime
import io

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

VALID_SYNC_STATUS = ['Not Syncronized', 'Syncronized', 'Updated']

class PersonController:

    @staticmethod
    def serialize_person(p: Person):
        return {
            'id': p.id,
            'patents': [{'id': pat.id, 'description': pat.description} for pat in p.patents],
            'nim': p.nim,
            'nuit': p.nuit,
            'fullname': p.fullname,
            'gender': p.gender,
            'dateofbirth': p.dateofbirth.isoformat() if p.dateofbirth else None,
            'incorporationdata': p.incorporationdata.isoformat() if p.incorporationdata else None,
            'forma_prestacao_servico_id': p.forma_prestacao_servico_id,
            'forma_prestacao_servico_description': p.forma_prestacao_servico.description if p.forma_prestacao_servico else None,
            'image': base64.b64encode(p.image).decode('utf-8') if p.image else None,
            'syncStatus': p.syncStatus,
            'syncStatusDate': p.syncStatusDate.isoformat() if p.syncStatusDate else None,
            'createAt': p.createAt.isoformat() if p.createAt else None,
            'updateAt': p.updateAt.isoformat() if p.updateAt else None
        }

    @staticmethod
    def get_all():
        try:
            persons = Person.query.all()
            return jsonify([PersonController.serialize_person(p) for p in persons]), 200
        except Exception as e:
            logger.exception("[GET ALL] Failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            p = Person.query.get(id)
            if not p:
                return jsonify({'message': 'Person not found'}), 404
            return jsonify(PersonController.serialize_person(p)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Error {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            image_binary = base64.b64decode(data['image']) if data.get('image') else None

            sync_status = data.get('syncStatus')
            if sync_status not in VALID_SYNC_STATUS:
                sync_status = 'Not Syncronized'

            new_person = Person(
                nim=data.get('nim'),
                nuit=data.get('nuit'),
                fullname=data['fullname'],
                gender=data.get('gender'),
                dateofbirth=datetime.fromisoformat(data['dateofbirth']).date() if data.get('dateofbirth') else None,
                incorporationdata=datetime.fromisoformat(data['incorporationdata']).date() if data.get('incorporationdata') else None,
                image=image_binary,
                syncStatus=sync_status,
                syncStatusDate=datetime.fromisoformat(data['syncStatusDate']) if data.get('syncStatusDate') else None
            )

            forma_id_raw = data.get('forma_prestacao_servico_id')
            if forma_id_raw and forma_id_raw.isdigit():
                new_person.forma_prestacao_servico = FormaPrestacaoServico.query.get(int(forma_id_raw))

            patent_ids = data.get('patent_ids', [])
            if patent_ids:
                new_person.patents = Patent.query.filter(Patent.id.in_(patent_ids)).all()

            db.session.add(new_person)
            db.session.commit()
            db.session.refresh(new_person)
            return jsonify({'message': 'Person created successfully', 'id': new_person.id}), 201

        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed")
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def update(id):
        try:
            p = Person.query.get(id)
            if not p:
                return jsonify({'message': 'Person not found'}), 404

            data = request.get_json()
            p.fullname = data.get('fullname', p.fullname)
            p.nim = data.get('nim', p.nim)
            p.nuit = data.get('nuit', p.nuit)
            p.gender = data.get('gender', p.gender)
            p.dateofbirth = datetime.fromisoformat(data['dateofbirth']).date() if data.get('dateofbirth') else p.dateofbirth
            p.incorporationdata = datetime.fromisoformat(data['incorporationdata']).date() if data.get('incorporationdata') else p.incorporationdata

            forma_id_raw = data.get('forma_prestacao_servico_id')
            if forma_id_raw and forma_id_raw.isdigit():
                p.forma_prestacao_servico = FormaPrestacaoServico.query.get(int(forma_id_raw))
            elif forma_id_raw == "":
                p.forma_prestacao_servico = None

            if 'image' in data and data['image']:
                p.image = base64.b64decode(data['image'])

            if 'syncStatus' in data and data['syncStatus'] in VALID_SYNC_STATUS:
                p.syncStatus = data['syncStatus']
            if 'syncStatusDate' in data and data['syncStatusDate']:
                p.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])

            if 'patent_ids' in data:
                p.patents = Patent.query.filter(Patent.id.in_(data['patent_ids'])).all()

            p.updateAt = datetime.utcnow()
            db.session.commit()
            db.session.refresh(p)
            return jsonify({'message': 'Person updated successfully', 'id': p.id}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed {id}")
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def delete(id):
        try:
            p = Person.query.get(id)
            if not p:
                return jsonify({'message': 'Person not found'}), 404
            db.session.delete(p)
            db.session.commit()
            return jsonify({'message': 'Person deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed {id}")
            return jsonify({'error': str(e)}), 500


    # ---------- Métodos para documentos (suporte a múltiplos uploads) ----------
    @staticmethod
    def add_multiple_documents(person_id):
        try:
            p = Person.query.get(person_id)
            if not p:
                return jsonify({'message': 'Person not found'}), 404

            files = request.files.getlist('files')
            if not files:
                return jsonify({'error': 'No files provided'}), 400

            created_docs = []
            for file in files:
                if file.filename == '':
                    continue

                # Recupera os metadados do formulário (enviados pelo frontend)
                doc_type = request.form.get(f'doc_type_{file.filename}', 'OTHER')
                description = request.form.get(f'description_{file.filename}', '')
                file_data = file.read()

                doc = PersonDocument(
                    person_id=person_id,
                    doc_type=doc_type,
                    doc_name=file.filename,
                    description=description,
                    file_data=file_data
                    # Removido: mime_type, uploaded_by
                )
                db.session.add(doc)
                created_docs.append(doc)

            db.session.commit()

            result = [{
                'id': d.id,
                'doc_type': d.doc_type,
                'doc_name': d.doc_name,
                'description': d.description,
                'uploaded_at': d.uploaded_at.isoformat() if d.uploaded_at else None
            } for d in created_docs]

            return jsonify(result), 201

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[ADD MULTIPLE DOCUMENTS] Failed for person {person_id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_documents(person_id):
        """Lista documentos de uma pessoa, retornando metadados."""
        try:
            p = Person.query.get(person_id)
            if not p:
                return jsonify({'message': 'Person not found'}), 404

            docs = PersonDocument.query.filter_by(person_id=person_id).all()
            result = []
            for d in docs:
                result.append({
                    'id': d.id,
                    'doc_type': d.doc_type,
                    'doc_name': d.doc_name,
                    'description': d.description,
                    'uploaded_at': d.uploaded_at.isoformat() if d.uploaded_at else None
                })
            return jsonify(result), 200
        except Exception as e:
            logger.exception(f"[GET DOCUMENTS] Failed for person {person_id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_document_file(document_id):
        try:
            doc = PersonDocument.query.get(document_id)
            if not doc:
                return jsonify({'message': 'Document not found'}), 404

            # Se o campo mime_type não existe, usa fallback
            mimetype = doc.mime_type if hasattr(doc, 'mime_type') else 'application/octet-stream'
            return send_file(
                io.BytesIO(doc.file_data),
                mimetype=mimetype,
                as_attachment=True,
                download_name=doc.doc_name
            )
        except Exception as e:
            logger.exception(f"[GET DOCUMENT FILE] Failed for document {document_id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete_document(document_id):
        """Remove um documento."""
        try:
            doc = PersonDocument.query.get(document_id)
            if not doc:
                return jsonify({'message': 'Document not found'}), 404

            db.session.delete(doc)
            db.session.commit()
            return jsonify({'message': 'Document deleted'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE DOCUMENT] Failed for document {document_id}")
            return jsonify({'error': str(e)}), 500