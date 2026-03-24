from datetime import datetime
from sqlalchemy import LargeBinary, Text, Float, ForeignKey, Date, String, Integer, Column
from . import db

# Tabela associativa para Location <-> Resource com campos extras
location_resource = db.Table('location_resource',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('location_id', db.Integer, db.ForeignKey('location.id'), nullable=False),
    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'), nullable=False),
    
    # Campos já existentes
    db.Column('quantity', db.Integer, nullable=False, default=0),
    db.Column('status', db.String(50), nullable=False, default='Available'),
    db.Column('condition', db.String(50), nullable=True, default='Good'),
    db.Column('name', db.String(100), nullable=False),
    db.Column('description', db.String(1000), nullable=True),
    db.Column('recebidopor', db.String(100), nullable=True),
    
    # Campos anteriores (Asset Code, Budget, Imagens)
    db.Column('asset_code', db.String(100), nullable=True),
    db.Column('budget_to_location', db.String(100), nullable=True),
    db.Column('imagem_principal', LargeBinary, nullable=True),
    db.Column('imagem_principal_mime', db.String(50), nullable=True),
    db.Column('imagens', db.Text, nullable=True),
    db.Column('anexospdf', LargeBinary, nullable=True),
    db.Column('datarecepcao', db.Date, nullable=True),
    
    # NOVOS CAMPOS SOLICITADOS
    db.Column('serial_number', db.String(100), nullable=True),          # Serial Number
    db.Column('item_number', db.String(100), nullable=True),           # Item Number
    db.Column('owner', db.String(100), nullable=True),                 # Owner
    db.Column('comments', db.Text, nullable=True),                     # Comments
    db.Column('purchase_date', db.Date, nullable=True),                # Purchase Date
    db.Column('purchase_cost', db.Numeric(10,2), nullable=True),      # Purchase Cost (valor decimal)
    db.Column('inventory_date', db.Date, nullable=True),               # Inventory Date
    db.Column('vendor', db.String(200), nullable=True),                # Vendor
    db.Column('project', db.String(200), nullable=True),               # Project (Award Name)
    db.Column('po_number', db.String(100), nullable=True),             # PO#
    db.Column('observation', db.Text, nullable=True),                  # Observação adicional
    
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