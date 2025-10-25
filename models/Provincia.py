from . import db
from sqlalchemy import Enum, Float, ForeignKey
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

# Enum para syncStatus
class SyncStatusEnum(enum.Enum):
    NotSyncronized = "Not Syncronized"
    Syncronized = "Syncronized"
    Updated = "Updated"

# -------------------------
# Modelo: Provincia
# -------------------------
class Provincia(db.Model):
    __tablename__ = 'provincia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    # Relação com Armazéns
    armazens = relationship('Armazem', back_populates='provincia', cascade="all, delete-orphan")

    # Campos de sincronização
    syncStatus = db.Column(Enum(SyncStatusEnum), nullable=False, default=SyncStatusEnum.NotSyncronized)
    syncStatusDate = db.Column(db.DateTime, nullable=True)

    # Timestamps
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Provincia {self.nome}>'
