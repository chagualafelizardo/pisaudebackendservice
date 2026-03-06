import logging
from flask import jsonify, request
from models import db, StockSemanalLote, StockSemanal
from datetime import datetime

# Configuração básica de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class StockSemanalLoteController:

    @staticmethod
    def get_all():
        """
        Retorna todos os lotes de stock semanal.
        Suporta filtro opcional por id_stock_semanal via query string.
        """
        logger.info("[GET ALL] Request received to fetch all stock semanal lotes.")
        try:
            query = StockSemanalLote.query

            # Filtro opcional por stock_semanal
            id_stock_semanal = request.args.get('id_stock_semanal', type=int)
            if id_stock_semanal:
                query = query.filter_by(id_stock_semanal=id_stock_semanal)

            lotes = query.all()
            result = []
            for l in lotes:
                result.append({
                    'id': l.id,
                    'id_stock_semanal': l.id_stock_semanal,
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
            logger.exception("[GET ALL] Failed to fetch stock semanal lotes.")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        logger.info(f"[GET BY ID] Request received for stock semanal lote ID {id}.")
        try:
            l = StockSemanalLote.query.get(id)
            if not l:
                return jsonify({'message': 'Lote de stock semanal não encontrado'}), 404
            result = {
                'id': l.id,
                'id_stock_semanal': l.id_stock_semanal,
                'quantidade': l.quantidade,
                'data_validade': l.data_validade.isoformat() if l.data_validade else None,
                'codigo_lote': l.codigo_lote,
                'observacoes': l.observacoes,
                'syncStatus': l.syncStatus,
                'syncStatusDate': l.syncStatusDate.isoformat() if l.syncStatusDate else None,
                'createAt': l.createAt.isoformat() if l.createAt else None,
                'updateAt': l.updateAt.isoformat() if l.updateAt else None,
            }
            return jsonify(result), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch stock semanal lote ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        logger.info("[CREATE] Request received to create new stock semanal lote.")
        try:
            data = request.get_json(force=True)

            # Campos obrigatórios
            id_stock_semanal = data.get('id_stock_semanal')
            quantidade = data.get('quantidade')
            data_validade = data.get('data_validade')

            if not all([id_stock_semanal, quantidade, data_validade]):
                return jsonify({'message': 'Campos obrigatórios: id_stock_semanal, quantidade, data_validade'}), 400

            # Validar stock_semanal existente
            stock = StockSemanal.query.get(id_stock_semanal)
            if not stock:
                return jsonify({'message': 'Registo de stock semanal não encontrado'}), 404

            # Validar quantidade positiva
            if quantidade <= 0:
                return jsonify({'message': 'A quantidade deve ser maior que zero'}), 400

            # Converter data_validade
            try:
                data_validade_date = datetime.fromisoformat(data_validade).date()
            except Exception:
                return jsonify({'message': f'Data de validade inválida: {data_validade}'}), 400

            # Criar o lote
            lote = StockSemanalLote(
                id_stock_semanal=id_stock_semanal,
                quantidade=quantidade,
                data_validade=data_validade_date,
                codigo_lote=data.get('codigo_lote'),
                observacoes=data.get('observacoes'),
                syncStatus=data.get('syncStatus', 'Not Syncronized')
            )
            if data.get('syncStatusDate'):
                try:
                    lote.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])
                except:
                    pass

            db.session.add(lote)
            db.session.commit()

            return jsonify({
                'message': 'Lote de stock semanal criado com sucesso',
                'id': lote.id
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create stock semanal lote.")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        logger.info(f"[UPDATE] Request received to update stock semanal lote ID {id}.")
        try:
            lote = StockSemanalLote.query.get(id)
            if not lote:
                return jsonify({'message': 'Lote de stock semanal não encontrado'}), 404

            data = request.get_json(force=True)

            # Atualizar campos fornecidos
            if 'id_stock_semanal' in data:
                id_stock_semanal = data['id_stock_semanal']
                stock = StockSemanal.query.get(id_stock_semanal)
                if not stock:
                    return jsonify({'message': 'Registo de stock semanal não encontrado'}), 404
                lote.id_stock_semanal = id_stock_semanal

            if 'quantidade' in data:
                quantidade = data['quantidade']
                if quantidade <= 0:
                    return jsonify({'message': 'A quantidade deve ser maior que zero'}), 400
                lote.quantidade = quantidade

            if 'data_validade' in data:
                try:
                    lote.data_validade = datetime.fromisoformat(data['data_validade']).date()
                except Exception:
                    return jsonify({'message': f'Data de validade inválida: {data["data_validade"]}'}), 400

            if 'codigo_lote' in data:
                lote.codigo_lote = data['codigo_lote']

            if 'observacoes' in data:
                lote.observacoes = data['observacoes']

            if 'syncStatus' in data:
                lote.syncStatus = data['syncStatus']

            if 'syncStatusDate' in data:
                try:
                    lote.syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])
                except:
                    pass

            lote.updateAt = datetime.utcnow()
            db.session.commit()
            return jsonify({'message': 'Lote de stock semanal atualizado com sucesso', 'id': lote.id}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update stock semanal lote ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        logger.info(f"[DELETE] Request received to delete stock semanal lote ID {id}.")
        try:
            lote = StockSemanalLote.query.get(id)
            if not lote:
                return jsonify({'message': 'Lote de stock semanal não encontrado'}), 404

            db.session.delete(lote)
            db.session.commit()
            return jsonify({'message': 'Lote de stock semanal deletado com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete stock semanal lote ID {id}")
            return jsonify({'error': str(e)}), 500