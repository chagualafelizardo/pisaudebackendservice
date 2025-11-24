from flask import Blueprint
from controllers.ParticipanteController import ParticipanteController

participante_bp = Blueprint('participante', __name__)

# ======================================================
# 🔹 PARTICIPANTES
# ======================================================

@participante_bp.route('/participantes', methods=['GET'])
def get_participantes():
    """Lista todos os participantes"""
    return ParticipanteController.get_all()

@participante_bp.route('/participantes/<int:id>', methods=['GET'])
def get_participante(id):
    """Obtém um participante pelo ID"""
    return ParticipanteController.get_by_id(id)

@participante_bp.route('/participantes', methods=['POST'])
def create_participante():
    """Cria um novo participante"""
    return ParticipanteController.create()

@participante_bp.route('/participantes/<int:id>', methods=['PUT'])
def update_participante(id):
    """Atualiza um participante"""
    return ParticipanteController.update(id)

@participante_bp.route('/participantes/<int:id>', methods=['DELETE'])
def delete_participante(id):
    """Deleta um participante"""
    return ParticipanteController.delete(id)


# ======================================================
# 🔹 PARTICIPANTES DE UMA FORMAÇÃO
# ======================================================

@participante_bp.route('/formacoes/<int:formacao_id>/participantes', methods=['GET'])
def get_participantes_por_formacao(formacao_id):
    """Lista os participantes de uma formação específica"""
    return ParticipanteController.get_by_formacao(formacao_id)


# ======================================================
# 🔹 MARCAR PRESENÇA
# ======================================================

@participante_bp.route('/participantes/<int:id>/presenca', methods=['PUT'])
def marcar_presenca_participante(id):
    """Marca presença do participante"""
    return ParticipanteController.marcar_presenca(id)
