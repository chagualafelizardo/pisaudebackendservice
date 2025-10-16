from . import db
from sqlalchemy import Enum, DateTime, func
import enum

class EstadoDespachoEnum(enum.Enum):
    PENDENTE = "Pendente"
    APROVADO = "Aprovado"
    REJEITADO = "Rejeitado"
    CONCLUIDO = "Concluído"
    CANCELADO = "Cancelado"

class Despacho(db.Model):
    __tablename__ = 'despacho'

    id = db.Column(db.Integer, primary_key=True)
    
    # Relacionamento opcional com Person
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)
    
    # Campos principais
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data_despacho = db.Column(db.Date, nullable=False, default=func.current_date())
    estado = db.Column(Enum(EstadoDespachoEnum), default=EstadoDespachoEnum.PENDENTE)
    observacao = db.Column(db.Text, nullable=True)

    # 🔹 Campo para anexo (ficheiro PDF, DOCX, imagem, etc.)
    anexo_nome = db.Column(db.String(255), nullable=True)
    anexo_tipo = db.Column(db.String(50), nullable=True)   # Ex: 'application/pdf', 'image/png'
    anexo_dados = db.Column(db.LargeBinary, nullable=True) # Conteúdo binário

    # Auditoria
    criado_em = db.Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = db.Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamento
    person = db.relationship('Person', backref=db.backref('despachos', lazy=True))

    def __repr__(self):
        person_name = self.person.fullname if self.person else "Sem pessoa"
        return f"<Despacho {self.titulo} ({self.estado.value}) de {person_name}>"
