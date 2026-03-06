from sqlalchemy import UniqueConstraint
from datetime import datetime
from . import db

# ======================================================
# Tabela: stock_semanal (cabeçalho)
# ======================================================
class StockSemanal(db.Model):
    __tablename__ = 'stock_semanal'
    __table_args__ = (
        UniqueConstraint('id_unidade_sanitaria', 'id_medicamento', 'semana', 'ano',
                         name='uq_stock_semanal_unidade_medicamento_semana_ano'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_unidade_sanitaria = db.Column(db.Integer, db.ForeignKey('unidade_sanitaria.id'), nullable=False)
    id_medicamento = db.Column(db.Integer, db.ForeignKey('medicamento.id'), nullable=False)
    semana = db.Column(db.Integer, nullable=False)  # 1 a 53
    ano = db.Column(db.Integer, nullable=False)
    data_registo = db.Column(db.DateTime, default=db.func.current_timestamp())
    registado_por = db.Column(db.Integer, db.ForeignKey('utilizador.id'), nullable=False)
    observacoes = db.Column(db.Text, nullable=True)

    # Campos de controlo
    syncStatus = db.Column(db.String(50), nullable=False, default='Not Syncronized')
    syncStatusDate = db.Column(db.DateTime, nullable=True)
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relacionamentos
    unidade_sanitaria = db.relationship('UnidadeSanitaria', backref='stocks_semanais')
    medicamento = db.relationship('Medicamento', backref='stocks_semanais')
    registado_por_user = db.relationship('Utilizador', foreign_keys=[registado_por])
    lotes = db.relationship('StockSemanalLote', backref='stock_semanal', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<StockSemanal {self.id} - US: {self.id_unidade_sanitaria} - Med: {self.id_medicamento} - Semana {self.semana}/{self.ano}>'

