from datetime import datetime
from . import db
from .keyPopulation import KeyPopulation

class DailyRecord(db.Model):
    __tablename__ = 'dailyrecord'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datasistema = db.Column(db.DateTime, nullable=False)
    dataregisto = db.Column(db.DateTime, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    idadeunidade = db.Column(db.String(50), nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    parceirosexual = db.Column(db.String(100), nullable=False)
    filhomenordezanos = db.Column(db.String(100), nullable=False)
    maepaiCIPeddezanos = db.Column(db.String(100), nullable=False)
    confirmacaoautoteste_hiv = db.Column(db.String(100), nullable=False)
    testagemdetermine1 = db.Column(db.String(100), nullable=False)
    testagemunigold1 = db.Column(db.String(100), nullable=False)
    testagemdetermine2 = db.Column(db.String(100), nullable=False)
    testagemunigold2 = db.Column(db.String(100), nullable=False)
    resultadofinal = db.Column(db.String(100), nullable=False)
    historialtestagem_primeira_testado = db.Column(db.String(100), nullable=False)
    historialtestagem_positivo_no_passado = db.Column(db.String(100), nullable=False)
    ocupacao = db.Column(db.String(100), nullable=False)
    referenciaconselheironome = db.Column(db.String(100), nullable=False)
    cpnopcao = db.Column(db.String(100), nullable=False)
    casoindiceopcao = db.Column(db.String(100), nullable=False)
    cpfopcao = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.String(100), nullable=False)
    sincronizado = db.Column(db.Boolean, nullable=False, default=False)
    ultima_sincronizacao = db.Column(db.DateTime)

    # Foreign Keys
    locationId = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    portatestagemId = db.Column(db.Integer, db.ForeignKey('portatestagem.id'), nullable=False)
    referenciauserId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    keypopulationId = db.Column(db.Integer, db.ForeignKey('keypopulation.id'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relacionamentos
    location = db.relationship('Location', backref='dailyrecords')
    portatestagem = db.relationship('PortaTestagem', backref='dailyrecords')
    referenciauser = db.relationship('User', foreign_keys=[referenciauserId])
    keypopulation = db.relationship('KeyPopulation', backref='dailyrecords', foreign_keys=[keypopulationId])
    user = db.relationship('User', foreign_keys=[userId])

    createAt = db.Column(db.DateTime, default=db.func.now())
    updateAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<DailyRecord {self.id}>'
