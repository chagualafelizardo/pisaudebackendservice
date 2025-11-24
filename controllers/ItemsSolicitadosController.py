import logging
from flask import jsonify, request
from models import db, ItemsSolicitados
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ItemsSolicitadosController:

    @staticmethod
    def get_all():
        try:
            logger.info("📦 GET /api/items_solicitados - Buscando todos os itens solicitados")
            
            items = ItemsSolicitados.query.order_by(ItemsSolicitados.id.desc()).all()
            logger.info(f"✅ Encontrados {len(items)} itens solicitados")
            
            result = [{
                'id': i.id,
                'nome': i.nome,
                'quantidade': i.quantidade,
                'data_solicitacao': i.data_solicitacao.isoformat() if i.data_solicitacao else None,
                'createAt': i.createAt.isoformat() if i.createAt else None,
                'updateAt': i.updateAt.isoformat() if i.updateAt else None
            } for i in items]

            return jsonify(result), 200

        except Exception as e:
            logger.exception("❌ ERRO CRÍTICO: Falha ao buscar ItemsSolicitados")
            return jsonify({'error': 'Erro interno do servidor', 'details': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            logger.info(f"🔍 GET /api/items_solicitados/{id} - Buscando item por ID")
            
            i = ItemsSolicitados.query.get(id)
            if not i:
                logger.warning(f"⚠️ Item solicitado {id} não encontrado")
                return jsonify({'message': 'Item solicitado não encontrado'}), 404

            logger.info(f"✅ Item {id} encontrado: {i.nome}")
            return jsonify({
                'id': i.id,
                'nome': i.nome,
                'quantidade': i.quantidade,
                'data_solicitacao': i.data_solicitacao.isoformat() if i.data_solicitacao else None,
                'createAt': i.createAt.isoformat() if i.createAt else None,
                'updateAt': i.updateAt.isoformat() if i.updateAt else None
            }), 200

        except Exception as e:
            logger.exception(f"❌ ERRO: Falha ao buscar ItemsSolicitados ID {id}")
            return jsonify({'error': 'Erro interno do servidor', 'details': str(e)}), 500

    @staticmethod
    def create():
        try:
            logger.info("🆕 POST /api/items_solicitados - Criando novo item solicitado")
            
            data = request.get_json(force=True)
            logger.info(f"📥 Dados recebidos: {data}")
            
            # 🔥 CORREÇÃO: Usar os mesmos nomes do frontend
            nome = data.get('nome_item') or data.get('nome')  # ✅ Suporte a ambos
            quantidade = data.get('quantidade_solicitada') or data.get('quantidade')  # ✅ Suporte a ambos
            data_solicitacao = data.get('data_necessaria') or data.get('data_solicitacao')

            # Validações
            if not nome:
                logger.warning("❌ Validação falhou: Nome é obrigatório")
                return jsonify({'message': 'Nome do item é obrigatório'}), 400
            
            if not quantidade:
                logger.warning("❌ Validação falhou: Quantidade é obrigatória")
                return jsonify({'message': 'Quantidade é obrigatória'}), 400

            try:
                quantidade = int(quantidade)
                if quantidade <= 0:
                    logger.warning("❌ Validação falhou: Quantidade deve ser positiva")
                    return jsonify({'message': 'Quantidade deve ser maior que zero'}), 400
            except (ValueError, TypeError):
                logger.warning("❌ Validação falhou: Quantidade deve ser um número válido")
                return jsonify({'message': 'Quantidade deve ser um número válido'}), 400

            # Converter data se fornecida
            data_solicitacao_obj = None
            if data_solicitacao:
                try:
                    data_solicitacao_obj = datetime.fromisoformat(data_solicitacao.replace('Z', '+00:00'))
                except ValueError:
                    logger.warning("❌ Formato de data inválido, usando data atual")
                    data_solicitacao_obj = datetime.utcnow()

            # Criar novo item
            new_item = ItemsSolicitados(
                nome=nome,
                quantidade=quantidade,
                data_solicitacao=data_solicitacao_obj or datetime.utcnow()
            )

            db.session.add(new_item)
            db.session.commit()

            logger.info(f"✅ ItemSolicitado criado com sucesso - ID: {new_item.id}, Nome: {new_item.nome}, Quantidade: {new_item.quantidade}")

            return jsonify({
                'message': 'Item solicitado criado com sucesso',
                'id': new_item.id,
                'nome': new_item.nome,
                'quantidade': new_item.quantidade,
                'data_solicitacao': new_item.data_solicitacao.isoformat() if new_item.data_solicitacao else None,
                'createAt': new_item.createAt.isoformat() if new_item.createAt else None
            }), 201

        except Exception as e:
            db.session.rollback()
            logger.exception("❌ ERRO CRÍTICO: Falha ao criar ItemsSolicitados")
            return jsonify({'error': 'Erro interno do servidor', 'details': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            logger.info(f"✏️ PUT /api/items_solicitados/{id} - Atualizando item")
            
            i = ItemsSolicitados.query.get(id)
            if not i:
                logger.warning(f"⚠️ Item solicitado {id} não encontrado para atualização")
                return jsonify({'message': 'Item solicitado não encontrado'}), 404

            data = request.get_json(force=True)
            logger.info(f"📥 Dados para atualização: {data}")
            
            # 🔥 CORREÇÃO: Usar os mesmos nomes do frontend
            nome = data.get('nome_item') or data.get('nome')
            quantidade = data.get('quantidade_solicitada') or data.get('quantidade')
            data_solicitacao = data.get('data_necessaria') or data.get('data_solicitacao')

            # Validações
            if not nome:
                return jsonify({'message': 'Nome é obrigatório'}), 400
            
            if not quantidade:
                return jsonify({'message': 'Quantidade é obrigatória'}), 400

            try:
                quantidade = int(quantidade)
                if quantidade <= 0:
                    return jsonify({'message': 'Quantidade deve ser maior que zero'}), 400
            except (ValueError, TypeError):
                return jsonify({'message': 'Quantidade deve ser um número válido'}), 400

            # Atualizar campos
            i.nome = nome
            i.quantidade = quantidade
            i.updateAt = datetime.utcnow()

            if data_solicitacao:
                try:
                    i.data_solicitacao = datetime.fromisoformat(data_solicitacao.replace('Z', '+00:00'))
                except ValueError:
                    logger.warning("Formato de data inválido, mantendo data original")

            db.session.commit()

            logger.info(f"✅ ItemSolicitado atualizado com sucesso - ID: {i.id}")

            return jsonify({
                'message': 'Item solicitado atualizado com sucesso',
                'id': i.id,
                'nome': i.nome,
                'quantidade': i.quantidade,
                'data_solicitacao': i.data_solicitacao.isoformat() if i.data_solicitacao else None,
                'updateAt': i.updateAt.isoformat() if i.updateAt else None
            }), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"❌ ERRO: Falha ao atualizar ItemsSolicitados ID {id}")
            return jsonify({'error': 'Erro interno do servidor', 'details': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            logger.info(f"🗑️ DELETE /api/items_solicitados/{id} - Removendo item")
            
            i = ItemsSolicitados.query.get(id)
            if not i:
                logger.warning(f"⚠️ Item solicitado {id} não encontrado para remoção")
                return jsonify({'message': 'Item solicitado não encontrado'}), 404

            item_info = f"ID: {i.id}, Nome: {i.nome}, Quantidade: {i.quantidade}"
            db.session.delete(i)
            db.session.commit()

            logger.info(f"✅ ItemSolicitado removido com sucesso - {item_info}")

            return jsonify({
                'message': 'Item solicitado removido com sucesso',
                'deleted_item': item_info
            }), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"❌ ERRO: Falha ao remover ItemsSolicitados ID {id}")
            return jsonify({'error': 'Erro interno do servidor', 'details': str(e)}), 500