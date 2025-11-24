from . import db
from sqlalchemy import DateTime  # ⬅️ IMPORT NECESSÁRIO
from datetime import datetime

class ItemsSolicitados(db.Model):
    __tablename__ = 'items_solicitados'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    # 🔹 Novo campo — data da solicitação
    data_solicitacao = db.Column(DateTime, default=db.func.current_timestamp())

    # 🔹 Timestamps
    createAt = db.Column(DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"<ItemsSolicitados {self.nome} ({self.quantidade})>"
