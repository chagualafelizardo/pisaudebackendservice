from sqlalchemy import UniqueConstraint
from datetime import datetime
from . import db


# ======================================================
# Tabela: stock_semanal_lote (detalhe)
# ======================================================
class StockSemanalLote(db.Model):
    __tablename__ = 'stock_semanal_lote'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_stock_semanal = db.Column(db.Integer, db.ForeignKey('stock_semanal.id', ondelete='CASCADE'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_validade = db.Column(db.Date, nullable=False)
    codigo_lote = db.Column(db.String(100), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    # Campos de controlo
    syncStatus = db.Column(db.String(50), nullable=False, default='Not Syncronized')
    syncStatusDate = db.Column(db.DateTime, nullable=True)
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<StockSemanalLote {self.id} - Lote: {self.codigo_lote} - Qtd: {self.quantidade}>'

