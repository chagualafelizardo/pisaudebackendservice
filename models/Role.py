from datetime import datetime
from . import db

class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100), nullable=False, unique=True)

    # Permissões
    can_create = db.Column(db.Boolean, default=False)
    can_read = db.Column(db.Boolean, default=True)
    can_update = db.Column(db.Boolean, default=False)
    can_delete = db.Column(db.Boolean, default=False)
    
    user_roles = db.relationship('UserRole', back_populates='role', cascade='all, delete-orphan')
    
    createAt = db.Column(db.DateTime, default=db.func.now())
    updateAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'can_create': self.can_create,
            'can_read': self.can_read,
            'can_update': self.can_update,
            'can_delete': self.can_delete,
            'createAt': self.createAt,
            'updateAt': self.updateAt
        }

    def __repr__(self):
        return f'<Role {self.description}>'
