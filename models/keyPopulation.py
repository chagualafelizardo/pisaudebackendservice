from datetime import datetime
from . import db

class KeyPopulation(db.Model):
    __tablename__ = 'keypopulation'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100), nullable=False, unique=True)
    
    createAt = db.Column(db.DateTime, default=datetime.utcnow)
    updateAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<KeyPopulation {self.description}>'
