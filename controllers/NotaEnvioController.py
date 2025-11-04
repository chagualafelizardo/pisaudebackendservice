import logging
import base64
from flask import jsonify, request
from datetime import datetime

from models import (
    db,
    NotaEnvio,
    NotaEnvioItem,
    NotaEnvioDocument,
    TipoItem,
    Item,
    SyncStatusEnum
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

VALID_SYNC_STATUS = [e.value for e in SyncStatusEnum]

# ======================================================
# 🔹 Configuração de Logging Global
# ======================================================
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] - %(message)s"
)
logger = logging.getLogger("NotaEnvioController")

VALID_SYNC_STATUS = [e.value for e in SyncStatusEnum]


class NotaEnvioController:

    # ======================================================
    # 🔹 Serialização
    # ======================================================
    @staticmethod
    def serialize(n: NotaEnvio):
        return {
            'id': n.id,
            'numero_nota': n.numero_nota,
            'tipo_item_id': n.tipo_item_id,
            'tipo_item_nome': n.tipo_item.nome if n.tipo_item else None,
            'data_envio': n.data_envio.isoformat() if n.data_envio else None,
            'origem': n.origem,
            'destino': n.destino,
            'observacoes': n.observacoes,
            'syncStatus': n.syncStatus.value if n.syncStatus else None,
            'syncStatusDate': n.syncStatusDate.isoformat() if n.syncStatusDate else None,
            'createAt': n.createAt.isoformat() if n.createAt else None,
            'updateAt': n.updateAt.isoformat() if n.updateAt else None,
            'itens': [
                {
                    'id': i.id,
                    'item_id': i.item_id,
                    'item_nome': i.item.designacao if i.item else None,
                    'quantidade_enviada': i.quantidade_enviada
                } for i in n.itens
            ],
            'documentos': [
                {
                    'id': d.id,
                    'nome_arquivo': d.nome_arquivo,
                    'tipo_mime': d.tipo_mime,
                    'dados_arquivo': base64.b64encode(d.dados_arquivo).decode('utf-8')
                        if d.dados_arquivo else None
                } for d in n.documentos
            ]
        }

    # ======================================================
    # 🔹 Listar todas
    # ======================================================
    @staticmethod
    def get_all():
        notas = NotaEnvio.query.all()
        return jsonify([{
            'id': n.id,
            'numero_nota': n.numero_nota,
            'origem': n.origem,
            'destino': n.destino,
            'observacoes': n.observacoes
        } for n in notas])

    @staticmethod
    def get_by_id(id):
        nota = NotaEnvio.query.get(id)
        if not nota:
            return jsonify({'message': 'NotaEnvio not found'}), 404

        return jsonify({
            'id': nota.id,
            'numero_nota': nota.numero_nota,
            'origem': nota.origem,
            'destino': nota.destino,
            'observacoes': nota.observacoes,
            'documentos': [
                {
                    'id': d.id,
                    'nome_arquivo': d.nome_arquivo
                } for d in nota.documentos
            ]
        })

    # ======================================================
    # 🔹 Criar nova
    # ======================================================
    @staticmethod
    def create():
        logger.info("➡️ [CREATE] Requisição recebida para criar NotaEnvio")
        try:
            # Detecta se é JSON ou multipart/form-data
            if request.content_type.startswith("application/json"):
                data = request.get_json(force=True)
            else:
                data = request.form.to_dict()
                # Convertendo campos JSON (itens/documentos) se vierem como string
                documentos = {}
                for key, value in data.items():
                    if key.startswith("documentos["):
                        # Ex.: documentos[0][nome_arquivo]
                        idx = key.split("[")[1].split("]")[0]
                        campo = key.split("[")[2].split("]")[0]
                        documentos.setdefault(idx, {})[campo] = value
                # Converte em lista ordenada
                data["documentos"] = [documentos[i] for i in sorted(documentos.keys(), key=int)]
                logger.info(f"📎 Documentos reconstruídos do form: {data['documentos']}")

                # Convertendo campos JSON se vierem como string
                import json
                if 'itens' in data:
                    data['itens'] = json.loads(data['itens'])

            logger.info(f"📦 Dados recebidos: {data}")

            # 🔹 Validação de campos obrigatórios
            required_fields = ['numero_nota', 'tipo_item_id', 'origem', 'destino']
            missing = [f for f in required_fields if not data.get(f)]
            if missing:
                logger.warning(f"❌ Campos obrigatórios ausentes: {missing}")
                return jsonify({'error': f"Campos obrigatórios ausentes: {missing}"}), 400

            # 🔹 Status de sincronização
            sync_status_str = data.get('syncStatus', 'Not Syncronized')
            sync_status = (
                SyncStatusEnum(sync_status_str)
                if sync_status_str in VALID_SYNC_STATUS
                else SyncStatusEnum.NotSyncronized
            )

            # 🔹 Criar NotaEnvio
            nota = NotaEnvio(
                numero_nota=data['numero_nota'],
                tipo_item_id=data['tipo_item_id'],
                origem=data['origem'],
                destino=data['destino'],
                observacoes=data.get('observacoes'),
                syncStatus=sync_status,
                syncStatusDate=datetime.fromisoformat(data['syncStatusDate'])
                    if data.get('syncStatusDate') else None,
                data_envio=datetime.fromisoformat(data['data_envio'])
                    if data.get('data_envio') else datetime.utcnow()
            )

            db.session.add(nota)
            db.session.flush()  # 🔹 Necessário para gerar ID da nota antes de adicionar itens/documents
            logger.info(f"🆕 NotaEnvio criada (id={nota.id}) — adicionando itens e documentos")

            # 🔹 Itens
            itens = data.get('itens', [])
            itens_adicionados = 0
            for i in itens:
                if not i.get('item_id') or not i.get('quantidade_enviada'):
                    logger.warning(f"⚠️ Item inválido ignorado: {i}")
                    continue
                nota_item = NotaEnvioItem(
                    nota_envio_id=nota.id,
                    item_id=i['item_id'],
                    quantidade_enviada=i['quantidade_enviada']
                )
                db.session.add(nota_item)
                itens_adicionados += 1
            logger.info(f"📦 {itens_adicionados} itens adicionados")

            # 🔹 Documentos (JSON com base64)
            documentos = data.get('documentos', [])
            # 🔹 Documentos vindos de multipart/form-data
            documentos_adicionados = 0
            # 🔹 Se houver arquivos enviados via form (multipart/form-data)
            if 'file' in request.files:
                files = request.files.getlist('file')
                for file in files:
                    doc = NotaEnvioDocument(
                        nota_envio_id=nota.id,
                        nome_arquivo=file.filename,
                        tipo_mime=file.mimetype,
                        dados_arquivo=file.read()
                    )
                    nota.documentos.append(doc)
                    documentos_adicionados += 1

            # 🔹 Caso contrário, processa JSON/base64
            elif 'documentos' in data:
                for d in data['documentos']:
                    if 'dados_arquivo' in d:
                        try:
                            dados_bin = base64.b64decode(d['dados_arquivo'])
                            doc = NotaEnvioDocument(
                                nota_envio_id=nota.id,
                                nome_arquivo=d['nome_arquivo'],
                                tipo_mime=d.get('tipo_mime'),
                                dados_arquivo=dados_bin
                            )
                            nota.documentos.append(doc)
                            documentos_adicionados += 1
                        except Exception as e:
                            logger.error(f"❌ Erro ao decodificar documento {d.get('nome_arquivo')}: {e}")
                            continue

            logger.info(f"📎 {documentos_adicionados} documentos vinculados à nota")


            # 🔹 Commit final
            db.session.commit()
            logger.info(f"✅ NotaEnvio salva com sucesso (id={nota.id})")
            return jsonify({
                'message': 'NotaEnvio criada com sucesso',
                'id': nota.id,
                'itens_adicionados': itens_adicionados,
                'documentos_adicionados': documentos_adicionados
            }), 201

        except Exception as e:
            db.session.rollback()
            logger.exception("❌ Erro inesperado ao criar NotaEnvio")
            return jsonify({'error': str(e)}), 500

        finally:
            db.session.close()
            logger.info("🧹 Sessão fechada após operação de criação")

    # ======================================================
    # 🔹 Atualizar
    # ======================================================
    @staticmethod
    def update(id):
        logger.info(f"➡️ [UPDATE] Atualizando NotaEnvio ID={id}")
        try:
            nota = NotaEnvio.query.get(id)
            if not nota:
                logger.warning(f"❌ NotaEnvio ID={id} não encontrada")
                return jsonify({'message': 'NotaEnvio not found'}), 404

            # Suporta JSON ou multipart/form-data
            if request.content_type.startswith("application/json"):
                data = request.get_json(force=True)
            else:
                data = request.form.to_dict()
                # Se houver itens/documentos enviados via form
                import json
                if 'itens' in data:
                    data['itens'] = json.loads(data['itens'])
                if 'documentos' in data:
                    data['documentos'] = json.loads(data['documentos'])

            logger.info(f"📦 Dados recebidos: {data}")

            # Atualiza campos básicos
            for field in ['numero_nota', 'tipo_item_id', 'origem', 'destino', 'observacoes']:
                if field in data:
                    setattr(nota, field, data[field])

            if 'data_envio' in data and data['data_envio']:
                nota.data_envio = datetime.fromisoformat(data['data_envio'])
            if 'syncStatus' in data and data['syncStatus'] in VALID_SYNC_STATUS:
                nota.syncStatus = SyncStatusEnum(data['syncStatus'])
            if 'syncStatusDate' in data and data['syncStatusDate']:
                nota.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])

            # Atualiza itens
            if 'itens' in data:
                # Remove itens antigos
                NotaEnvioItem.query.filter_by(nota_envio_id=nota.id).delete()
                for i in data['itens']:
                    if not i.get('item_id') or not i.get('quantidade_enviada'):
                        continue
                    nota_item = NotaEnvioItem(
                        nota_envio_id=nota.id,
                        item_id=i['item_id'],
                        quantidade_enviada=i['quantidade_enviada']
                    )
                    db.session.add(nota_item)

            # Atualiza documentos
            if 'documentos' in data:
                # Remove documentos antigos
                NotaEnvioDocument.query.filter_by(nota_envio_id=nota.id).delete()
                for d in data['documentos']:
                    if 'dados_arquivo' in d:
                        doc = NotaEnvioDocument(
                            nota_envio_id=nota.id,
                            nome_arquivo=d['nome_arquivo'],
                            tipo_mime=d.get('tipo_mime'),
                            dados_arquivo=base64.b64decode(d['dados_arquivo'])
                        )
                        db.session.add(doc)

            db.session.commit()
            logger.info(f"✅ NotaEnvio ID={id} atualizada com sucesso")
            return jsonify({'message': 'NotaEnvio atualizada com sucesso'}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"❌ Erro ao atualizar NotaEnvio ID={id}")
            return jsonify({'error': str(e)}), 500

        finally:
            db.session.close()
            logger.info("🧹 Sessão fechada após atualização")


    # ======================================================
    # 🔹 Deletar
    # ======================================================
    @staticmethod
    def delete(id):
        logger.info(f"➡️ [DELETE] Solicitada exclusão da NotaEnvio ID={id}")
        try:
            nota = NotaEnvio.query.get(id)
            if not nota:
                logger.warning(f"❌ NotaEnvio ID={id} não encontrada")
                return jsonify({'message': 'NotaEnvio not found'}), 404

            # Deleta itens e documentos antes da nota
            NotaEnvioItem.query.filter_by(nota_envio_id=nota.id).delete()
            NotaEnvioDocument.query.filter_by(nota_envio_id=nota.id).delete()
            db.session.delete(nota)
            db.session.commit()
            logger.info(f"✅ NotaEnvio ID={id} excluída com sucesso")
            return jsonify({'message': 'NotaEnvio excluída com sucesso'}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"❌ Erro ao excluir NotaEnvio ID={id}")
            return jsonify({'error': str(e)}), 500

        finally:
            db.session.close()
            logger.info("🧹 Sessão fechada após exclusão")
