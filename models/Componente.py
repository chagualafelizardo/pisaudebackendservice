from datetime import datetime
from . import db

class Componente(db.Model):
    __tablename__ = 'componente'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    componente_id = db.Column(db.String(150), nullable=False, unique=True)  # Ex: gestaoAlocacaoMenu
    descricao = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    createAt = db.Column(db.DateTime, default=db.func.now())
    updateAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # relacionamento com permissões de user
    user_componentes = db.relationship('UserComponente', back_populates='componente', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Componente {self.descricao}>'
