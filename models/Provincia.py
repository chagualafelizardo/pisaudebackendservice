from . import db
from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

# -------------------------
# Modelo: Provincia
# -------------------------
class Provincia(db.Model):
    __tablename__ = 'provincia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    # Relação com Armazéns
    armazens = relationship('Armazem', back_populates='provincia', cascade="all, delete-orphan")

    # Campo simples de sincronização (string)
    syncStatus = db.Column(db.String(50), nullable=False, default='Not Syncronized')
    syncStatusDate = db.Column(db.DateTime, nullable=True)

    # Timestamps
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Provincia {self.nome}>'
