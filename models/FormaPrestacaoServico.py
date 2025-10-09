from datetime import datetime
from . import db

class FormaPrestacaoServico(db.Model):
    __tablename__ = 'formaprestacaoservico'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100), nullable=False, unique=True)

    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<FormaPrestacaoServico {self.description}>'
