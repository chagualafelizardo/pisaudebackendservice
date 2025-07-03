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
    sincronizado = db.Column(db.String(100), nullable=False)
    ultimasincronizacao = db.Column(db.String(100), nullable=False)

    locationId = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    portatestagemId = db.Column(db.Integer, db.ForeignKey('portatestagem.id'), nullable=False)
    referenciauserId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ligacaocontactosId = db.Column(db.Integer, db.ForeignKey('contactlink.id'), nullable=False)
    registocontactoId = db.Column(db.Integer, db.ForeignKey('dailyrecord.id'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    createAt = db.Column(db.DateTime, default=datetime.utcnow)
    updateAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ContactLink {self.id}>'
