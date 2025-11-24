from . import db
from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

# -------------------------
# Modelo: Armazem
# -------------------------
class Armazem(db.Model):
    __tablename__ = 'armazem'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # 🔹 Novo campo de observação (texto livre)
    observacao = db.Column(db.Text, nullable=True)

    # Relação com Provincia
    provincia_id = db.Column(db.Integer, ForeignKey('provincia.id'), nullable=False)
    provincia = relationship('Provincia', back_populates='armazens')

    # Relação com Itens
    itens = relationship('Item', back_populates='armazem', cascade="all, delete-orphan")

    # Campo de sincronização (simples string)
    syncStatus = db.Column(db.String(50), nullable=False, default='Not Syncronized')
    syncStatusDate = db.Column(db.DateTime, nullable=True)

    # Timestamps
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Armazem {self.nome}>'
