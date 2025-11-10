import logging
from flask import jsonify, request, send_file
from io import BytesIO
from models import db, NotaEnvioDocument

# 🔹 Configuração global de logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)


class NotaEnvioDocumentController:

    # ===============================================================
    # 🔹 Serialização
    # ===============================================================
    @staticmethod
    def serialize(doc: NotaEnvioDocument):
        return {
            'id': doc.id,
            'nota_envio_id': doc.nota_envio_id,
            'nome_arquivo': doc.nome_arquivo,
            'tipo_mime': doc.tipo_mime,
            'data_upload': doc.data_upload.isoformat() if doc.data_upload else None
        }

    # ===============================================================
    # 🔹 Listar todos os documentos
    # ===============================================================
    @staticmethod
    def get_all():
        logger.info("[GET ALL] Iniciando busca de todos os NotaEnvioDocument")
        try:
            documentos = NotaEnvioDocument.query.all()
            logger.info(f"[GET ALL] Encontrados {len(documentos)} documentos")
            return jsonify([NotaEnvioDocumentController.serialize(d) for d in documentos]), 200
        except Exception as e:
            logger.exception("[GET ALL] Erro ao buscar documentos")
            return jsonify({'error': str(e)}), 500

    # ===============================================================
    # 🔹 Buscar por ID
    # ===============================================================
    @staticmethod
    def get_by_id(id):
        logger.info(f"[GET BY ID] Solicitado documento ID={id}")
        try:
            doc = NotaEnvioDocument.query.get(id)
            if not doc:
                logger.warning(f"[GET BY ID] Documento ID={id} não encontrado")
                return jsonify({'message': 'Documento não encontrado'}), 404

            logger.info(f"[GET BY ID] Documento ID={id} encontrado")
            return jsonify(NotaEnvioDocumentController.serialize(doc)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Erro ao buscar documento ID={id}")
            return jsonify({'error': str(e)}), 500

    # ===============================================================
    # 🔹 Download do arquivo (opcional)
    # ===============================================================
    @staticmethod
    def download(id):
        logger.info(f"[DOWNLOAD] Solicitado download de documento ID={id}")
        try:
            doc = NotaEnvioDocument.query.get(id)
            if not doc:
                logger.warning(f"[DOWNLOAD] Documento ID={id} não encontrado")
                return jsonify({'message': 'Documento não encontrado'}), 404

            logger.info(f"[DOWNLOAD] Enviando arquivo '{doc.nome_arquivo}' para download")
            return send_file(
                BytesIO(doc.dados_arquivo),
                mimetype=doc.tipo_mime or 'application/octet-stream',
                as_attachment=True,
                download_name=doc.nome_arquivo
            )
        except Exception as e:
            logger.exception(f"[DOWNLOAD] Erro ao fazer download de documento ID={id}")
            return jsonify({'error': str(e)}), 500

    # ===============================================================
    # 🔹 Upload / Criar novo documento
    # ===============================================================
    @staticmethod
    def download(id):
        try:
            documento = NotaEnvioDocument.query.get(id)
            if not documento:
                return jsonify({'message': 'Documento not found'}), 404
            
            from flask import send_file, request
            import io
            
            # Se for visualização (não download)
            if request.args.get('view') == 'true':
                return send_file(
                    io.BytesIO(documento.dados_arquivo),
                    mimetype=documento.tipo_mime,
                    as_attachment=False,  # Abre no browser
                    download_name=documento.nome_arquivo
                )
            else:
                # Download normal
                return send_file(
                    io.BytesIO(documento.dados_arquivo),
                    as_attachment=True,  # Força download
                    download_name=documento.nome_arquivo,
                    mimetype=documento.tipo_mime
                )
                
        except Exception as e:
            logger.exception(f"Erro ao baixar documento {id}")
            return jsonify({'error': str(e)}), 500
        
    # ===============================================================
    # 🔹 Deletar documento
    # ===============================================================
    @staticmethod
    def delete(id):
        logger.info(f"[DELETE] Solicitada exclusão de documento ID={id}")
        try:
            doc = NotaEnvioDocument.query.get(id)
            if not doc:
                logger.warning(f"[DELETE] Documento ID={id} não encontrado")
                return jsonify({'message': 'Documento não encontrado'}), 404

            db.session.delete(doc)
            db.session.commit()

            logger.info(f"[DELETE] Documento ID={id} excluído com sucesso")
            return jsonify({'message': 'Documento excluído com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Erro ao excluir documento ID={id}")
            return jsonify({'error': str(e)}), 500
