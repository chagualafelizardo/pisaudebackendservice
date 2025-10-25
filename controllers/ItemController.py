import logging
import base64
from flask import jsonify, request
from models import db, Item, Armazem, SyncStatusEnum
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Lista de valores válidos para validação
VALID_SYNC_STATUS = [e.value for e in SyncStatusEnum]


class ItemController:

    @staticmethod
    def serialize(i: Item):
        return {
            'id': i.id,
            'codigo': i.codigo,
            'designacao': i.designacao,
            'imagem': base64.b64encode(i.imagem).decode('utf-8') if i.imagem else None,
            'armazem_id': i.armazem_id,
            'armazem_nome': i.armazem.nome if i.armazem else None,
            'syncStatus': i.syncStatus.value if i.syncStatus else None,
            'syncStatusDate': i.syncStatusDate.isoformat() if i.syncStatusDate else None,
            'createAt': i.createAt.isoformat() if i.createAt else None,
            'updateAt': i.updateAt.isoformat() if i.updateAt else None
        }

    @staticmethod
    def get_all():
        try:
            itens = Item.query.all()
            return jsonify([ItemController.serialize(i) for i in itens]), 200
        except Exception as e:
            logger.exception("[GET ALL] Item failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            item = Item.query.get(id)
            if not item:
                return jsonify({'message': 'Item not found'}), 404
            return jsonify(ItemController.serialize(item)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Item {id} failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            imagem_bin = base64.b64decode(data['imagem']) if data.get('imagem') else None

            # Validação e conversão para Enum
            sync_status_str = data.get('syncStatus', 'Not Syncronized')
            sync_status = SyncStatusEnum(sync_status_str) if sync_status_str in VALID_SYNC_STATUS else SyncStatusEnum.NotSyncronized

            item = Item(
                codigo=data['codigo'],
                designacao=data['designacao'],
                imagem=imagem_bin,
                armazem_id=data['armazem_id'],
                syncStatus=sync_status,
                syncStatusDate=datetime.fromisoformat(data['syncStatusDate']) if data.get('syncStatusDate') else None
            )
            db.session.add(item)
            db.session.commit()
            return jsonify({'message': 'Item created successfully', 'id': item.id}), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Item failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            item = Item.query.get(id)
            if not item:
                return jsonify({'message': 'Item not found'}), 404

            data = request.get_json()
            item.codigo = data.get('codigo', item.codigo)
            item.designacao = data.get('designacao', item.designacao)
            if 'imagem' in data and data['imagem']:
                item.imagem = base64.b64decode(data['imagem'])
            item.armazem_id = data.get('armazem_id', item.armazem_id)

            # Atualiza o SyncStatus se válido
            if 'syncStatus' in data and data['syncStatus'] in VALID_SYNC_STATUS:
                item.syncStatus = SyncStatusEnum(data['syncStatus'])
            if 'syncStatusDate' in data and data['syncStatusDate']:
                item.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])

            db.session.commit()
            return jsonify({'message': 'Item updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Item {id} failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            item = Item.query.get(id)
            if not item:
                return jsonify({'message': 'Item not found'}), 404
            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': 'Item deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Item {id} failed")
            return jsonify({'error': str(e)}), 500
