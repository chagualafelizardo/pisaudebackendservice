from datetime import datetime
from . import db

class ContactLink(db.Model):
    __tablename__ = 'contactlink'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_sistema = db.Column(db.DateTime, nullable=False)
    data_registo = db.Column(db.DateTime, nullable=False)
    nomeutente = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(100), nullable=False)
    nestaus = db.Column(db.String(100), nullable=False)
    outraus = db.Column(db.String(100), nullable=False)
    nameustarv = db.Column(db.String(100), nullable=False)
    nid = db.Column(db.String(100), nullable=False)
    dataprimeiraconsultaclinica = db.Column(db.String(100), nullable=False)
    ligacaoconfirmada = db.Column(db.String(100), nullable=False)
    parceirosexual = db.Column(db.String(100), nullable=False)
    parceirosexualquantos = db.Column(db.String(100), nullable=False)
    filhomenordezanos = db.Column(db.String(100), nullable=False)
    filhomenordezanosquantos = db.Column(db.String(100), nullable=False)
    maepaiCIPeddezanos = db.Column(db.String(100), nullable=False)
    maepaiCIPeddezanosquantos = db.Column(db.String(100), nullable=False)
    ocupacao = db.Column(db.String(100), nullable=False)
    obs = db.Column(db.String(100), nullable=False)
    referenciaconselheironome = db.Column(db.String(100), nullable=False)
    sincronizado = db.Column(db.Boolean, nullable=False, default=False)
    ultimasincronizacao = db.Column(db.DateTime)

    # Foreign keys
    locationId = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    portatestagemId = db.Column(db.Integer, db.ForeignKey('portatestagem.id'), nullable=False)
    referenciauserId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ligacaocontactosId = db.Column(db.Integer, db.ForeignKey('contactlink.id'))  # contato que indicou este
    registocontactoId = db.Column(db.Integer, db.ForeignKey('dailyrecord.id'), nullable=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    keypopulationId = db.Column(db.Integer, db.ForeignKey('keypopulation.id'), nullable=False)  # ✅ novo campo

    # Relacionamentos
    location = db.relationship('Location', backref='contactlinks')
    portatestagem = db.relationship('PortaTestagem', backref='contactlinks')
    referenciauser = db.relationship('User', foreign_keys=[referenciauserId])
    user = db.relationship('User', foreign_keys=[userId])
    registocontacto = db.relationship('DailyRecord', backref='contactlinks', foreign_keys=[registocontactoId])
    ligacaocontacto = db.relationship('ContactLink', remote_side=[id], foreign_keys=[ligacaocontactosId])
    keypopulation = db.relationship('KeyPopulation', backref='contactlinks', foreign_keys=[keypopulationId])  # ✅ novo relacionamento

    createAt = db.Column(db.DateTime, default=datetime.utcnow)
    updateAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ContactLink {self.id}>'
