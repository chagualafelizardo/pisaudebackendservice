# models/ItemLocationNecessidade.py
from models import db
from datetime import datetime

class ItemLocationNecessidade(db.Model):
    __tablename__ = 'item_location_necessidade'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(255))
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # 🔹 Novo campo para armazenar o nome do usuário que adicionou a necessidade
    user = db.Column(db.String(150), nullable=True)

    # relacionamentos
    item = db.relationship('Item', backref=db.backref('item_location_necessidades', lazy=True))
    location = db.relationship('Location', backref=db.backref('item_location_necessidades', lazy=True))
