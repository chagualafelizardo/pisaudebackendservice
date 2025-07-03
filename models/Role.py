from datetime import datetime
from . import db

class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descriton = db.Column(db.String(100), nullable=False, unique=True)
    
    # Relacionamento com UserRole
    user_roles = db.relationship('UserRole', back_populates='role', cascade='all, delete-orphan')
    
    createAt = db.Column(db.DateTime, default=db.func.now())
    updateAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<Role {self.id}>'