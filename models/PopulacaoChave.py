from datetime import datetime
from . import db

class PopulacaoChave(db.Model):
    __tablename__ = 'populacaochave'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(100), nullable=False, unique=True)
    
    # Relacionamento com DailyRecord
    daily_records = db.relationship('DailyRecord', backref='populacao_chave')
    
    createAt = db.Column(db.DateTime, default=datetime.utcnow)
    updateAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<PopulacaoChave {self.descricao}>'