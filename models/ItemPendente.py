from . import db
from datetime import datetime

class ItemPendente(db.Model):
    __tablename__ = 'item_pendente'

    id = db.Column(db.Integer, primary_key=True)
    nome_item = db.Column(db.String(120), nullable=False)
    quantidade_esperada = db.Column(db.Integer, nullable=False)
    prioridade = db.Column(db.String(50), nullable=True)
    data_esperada_entrega = db.Column(db.DateTime, nullable=True)
    categoria = db.Column(db.String(100), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    fornecedor_origem = db.Column(db.String(120), nullable=True)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ItemPendente {self.nome_item}>"
