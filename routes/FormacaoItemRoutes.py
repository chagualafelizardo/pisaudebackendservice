from flask import Blueprint
from controllers.FormacaoItemController import FormacaoItemController

formacao_bp = Blueprint('formacao_item', __name__)

# ======================================================
# 🔹 FORMAÇÕES
# ======================================================
@formacao_bp.route('/formacao_item', methods=['GET'])
def get_formacoes():
    return FormacaoItemController.get_all()

@formacao_bp.route('/formacao_item/<int:id>', methods=['GET'])
def get_formacao(id):
    return FormacaoItemController.get_by_id(id)

@formacao_bp.route('/formacao_item', methods=['POST'])
def create_formacao():
    return FormacaoItemController.create()

@formacao_bp.route('/formacao_item/<int:id>', methods=['PUT'])
def update_formacao(id):
    return FormacaoItemController.update(id)

@formacao_bp.route('/formacao_item/<int:id>', methods=['DELETE'])
def delete_formacao(id):
    return FormacaoItemController.delete(id)


# ======================================================
# 🔹 PARTICIPANTES EM UMA FORMAÇÃO
# ======================================================
@formacao_bp.route('/formacao_item/<int:formacao_id>/participante', methods=['POST'])
def adicionar_participante(formacao_id):
    return FormacaoItemController.adicionar_participante(formacao_id)
