from flask import Blueprint
from controllers.NotaEnvioDocumentController import NotaEnvioDocumentController

# 🔹 Criação do Blueprint
nota_envio_document_bp = Blueprint('nota_envio_document', __name__)

# ===============================================================
# 🔹 ROTAS PADRÃO CRUD
# ===============================================================

@nota_envio_document_bp.route('/notaenviodocument', methods=['GET'])
def get_nota_envio_documents():
    """Listar todos os documentos"""
    return NotaEnvioDocumentController.get_all()


@nota_envio_document_bp.route('/notaenviodocument/<int:id>', methods=['GET'])
def get_nota_envio_document(id):
    """Buscar documento por ID"""
    return NotaEnvioDocumentController.get_by_id(id)


@nota_envio_document_bp.route('/notaenviodocument', methods=['POST'])
def create_nota_envio_document():
    """Fazer upload de um novo documento"""
    return NotaEnvioDocumentController.create()


@nota_envio_document_bp.route('/notaenviodocument/<int:id>', methods=['DELETE'])
def delete_nota_envio_document(id):
    """Excluir documento"""
    return NotaEnvioDocumentController.delete(id)


# ===============================================================
# 🔹 ROTA EXTRA — Download de arquivo
# ===============================================================

@nota_envio_document_bp.route('/notaenviodocument/<int:id>/download', methods=['GET'])
def download_nota_envio_document(id):
    """Baixar o arquivo binário de um documento"""
    return NotaEnvioDocumentController.download(id)
