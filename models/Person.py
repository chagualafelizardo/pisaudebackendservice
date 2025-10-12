from . import db
from sqlalchemy.orm import relationship
from datetime import datetime

# Tabela associativa Person <-> Patent
person_patent = db.Table(
    'person_patent',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
    db.Column('patent_id', db.Integer, db.ForeignKey('patent.id'), primary_key=True)
)

person_transferencia = db.Table(
    'person_transferencia',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
    db.Column('transferencia_id', db.Integer, db.ForeignKey('transferencia.id'), primary_key=True)
)

class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nim = db.Column(db.String(50), nullable=True)
    nuit = db.Column(db.String(50), nullable=True)
    fullname = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    dateofbirth = db.Column(db.Date, nullable=True)
    incorporationdata = db.Column(db.Date, nullable=True)

    # Relacionamento com Service Form
    forma_prestacao_servico_id = db.Column(db.Integer, db.ForeignKey('formaprestacaoservico.id'), nullable=True)
    forma_prestacao_servico = relationship('FormaPrestacaoServico', backref='persons')

    # Relacionamento com Patents
    patents = relationship('Patent', secondary=person_patent, back_populates='persons')

    # Relacionamento com transferencias
    transferencias = relationship('Transferencia', secondary=person_transferencia, back_populates='persons')

    # Imagem do person
    image = db.Column(db.LargeBinary, nullable=True)

    # Campos de sincronização como string
    syncStatus = db.Column(db.String(50), nullable=False, default='Not Syncronized')
    syncStatusDate = db.Column(db.DateTime, nullable=True)

    # Timestamps
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Person {self.fullname}>'
