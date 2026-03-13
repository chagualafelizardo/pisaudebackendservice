from . import db
from sqlalchemy import Enum, Date
from datetime import datetime

class HistoricoMovimento(db.Model):
    __tablename__ = 'historico_movimento'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    id_medicamento = db.Column(db.Integer, db.ForeignKey('medicamento.id'), nullable=False)
    tipo_movimento = db.Column(Enum('Entrada', 'Saída', 'Ajuste', name='tipo_movimento_enum'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_movimento = db.Column(db.DateTime, default=db.func.current_timestamp())
    registado_por = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    observacoes = db.Column(db.Text, nullable=True)

    # NOVOS CAMPOS
    data_validade = db.Column(Date, nullable=True)
    codigo_lote = db.Column(db.String(100), nullable=True)

    # Campos de controlo
    syncStatus = db.Column(db.String(50), nullable=False, default='Not Syncronized')
    syncStatusDate = db.Column(db.DateTime, nullable=True)
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relacionamentos
    location = db.relationship('Location', backref='historico_movimentos')
    medicamento = db.relationship('Medicamento', backref='historico_movimentos')
    registado_por_user = db.relationship('User', foreign_keys=[registado_por])

    def __repr__(self):
        return f'<HistoricoMovimento {self.id} - {self.tipo_movimento} - Qtd: {self.quantidade}>'