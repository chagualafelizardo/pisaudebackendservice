from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum, LargeBinary, DateTime, Float, Integer, String, Text, ForeignKey
from datetime import datetime

# ===============================================================
# 🔹 Tabela associativa — NotaEnvioItem (N Itens por Nota)
# ===============================================================
class NotaEnvioItem(db.Model):
    __tablename__ = 'nota_envio_item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nota_envio_id = db.Column(db.Integer, db.ForeignKey('nota_envio.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    quantidade_enviada = db.Column(db.Integer, nullable=False)

    # 🔹 Relacionamentos
    nota_envio = relationship('NotaEnvio', back_populates='itens')
    item = relationship('Item', backref=db.backref('nota_envio_itens', lazy=True))

    def __repr__(self):
        return f'<NotaEnvioItem nota={self.nota_envio_id}, item={self.item_id}, qtd={self.quantidade_enviada}>'

