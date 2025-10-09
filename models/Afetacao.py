from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum as SQLAlchemyEnum
import enum

# Enum para syncStatus
class SyncStatusEnum(enum.Enum):
    NotSyncronized = "Not Syncronized"
    Syncronized = "Syncronized"
    Updated = "Updated"

class Afetacao(db.Model):
    __tablename__ = 'afetacao'

    id = Column(Integer, primary_key=True, autoincrement=True)

    # --------------------------
    # Relações / Chaves estrangeiras
    # --------------------------
    personId = Column(Integer, ForeignKey('person.id'), nullable=False)
    ramoId = Column(Integer, ForeignKey('ramo.id'), nullable=False)
    unidadeMilitarId = Column(Integer, ForeignKey('location.id'), nullable=False)
    subunidadeId = Column(Integer, ForeignKey('subunidade.id'), nullable=False)
    especialidadeId = Column(Integer, ForeignKey('especialidade.id'), nullable=False)
    subespecialidadeId = Column(Integer, ForeignKey('subespecialidade.id'), nullable=False)
    funcaoId = Column(Integer, ForeignKey('funcao.id'), nullable=False)
    situacaoGeralId = Column(Integer, ForeignKey('situacao_geral.id'), nullable=False)
    situacaoPrestacaoServicoId = Column(Integer, ForeignKey('situacao_prestacao_servico.id'), nullable=False)

    # --------------------------
    # Campos adicionais
    # --------------------------
    ultimoAnoPromocao = Column(Date, nullable=True)
    ordemServicoPromocao = Column(String(255), nullable=True)

    # --------------------------
    # Relacionamentos
    # --------------------------
    person = relationship("Person", backref="afetacoes")
    ramo = relationship("Ramo")
    unidadeMilitar = relationship("Location")
    subunidade = relationship("Subunidade")
    especialidade = relationship("Especialidade")
    subespecialidade = relationship("Subespecialidade")
    funcao = relationship("Funcao")
    situacaoGeral = relationship("SituacaoGeral")
    situacaoPrestacaoServico = relationship("SituacaoPrestacaoServico")

    # --------------------------
    # Sincronização
    # --------------------------
    syncStatus = Column(SQLAlchemyEnum(SyncStatusEnum), nullable=False, default=SyncStatusEnum.NotSyncronized)
    syncStatusDate = Column(DateTime, nullable=True)

    # --------------------------
    # Timestamps
    # --------------------------
    createdAt = Column(DateTime, default=db.func.current_timestamp())
    updatedAt = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Afetacao ID: {self.id} - Person: {self.person.fullname if self.person else "None"}>'
