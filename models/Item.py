from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum
from datetime import datetime
import enum

# Enum para syncStatus
class SyncStatusEnum(enum.Enum):
    NotSyncronized = "Not Syncronized"
    Syncronized = "Syncronized"
    Updated = "Updated"


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(50), nullable=False, unique=True)
    designacao = db.Column(db.String(150), nullable=False)

    # Imagem do item (armazenada como binário)
    imagem = db.Column(db.LargeBinary, nullable=True)

    # Relação com Armazém
    armazem_id = db.Column(db.Integer, db.ForeignKey('armazem.id'), nullable=False)
    armazem = relationship('Armazem', back_populates='itens')

    # Campos de sincronização (usando Enum)
    syncStatus = db.Column(Enum(SyncStatusEnum), nullable=False, default=SyncStatusEnum.NotSyncronized)
    syncStatusDate = db.Column(db.DateTime, nullable=True)

    # Timestamps
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __repr__(self):
        return f'<Item {self.designacao}>'
