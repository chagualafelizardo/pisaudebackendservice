from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from . import db

# Enum Python para SyncStatus
class SyncStatusEnum(PyEnum):
    NotSyncronized = "Not Syncronized"
    Syncronized = "Syncronized"
    Updated = "Updated"

class Formacao(db.Model):
    __tablename__ = 'formacao'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    inicio = db.Column(db.DateTime, nullable=False)
    duracao = db.Column(db.String(50), nullable=False)
    anoacademico = db.Column(db.String(50), nullable=False)
    despachoautorizacao = db.Column(db.String(200), nullable=False)
    
    # Relacionamento com Person
    person_id = db.Column(db.Integer, ForeignKey('person.id'), nullable=False)
    person = relationship('Person', backref='formacoes')

    # Relacionamento com Pais (instituição)
    pais_id = db.Column(db.Integer, ForeignKey('pais.id'), nullable=False)
    pais = relationship('Pais', backref='formacoes')

    # Relacionamento com TipoLicenca
    tipo_licenca_id = db.Column(db.Integer, ForeignKey('tipolicenca.id'), nullable=False)
    tipo_licenca = relationship('TipoLicenca', backref='formacoes')

    syncStatus = db.Column(SQLEnum(SyncStatusEnum), nullable=False, default=SyncStatusEnum.NotSyncronized)
    syncStatusDate = db.Column(db.DateTime, nullable=True)

    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Formacao {self.id} - {self.tipo_licenca.description} - {self.person.fullname} - {self.pais.description}>'
