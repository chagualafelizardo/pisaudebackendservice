from datetime import datetime
from . import db

class UserRole(db.Model):
    __tablename__ = 'userrole'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    roleId = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    createAt = db.Column(db.DateTime, default=db.func.now())
    updateAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    # Relacionamentos
    user = db.relationship('User', back_populates='user_roles')
    role = db.relationship('Role', back_populates='user_roles')

    def __repr__(self):
        return f'<UserRole {self.id}>'