import logging
from flask import jsonify, request
from models import db, HistoricoMovimento, Location, Medicamento, User, StockSemanal, StockSemanalLote
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class HistoricoMovimentoController:

    @staticmethod
    def get_all():
        logger.info("[GET ALL] Request received to fetch all historico movimentos.")
        try:
            query = HistoricoMovimento.query

            # Filtros opcionais
            id_location = request.args.get('id_location', type=int)
            if id_location:
                query = query.filter_by(id_location=id_location)

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
                    'id_location': m.id_location,
                    'location_nome': m.location.name if m.location else None,
                    'id_medicamento': m.id_medicamento,
                    'medicamento_nome': m.medicamento.nome_padronizado if m.medicamento else None,
                    'medicamento_apresentacao': m.medicamento.apresentacao if m.medicamento else None,
                    'tipo_movimento': m.tipo_movimento,
                    'quantidade': m.quantidade,
                    'data_movimento': m.data_movimento.isoformat() if m.data_movimento else None,
                    'observacoes': m.observacoes,
                    'registado_por': m.registado_por,
                    'registado_por_nome': m.registado_por_user.fullname if m.registado_por_user else None,
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
                'id_location': m.id_location,
                'location_nome': m.location.name if m.location else None,
                'id_medicamento': m.id_medicamento,
                'medicamento_nome': m.medicamento.nome_padronizado if m.medicamento else None,
                'medicamento_apresentacao': m.medicamento.apresentacao if m.medicamento else None,
                'tipo_movimento': m.tipo_movimento,
                'quantidade': m.quantidade,
                'data_movimento': m.data_movimento.isoformat() if m.data_movimento else None,
                'observacoes': m.observacoes,
                'registado_por': m.registado_por,
                'registado_por_nome': m.registado_por_user.fullname if m.registado_por_user else None,
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
        # (já estava implementado, mantido)
        logger.info("[CREATE] Request received to create new historico movimento.")
        try:
            data = request.get_json(force=True)

            try:
                id_location = int(data.get('id_location'))
                id_medicamento = int(data.get('id_medicamento'))
                quantidade = int(data.get('quantidade'))
                registado_por = int(data.get('registado_por'))
            except (TypeError, ValueError):
                return jsonify({'message': 'Campos id_location, id_medicamento, quantidade, registado_por devem ser números inteiros'}), 400

            tipo_movimento = data.get('tipo_movimento')
            codigo_lote = data.get('codigo_lote')
            data_validade = data.get('data_validade')

            if not all([id_location, id_medicamento, tipo_movimento, quantidade, registado_por]):
                return jsonify({'message': 'Campos obrigatórios: id_location, id_medicamento, tipo_movimento, quantidade, registado_por'}), 400

            tipos_validos = ['Entrada', 'Saída', 'Ajuste']
            if tipo_movimento not in tipos_validos:
                return jsonify({'message': f'tipo_movimento inválido. Valores permitidos: {tipos_validos}'}), 400

            if quantidade <= 0:
                return jsonify({'message': 'A quantidade deve ser maior que zero'}), 400

            location = Location.query.get(id_location)
            if not location:
                return jsonify({'message': 'Unidade sanitária não encontrada'}), 404

            medicamento = Medicamento.query.get(id_medicamento)
            if not medicamento:
                return jsonify({'message': 'Medicamento não encontrado'}), 404

            user = User.query.get(registado_por)
            if not user:
                return jsonify({'message': 'User não encontrado'}), 404

            data_validade_date = None
            if data_validade:
                try:
                    data_validade_date = datetime.fromisoformat(data_validade).date()
                except:
                    return jsonify({'message': f'Data de validade inválida: {data_validade}'}), 400

            # Localizar o lote
            lote = None
            if codigo_lote and data_validade_date:
                stock = StockSemanal.query.filter_by(
                    id_location=id_location,
                    id_medicamento=id_medicamento
                ).first()
                if stock:
                    lote = StockSemanalLote.query.filter_by(
                        id_stock_semanal=stock.id,
                        codigo_lote=codigo_lote,
                        data_validade=data_validade_date
                    ).first()

            if not lote:
                if tipo_movimento == 'Entrada':
                    stock = StockSemanal.query.filter_by(
                        id_location=id_location,
                        id_medicamento=id_medicamento
                    ).first()
                    if not stock:
                        return jsonify({'message': 'Stock semanal não encontrado para esta unidade/medicamento. Crie um registo de stock primeiro.'}), 400
                    lote = StockSemanalLote(
                        id_stock_semanal=stock.id,
                        quantidade=0,
                        data_validade=data_validade_date,
                        codigo_lote=codigo_lote,
                        observacoes='Criado por movimento'
                    )
                    db.session.add(lote)
                    db.session.flush()
                else:
                    return jsonify({'message': 'Lote não encontrado para o movimento. Verifique código e data de validade.'}), 404

            if tipo_movimento == 'Entrada':
                lote.quantidade += quantidade
            elif tipo_movimento == 'Saída':
                if lote.quantidade < quantidade:
                    return jsonify({'message': f'Quantidade insuficiente no lote. Disponível: {lote.quantidade}, solicitado: {quantidade}'}), 400
                lote.quantidade -= quantidade
            elif tipo_movimento == 'Ajuste':
                # Não implementado
                return jsonify({'message': 'Tipo Ajuste não suportado. Use Entrada ou Saída.'}), 400

            movimento = HistoricoMovimento(
                id_location=id_location,
                id_medicamento=id_medicamento,
                tipo_movimento=tipo_movimento,
                quantidade=quantidade,
                observacoes=data.get('observacoes'),
                registado_por=registado_por,
                data_validade=data_validade_date,
                codigo_lote=codigo_lote,
                syncStatus=data.get('syncStatus', 'Not Syncronized')
            )
            if data.get('syncStatusDate'):
                try:
                    movimento.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])
                except:
                    pass

            db.session.add(movimento)
            db.session.commit()
            return jsonify({'message': 'Movimento histórico criado com sucesso', 'id': movimento.id}), 201

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

            if any(k in data for k in ['tipo_movimento', 'quantidade', 'codigo_lote', 'data_validade', 'id_location', 'id_medicamento']):
                return jsonify({'message': 'Não é permitido editar campos que alteram o stock. Delete e crie um novo movimento.'}), 400

            if 'observacoes' in data:
                movimento.observacoes = data['observacoes']
            if 'data_movimento' in data:
                try:
                    movimento.data_movimento = datetime.fromisoformat(data['data_movimento'])
                except:
                    return jsonify({'message': 'data_movimento inválida'}), 400
            if 'registado_por' in data:
                try:
                    registado_por = int(data['registado_por'])
                except ValueError:
                    return jsonify({'message': 'registado_por deve ser inteiro'}), 400
                user = User.query.get(registado_por)
                if not user:
                    return jsonify({'message': 'User não encontrado'}), 404
                movimento.registado_por = registado_por
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

            stock = StockSemanal.query.filter_by(
                id_location=movimento.id_location,
                id_medicamento=movimento.id_medicamento
            ).first()
            if not stock:
                return jsonify({'message': 'Stock semanal associado não encontrado'}), 404

            lote = StockSemanalLote.query.filter_by(
                id_stock_semanal=stock.id,
                codigo_lote=movimento.codigo_lote,
                data_validade=movimento.data_validade
            ).first()
            if not lote:
                return jsonify({'message': 'Lote associado não encontrado'}), 404

            if movimento.tipo_movimento == 'Entrada':
                if lote.quantidade < movimento.quantidade:
                    return jsonify({'message': 'Inconsistência: quantidade do lote menor que a entrada a deletar'}), 400
                lote.quantidade -= movimento.quantidade
            elif movimento.tipo_movimento == 'Saída':
                lote.quantidade += movimento.quantidade
            elif movimento.tipo_movimento == 'Ajuste':
                return jsonify({'message': 'Deleção de ajuste não implementada'}), 400

            db.session.delete(movimento)
            db.session.commit()
            return jsonify({'message': 'Movimento histórico deletado e lote ajustado'}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete historico movimento ID {id}")
            return jsonify({'error': str(e)}), 500