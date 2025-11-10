# controllers/ItemLocationNecessidadeController.py
import logging
from flask import jsonify, request
from sqlalchemy.orm import joinedload
from models import db, ItemLocationNecessidade, Item, Location
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ItemLocationNecessidadeController:

    @staticmethod
    def _safe_attr(obj, attrs, default=None):
        if not obj:
            return default
        for a in attrs:
            if hasattr(obj, a):
                val = getattr(obj, a)
                if callable(val):
                    try:
                        return val()
                    except Exception:
                        continue
                return val
        return default

    @staticmethod
    def serialize(n: ItemLocationNecessidade):
        """Serializa uma necessidade para JSON (safe access aos relationships)."""
        item_designacao = None
        try:
            item_designacao = ItemLocationNecessidadeController._safe_attr(n.item, ['designacao'])
        except Exception:
            item_p = Item.query.get(n.item_id)
            item_designacao = ItemLocationNecessidadeController._safe_attr(item_p, ['designacao'])

        location_nome = None
        try:
            location_nome = ItemLocationNecessidadeController._safe_attr(n.location, ['descricao'])
        except Exception:
            loc = Location.query.get(n.location_id)
            location_nome = ItemLocationNecessidadeController._safe_attr(loc, ['designacao'])

        return {
            'id': n.id,
            'item_id': n.item_id,
            'item_designacao': item_designacao,
            'location_id': n.location_id,
            'location_nome': location_nome,
            'quantidade': n.quantidade,
            'descricao': n.descricao,
            'data_registro': n.data_registro.isoformat() if n.data_registro else None,
            'user': n.user  # ✅ novo campo
        }

    @staticmethod
    def get_all():
        try:
            logger.info("[GET ALL] Buscando todas as necessidades com nome do item")

            necessidades = (
                db.session.query(ItemLocationNecessidade, Item.nome.label("item_nome"))
                .join(Item, Item.id == ItemLocationNecessidade.item_id)
                .all()
            )

            result = [
                {
                    "id": n.ItemLocationNecessidade.id,
                    "item_id": n.ItemLocationNecessidade.item_id,
                    "item_nome": n.ItemLocationNecessidade.descricao,  # mantém lógica atual
                    "location_id": n.ItemLocationNecessidade.location_id,
                    "quantidade": n.ItemLocationNecessidade.quantidade,
                    "descricao": n.ItemLocationNecessidade.descricao,
                    "data_registro": n.ItemLocationNecessidade.data_registro.isoformat()
                    if n.ItemLocationNecessidade.data_registro
                    else None,
                    "user": n.ItemLocationNecessidade.user  # ✅ novo campo
                }
                for n in necessidades
            ]

            logger.info(f"[GET ALL] {len(result)} necessidades encontradas")
            return jsonify(result), 200

        except Exception as e:
            logger.exception(f"[GET ALL] Erro ao buscar necessidades: {e}")
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            n = ItemLocationNecessidade.query.get(id)
            if not n:
                return jsonify({'message': 'Necessidade not found'}), 404
            return jsonify(ItemLocationNecessidadeController.serialize(n)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Necessidade {id} failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_item(item_id):
        try:
            necessidades = (
                ItemLocationNecessidade.query
                .filter_by(item_id=item_id)
                .options(
                    joinedload(ItemLocationNecessidade.location),
                    joinedload(ItemLocationNecessidade.item)
                )
                .all()
            )
            return jsonify([ItemLocationNecessidadeController.serialize(n) for n in necessidades]), 200
        except Exception as e:
            logger.exception(f"[GET BY ITEM] Necessidades for Item {item_id} failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        """Cria uma nova necessidade"""
        try:
            data = request.get_json() or {}
            if 'item_id' not in data or 'location_id' not in data or 'quantidade' not in data:
                return jsonify({'error': 'item_id, location_id e quantidade são obrigatórios'}), 400

            n = ItemLocationNecessidade(
                item_id=int(data['item_id']),
                location_id=int(data['location_id']),
                quantidade=int(data['quantidade']),
                descricao=data.get('descricao'),
                data_registro=(
                    datetime.fromisoformat(data['data_registro'])
                    if data.get('data_registro')
                    else datetime.utcnow()
                ),
                user=data.get('user')  # ✅ novo campo
            )
            db.session.add(n)
            db.session.commit()
            return jsonify({'message': 'Necessidade criada com sucesso', 'id': n.id}), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Necessidade failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        """Atualiza uma necessidade"""
        try:
            n = ItemLocationNecessidade.query.get(id)
            if not n:
                return jsonify({'message': 'Necessidade not found'}), 404

            data = request.get_json() or {}
            if 'item_id' in data:
                n.item_id = int(data.get('item_id'))
            if 'location_id' in data:
                n.location_id = int(data.get('location_id'))
            if 'quantidade' in data:
                n.quantidade = int(data.get('quantidade'))
            if 'descricao' in data:
                n.descricao = data.get('descricao')
            if data.get('data_registro'):
                n.data_registro = datetime.fromisoformat(data['data_registro'])
            if 'user' in data:
                n.user = data.get('user')  # ✅ novo campo

            db.session.commit()
            return jsonify({'message': 'Necessidade atualizada com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Necessidade {id} failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            n = ItemLocationNecessidade.query.get(id)
            if not n:
                return jsonify({'message': 'Necessidade not found'}), 404

            db.session.delete(n)
            db.session.commit()
            return jsonify({'message': 'Necessidade eliminada com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Necessidade {id} failed")
            return jsonify({'error': str(e)}), 500
