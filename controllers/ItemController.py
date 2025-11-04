import logging
import base64
from flask import jsonify, request
from models import db, Item, Armazem, Porto
from datetime import datetime
from controllers.StockController import StockController

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ItemController:

    @staticmethod
    def serialize(i: Item):
        return {
            'id': i.id,
            'codigo': i.codigo,
            'designacao': i.designacao,
            'armazem_id': i.armazem_id,
            'armazem_nome': i.armazem.nome if i.armazem else None,
            'porto_id': i.porto_id,
            'porto_nome': i.porto.nome if i.porto else None,
            'imagem': base64.b64encode(i.imagem).decode('utf-8') if i.imagem else None,
            'pdf_nome': i.pdf_nome,
            'pdf_tipo': i.pdf_tipo,
            'pdf_dados': base64.b64encode(i.pdf_dados).decode('utf-8') if i.pdf_dados else None,
            'observacoes': i.observacoes,
            'hs_code': i.hs_code,
            'quantidade': i.quantidade,
            'batch_no': i.batch_no,
            'data_fabricacao': i.data_fabricacao.isoformat() if i.data_fabricacao else None,
            'data_validade': i.data_validade.isoformat() if i.data_validade else None,
            'no_cartoes': i.no_cartoes,
            'peso_bruto_total': i.peso_bruto_total,
            'volume_total_cbm': i.volume_total_cbm,
            'total_cartoes': i.total_cartoes,
            'total_paletes': i.total_paletes,
            'dimensoes_palete_cm': i.dimensoes_palete_cm,
            'syncStatus': i.syncStatus,  # agora é apenas string
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
    def get_historico(id):
        try:
            item = Item.query.get(id)
            if not item:
                return jsonify({'message': 'Item not found'}), 404

            historico = [
                {
                    'id': h.id,
                    'tipo_movimento': h.tipo_movimento,
                    'quantidade': h.quantidade,
                    'observacoes': h.observacoes,
                    'data_movimento': h.data_movimento.isoformat()
                } for h in item.historico
            ]

            return jsonify(historico), 200
        except Exception as e:
            logger.exception(f"[HISTORICO] Item {id} failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            imagem_bin = base64.b64decode(data['imagem']) if data.get('imagem') else None
            pdf_bin = base64.b64decode(data['pdf_dados']) if data.get('pdf_dados') else None

            # ✅ syncStatus agora é apenas string
            sync_status = data.get('syncStatus', 'Not Syncronized')

            item = Item(
                codigo=data['codigo'],
                designacao=data['designacao'],
                armazem_id=data['armazem_id'],
                porto_id=data.get('porto_id'),
                imagem=imagem_bin,
                pdf_nome=data.get('pdf_nome'),
                pdf_tipo=data.get('pdf_tipo'),
                pdf_dados=pdf_bin,
                observacoes=data.get('observacoes'),
                hs_code=data.get('hs_code'),
                quantidade=data.get('quantidade'),
                batch_no=data.get('batch_no'),
                data_fabricacao=datetime.fromisoformat(data['data_fabricacao']) if data.get('data_fabricacao') else None,
                data_validade=datetime.fromisoformat(data['data_validade']) if data.get('data_validade') else None,
                no_cartoes=data.get('no_cartoes'),
                peso_bruto_total=data.get('peso_bruto_total'),
                volume_total_cbm=data.get('volume_total_cbm'),
                total_cartoes=data.get('total_cartoes'),
                total_paletes=data.get('total_paletes'),
                dimensoes_palete_cm=data.get('dimensoes_palete_cm'),
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
            item.armazem_id = data.get('armazem_id', item.armazem_id)
            item.porto_id = data.get('porto_id', item.porto_id)
            if 'imagem' in data and data['imagem']:
                item.imagem = base64.b64decode(data['imagem'])
            if 'pdf_dados' in data and data['pdf_dados']:
                item.pdf_dados = base64.b64decode(data['pdf_dados'])
            item.pdf_nome = data.get('pdf_nome', item.pdf_nome)
            item.pdf_tipo = data.get('pdf_tipo', item.pdf_tipo)
            item.observacoes = data.get('observacoes', item.observacoes)
            item.hs_code = data.get('hs_code', item.hs_code)
            item.quantidade = data.get('quantidade', item.quantidade)
            item.batch_no = data.get('batch_no', item.batch_no)
            item.data_fabricacao = datetime.fromisoformat(data['data_fabricacao']) if data.get('data_fabricacao') else item.data_fabricacao
            item.data_validade = datetime.fromisoformat(data['data_validade']) if data.get('data_validade') else item.data_validade
            item.no_cartoes = data.get('no_cartoes', item.no_cartoes)
            item.peso_bruto_total = data.get('peso_bruto_total', item.peso_bruto_total)
            item.volume_total_cbm = data.get('volume_total_cbm', item.volume_total_cbm)
            item.total_cartoes = data.get('total_cartoes', item.total_cartoes)
            item.total_paletes = data.get('total_paletes', item.total_paletes)
            item.dimensoes_palete_cm = data.get('dimensoes_palete_cm', item.dimensoes_palete_cm)

            # ✅ atualiza syncStatus como string
            if 'syncStatus' in data:
                item.syncStatus = data['syncStatus']
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

    @staticmethod
    def adicionar_entrada_stock(id):
        try:
            data = request.get_json()
            quantidade = int(data.get('quantidade', 0))
            observacoes = data.get('observacoes')
            return StockController.adicionar_entrada(id, quantidade, observacoes)
        except Exception as e:
            import traceback
            logger.exception(f"[ENTRADA STOCK] Item {id} failed")
            print(traceback.format_exc())
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def distribuir_item(item_id):
        try:
            data = request.get_json()
            quantidade = int(data.get("quantidade", 0))
            location_id = data.get("location_id")
            observacoes = data.get("observacoes", None)

            item = Item.query.get(item_id)
            if not item:
                return jsonify({"message": "Item não encontrado"}), 404

            if quantidade <= 0:
                return jsonify({"message": "Quantidade inválida"}), 400

            if item.quantidade < quantidade:
                return jsonify({"message": "Quantidade insuficiente"}), 400

            from models import Distribuicao  # importa aqui para evitar import circular

            distrib = Distribuicao(
                item_id=item_id,
                location_id=location_id,
                quantidade=quantidade,
                data_distribuicao=datetime.utcnow(),
                observacao=observacoes
            )
            db.session.add(distrib)
            item.quantidade -= quantidade
            db.session.commit()
            return jsonify({"message": "Distribuição registrada com sucesso"}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DISTRIBUIR ITEM] Item {item_id} failed")
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_necessidades_por_item():
        try:
            from models import ItemLocationNecessidade
            logger.info("[GET NECESSIDADES] Buscando todas as necessidades com nome do item")

            necessidades = (
                db.session.query(
                    ItemLocationNecessidade.id,
                    ItemLocationNecessidade.item_id,
                    Item.designacao.label("item_nome"),
                    ItemLocationNecessidade.location_id,
                    ItemLocationNecessidade.quantidade,
                    ItemLocationNecessidade.descricao,
                    ItemLocationNecessidade.data_registro
                )
                .join(Item, Item.id == ItemLocationNecessidade.item_id)
                .all()
            )

            result = []
            for n in necessidades:
                result.append({
                    "id": n.id,
                    "item_id": n.item_id,
                    "item_nome": n.item_nome,
                    "location_id": n.location_id,
                    "quantidade": n.quantidade,
                    "descricao": n.descricao,
                    "data_registro": n.data_registro.isoformat() if n.data_registro else None
                })

            logger.info(f"[GET NECESSIDADES] {len(result)} necessidades encontradas")
            return jsonify(result), 200

        except Exception as e:
            logger.exception(f"[GET NECESSIDADES] Erro ao buscar necessidades: {e}")
            return jsonify({"error": str(e)}), 500
