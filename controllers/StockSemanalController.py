import logging
from flask import jsonify, request
from models import db, StockSemanal, StockSemanalLote, UnidadeSanitaria, Medicamento, Utilizador
from datetime import datetime

# Configuração básica de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class StockSemanalController:

    @staticmethod
    def get_all():
        logger.info("[GET ALL] Request received to fetch all stock semanal.")
        try:
            stocks = StockSemanal.query.all()
            result = []
            for s in stocks:
                # Serializar o cabeçalho
                item = {
                    'id': s.id,
                    'id_unidade_sanitaria': s.id_unidade_sanitaria,
                    'unidade_sanitaria_nome': s.unidade_sanitaria.nome if s.unidade_sanitaria else None,
                    'id_medicamento': s.id_medicamento,
                    'medicamento_nome': s.medicamento.nome_padronizado if s.medicamento else None,
                    'medicamento_apresentacao': s.medicamento.apresentacao if s.medicamento else None,
                    'semana': s.semana,
                    'ano': s.ano,
                    'data_registo': s.data_registo.isoformat() if s.data_registo else None,
                    'registado_por': s.registado_por,
                    'registado_por_nome': s.registado_por_user.nome if s.registado_por_user else None,
                    'observacoes': s.observacoes,
                    'syncStatus': s.syncStatus,
                    'syncStatusDate': s.syncStatusDate.isoformat() if s.syncStatusDate else None,
                    'createAt': s.createAt.isoformat() if s.createAt else None,
                    'updateAt': s.updateAt.isoformat() if s.updateAt else None,
                    'lotes': []
                }
                # Adicionar os lotes
                for l in s.lotes:
                    item['lotes'].append({
                        'id': l.id,
                        'quantidade': l.quantidade,
                        'data_validade': l.data_validade.isoformat() if l.data_validade else None,
                        'codigo_lote': l.codigo_lote,
                        'observacoes': l.observacoes,
                        'syncStatus': l.syncStatus,
                        'syncStatusDate': l.syncStatusDate.isoformat() if l.syncStatusDate else None,
                        'createAt': l.createAt.isoformat() if l.createAt else None,
                        'updateAt': l.updateAt.isoformat() if l.updateAt else None,
                    })
                result.append(item)
            return jsonify(result), 200
        except Exception as e:
            logger.exception("[GET ALL] Failed to fetch stock semanal.")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        logger.info(f"[GET BY ID] Request received for stock semanal ID {id}.")
        try:
            s = StockSemanal.query.get(id)
            if not s:
                return jsonify({'message': 'Registo de stock semanal não encontrado'}), 404
            result = {
                'id': s.id,
                'id_unidade_sanitaria': s.id_unidade_sanitaria,
                'unidade_sanitaria_nome': s.unidade_sanitaria.nome if s.unidade_sanitaria else None,
                'id_medicamento': s.id_medicamento,
                'medicamento_nome': s.medicamento.nome_padronizado if s.medicamento else None,
                'medicamento_apresentacao': s.medicamento.apresentacao if s.medicamento else None,
                'semana': s.semana,
                'ano': s.ano,
                'data_registo': s.data_registo.isoformat() if s.data_registo else None,
                'registado_por': s.registado_por,
                'registado_por_nome': s.registado_por_user.nome if s.registado_por_user else None,
                'observacoes': s.observacoes,
                'syncStatus': s.syncStatus,
                'syncStatusDate': s.syncStatusDate.isoformat() if s.syncStatusDate else None,
                'createAt': s.createAt.isoformat() if s.createAt else None,
                'updateAt': s.updateAt.isoformat() if s.updateAt else None,
                'lotes': []
            }
            for l in s.lotes:
                result['lotes'].append({
                    'id': l.id,
                    'quantidade': l.quantidade,
                    'data_validade': l.data_validade.isoformat() if l.data_validade else None,
                    'codigo_lote': l.codigo_lote,
                    'observacoes': l.observacoes,
                    'syncStatus': l.syncStatus,
                    'syncStatusDate': l.syncStatusDate.isoformat() if l.syncStatusDate else None,
                    'createAt': l.createAt.isoformat() if l.createAt else None,
                    'updateAt': l.updateAt.isoformat() if l.updateAt else None,
                })
            return jsonify(result), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch stock semanal ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        logger.info("[CREATE] Request received to create new stock semanal.")
        try:
            data = request.get_json(force=True)

            # Campos obrigatórios do cabeçalho
            id_unidade_sanitaria = data.get('id_unidade_sanitaria')
            id_medicamento = data.get('id_medicamento')
            semana = data.get('semana')
            ano = data.get('ano')
            registado_por = data.get('registado_por')
            lotes = data.get('lotes', [])  # Lista de lotes

            if not all([id_unidade_sanitaria, id_medicamento, semana, ano, registado_por]):
                return jsonify({'message': 'Campos obrigatórios: id_unidade_sanitaria, id_medicamento, semana, ano, registado_por'}), 400

            # Validação de semana (1-53)
            if not (1 <= semana <= 53):
                return jsonify({'message': 'A semana deve estar entre 1 e 53'}), 400

            # Validação de ano (ex: maior que 2000)
            if ano < 2000 or ano > 2100:
                return jsonify({'message': 'Ano inválido'}), 400

            # Verificar existência das chaves estrangeiras
            unidade = UnidadeSanitaria.query.get(id_unidade_sanitaria)
            if not unidade:
                return jsonify({'message': 'Unidade sanitária não encontrada'}), 404

            medicamento = Medicamento.query.get(id_medicamento)
            if not medicamento:
                return jsonify({'message': 'Medicamento não encontrado'}), 404

            user = Utilizador.query.get(registado_por)
            if not user:
                return jsonify({'message': 'Utilizador não encontrado'}), 404

            # Verificar duplicidade (unique constraint)
            existing = StockSemanal.query.filter_by(
                id_unidade_sanitaria=id_unidade_sanitaria,
                id_medicamento=id_medicamento,
                semana=semana,
                ano=ano
            ).first()
            if existing:
                return jsonify({'message': 'Já existe um registo de stock para esta unidade, medicamento, semana e ano.'}), 409

            # Criar o cabeçalho
            stock = StockSemanal(
                id_unidade_sanitaria=id_unidade_sanitaria,
                id_medicamento=id_medicamento,
                semana=semana,
                ano=ano,
                registado_por=registado_por,
                observacoes=data.get('observacoes'),
                syncStatus=data.get('syncStatus', 'Not Syncronized')
            )
            if data.get('syncStatusDate'):
                try:
                    stock.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])
                except:
                    pass

            db.session.add(stock)
            db.session.flush()  # Para obter o ID do stock antes de adicionar lotes

            # Processar lotes
            if not isinstance(lotes, list):
                return jsonify({'message': 'O campo lotes deve ser uma lista'}), 400

            for lote_data in lotes:
                quantidade = lote_data.get('quantidade')
                data_validade = lote_data.get('data_validade')
                codigo_lote = lote_data.get('codigo_lote')
                observacoes_lote = lote_data.get('observacoes')

                if quantidade is None or data_validade is None:
                    return jsonify({'message': 'Cada lote deve conter quantidade e data_validade'}), 400

                # Validar quantidade positiva
                if quantidade <= 0:
                    return jsonify({'message': 'A quantidade do lote deve ser maior que zero'}), 400

                # Converter data_validade de string para date
                try:
                    data_validade_date = datetime.fromisoformat(data_validade).date()
                except:
                    return jsonify({'message': f'Data de validade inválida: {data_validade}'}), 400

                lote = StockSemanalLote(
                    id_stock_semanal=stock.id,
                    quantidade=quantidade,
                    data_validade=data_validade_date,
                    codigo_lote=codigo_lote,
                    observacoes=observacoes_lote,
                    syncStatus=lote_data.get('syncStatus', 'Not Syncronized')
                )
                if lote_data.get('syncStatusDate'):
                    try:
                        lote.syncStatusDate = datetime.fromisoformat(lote_data['syncStatusDate'])
                    except:
                        pass
                db.session.add(lote)

            db.session.commit()
            return jsonify({
                'message': 'Stock semanal criado com sucesso',
                'id': stock.id
            }), 201

        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create stock semanal.")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        logger.info(f"[UPDATE] Request received to update stock semanal ID {id}.")
        try:
            stock = StockSemanal.query.get(id)
            if not stock:
                return jsonify({'message': 'Registo de stock semanal não encontrado'}), 404

            data = request.get_json(force=True)

            # Atualizar campos do cabeçalho (apenas os fornecidos)
            if 'id_unidade_sanitaria' in data:
                id_unidade_sanitaria = data['id_unidade_sanitaria']
                unidade = UnidadeSanitaria.query.get(id_unidade_sanitaria)
                if not unidade:
                    return jsonify({'message': 'Unidade sanitária não encontrada'}), 404
                stock.id_unidade_sanitaria = id_unidade_sanitaria

            if 'id_medicamento' in data:
                id_medicamento = data['id_medicamento']
                medicamento = Medicamento.query.get(id_medicamento)
                if not medicamento:
                    return jsonify({'message': 'Medicamento não encontrado'}), 404
                stock.id_medicamento = id_medicamento

            if 'semana' in data:
                semana = data['semana']
                if not (1 <= semana <= 53):
                    return jsonify({'message': 'A semana deve estar entre 1 e 53'}), 400
                stock.semana = semana

            if 'ano' in data:
                ano = data['ano']
                if ano < 2000 or ano > 2100:
                    return jsonify({'message': 'Ano inválido'}), 400
                stock.ano = ano

            if 'registado_por' in data:
                registado_por = data['registado_por']
                user = Utilizador.query.get(registado_por)
                if not user:
                    return jsonify({'message': 'Utilizador não encontrado'}), 404
                stock.registado_por = registado_por

            if 'observacoes' in data:
                stock.observacoes = data['observacoes']

            if 'syncStatus' in data:
                stock.syncStatus = data['syncStatus']

            if 'syncStatusDate' in data:
                try:
                    stock.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])
                except:
                    pass

            # Atualizar lotes: se fornecidos, substituir completamente
            if 'lotes' in data:
                lotes = data['lotes']
                if not isinstance(lotes, list):
                    return jsonify({'message': 'O campo lotes deve ser uma lista'}), 400

                # Remover lotes antigos (cascade fará isso automaticamente se usarmos delete)
                # Mas para evitar duplicar, podemos simplesmente apagar e recriar
                StockSemanalLote.query.filter_by(id_stock_semanal=stock.id).delete()

                # Adicionar novos lotes
                for lote_data in lotes:
                    quantidade = lote_data.get('quantidade')
                    data_validade = lote_data.get('data_validade')
                    codigo_lote = lote_data.get('codigo_lote')
                    observacoes_lote = lote_data.get('observacoes')

                    if quantidade is None or data_validade is None:
                        return jsonify({'message': 'Cada lote deve conter quantidade e data_validade'}), 400

                    if quantidade <= 0:
                        return jsonify({'message': 'A quantidade do lote deve ser maior que zero'}), 400

                    try:
                        data_validade_date = datetime.fromisoformat(data_validade).date()
                    except:
                        return jsonify({'message': f'Data de validade inválida: {data_validade}'}), 400

                    lote = StockSemanalLote(
                        id_stock_semanal=stock.id,
                        quantidade=quantidade,
                        data_validade=data_validade_date,
                        codigo_lote=codigo_lote,
                        observacoes=observacoes_lote,
                        syncStatus=lote_data.get('syncStatus', 'Not Syncronized')
                    )
                    if lote_data.get('syncStatusDate'):
                        try:
                            lote.syncStatusDate = datetime.fromisoformat(lote_data['syncStatusDate'])
                        except:
                            pass
                    db.session.add(lote)

            # Verificar unique constraint após alterações (pode ter sido violado)
            # Ignorar o próprio registo na verificação
            existing = StockSemanal.query.filter(
                StockSemanal.id_unidade_sanitaria == stock.id_unidade_sanitaria,
                StockSemanal.id_medicamento == stock.id_medicamento,
                StockSemanal.semana == stock.semana,
                StockSemanal.ano == stock.ano,
                StockSemanal.id != stock.id
            ).first()
            if existing:
                return jsonify({'message': 'Já existe outro registo de stock com a mesma unidade, medicamento, semana e ano.'}), 409

            stock.updateAt = datetime.utcnow()
            db.session.commit()
            return jsonify({'message': 'Stock semanal atualizado com sucesso', 'id': stock.id}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update stock semanal ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        logger.info(f"[DELETE] Request received to delete stock semanal ID {id}.")
        try:
            stock = StockSemanal.query.get(id)
            if not stock:
                return jsonify({'message': 'Registo de stock semanal não encontrado'}), 404

            db.session.delete(stock)  # A cascade removerá os lotes
            db.session.commit()
            return jsonify({'message': 'Stock semanal deletado com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete stock semanal ID {id}")
            return jsonify({'error': str(e)}), 500