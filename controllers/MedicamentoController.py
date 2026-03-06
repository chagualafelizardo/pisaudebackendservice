import logging
from flask import jsonify, request
from models import db, Medicamento
from datetime import datetime

# Configuração básica de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MedicamentoController:

    @staticmethod
    def get_all():
        logger.info("[GET ALL] Request received to fetch all medicamentos.")
        try:
            medicamentos = Medicamento.query.all()
            result = []
            for m in medicamentos:
                result.append({
                    'id': m.id,
                    'nome_padronizado': m.nome_padronizado,
                    'categoria': m.categoria,
                    'forma_farmaceutica': m.forma_farmaceutica,
                    'unidade_medida': m.unidade_medida,
                    'apresentacao': m.apresentacao,
                    'stock_minimo': m.stock_minimo,
                    'ativo': m.ativo,
                    'syncStatus': m.syncStatus,
                    'syncStatusDate': m.syncStatusDate.isoformat() if m.syncStatusDate else None,
                    'createAt': m.createAt.isoformat() if m.createAt else None,
                    'updateAt': m.updateAt.isoformat() if m.updateAt else None,
                })
            return jsonify(result), 200
        except Exception as e:
            logger.exception("[GET ALL] Failed to fetch medicamentos.")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        logger.info(f"[GET BY ID] Request received for medicamento ID {id}.")
        try:
            m = Medicamento.query.get(id)
            if not m:
                return jsonify({'message': 'Medicamento not found'}), 404
            result = {
                'id': m.id,
                'nome_padronizado': m.nome_padronizado,
                'categoria': m.categoria,
                'forma_farmaceutica': m.forma_farmaceutica,
                'unidade_medida': m.unidade_medida,
                'apresentacao': m.apresentacao,
                'stock_minimo': m.stock_minimo,
                'ativo': m.ativo,
                'syncStatus': m.syncStatus,
                'syncStatusDate': m.syncStatusDate.isoformat() if m.syncStatusDate else None,
                'createAt': m.createAt.isoformat() if m.createAt else None,
                'updateAt': m.updateAt.isoformat() if m.updateAt else None,
            }
            return jsonify(result), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch medicamento ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        logger.info("[CREATE] Request received to create new medicamento.")
        try:
            data = request.get_json(force=True)

            # Campos obrigatórios
            nome_padronizado = data.get('nome_padronizado')
            categoria = data.get('categoria')
            forma_farmaceutica = data.get('forma_farmaceutica')
            unidade_medida = data.get('unidade_medida')
            apresentacao = data.get('apresentacao')

            if not all([nome_padronizado, categoria, forma_farmaceutica, unidade_medida, apresentacao]):
                return jsonify({'message': 'Campos obrigatórios: nome_padronizado, categoria, forma_farmaceutica, unidade_medida, apresentacao'}), 400

            # Validação dos valores ENUM (opcional, o banco também rejeitaria)
            categorias_validas = ['TARV', 'PrEP', 'TB Sensível', 'TB-DR', 'Profilaxia', 'Testes Rápidos']
            if categoria not in categorias_validas:
                return jsonify({'message': f'Categoria inválida. Valores permitidos: {categorias_validas}'}), 400

            formas_validas = ['Comprimido', 'Suspensão', 'Kit', 'Frasco']
            if forma_farmaceutica not in formas_validas:
                return jsonify({'message': f'Forma farmacêutica inválida. Valores permitidos: {formas_validas}'}), 400

            unidades_validas = ['Comprimido', 'Frasco', 'Kit', 'ml']
            if unidade_medida not in unidades_validas:
                return jsonify({'message': f'Unidade de medida inválida. Valores permitidos: {unidades_validas}'}), 400

            # Verificar duplicidade (nome_padronizado + apresentacao)
            existing = Medicamento.query.filter_by(nome_padronizado=nome_padronizado, apresentacao=apresentacao).first()
            if existing:
                return jsonify({'message': 'Já existe um medicamento com este nome e apresentação.'}), 409

            # Campos opcionais com default
            stock_minimo = data.get('stock_minimo', 0)
            ativo = data.get('ativo', True)
            syncStatus = data.get('syncStatus', 'Not Syncronized')
            syncStatusDate = None
            if data.get('syncStatusDate'):
                try:
                    syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])
                except:
                    pass

            medicamento = Medicamento(
                nome_padronizado=nome_padronizado,
                categoria=categoria,
                forma_farmaceutica=forma_farmaceutica,
                unidade_medida=unidade_medida,
                apresentacao=apresentacao,
                stock_minimo=stock_minimo,
                ativo=ativo,
                syncStatus=syncStatus,
                syncStatusDate=syncStatusDate
            )

            db.session.add(medicamento)
            db.session.commit()
            return jsonify({
                'message': 'Medicamento criado com sucesso',
                'id': medicamento.id
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create medicamento.")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        logger.info(f"[UPDATE] Request received to update medicamento ID {id}.")
        try:
            m = Medicamento.query.get(id)
            if not m:
                return jsonify({'message': 'Medicamento not found'}), 404

            data = request.get_json(force=True)

            # Atualizar apenas campos fornecidos (PATCH implícito)
            nome_padronizado = data.get('nome_padronizado', m.nome_padronizado)
            categoria = data.get('categoria', m.categoria)
            forma_farmaceutica = data.get('forma_farmaceutica', m.forma_farmaceutica)
            unidade_medida = data.get('unidade_medida', m.unidade_medida)
            apresentacao = data.get('apresentacao', m.apresentacao)
            stock_minimo = data.get('stock_minimo', m.stock_minimo)
            ativo = data.get('ativo', m.ativo)
            syncStatus = data.get('syncStatus', m.syncStatus)
            syncStatusDate = m.syncStatusDate
            if data.get('syncStatusDate'):
                try:
                    syncStatusDate = datetime.fromisoformat(data['syncStatusDate'])
                except:
                    pass

            # Validação de campos obrigatórios (se não foram fornecidos, mantém os antigos)
            if not all([nome_padronizado, categoria, forma_farmaceutica, unidade_medida, apresentacao]):
                return jsonify({'message': 'Campos obrigatórios não podem ser vazios'}), 400

            # Validação ENUM
            categorias_validas = ['TARV', 'PrEP', 'TB Sensível', 'TB-DR', 'Profilaxia', 'Testes Rápidos']
            if categoria not in categorias_validas:
                return jsonify({'message': f'Categoria inválida. Valores permitidos: {categorias_validas}'}), 400

            formas_validas = ['Comprimido', 'Suspensão', 'Kit', 'Frasco']
            if forma_farmaceutica not in formas_validas:
                return jsonify({'message': f'Forma farmacêutica inválida. Valores permitidos: {formas_validas}'}), 400

            unidades_validas = ['Comprimido', 'Frasco', 'Kit', 'ml']
            if unidade_medida not in unidades_validas:
                return jsonify({'message': f'Unidade de medida inválida. Valores permitidos: {unidades_validas}'}), 400

            # Verificar duplicidade com outro registro (ignorando o próprio)
            existing = Medicamento.query.filter(
                Medicamento.nome_padronizado == nome_padronizado,
                Medicamento.apresentacao == apresentacao,
                Medicamento.id != id
            ).first()
            if existing:
                return jsonify({'message': 'Já existe outro medicamento com este nome e apresentação.'}), 409

            m.nome_padronizado = nome_padronizado
            m.categoria = categoria
            m.forma_farmaceutica = forma_farmaceutica
            m.unidade_medida = unidade_medida
            m.apresentacao = apresentacao
            m.stock_minimo = stock_minimo
            m.ativo = ativo
            m.syncStatus = syncStatus
            m.syncStatusDate = syncStatusDate
            m.updateAt = datetime.utcnow()

            db.session.commit()
            return jsonify({'message': 'Medicamento atualizado com sucesso', 'id': m.id}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update medicamento ID {id}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        logger.info(f"[DELETE] Request received to delete medicamento ID {id}.")
        try:
            m = Medicamento.query.get(id)
            if not m:
                return jsonify({'message': 'Medicamento not found'}), 404

            db.session.delete(m)
            db.session.commit()
            return jsonify({'message': 'Medicamento deletado com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete medicamento ID {id}")
            return jsonify({'error': str(e)}), 500