from datetime import datetime
from . import db

# Tabela associativa para Subunidade <-> Resource com quantidade
subunidade_resource = db.Table('subunidade_resource',
    db.Column('subunidade_id', db.Integer, db.ForeignKey('subunidade.id'), primary_key=True),
    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False, default=0)
)

class Subunidade(db.Model):
    __tablename__ = 'subunidade'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False, unique=True)

    # Novas colunas para localização
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Relacionamentos
    # observations = db.relationship('Observation', back_populates='subunidade')
    # users = db.relationship('User', back_populates='subunidade')

    resources = db.relationship(
        'Resource',
        secondary=subunidade_resource,
        backref=db.backref('subunidades', lazy='dynamic'),
        lazy='subquery'
    )

    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Subunidade {self.name}>'
