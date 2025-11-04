from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum, LargeBinary, DateTime, Float, Integer, String, Text, ForeignKey
from datetime import datetime
import enum


# 🔹 Enum para status de sincronização (igual ao usado no Item)
class SyncStatusEnum(enum.Enum):
    NotSyncronized = "Not Syncronized"
    Syncronized = "Syncronized"
    Updated = "Updated"


# ===============================================================
# 🔹 Modelo principal — NotaEnvio
# ===============================================================
class NotaEnvio(db.Model):
    __tablename__ = 'nota_envio'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_item_id = db.Column(db.Integer, db.ForeignKey('tipo_item.id'), nullable=False)
    tipo_item = relationship('TipoItem', back_populates='notas_envio')

    numero_nota = db.Column(db.String(100), nullable=False, unique=True)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    origem = db.Column(db.String(150), nullable=False)
    destino = db.Column(db.String(150), nullable=False)
    observacoes = db.Column(Text, nullable=True)

    itens = relationship('NotaEnvioItem', back_populates='nota_envio', cascade="all, delete-orphan")
    documentos = relationship('NotaEnvioDocument', back_populates='nota_envio', cascade="all, delete-orphan")

    syncStatus = db.Column(Enum(SyncStatusEnum), nullable=False, default=SyncStatusEnum.NotSyncronized)
    syncStatusDate = db.Column(db.DateTime, nullable=True)

    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<NotaEnvio {self.numero_nota}>'

