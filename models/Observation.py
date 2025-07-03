from datetime import datetime
from . import db  # Importa db do __init__.py

class Observation(db.Model):
    __tablename__ = 'observation'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nid = db.Column(db.String(100), nullable=False, unique=True)
    fullname = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    datainiciotarv = db.Column(db.DateTime, nullable=False)
    datalevantamento = db.Column(db.DateTime, nullable=False)
    dataproximolevantamento = db.Column(db.DateTime, nullable=False)
    dataconsulta = db.Column(db.DateTime, nullable=False)
    dataproximaconsulta = db.Column(db.DateTime, nullable=False)
    dataalocacao = db.Column(db.DateTime, nullable=False)
    dataenvio = db.Column(db.DateTime, nullable=False)
    smssendernumber = db.Column(db.String(100), nullable=False)
    smssuporternumber = db.Column(db.String(100), nullable=False)
    dataprimeiracv = db.Column(db.DateTime, nullable=False)
    valorprimeiracv = db.Column(db.Integer, nullable=False)
    dataultimacv = db.Column(db.DateTime, nullable=False)
    valorultimacv = db.Column(db.Integer, nullable=False)
    linhaterapeutica = db.Column(db.String(100), nullable=False)
    regime = db.Column(db.String(100), nullable=False)
    
    # Chaves estrangeiras (removido unique=True pois não faz sentido para FKs)
    stateId = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    textmessageId = db.Column(db.Integer, db.ForeignKey('textmessage.id'), nullable=False)
    grouptypeId = db.Column(db.Integer, db.ForeignKey('grouptype.id'), nullable=False)
    groupId = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    locationId = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    createAt = db.Column(db.DateTime, default=db.func.now())
    updateAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # Relacionamentos
    state = db.relationship('State', backref='observations')
    textmessage = db.relationship('Textmessage', backref='observations')
    grouptype = db.relationship('Grouptype', backref='observations')
    group = db.relationship('Group', backref='observations')
    location = db.relationship('Location', backref='observations')
    user = db.relationship('User', backref='observations')

    def __repr__(self):
        return f'<Observation {self.id}>'