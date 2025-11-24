import logging
import base64
from flask import jsonify, request
from models import db, Item, Armazem, Porto
from datetime import datetime
from controllers.StockController import StockController
from models import Distribuicao  # importa aqui para evitar import circular

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

            # 📄 Comprovativo de envio
            'pdf_nome': i.pdf_nome,
            'pdf_tipo': i.pdf_tipo,
            'pdf_dados': base64.b64encode(i.pdf_dados).decode('utf-8') if i.pdf_dados else None,

            # 📑 Guia assinada (novo)
            'guia_assinada_nome': i.guia_assinada_nome,
            'data_recepcao': i.data_recepcao,
            'guia_assinada_tipo': i.guia_assinada_tipo,
            'guia_assinada_dados': base64.b64encode(i.guia_assinada_dados).decode('utf-8') if i.guia_assinada_dados else None,

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
            'syncStatus': i.syncStatus,
            'syncStatusDate': i.syncStatusDate.isoformat() if i.syncStatusDate else None,

            # 👥 Utilizadores
            'user': i.user,
            'recebeu': i.recebeu,  # ✅ Novo campo

            'createAt': i.createAt.isoformat() if i.createAt else None,
            'updateAt': i.updateAt.isoformat() if i.updateAt else None
        }

     # ======================================================
    # 🔹 FUNÇÃO AUXILIAR: Capturar usuário automaticamente
    # ======================================================
    @staticmethod
    def _get_user_from_request():
        user_value = None
        if request.is_json:
            data = request.get_json(silent=True) or {}
            user_value = data.get('user') or data.get('username')
        else:
            data = request.form.to_dict()
            user_value = data.get('user') or data.get('username')

        if not user_value:
            try:
                from flask import session
                user_value = session.get('username') or session.get('user')
            except Exception:
                pass

        if not user_value:
            user_value = request.headers.get('X-User') or request.headers.get('X-Username')

        if not user_value:
            user_value = request.cookies.get('username')

        if not user_value:
            try:
                from flask_login import current_user
                if current_user and getattr(current_user, 'is_authenticated', False):
                    user_value = getattr(current_user, 'username', None) or \
                               getattr(current_user, 'email', None) or \
                               getattr(current_user, 'name', None)
            except Exception:
                pass

        if not user_value:
            user_value = 'Usuário não identificado'
            logger.warning("⚠️ Usuário não pôde ser determinado no ItemController")

        logger.info(f"👤 User determinado no ItemController: {user_value}")
        return user_value


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

    # No método get_historico, substitua esta parte:
    
    @staticmethod
    def get_historico(id):
        try:
            logging.info(f"📊 [HISTORICO] Buscando histórico para item {id}")
            
            # ✅ CORREÇÃO: Usar o modelo ItemHistorico diretamente com SQLAlchemy
            from models import ItemHistorico
            
            historico = ItemHistorico.query.filter_by(item_id=id).order_by(ItemHistorico.data_movimento.desc()).all()
            
            historico_data = [
                {
                    'id': h.id,
                    'item_id': h.item_id,
                    'tipo_movimento': h.tipo_movimento,
                    'quantidade': h.quantidade,
                    'data_movimento': h.data_movimento.isoformat() if h.data_movimento else None,
                    'observacoes': h.observacoes,
                    'user': getattr(h, 'user', None)  # ✅ Adicionar user se existir
                }
                for h in historico
            ]
            
            logging.info(f"✅ [HISTORICO] Retornando {len(historico_data)} registros")
            return jsonify(historico_data), 200
            
        except Exception as e:
            logging.error(f"❌ [HISTORICO] Item {id} failed: {str(e)}")
            return jsonify({'error': str(e)}), 500
            
        except Exception as e:
            logging.error(f"❌ [HISTORICO] Item {id} failed: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def adicionar_entrada_stock(id):
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Dados JSON necessários'}), 400

            quantidade = data.get('quantidade')
            observacoes = data.get('observacoes', '')
            user = data.get('user', 'Sistema')

            if not quantidade:
                return jsonify({'error': 'Quantidade é obrigatória'}), 400

            logger.info(f"➡️ [ENTRADA STOCK] Adicionando entrada para Item ID={id}")
            logger.info(f"👤 User: {user}")
            logger.info(f"📦 Quantidade: {quantidade}")

            # ✅ Chama o StockController corretamente
            return StockController.adicionar_entrada(id, quantidade, observacoes, user)

        except Exception as e:
            logger.error(f"❌ [ENTRADA STOCK] Item {id} failed: {str(e)}")
            return jsonify({'error': str(e)}), 500

        
    @staticmethod
    def create():
        try:
            logger.info("➡️ [CREATE ITEM] Requisição recebida para criar Item")
            data = request.get_json() if request.is_json else request.form.to_dict()
            logger.info(f"📦 Dados recebidos: {data.keys()}")

            user_value = ItemController._get_user_from_request()

            if not data.get('codigo') or not data.get('designacao'):
                return jsonify({'error': 'Código e designação são obrigatórios'}), 400

            imagem_bin = base64.b64decode(data['imagem']) if data.get('imagem') else None
            pdf_bin = base64.b64decode(data['pdf_dados']) if data.get('pdf_dados') else None
            guia_bin = base64.b64decode(data['guia_assinada_dados']) if data.get('guia_assinada_dados') else None

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
                guia_assinada_nome=data.get('guia_assinada_nome'),
                data_recepcao=data.get('data_recepcao'),
                guia_assinada_tipo=data.get('guia_assinada_tipo'),
                guia_assinada_dados=guia_bin,
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
                syncStatusDate=datetime.fromisoformat(data['syncStatusDate']) if data.get('syncStatusDate') else None,
                user=user_value,
                recebeu=data.get('recebeu')
            )

            db.session.add(item)
            db.session.flush()  # 🔥 Garante que o ID é gerado antes do commit
            db.session.commit()

            logger.info(f"✅ Item criado com sucesso (ID={item.id}) por {user_value}")

            return jsonify({
                'message': 'Item created successfully',
                'id': item.id  # 🔥 ID agora é retornado sempre
            }), 201

        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Item failed")
            return jsonify({'error': str(e)}), 500


    # ======================================================
    # 🔹 UPDATE ajustado com os novos campos
    # ======================================================
    @staticmethod
    def update(id):
        try:
            logger.info(f"➡️ [UPDATE ITEM] Atualizando Item ID={id}")

            item = Item.query.get(id)
            if not item:
                return jsonify({'message': 'Item not found'}), 404

            data = request.get_json() if request.is_json else request.form.to_dict()
            logger.info(f"📦 Dados recebidos: {data.keys()}")

            user_value = ItemController._get_user_from_request()

            # 🔹 Atualiza campos existentes
            item.codigo = data.get('codigo', item.codigo)
            item.designacao = data.get('designacao', item.designacao)
            item.armazem_id = data.get('armazem_id', item.armazem_id)
            item.porto_id = data.get('porto_id', item.porto_id)

            # 🔹 Atualiza imagem e PDFs
            if data.get('imagem'):
                item.imagem = base64.b64decode(data['imagem'])
            if data.get('pdf_dados'):
                item.pdf_dados = base64.b64decode(data['pdf_dados'])
            if data.get('guia_assinada_dados'):
                item.guia_assinada_dados = base64.b64decode(data['guia_assinada_dados'])

            item.pdf_nome = data.get('pdf_nome', item.pdf_nome)
            item.pdf_tipo = data.get('pdf_tipo', item.pdf_tipo)
            item.guia_assinada_nome = data.get('guia_assinada_nome', item.guia_assinada_nome)
            item.data_recepcao = data.get('data_recepcao', item.data_recepcao)
            item.guia_assinada_tipo = data.get('guia_assinada_tipo', item.guia_assinada_tipo)

            item.observacoes = data.get('observacoes', item.observacoes)
            item.hs_code = data.get('hs_code', item.hs_code)
            item.quantidade = data.get('quantidade', item.quantidade)
            item.batch_no = data.get('batch_no', item.batch_no)

            if data.get('data_fabricacao'):
                item.data_fabricacao = datetime.fromisoformat(data['data_fabricacao'])
            if data.get('data_validade'):
                item.data_validade = datetime.fromisoformat(data['data_validade'])

            item.no_cartoes = data.get('no_cartoes', item.no_cartoes)
            item.peso_bruto_total = data.get('peso_bruto_total', item.peso_bruto_total)
            item.volume_total_cbm = data.get('volume_total_cbm', item.volume_total_cbm)
            item.total_cartoes = data.get('total_cartoes', item.total_cartoes)
            item.total_paletes = data.get('total_paletes', item.total_paletes)
            item.dimensoes_palete_cm = data.get('dimensoes_palete_cm', item.dimensoes_palete_cm)

            # 🔹 Novos campos
            item.recebeu = data.get('recebeu', item.recebeu)  # ✅ Novo campo
            item.user = user_value

            if data.get('syncStatus'):
                item.syncStatus = data['syncStatus']
            if data.get('syncStatusDate'):
                item.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])

            db.session.commit()
            logger.info(f"✅ Item atualizado (id={item.id}) por {user_value}")
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
            
            logger.info(f"✅ Item deletado com sucesso (id={id})")
            return jsonify({'message': 'Item deleted successfully'}), 200
            
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Item {id} failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def adicionar_entrada(self, item_id, quantidade, observacoes=None, user=None):
        """
        Adiciona uma entrada de stock para um item
        """
        try:
            logging.info(f"📥 [STOCK CONTROLLER] Entrada para item {item_id}: {quantidade} unidades")
            
            # Buscar o item atual
            item = self.db.get_item_by_id(item_id)
            if not item:
                return jsonify({'error': 'Item não encontrado'}), 404
            
            # Calcular nova quantidade
            nova_quantidade = (item.quantidade or 0) + quantidade
            
            # Atualizar quantidade do item
            self.db.update_item_quantidade(item_id, nova_quantidade)
            
            # Registrar no histórico
            historico_data = {
                'item_id': item_id,
                'tipo_movimento': 'entrada',
                'quantidade': quantidade,
                'observacoes': observacoes,
                'user': user  # ✅ Agora aceita o parâmetro user
            }
            
            self.db.add_item_historico(historico_data)
            
            logging.info(f"✅ [STOCK CONTROLLER] Entrada registrada: Item {item_id} = {nova_quantidade} unidades")
            
            return jsonify({
                'message': 'Entrada de stock registrada com sucesso',
                'nova_quantidade': nova_quantidade
            }), 200
            
        except Exception as e:
            logging.error(f"❌ [STOCK CONTROLLER] Erro ao adicionar entrada: {str(e)}")
            return jsonify({'error': str(e)}), 500
            
        except Exception as e:
            import traceback
            logger.exception(f"[ENTRADA STOCK] Item {id} failed")
            print(traceback.format_exc())
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def distribuir_item(item_id):
        try:
            logger.info(f"➡️ [DISTRIBUIR ITEM] Distribuindo Item ID={item_id}")
            
            data = request.get_json()
            quantidade = int(data.get("quantidade", 0))
            location_id = data.get("location_id")
            observacoes = data.get("observacoes", None)

            # ======================================================
            # 🔹 Capturar USER automaticamente
            # ======================================================
            user_value = ItemController._get_user_from_request()

            item = Item.query.get(item_id)
            if not item:
                return jsonify({"message": "Item não encontrado"}), 404

            if quantidade <= 0:
                return jsonify({"message": "Quantidade inválida"}), 400

            if item.quantidade < quantidade:
                return jsonify({"message": "Quantidade insuficiente"}), 400

            distrib = Distribuicao(
                item_id=item_id,
                location_id=location_id,
                quantidade=quantidade,
                data_distribuicao=datetime.utcnow(),
                observacao=observacoes,
                user=user_value  # ✅ usuário logado que está fazendo a distribuição
            )
            
            db.session.add(distrib)
            item.quantidade -= quantidade
            db.session.commit()
            
            logger.info(f"✅ Item {item_id} distribuído: {quantidade} unidades para location {location_id} por usuário: {user_value}")
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
                    ItemLocationNecessidade.data_registro,
                    ItemLocationNecessidade.user  # ✅ Inclui usuário que registrou a necessidade
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
                    "data_registro": n.data_registro.isoformat() if n.data_registro else None,
                    "user": n.user  # ✅ Retorna usuário
                })

            logger.info(f"[GET NECESSIDADES] {len(result)} necessidades encontradas")
            return jsonify(result), 200

        except Exception as e:
            logger.exception(f"[GET NECESSIDADES] Erro ao buscar necessidades: {e}")
            return jsonify({"error": str(e)}), 500
        
    # ======================================================
    # 🔹 CONFIRMAR RECEPÇÃO DE ITEM (versão com logs reforçados)
    # ======================================================
    @staticmethod
    def confirmar_recepcao(id):
        """
        Atualiza os dados de recepção de um item com logs detalhados para debugar respostas inválidas.
        """
        try:
            logger.info(f"📥 [CONFIRMAR RECEPÇÃO] Item ID={id} - Iniciando")

            # Log dos headers e tamanho do corpo (não logues ficheiros inteiros em produção)
            try:
                raw_body = request.get_data(as_text=True)
                body_len = len(raw_body) if raw_body is not None else 0
            except Exception as ex:
                raw_body = None
                body_len = 0
                logger.exception("⚠️ Erro ao obter request.get_data()")

            logger.info(f"➡️ Headers recebidos: {dict(request.headers)}")
            logger.info(f"➡️ Tamanho do corpo: {body_len} caracteres")
            if raw_body:
                # log apenas os primeiros 1000 caracteres para evitar flood
                logger.debug(f"➡️ Corpo (truncado 1000): {raw_body[:1000]}")

            # Tentar obter JSON de forma robusta
            try:
                data = request.get_json(force=False, silent=True)
                if data is None:
                    # tentar parse manual para logar erros de JSON
                    try:
                        data = json.loads(raw_body) if raw_body else None
                    except Exception as parse_ex:
                        logger.warning("❌ JSON inválido no corpo da request", exc_info=parse_ex)
                        return jsonify({
                            'error': 'JSON inválido no corpo da request',
                            'details': str(parse_ex),
                            'received_body_preview': (raw_body[:500] + '...') if raw_body and len(raw_body) > 500 else raw_body
                        }), 400
            except Exception as ex:
                logger.exception("❌ Erro ao ler JSON da request")
                return jsonify({'error': 'Erro ao ler JSON da request', 'details': str(ex)}), 400

            if not data:
                logger.warning("❌ Sem JSON no corpo da request")
                return jsonify({'error': 'JSON com dados é necessário'}), 400

            # Procura do item
            item = Item.query.get(id)
            if not item:
                logger.warning(f"❌ Item ID={id} não encontrado")
                return jsonify({'message': 'Item não encontrado'}), 404

            # Dados recebidos
            nome_recebedor = data.get('recebeu')
            data_recepcao = data.get('data_recepcao')
            guia_nome = data.get('guia_assinada_nome')
            guia_tipo = data.get('guia_assinada_tipo')
            guia_dados = data.get('guia_assinada_dados')

            logger.info(f"➡️ Payload parseado: recebeu={nome_recebedor}, data_recepcao={data_recepcao}, "
                        f"guia_nome={guia_nome}, guia_tipo={guia_tipo}, guia_dados_presente={bool(guia_dados)}")

            # Validação básica
            if not nome_recebedor:
                logger.warning("❌ Falta 'recebeu' no payload")
                return jsonify({'error': 'O nome do recebedor é obrigatório'}), 400
            if not guia_dados:
                logger.warning("❌ Falta 'guia_assinada_dados' no payload")
                return jsonify({'error': 'O ficheiro da guia assinada é obrigatório'}), 400

            # Decodificar base64 de forma segura e logar erros
            try:
                # remover prefixos como "data:...;base64," se existirem
                if guia_dados.startswith('data:'):
                    # separar na primeira vírgula
                    _parts = guia_dados.split(',', 1)
                    guia_dados_b64 = _parts[1] if len(_parts) == 2 else _parts[0]
                else:
                    guia_dados_b64 = guia_dados

                # validação ao decodificar - validate=True garante que somente base64 válido é aceite
                guia_bytes = base64.b64decode(guia_dados_b64, validate=True)
                logger.info(f"➡️ Ficheiro decodificado com sucesso, bytes={len(guia_bytes)}")
            except (binascii.Error, ValueError) as b64err:
                logger.exception("❌ Erro na decodificação Base64 da guia_assinada_dados")
                return jsonify({
                    'error': 'Erro ao decodificar o ficheiro base64',
                    'details': str(b64err),
                    'received_b64_preview': guia_dados_b64[:200] + '...' if guia_dados_b64 and len(guia_dados_b64) > 200 else guia_dados_b64
                }), 400

            # Atualização dos campos no modelo
            item.recebeu = nome_recebedor
            item.data_recepcao = datetime.fromisoformat(data_recepcao) if data_recepcao else datetime.utcnow()
            item.guia_assinada_nome = guia_nome
            item.guia_assinada_tipo = guia_tipo
            item.guia_assinada_dados = guia_bytes

            db.session.commit()

            logger.info(f"✅ [CONFIRMAR RECEPÇÃO] Item {id} atualizado por recebedor '{nome_recebedor}'")
            return jsonify({'message': 'Confirmação de recepção registrada com sucesso'}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"❌ [CONFIRMAR RECEPÇÃO] Erro ao confirmar recepção do item {id}")
            # Em dev pode ser útil enviar detalhes; em produção envia apenas mensagem genérica
            return jsonify({'error': 'Erro interno no servidor', 'details': str(e)}), 500