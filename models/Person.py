from . import db
from sqlalchemy.orm import relationship
from datetime import datetime

# Tabelas associativas existentes
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

# ----------------- MODELO DE DOCUMENTO (renomeado para PersonDocument) -----------------
class PersonDocument(db.Model):
    __tablename__ = 'person_document'   # pode manter 'document' ou mudar para 'person_document'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    doc_type = db.Column(db.String(50), nullable=False)          # BI, NUIT, NIM, CERTIFICATE, OTHER
    doc_name = db.Column(db.String(255), nullable=False)         # nome original do ficheiro
    file_data = db.Column(db.LargeBinary, nullable=True)         # conteúdo do ficheiro (binário)
    description = db.Column(db.Text, nullable=True)              # descrição opcional
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com Person (um-para-muitos)
    person = relationship('Person', back_populates='documents')

    def __repr__(self):
        return f'<PersonDocument {self.doc_name}>'

# ----------------- CLASSE PERSON ATUALIZADA -----------------
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

    # Relacionamento com Patents (muitos-para-muitos)
    patents = relationship('Patent', secondary=person_patent, back_populates='persons')

    # Relacionamento com Transferencias (muitos-para-muitos)
    transferencias = relationship('Transferencia', secondary=person_transferencia, back_populates='persons')

    # CORREÇÃO: agora referencia 'PersonDocument' em vez de 'Document'
    documents = relationship('PersonDocument', back_populates='person', cascade='all, delete-orphan')

    # Imagem do person (binário)
    image = db.Column(db.LargeBinary, nullable=True)

    # Campos de sincronização
    syncStatus = db.Column(db.String(50), nullable=False, default='Not Syncronized')
    syncStatusDate = db.Column(db.DateTime, nullable=True)

    # Timestamps
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Person {self.fullname}>'