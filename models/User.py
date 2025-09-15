from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(500), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    profile = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    locationId = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    
    # Relacionamentos - CORRIGIDO: user_roles (com underscore)
    location = db.relationship('Location', back_populates='users')
    observations = db.relationship('Observation', back_populates='user')
    user_roles = db.relationship('UserRole', back_populates='user', cascade='all, delete-orphan')  # ← CORRIGIDO
    
    createAt = db.Column(db.DateTime, default=db.func.now())
    updateAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<User {self.fullname}>'