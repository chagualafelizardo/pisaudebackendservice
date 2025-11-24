from datetime import datetime
from . import db

# Tabela associativa para Location <-> Resource com quantidade
location_resource = db.Table('location_resource',
    db.Column('location_id', db.Integer, db.ForeignKey('location.id'), primary_key=True),
    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False, default=0)
)

class Location(db.Model):
    __tablename__ = 'location'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False, unique=True)

    # Novas colunas para localização
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # 🔹 NOVO CAMPO: Responsável com valores fixos (DOD, Jhpiego)
    responsavel = db.Column(
        db.String(20), 
        nullable=False, 
        default='DOD',
        server_default='DOD'
    )
    # NOVO CAMPO: Observações (texto livre, sem relacionamento)
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

    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Location {self.name}>'

    # 🔹 MÉTODO PARA VALIDAÇÃO DOS VALORES PERMITIDOS
    @staticmethod
    def get_responsaveis_permitidos():
        """Retorna a lista de responsáveis permitidos"""
        return ['DOD', 'Jhpiego','RISE']

    # 🔹 MÉTODO PARA VALIDAR O VALOR DO RESPONSÁVEL
    def validar_responsavel(self):
        """Valida se o responsável está na lista de permitidos"""
        return self.responsavel in self.get_responsaveis_permitidos()