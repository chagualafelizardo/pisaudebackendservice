from datetime import datetime
from . import db

class DailyRecord(db.Model):  # Mude o nome da classe para refletir a tabela
    __tablename__ = 'dailyrecord'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datasistema = db.Column(db.DateTime, nullable=False)  # Removido unique=True
    dataregisto = db.Column(db.DateTime, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    idadeunidade = db.Column(db.String(50), nullable=False)  # Adicionado length
    sexo = db.Column(db.String(1), nullable=False)  # Alterado de Char para String(1)
    parceirosexual = db.Column(db.String(100), nullable=False)  # Removido unique=True
    filhomenordezanos = db.Column(db.String(100), nullable=False)  # Removido unique=True
    maepaiCIPeddezanos = db.Column(db.String(100), nullable=False)  # Removido unique=True
    confirmacaoautoteste_hiv = db.Column(db.String(100), nullable=False)  # Removido unique=True
    testagemdetermine1 = db.Column(db.String(100), nullable=False)  # Removido unique=True
    testagemunigold1 = db.Column(db.String(100), nullable=False)  # Removido unique=True
    testagemdetermine2 = db.Column(db.String(100), nullable=False)  # Removido unique=True
    testagemunigold2 = db.Column(db.String(100), nullable=False)  # Removido unique=True
    resultadofinal = db.Column(db.String(100), nullable=False)  # Removido unique=True
    historialtestagem_primeira_testado = db.Column(db.String(100), nullable=False)  # Removido unique=True
    historialtestagem_positivo_no_passado = db.Column(db.String(100), nullable=False)  # Removido unique=True
    ocupacao = db.Column(db.String(100), nullable=False)  # Removido unique=True
    referenciaconselheironome = db.Column(db.String(100), nullable=False)  # Removido unique=True
    cpnopcao = db.Column(db.String(100), nullable=False)  # Removido unique=True
    casoindiceopcao = db.Column(db.String(100), nullable=False)  # Removido unique=True
    cpfopcao = db.Column(db.String(100), nullable=False)  # Removido unique=True

    latitude = db.Column(db.String(100), nullable=False)  # Removido unique=True
    longitude = db.Column(db.String(100), nullable=False)  # Removido unique=True
    sincronizado = db.Column(db.Boolean, nullable=False, default=False)  # Alterado para Boolean
    ultima_sincronizacao = db.Column(db.DateTime)  # Removido unique=True e nullable=False

    # Relacionamentos
    locationId = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    portatestagemId = db.Column(db.Integer, db.ForeignKey('portatestagem.id'), nullable=False)
    referenciauserId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    keypopulationId = db.Column(db.Integer, db.ForeignKey('keypopulation.id'), nullable=False)
    ligacaocontactosId = db.Column(db.Integer, db.ForeignKey('contactlink.id'), nullable=False)
    registocontactoId = db.Column(db.Integer, db.ForeignKey('dailyrecord.id'))  # Removido nullable=False
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    createAt = db.Column(db.DateTime, default=db.func.now())
    updateAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<DailyRecord {self.id}>'  # Atualizado para refletir o nome da classe