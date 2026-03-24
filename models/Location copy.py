from datetime import datetime
from sqlalchemy import LargeBinary, Text
from . import db

# Tabela associativa para Location <-> Resource com campos extras
location_resource = db.Table('location_resource',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('location_id', db.Integer, db.ForeignKey('location.id'), nullable=False),
    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'), nullable=False),
    db.Column('quantity', db.Integer, nullable=False, default=0),
    db.Column('status', db.String(50), nullable=False, default='Available'),
    db.Column('condition', db.String(50), nullable=True, default='Good'),
    db.Column('name', db.String(100), nullable=False),
    db.Column('description', db.String(1000), nullable=True),
    db.Column('recebidopor', db.String(100), nullable=True),
    
    # NOVOS CAMPOS
    db.Column('asset_code', db.String(100), nullable=True),
    db.Column('budget_to_location', db.String(100), nullable=True),
    
    # Imagem principal: binário + tipo MIME
    db.Column('imagem_principal', LargeBinary, nullable=True),
    db.Column('imagem_principal_mime', db.String(50), nullable=True),
    
    # Imagens adicionais: armazenar JSON (array de data URLs)
    db.Column('imagens', db.Text, nullable=True),
    
    # PDF: binário (sempre application/pdf)
    db.Column('anexospdf', LargeBinary, nullable=True),
    
    db.Column('datarecepcao', db.Date, nullable=True),
    db.Column('createAt', db.DateTime, default=datetime.utcnow),
    db.Column('updateAt', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
)

class Location(db.Model):
    __tablename__ = 'location'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False, unique=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    responsavel = db.Column(
        db.String(20), 
        nullable=False, 
        default='DOD',
        server_default='DOD'
    )
    observacoes = db.Column(db.Text, nullable=True)
    
    # Relacionamentos
    observations = db.relationship('Observation', back_populates='location')
    users = db.relationship('User', back_populates='location')

    resources = db.relationship(
        'Resource',
        secondary=location_resource,
        backref=db.backref('locations', lazy='dynamic'),
        lazy='subquery'
    )

    medicamentos = db.relationship('MedicamentoLocation', backref='location', lazy='dynamic', cascade='all, delete-orphan')

    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Location {self.name}>'

    @staticmethod
    def get_responsaveis_permitidos():
        return ['DOD', 'Jhpiego', 'RISE']

    def validar_responsavel(self):
        return self.responsavel in self.get_responsaveis_permitidos()