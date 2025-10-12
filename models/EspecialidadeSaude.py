from . import db
from sqlalchemy import Enum
import enum
from datetime import datetime

# Enum para syncStatus
class SyncStatusEnum(enum.Enum):
    NotSyncronized = "Not Syncronized"
    Syncronized = "Syncronized"
    Updated = "Updated"

class EspecialidadeSaude(db.Model):
    __tablename__ = 'especialidadesaude'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    curso = db.Column(db.String(100), nullable=False)
    anoFormacao = db.Column(db.String(10), nullable=True)
    instituicaoFormacao = db.Column(db.String(150), nullable=True)
    observation = db.Column(db.Text, nullable=True)

    # Campos de sincronização com Enum
    syncStatus = db.Column(Enum(SyncStatusEnum), nullable=False, default=SyncStatusEnum.NotSyncronized)
    syncStatusDate = db.Column(db.DateTime, nullable=True)

    # Timestamps
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<EspecialidadeSaude {self.curso}>'
