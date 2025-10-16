from . import db
from sqlalchemy import Enum, DateTime, func
from datetime import datetime
import enum
from models import Person, TipoLicenca, Despacho  # ✅ inclui Despacho

class EstadoLicencaEnum(enum.Enum):
    PENDENTE = "Pendente"
    APROVADA = "Aprovada"
    REJEITADA = "Rejeitada"
    CONCLUIDA = "Concluída"
    CANCELADA = "Cancelada"

class Licenca(db.Model):
    __tablename__ = 'licenca'

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipolicenca.id'), nullable=False)
    despacho_id = db.Column(db.Integer, db.ForeignKey('despacho.id'), nullable=True)  # ✅ opcional

    motivo = db.Column(db.String(255), nullable=True)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    estado = db.Column(Enum(EstadoLicencaEnum), default=EstadoLicencaEnum.PENDENTE)
    observacao = db.Column(db.Text, nullable=True)

    # 🔹 Anexo
    anexo_nome = db.Column(db.String(255), nullable=True)
    anexo_tipo = db.Column(db.String(50), nullable=True)
    anexo_dados = db.Column(db.LargeBinary, nullable=True)

    # Auditoria
    criado_em = db.Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = db.Column(DateTime(timezone=True), onupdate=func.now())

    # 🔹 Relacionamentos
    person = db.relationship('Person', backref=db.backref('licencas', lazy=True))
    tipo = db.relationship('TipoLicenca', backref=db.backref('licencas', lazy=True))
    despacho = db.relationship('Despacho', backref=db.backref('licencas', lazy=True))  # ✅

    def __repr__(self):
        return f"<Licenca {self.tipo.description} de {self.person.fullname} ({self.estado.value})>"
