import logging
from flask import jsonify, request
from models import db, Distribuicao, Item, Armazem, Location
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DistribuicaoController:

    # ======================================================
    # 🔹 FUNÇÃO AUXILIAR: Capturar usuário automaticamente
    # ======================================================
    @staticmethod
    def _get_user_from_request():
        """Captura o usuário de múltiplas fontes possíveis"""
        user_value = None
        
        # 1️⃣ Do JSON ou form (prioridade máxima - vem do frontend)
        if request.is_json:
            data = request.get_json(silent=True) or {}
            user_value = data.get('user') or data.get('username')
        else:
            data = request.form.to_dict()
            user_value = data.get('user') or data.get('username')

        # 2️⃣ Da sessão Flask (segunda opção)
        if not user_value:
            try:
                from flask import session
                user_value = session.get('username') or session.get('user')
            except Exception:
                pass

        # 3️⃣ Headers HTTP (terceira opção)
        if not user_value:
            user_value = request.headers.get('X-User') or request.headers.get('X-Username')

        # 4️⃣ Cookies (quarta opção)
        if not user_value:
            user_value = request.cookies.get('username')

        # 5️⃣ Flask-login (se o app usar login)
        if not user_value:
            try:
                from flask_login import current_user
                if current_user and getattr(current_user, 'is_authenticated', False):
                    user_value = getattr(current_user, 'username', None) or \
                               getattr(current_user, 'email', None) or \
                               getattr(current_user, 'name', None)
            except Exception:
                pass

        # 6️⃣ Final fallback
        if not user_value:
            user_value = 'Usuário não identificado'
            logger.warning("⚠️ Usuário não pôde ser determinado no DistribuicaoController")

        logger.info(f"👤 User determinado no DistribuicaoController: {user_value}")
        return user_value

    # ======================================================
    # 🔹 Serialização
    # ======================================================
    @staticmethod
    def serialize(d: Distribuicao):
        return {
            'id': d.id,
            'item_id': d.item_id,
            'item_nome': d.item.designacao if d.item else None,
            'armazem_id': d.armazem_id,
            'armazem_nome': d.armazem.nome if d.armazem else None,
            'location_id': d.location_id,
            'location_nome': d.location.name if d.location else None,
            'quantidade': d.quantidade,
            'data_distribuicao': d.data_distribuicao.isoformat() if d.data_distribuicao else None,
            'observacao': d.observacao,
            'user': d.user  # ✅ novo campo
        }

    # ======================================================
    # 🔹 Listar todas
    # ======================================================
    @staticmethod
    def get_all():
        try:
            distribuicoes = Distribuicao.query.all()
            return jsonify([DistribuicaoController.serialize(d) for d in distribuicoes]), 200
        except Exception as e:
            logger.exception("[GET ALL] Distribuicao failed")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            distribuicao = Distribuicao.query.get(id)
            if not distribuicao:
                return jsonify({'message': 'Distribuicao not found'}), 404
            return jsonify(DistribuicaoController.serialize(distribuicao)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Distribuicao {id}")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 Criar nova - VERSÃO CORRIGIDA
    # ======================================================
    @staticmethod
    def create():
        try:
            logger.info("➡️ [CREATE DISTRIBUICAO] Requisição recebida para criar Distribuição")
            
            # Captura dados da requisição
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()

            logger.info(f"📦 Dados recebidos para criar distribuição: {data.keys()}")

            # ======================================================
            # 🔹 Capturar USER automaticamente
            # ======================================================
            user_value = DistribuicaoController._get_user_from_request()

            # Validações básicas
            required_fields = ['item_id', 'location_id', 'quantidade']
            missing = [f for f in required_fields if not data.get(f)]
            if missing:
                logger.warning(f"❌ Campos obrigatórios ausentes: {missing}")
                return jsonify({'error': f"Campos obrigatórios ausentes: {missing}"}), 400

            quantidade = int(data.get('quantidade', 0))
            if quantidade <= 0:
                return jsonify({'error': 'Quantidade deve ser maior que zero'}), 400

            # Verificar se o item existe e tem quantidade suficiente
            item = Item.query.get(data['item_id'])
            if not item:
                return jsonify({'error': 'Item não encontrado'}), 404

            if item.quantidade < quantidade:
                return jsonify({'error': 'Quantidade insuficiente em stock'}), 400

            # Criar distribuição
            distribuicao = Distribuicao(
                item_id=data['item_id'],
                armazem_id=data.get('armazem_id'),
                location_id=data['location_id'],
                quantidade=quantidade,
                data_distribuicao=datetime.fromisoformat(data['data_distribuicao']) if data.get('data_distribuicao') else datetime.utcnow(),
                observacao=data.get('observacao'),
                user=user_value  # ✅ AGORA SALVA O USUÁRIO CORRETAMENTE
            )
            
            # Atualizar quantidade do item
            item.quantidade -= quantidade
            
            db.session.add(distribuicao)
            db.session.commit()
            
            logger.info(f"✅ Distribuição criada com sucesso (id={distribuicao.id}) por usuário: {user_value}")
            return jsonify({
                'message': 'Distribuição criada com sucesso', 
                'id': distribuicao.id,
                'quantidade_distribuida': quantidade,
                'stock_restante': item.quantidade
            }), 201
            
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Distribuicao failed")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 Atualizar - VERSÃO CORRIGIDA
    # ======================================================
    @staticmethod
    def update(id):
        try:
            logger.info(f"➡️ [UPDATE DISTRIBUICAO] Atualizando Distribuição ID={id}")
            
            distribuicao = Distribuicao.query.get(id)
            if not distribuicao:
                return jsonify({'message': 'Distribuição não encontrada'}), 404

            # Captura dados da requisição
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()

            logger.info(f"📦 Dados recebidos para atualizar distribuição: {data.keys()}")

            # ======================================================
            # 🔹 Capturar USER automaticamente
            # ======================================================
            user_value = DistribuicaoController._get_user_from_request()

            # Guardar valores antigos para rollback se necessário
            quantidade_antiga = distribuicao.quantidade
            item_antigo = distribuicao.item_id

            # Atualizar campos
            if 'item_id' in data:
                distribuicao.item_id = data['item_id']
            if 'armazem_id' in data:
                distribuicao.armazem_id = data['armazem_id']
            if 'location_id' in data:
                distribuicao.location_id = data['location_id']
                
            if 'quantidade' in data:
                nova_quantidade = int(data['quantidade'])
                if nova_quantidade <= 0:
                    return jsonify({'error': 'Quantidade deve ser maior que zero'}), 400
                
                # Ajustar stock do item
                item = Item.query.get(distribuicao.item_id)
                if not item:
                    return jsonify({'error': 'Item não encontrado'}), 404
                
                # Reverter quantidade antiga e aplicar nova
                item.quantidade += quantidade_antiga  # Devolve o que foi distribuído
                if item.quantidade < nova_quantidade:
                    return jsonify({'error': 'Quantidade insuficiente em stock'}), 400
                
                item.quantidade -= nova_quantidade  # Aplica nova distribuição
                distribuicao.quantidade = nova_quantidade

            if 'data_distribuicao' in data and data['data_distribuicao']:
                distribuicao.data_distribuicao = datetime.fromisoformat(data['data_distribuicao'])
                
            distribuicao.observacao = data.get('observacao', distribuicao.observacao)
            
            # ✅ Atualiza user sempre
            distribuicao.user = user_value

            db.session.commit()
            
            logger.info(f"✅ Distribuição atualizada com sucesso (id={distribuicao.id}) por usuário: {user_value}")
            return jsonify({'message': 'Distribuição atualizada com sucesso'}), 200
            
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Distribuicao {id} failed")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 Deletar - VERSÃO CORRIGIDA
    # ======================================================
    @staticmethod
    def delete(id):
        try:
            logger.info(f"➡️ [DELETE DISTRIBUICAO] Deletando Distribuição ID={id}")
            
            distribuicao = Distribuicao.query.get(id)
            if not distribuicao:
                return jsonify({'message': 'Distribuição não encontrada'}), 404
            
            # Devolver quantidade ao stock do item
            item = Item.query.get(distribuicao.item_id)
            if item:
                item.quantidade += distribuicao.quantidade
                logger.info(f"🔄 Devolvendo {distribuicao.quantidade} unidades ao item {item.id}")
            
            db.session.delete(distribuicao)
            db.session.commit()
            
            logger.info(f"✅ Distribuição deletada com sucesso (id={id})")
            return jsonify({'message': 'Distribuição deletada com sucesso'}), 200
            
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Distribuicao {id} failed")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 Método adicional: Buscar distribuições por item
    # ======================================================
    @staticmethod
    def get_by_item(item_id):
        try:
            logger.info(f"📋 Buscando distribuições para o item ID={item_id}")
            
            distribuicoes = Distribuicao.query.filter_by(item_id=item_id).all()
            resultado = [DistribuicaoController.serialize(d) for d in distribuicoes]
            
            logger.info(f"✅ Encontradas {len(resultado)} distribuições para o item {item_id}")
            return jsonify(resultado), 200
            
        except Exception as e:
            logger.exception(f"[GET BY ITEM] Erro ao buscar distribuições do item {item_id}")
            return jsonify({'error': str(e)}), 500

    # ======================================================
    # 🔹 Método adicional: Buscar distribuições por location
    # ======================================================
    @staticmethod
    def get_by_location(location_id):
        try:
            logger.info(f"📋 Buscando distribuições para a location ID={location_id}")
            
            distribuicoes = Distribuicao.query.filter_by(location_id=location_id).all()
            resultado = [DistribuicaoController.serialize(d) for d in distribuicoes]
            
            logger.info(f"✅ Encontradas {len(resultado)} distribuições para a location {location_id}")
            return jsonify(resultado), 200
            
        except Exception as e:
            logger.exception(f"[GET BY LOCATION] Erro ao buscar distribuições da location {location_id}")
            return jsonify({'error': str(e)}), 500