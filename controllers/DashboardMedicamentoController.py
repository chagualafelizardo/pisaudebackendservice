import logging
from flask import jsonify, request
from models import db, Medicamento, Location, StockSemanal, StockSemanalLote, HistoricoMovimento
from datetime import datetime, timedelta
from sqlalchemy import func, desc

logger = logging.getLogger(__name__)

class DashboardMedicamentoController:

    @staticmethod
    def get_dashboard_data():
        try:
            # Capturar parâmetros de filtro
            id_location = request.args.get('id_location', type=int)
            data_inicio = request.args.get('data_inicio')
            data_fim = request.args.get('data_fim')

            # Converter datas se fornecidas
            dt_inicio = None
            dt_fim = None
            if data_inicio:
                try:
                    dt_inicio = datetime.fromisoformat(data_inicio)
                except:
                    return jsonify({'error': 'data_inicio inválida'}), 400
            if data_fim:
                try:
                    dt_fim = datetime.fromisoformat(data_fim)
                    # Ajustar para o final do dia
                    dt_fim = dt_fim.replace(hour=23, minute=59, second=59)
                except:
                    return jsonify({'error': 'data_fim inválida'}), 400

            # 1. Totais gerais (não filtrados)
            total_medicamentos = Medicamento.query.count()
            total_unidades = Location.query.count()

            # 2. Stocks e lotes (filtrados por localidade)
            stock_query = StockSemanal.query
            lote_query = StockSemanalLote.query
            if id_location:
                stock_query = stock_query.filter_by(id_location=id_location)
                # Para lotes, filtramos via join com StockSemanal
                lote_query = lote_query.join(StockSemanal).filter(StockSemanal.id_location == id_location)

            total_stocks = stock_query.count()
            total_lotes = lote_query.count()

            # 3. Movimentos (filtrados por localidade e datas)
            movimento_query = HistoricoMovimento.query
            if id_location:
                movimento_query = movimento_query.filter_by(id_location=id_location)
            if dt_inicio:
                movimento_query = movimento_query.filter(HistoricoMovimento.data_movimento >= dt_inicio)
            if dt_fim:
                movimento_query = movimento_query.filter(HistoricoMovimento.data_movimento <= dt_fim)

            total_movimentos = movimento_query.count()

            # 4. Lotes vencidos e próximos a vencer (filtrados por localidade)
            hoje = datetime.now().date()
            trinta_dias = hoje + timedelta(days=30)

            # Base para lotes com possível filtro de localidade
            lote_base = StockSemanalLote.query
            if id_location:
                lote_base = lote_base.join(StockSemanal).filter(StockSemanal.id_location == id_location)

            lotes_vencidos = lote_base.filter(StockSemanalLote.data_validade < hoje).count()
            lotes_proximos = lote_base.filter(
                StockSemanalLote.data_validade >= hoje,
                StockSemanalLote.data_validade <= trinta_dias
            ).count()

            # 5. Movimentos por tipo (com filtros)
            entradas = movimento_query.filter_by(tipo_movimento='Entrada').count()
            saidas = movimento_query.filter_by(tipo_movimento='Saída').count()
            ajustes = movimento_query.filter_by(tipo_movimento='Ajuste').count()

            # 6. Movimentos por mês (últimos 6 meses) - aplicando filtros
            seis_meses_atras = datetime.now() - timedelta(days=180)

            # Construir query base para movimentos por mês
            mes_query = db.session.query(
                func.to_char(HistoricoMovimento.data_movimento, 'YYYY-MM').label('mes'),
                func.count().label('total')
            ).filter(HistoricoMovimento.data_movimento >= seis_meses_atras)

            if id_location:
                mes_query = mes_query.filter(HistoricoMovimento.id_location == id_location)
            if dt_inicio and dt_inicio > seis_meses_atras:
                mes_query = mes_query.filter(HistoricoMovimento.data_movimento >= dt_inicio)
            if dt_fim:
                mes_query = mes_query.filter(HistoricoMovimento.data_movimento <= dt_fim)

            movimentos_por_mes = mes_query.group_by('mes').order_by('mes').all()

            meses = [m.mes for m in movimentos_por_mes]
            totais_meses = [m.total for m in movimentos_por_mes]

            # 7. Top 10 medicamentos por quantidade total em lotes (com filtro de localidade)
            top_med_query = db.session.query(
                Medicamento.nome_padronizado.label('medicamento'),
                func.sum(StockSemanalLote.quantidade).label('quantidade')
            ).join(StockSemanal, StockSemanal.id == StockSemanalLote.id_stock_semanal)\
             .join(Medicamento, Medicamento.id == StockSemanal.id_medicamento)

            if id_location:
                top_med_query = top_med_query.filter(StockSemanal.id_location == id_location)

            top_medicamentos = top_med_query.group_by(Medicamento.id, Medicamento.nome_padronizado)\
                                            .order_by(desc('quantidade'))\
                                            .limit(10).all()

            top_meds = [{'medicamento': m.medicamento, 'quantidade': m.quantidade} for m in top_medicamentos]

            # 8. Top 5 unidades com mais registos de stock (apenas se não houver filtro de localidade)
            if id_location:
                # Se filtrou por localidade, a lista só teria uma unidade, então talvez não faça sentido
                top_units = [{'unidade': Location.query.get(id_location).name, 'total': total_stocks}]
            else:
                top_unidades = db.session.query(
                    Location.name.label('unidade'),
                    func.count(StockSemanal.id).label('total')
                ).join(StockSemanal, StockSemanal.id_location == Location.id)\
                 .group_by(Location.id, Location.name)\
                 .order_by(desc('total'))\
                 .limit(5).all()
                top_units = [{'unidade': u.unidade, 'total': u.total} for u in top_unidades]

            # 9. Últimos 10 movimentos (com filtros)
            ultimos_movimentos = movimento_query.order_by(
                HistoricoMovimento.data_movimento.desc()
            ).limit(10).all()

            # Serializar
            ultimos = []
            for m in ultimos_movimentos:
                ultimos.append({
                    'data_movimento': m.data_movimento.isoformat() if m.data_movimento else None,
                    'location_nome': m.location.name if m.location else None,
                    'medicamento_nome': m.medicamento.nome_padronizado if m.medicamento else None,
                    'tipo_movimento': m.tipo_movimento,
                    'quantidade': m.quantidade,
                    'codigo_lote': m.codigo_lote,
                    'registado_por_nome': m.registado_por_user.fullname if m.registado_por_user else None
                })

            # Montar resposta
            response = {
                'totais': {
                    'medicamentos': total_medicamentos,
                    'unidades': total_unidades,
                    'stocks': total_stocks,
                    'lotes': total_lotes,
                    'movimentos': total_movimentos,
                    'lotes_vencidos': lotes_vencidos,
                    'lotes_proximos_validade': lotes_proximos
                },
                'movimentos_por_tipo': {
                    'entradas': entradas,
                    'saidas': saidas,
                    'ajustes': ajustes
                },
                'movimentos_por_mes': {
                    'meses': meses,
                    'totais': totais_meses
                },
                'top_medicamentos': top_meds,
                'top_unidades': top_units,
                'ultimos_movimentos': ultimos
            }

            return jsonify(response), 200

        except Exception as e:
            logger.exception("[DASHBOARD] Failed to fetch dashboard data.")
            return jsonify({'error': str(e)}), 500