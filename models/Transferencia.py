from . import db
from sqlalchemy import Column, Integer, Date, String, DateTime, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .Person import person_transferencia

# Enum para o campo de sincronização
class SyncStatusEnum(enum.Enum):
    NotSyncronized = "Not Syncronized"
    Syncronized = "Syncronized"
    Updated = "Updated"

class Transferencia(db.Model):
    __tablename__ = 'transferencia'

    id = Column(Integer, primary_key=True, autoincrement=True)

    # U.M. Origem (data e unidade)
    dataUmOrigem = Column(Date, nullable=True)
    unidadeMilitarOrigemId = Column(Integer, ForeignKey('location.id'), nullable=True)
    unidadeMilitarOrigem = relationship('Location', foreign_keys=[unidadeMilitarOrigemId], backref='transferencias_origem')

    # U.M. Atual (data e unidade)
    dataUmAtual = Column(Date, nullable=True)
    unidadeMilitarAtualId = Column(Integer, ForeignKey('location.id'), nullable=True)
    unidadeMilitarAtual = relationship('Location', foreign_keys=[unidadeMilitarAtualId], backref='transferencias_atual')

    observation = Column(String(255), nullable=True)

    # Relacionamento com Person
    persons = relationship('Person', secondary=person_transferencia, back_populates='transferencias')

    # Sincronização
    syncStatus = Column(SQLAlchemyEnum(SyncStatusEnum), nullable=False, default=SyncStatusEnum.NotSyncronized)
    syncStatusDate = Column(DateTime, nullable=True)

    # Timestamps
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Transferencia ID: {self.id}>"
