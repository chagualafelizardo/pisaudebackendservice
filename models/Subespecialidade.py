from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum, ForeignKey
import enum
from datetime import datetime
from models.Especialidade import Especialidade  # Certifique-se de que o caminho está correto

# Enum para syncStatus
class SyncStatusEnum(enum.Enum):
    NotSyncronized = "Not Syncronized"
    Syncronized = "Syncronized"
    Updated = "Updated"

class Subespecialidade(db.Model):
    __tablename__ = 'subespecialidade'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100), nullable=False, unique=True)

    # ForeignKey para Especialidade
    especialidadeId = db.Column(db.Integer, ForeignKey('especialidade.id'), nullable=False)
    
    # Relacionamento com Especialidade
    especialidade = relationship("Especialidade", backref="subespecialidades")

    # Campos de sincronização
    syncStatus = db.Column(Enum(SyncStatusEnum), nullable=False, default=SyncStatusEnum.NotSyncronized)
    syncStatusDate = db.Column(db.DateTime, nullable=True)

    # Timestamps
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Subespecialidade {self.description}>'
