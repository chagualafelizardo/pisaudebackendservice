from models import db
from datetime import datetime

class ItemHistorico(db.Model):
    __tablename__ = 'item_historico'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    tipo_movimento = db.Column(db.String(50))  # 'entrada' ou 'saida'
    quantidade = db.Column(db.Integer)
    observacoes = db.Column(db.Text)
    data_movimento = db.Column(db.DateTime, default=datetime.utcnow)

    item = db.relationship('Item', backref=db.backref('historico', lazy=True))
