from . import db
from datetime import datetime

class Distribuicao(db.Model):
    __tablename__ = 'distribuicao'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    armazem_id = db.Column(db.Integer, db.ForeignKey('armazem.id'), nullable=False)  # armazem provincial
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False) # unidade sanitária
    quantidade = db.Column(db.Integer, nullable=False)
    data_distribuicao = db.Column(db.DateTime, default=datetime.utcnow)
    observacao = db.Column(db.String(255), nullable=True)

    # 🔹 Novo campo para armazenar o nome do utilizador que adicionou a distribuição
    user = db.Column(db.String(150), nullable=True)

    # Relações opcionais
    item = db.relationship("Item", backref="distribuicoes")
    armazem = db.relationship("Armazem", backref="distribuicoes")
    location = db.relationship("Location", backref="distribuicoes")
