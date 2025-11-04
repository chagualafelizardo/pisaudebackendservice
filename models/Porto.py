from . import db
from sqlalchemy import Float, ForeignKey
from datetime import datetime

class Porto(db.Model):
    __tablename__ = 'porto'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Relação simples com Provincia via ForeignKey, sem relationship
    provincia_id = db.Column(db.Integer, ForeignKey('provincia.id'), nullable=False)

    # Campos de sincronização
    syncStatus = db.Column(db.String(50), nullable=False, default='Not Syncronized')
    syncStatusDate = db.Column(db.DateTime, nullable=True)

    # Timestamps
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Porto {self.nome}>'
