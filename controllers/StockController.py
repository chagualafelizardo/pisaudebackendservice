import logging
from flask import jsonify
from models import db, Item, ItemHistorico
from datetime import datetime

logger = logging.getLogger(__name__)

class StockController:

    @staticmethod
    def adicionar_entrada(item_id, quantidade, observacoes=None, user=None):
        try:
            logger.info(f"📥 [STOCK] Entrada para item {item_id}: {quantidade} unidades")

            # ✅ Buscar o item diretamente via SQLAlchemy
            item = Item.query.get(item_id)
            if not item:
                return jsonify({'error': 'Item não encontrado'}), 404

            # ✅ Atualizar a quantidade
            item.quantidade = (item.quantidade or 0) + int(quantidade)
            db.session.commit()

            # ✅ Registrar histórico
            historico = ItemHistorico(
                item_id=item_id,
                tipo_movimento='entrada',
                quantidade=quantidade,
                observacoes=observacoes,
                user=user,
                data_movimento=datetime.utcnow()
            )
            db.session.add(historico)
            db.session.commit()

            logger.info(f"✅ [STOCK] Entrada registrada: Item {item_id} = {item.quantidade} unidades")

            return jsonify({
                'message': 'Entrada de stock registrada com sucesso',
                'nova_quantidade': item.quantidade
            }), 200

        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ [STOCK] Erro ao adicionar entrada: {str(e)}")
            return jsonify({'error': str(e)}), 500
