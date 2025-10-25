from models import db, User, Componente
from datetime import datetime

class UserComponente(db.Model):
    __tablename__ = 'user_componente'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    componente_id = db.Column(db.Integer, db.ForeignKey('componente.id'), nullable=False)
    can_access = db.Column(db.Boolean, default=True)

    createAt = db.Column(db.DateTime, default=db.func.now())
    updateAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    user = db.relationship('User', back_populates='user_componentes')
    componente = db.relationship('Componente', back_populates='user_componentes')

    def __repr__(self):
        return f'<UserComponente user={self.user_id} componente={self.componente_id}>'
