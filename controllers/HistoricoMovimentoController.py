import logging
from flask import jsonify, request
from models import db, HistoricoMovimento, UnidadeSanitaria, Medicamento, Utilizador
from datetime import datetime

# Configuração básica de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class HistoricoMovimentoController:

    @staticmethod
    def get_all():
        """
        Retorna todos os movimentos históricos.
        Suporta filtros opcionais via query string:
        - id_unidade_sanitaria
        - id_medicamento
        - data_inicio (formato ISO)
        - data_fim (formato ISO)
        - tipo_movimento
        """
        logger.info("[GET ALL] Request received to fetch all historico movimentos.")
        try:
            query = HistoricoMovimento.query

            # Filtros opcionais
            id_unidade_sanitaria = request.args.get('id_unidade_sanitaria', type=int)
            if id_unidade_sanitaria:
                query = query.filter_by(id_unidade_sanitaria=id_unidade_sanitaria)

            id_medicamento = request.args.get('id_medicamento', type=int)
            if id_medicamento:
                query = query.filter_by(id_medicamento=id_medicamento)

            tipo_movimento = request.args.get('tipo_movimento')
            if tipo_movimento:
                if tipo_movimento not in ['Entrada', 'Saída', 'Ajuste']:
                    return jsonify({'message': 'tipo_movimento inválido. Valores permitidos: Entrada, Saída, Ajuste'}), 400
                query = query.filter_by(tipo_movimento=tipo_movimento)

            data_inicio = request.args.get('data_inicio')
            data_fim = request.args.get('data_fim')
            if data_inicio:
                try:
                    dt_inicio = datetime.fromisoformat(data_inicio)
                    query = query.filter(HistoricoMovimento.data_movimento >= dt_inicio)
                except:
                    return jsonify({'message': 'data_inicio inválida. Use formato ISO (ex: 2023-01-01)'}), 400
            if data_fim:
                try:
                    dt_fim = datetime.fromisoformat(data_fim)
                    query = query.filter(HistoricoMovimento.data_movimento <= dt_fim)
                except:
                    return jsonify({'message': 'data_fim inválida. Use formato ISO (ex: 2023-01-31)'}), 400

            movimentos = query.all()
            result = []
            for m in movimentos:
                result.append({
                    'id': m.id,
                    'id_unidade_sanitaria': m.id_unidade_sanitaria,
                    'unidade_sanitaria_nome': m.unidade_sanitaria.nome if m.unidade_sanitaria else None,
                    'id_medicamento': m.id_medicamento,
                    'medicamento_nome': m.medicamento.nome_padronizado if m.medicamento else None,
                    'medicamento_apresentacao': m.medicamento.apresentacao if m.medicamento else None,
                    'tipo_movimento': m.tipo_movimento,
                    'quantidade': m.quantidade,
                    'data_movimento': m.data_movimento.isoformat() if m.data_movimento else None,
                    'observacao': m.observacao,
                    'registado_por': m.registado_por,
                    'registado_por_nome': m.registado_por_user.nome if m.registado_por_user else None,
                    'data_validade': m.data_validade.isoformat() if m.data_validade else None,
                    'codigo_lote': m.codigo_lote,
                    'syncStatus': m.syncStatus,
                    'syncStatusDate': m.syncStatusDate.isoformat() if m.syncStatusDate else None,
                    'createAt': m.createAt.isoformat() if m.createAt else None,
                    'updateAt': m.updateAt.isoformat() if m.updateAt else None,
                })
            return jsonify(result), 200
        except Exception as e:
            logger.exception("[GET ALL] Failed to fetch historico movimentos.")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        logger.info(f"[GET BY ID] Request received for historico movimento ID {id}.")
        try:
            m = HistoricoMovimento.query.get(id)
            if not m:
                return jsonify({'message': 'Movimento histórico não encontrado'}), 404
            result = {
                'id': m.id,
                'id_unidade_sanitaria': m.id_unidade_sanitaria,
                'unidade_sanitaria_nome': m.unidade_sanitaria.nome if m.unidade_sanitaria else None,
                'id_medicamento': m.id_medicamento,
                'medicamento_nome': m.medicamento.nome_padronizado if m.medicamento else None,
                'medicamento_apresentacao': m.medicamento.apresentacao if m.medicamento else None,
                'tipo_movimento': m.tipo_movimento,
                'quantidade': m.quantidade,
                'data_movimento': m.data_movimento.isoformat() if m.data_movimento else None,
                'observacao': m.observacao,
                'registado_por': m.registado_por,
                'registado_por_nome': m.registado_por_user.nome if m.registado_por_user else None,
                'data_validade': m.data_validade.isoformat() if m.data_validade else None,
                'codigo_lote': m.codigo_lote,
                'syncStatus': m.syncStatus,
                'syncStatusDate': m.syncStatusDate.isoformat() if m.syncStatusDate else None,
                'createAt': m.createAt.isoformat() if m.createAt else None,
                'updateAt': m.updateAt.isoformat() if m.updateAt else None,
            }
            return jsonify(result), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch historico movimento ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        logger.info("[CREATE] Request received to create new historico movimento.")
        try:
            data = request.get_json(force=True)

            # Campos obrigatórios
            id_unidade_sanitaria = data.get('id_unidade_sanitaria')
            id_medicamento = data.get('id_medicamento')
            tipo_movimento = data.get('tipo_movimento')
            quantidade = data.get('quantidade')
            registado_por = data.get('registado_por')

            if not all([id_unidade_sanitaria, id_medicamento, tipo_movimento, quantidade, registado_por]):
                return jsonify({'message': 'Campos obrigatórios: id_unidade_sanitaria, id_medicamento, tipo_movimento, quantidade, registado_por'}), 400

            # Validação de tipo_movimento
            tipos_validos = ['Entrada', 'Saída', 'Ajuste']
            if tipo_movimento not in tipos_validos:
                return jsonify({'message': f'tipo_movimento inválido. Valores permitidos: {tipos_validos}'}), 400

            # Quantidade positiva
            if quantidade <= 0:
                return jsonify({'message': 'A quantidade deve ser maior que zero'}), 400

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

            # Processar data_validade se fornecida
            data_validade_date = None
            if data.get('data_validade'):
                try:
                    data_validade_date = datetime.fromisoformat(data['data_validade']).date()
                except:
                    return jsonify({'message': f'Data de validade inválida: {data["data_validade"]}'}), 400

            # Criar movimento
            movimento = HistoricoMovimento(
                id_unidade_sanitaria=id_unidade_sanitaria,
                id_medicamento=id_medicamento,
                tipo_movimento=tipo_movimento,
                quantidade=quantidade,
                observacao=data.get('observacao'),
                registado_por=registado_por,
                data_validade=data_validade_date,
                codigo_lote=data.get('codigo_lote'),
                syncStatus=data.get('syncStatus', 'Not Syncronized')
            )
            if data.get('syncStatusDate'):
                try:
                    movimento.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])
                except:
                    pass

            db.session.add(movimento)
            db.session.commit()

            return jsonify({
                'message': 'Movimento histórico criado com sucesso',
                'id': movimento.id
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create historico movimento.")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        logger.info(f"[UPDATE] Request received to update historico movimento ID {id}.")
        try:
            movimento = HistoricoMovimento.query.get(id)
            if not movimento:
                return jsonify({'message': 'Movimento histórico não encontrado'}), 404

            data = request.get_json(force=True)

            # Atualizar campos fornecidos
            if 'id_unidade_sanitaria' in data:
                id_unidade_sanitaria = data['id_unidade_sanitaria']
                unidade = UnidadeSanitaria.query.get(id_unidade_sanitaria)
                if not unidade:
                    return jsonify({'message': 'Unidade sanitária não encontrada'}), 404
                movimento.id_unidade_sanitaria = id_unidade_sanitaria

            if 'id_medicamento' in data:
                id_medicamento = data['id_medicamento']
                medicamento = Medicamento.query.get(id_medicamento)
                if not medicamento:
                    return jsonify({'message': 'Medicamento não encontrado'}), 404
                movimento.id_medicamento = id_medicamento

            if 'tipo_movimento' in data:
                tipo_movimento = data['tipo_movimento']
                tipos_validos = ['Entrada', 'Saída', 'Ajuste']
                if tipo_movimento not in tipos_validos:
                    return jsonify({'message': f'tipo_movimento inválido. Valores permitidos: {tipos_validos}'}), 400
                movimento.tipo_movimento = tipo_movimento

            if 'quantidade' in data:
                quantidade = data['quantidade']
                if quantidade <= 0:
                    return jsonify({'message': 'A quantidade deve ser maior que zero'}), 400
                movimento.quantidade = quantidade

            if 'observacao' in data:
                movimento.observacao = data['observacao']

            if 'registado_por' in data:
                registado_por = data['registado_por']
                user = Utilizador.query.get(registado_por)
                if not user:
                    return jsonify({'message': 'Utilizador não encontrado'}), 404
                movimento.registado_por = registado_por

            if 'data_validade' in data:
                if data['data_validade']:
                    try:
                        movimento.data_validade = datetime.fromisoformat(data['data_validade']).date()
                    except:
                        return jsonify({'message': f'Data de validade inválida: {data["data_validade"]}'}), 400
                else:
                    movimento.data_validade = None

            if 'codigo_lote' in data:
                movimento.codigo_lote = data['codigo_lote']

            if 'syncStatus' in data:
                movimento.syncStatus = data['syncStatus']

            if 'syncStatusDate' in data:
                try:
                    movimento.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])
                except:
                    pass

            movimento.updateAt = datetime.utcnow()
            db.session.commit()
            return jsonify({'message': 'Movimento histórico atualizado com sucesso', 'id': movimento.id}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update historico movimento ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        logger.info(f"[DELETE] Request received to delete historico movimento ID {id}.")
        try:
            movimento = HistoricoMovimento.query.get(id)
            if not movimento:
                return jsonify({'message': 'Movimento histórico não encontrado'}), 404

            db.session.delete(movimento)
            db.session.commit()
            return jsonify({'message': 'Movimento histórico deletado com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete historico movimento ID {id}")
            return jsonify({'error': str(e)}), 500