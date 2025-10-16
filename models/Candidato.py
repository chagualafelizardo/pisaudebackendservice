from . import db
from sqlalchemy.orm import relationship
from datetime import datetime


class CandidatoEdicao(db.Model):
    __tablename__ = 'candidato_edicao'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    candidatoId = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=False)
    candidato = relationship('Candidato', backref='edicoes')

    numeroedicao = db.Column(db.String(50))
    dataedicao = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Edicao {self.numeroedicao} - {self.dataedicao}>'


class Candidato(db.Model):
    __tablename__ = 'candidato'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    personId = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    person = relationship('Person', backref='candidatos')

    curso = db.Column(db.String(150), nullable=False)
    instituicao = db.Column(db.String(150), nullable=True)

    # Agora syncStatus é apenas uma string simples
    syncStatus = db.Column(db.String(50), nullable=False, default="Not Syncronized")
    syncStatusDate = db.Column(db.DateTime, nullable=True)

    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Candidato {self.person.fullname if self.person else "N/A"} - {self.curso}>'
