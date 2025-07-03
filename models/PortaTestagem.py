# models/portatestagem.py
from datetime import datetime
from . import db

class PortaTestagem(db.Model):
    __tablename__ = 'portatestagem'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100), nullable=False, unique=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<PortaTestagem {self.description}>'
