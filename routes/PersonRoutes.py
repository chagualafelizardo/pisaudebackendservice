from flask import Blueprint
from controllers.PersonController import PersonController

person_bp = Blueprint('person', __name__)

# GET all persons
@person_bp.route('/person', methods=['GET'])
def get_persons():
    return PersonController.get_all()

# GET person by ID
@person_bp.route('/person/<int:id>', methods=['GET'])
def get_person(id):
    return PersonController.get_by_id(id)

# POST create new person
@person_bp.route('/person', methods=['POST'])
def create_person():
    return PersonController.create()

# PUT update existing person
@person_bp.route('/person/<int:id>', methods=['PUT'])
def update_person(id):
    return PersonController.update(id)

# DELETE remove person
@person_bp.route('/person/<int:id>', methods=['DELETE'])
def delete_person(id):
    return PersonController.delete(id)

# ---------- Rotas para documentos ----------
# Listar documentos de uma pessoa
@person_bp.route('/person/<int:person_id>/documents', methods=['GET'])
def get_person_documents(person_id):
    return PersonController.get_documents(person_id)

# Upload de múltiplos documentos para uma pessoa
@person_bp.route('/person/<int:person_id>/documents', methods=['POST'])
def add_person_documents(person_id):
    return PersonController.add_multiple_documents(person_id)

# Download de um documento específico
@person_bp.route('/person/documents/<int:document_id>/file', methods=['GET'])
def download_document(document_id):
    return PersonController.get_document_file(document_id)

# Excluir um documento
@person_bp.route('/person/documents/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    return PersonController.delete_document(document_id)