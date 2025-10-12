from flask import Blueprint
from controllers.CandidatoController import CandidatoController

candidato_bp = Blueprint('candidato', __name__)

# -------------------- Candidato Routes --------------------

# GET all candidatos
@candidato_bp.route('/candidato', methods=['GET'])
def get_candidatos():
    return CandidatoController.get_all()

# GET candidato by ID
@candidato_bp.route('/candidato/<int:id>', methods=['GET'])
def get_candidato(id):
    return CandidatoController.get_by_id(id)

# POST create new candidato (inclui numero_da_edicao e data_edicao)
@candidato_bp.route('/candidato', methods=['POST'])
def create_candidato():
    return CandidatoController.create()

# PUT update existing candidato (inclui numero_da_edicao e data_edicao)
@candidato_bp.route('/candidato/<int:id>', methods=['PUT'])
def update_candidato(id):
    return CandidatoController.update(id)

# DELETE remove candidato
@candidato_bp.route('/candidato/<int:id>', methods=['DELETE'])
def delete_candidato(id):
    return CandidatoController.delete(id)
