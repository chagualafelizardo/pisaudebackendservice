from . import db
from sqlalchemy import Enum
import enum
from datetime import datetime

# Enum para syncStatus
class SyncStatusEnum(enum.Enum):
    NotSyncronized = "Not Syncronized"
    Syncronized = "Syncronized"
    Updated = "Updated"
    
class Observation(db.Model):
    __tablename__ = 'observation'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nid = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(500), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    age = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(1000), nullable=False)
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

    # Novo campo para flat status
    status = db.Column(db.String(100), nullable=False)
    
    # Campos de sincronização
    syncStatus = db.Column(Enum(SyncStatusEnum), nullable=False, default=SyncStatusEnum.NotSyncronized)
    syncStatusDate = db.Column(db.DateTime, nullable=True)
    
    # NOVO CAMPO: Status do SMS (apenas string)
    smsStatus = db.Column(db.String(50), nullable=True, default=None)

    # Chaves estrangeiras
    stateId = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    textmessageId = db.Column(db.Integer, db.ForeignKey('textmessage.id'), nullable=False)
    grouptypeId = db.Column(db.Integer, db.ForeignKey('grouptype.id'), nullable=False)
    groupId = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    locationId = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    createAt = db.Column(db.DateTime, default=db.func.now())
    updateAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # Relacionamentos
    state = db.relationship('State', backref='state_observations')
    textmessage = db.relationship('Textmessage', backref='textmessage_observations')
    grouptype = db.relationship('Grouptype', backref='grouptype_observations')
    group = db.relationship('Group', backref='group_observations')
    location = db.relationship('Location', backref='location_observations')
    user = db.relationship('User', backref='user_observations')

    def __repr__(self):
        return f'<Observation {self.id} nid={self.nid}>'