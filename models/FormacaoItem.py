from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from datetime import datetime


class FormacaoItem(db.Model):
    __tablename__ = 'formacao_item'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    nome_formacao = db.Column(String(150), nullable=False)
    data_formacao = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    observacao = db.Column(Text, nullable=True)

    # 🔹 Relação com os participantes
    participantes = relationship('Participante', back_populates='formacao', cascade="all, delete-orphan")

    # 🔹 Campos de utilizadores e sincronização (seguindo o padrão dos outros modelos)
    user = db.Column(String(150), nullable=True)
    syncStatus = db.Column(String(50), nullable=False, default='NotSyncronized')
    syncStatusDate = db.Column(DateTime, nullable=True)

    # 🔹 Timestamps
    createAt = db.Column(DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<FormacaoItem {self.nome_formacao}>'
