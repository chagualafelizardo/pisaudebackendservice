from sqlalchemy import UniqueConstraint
from datetime import datetime
from . import db

# ======================================================
# Tabela: historico_movimento
# ======================================================
class HistoricoMovimento(db.Model):
    __tablename__ = 'historico_movimento'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_unidade_sanitaria = db.Column(db.Integer, db.ForeignKey('unidade_sanitaria.id'), nullable=False)
    id_medicamento = db.Column(db.Integer, db.ForeignKey('medicamento.id'), nullable=False)
    tipo_movimento = db.Column(SAEnum('Entrada', 'Saída', 'Ajuste', name='tipo_movimento_enum'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_movimento = db.Column(db.DateTime, default=db.func.current_timestamp())
    observacao = db.Column(db.Text, nullable=True)
    registado_por = db.Column(db.Integer, db.ForeignKey('utilizador.id'), nullable=False)
    data_validade = db.Column(db.Date, nullable=True)  # opcional, para rastreabilidade do lote
    codigo_lote = db.Column(db.String(100), nullable=True)

    # Campos de controlo
    syncStatus = db.Column(db.String(50), nullable=False, default='Not Syncronized')
    syncStatusDate = db.Column(db.DateTime, nullable=True)
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relacionamentos
    unidade_sanitaria = db.relationship('UnidadeSanitaria', backref='movimentos')
    medicamento = db.relationship('Medicamento', backref='movimentos')
    registado_por_user = db.relationship('Utilizador', foreign_keys=[registado_por])

    def __repr__(self):
        return f'<HistoricoMovimento {self.id} - {self.tipo_movimento} - Qtd: {self.quantidade}>'