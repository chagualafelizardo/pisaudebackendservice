from . import db
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Participante(db.Model):
    __tablename__ = 'participante'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    nome = db.Column(String(150), nullable=False)
    contacto = db.Column(String(50), nullable=True)
    presente = db.Column(String(10), nullable=False, default='no')  # valores esperados: 'yes' ou 'no'

    # 🔹 Relação com Formação
    formacao_id = db.Column(Integer, ForeignKey('formacao_item.id'), nullable=False)
    formacao = relationship('FormacaoItem', back_populates='participantes')

    # 🔹 Campos de sincronização e data
    syncStatus = db.Column(String(50), nullable=False, default='NotSyncronized')
    syncStatusDate = db.Column(DateTime, nullable=True)

    # 🔹 Timestamps
    createAt = db.Column(DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Participante {self.nome}>'
