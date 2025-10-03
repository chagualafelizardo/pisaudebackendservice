from datetime import datetime
from . import db

class Location(db.Model):
    __tablename__ = 'location'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False, unique=True)
    
    # Relacionamentos
    observations = db.relationship('Observation', back_populates='location')
    users = db.relationship('User', back_populates='location')
    
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Location {self.name}>'