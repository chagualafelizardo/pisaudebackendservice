from datetime import datetime
from . import db

class Textmessage(db.Model):
    __tablename__ = 'textmessage'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    messagetext = db.Column(db.String(100), nullable=False, unique=True)
    
    # Relacionamento com Observation
    observations = db.relationship('Observation', back_populates='textmessage')
    
    createAt = db.Column(db.DateTime, default=db.func.now())
    updateAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<Textmessage {self.messagetext}>'