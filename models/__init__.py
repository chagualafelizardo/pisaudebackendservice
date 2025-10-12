from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Importação de modelos
from .Role import Role
from .State import State
from .Grouptype import Grouptype
from .Group import Group
from .Location import Location
from .Textmessage import Textmessage
from .User import User
from .UserRole import UserRole
from .Observation import Observation
from .keyPopulation import KeyPopulation
from .PortaTestagem import PortaTestagem
from .ContactLink import ContactLink 
from .DailyRecord import DailyRecord
from .Resource import Resource
from .ResourceType import ResourceType
from .FormaPrestacaoServico import FormaPrestacaoServico
from .Patent import Patent
from .Person import Person
from .Ramo import Ramo, SyncStatusEnum
from .Subunidade import Subunidade
from .Especialidade import Especialidade
from .Subespecialidade import Subespecialidade
from .SituacaoGeral import SituacaoGeral
from .Funcao import Funcao
from .SituacaoPrestacaoServico import SituacaoPrestacaoServico
from .Afetacao import Afetacao
from .Transferencia import Transferencia, SyncStatusEnum
from .EspecialidadeSaude import EspecialidadeSaude, SyncStatusEnum
from .Candidato import Candidato, CandidatoEdicao, SyncStatusEnum
from .TipoLicenca import TipoLicenca
from .Pais import Pais, SyncStatusEnum
from .Formacao import Formacao, SyncStatusEnum

__all__ = [
    'db', 'Role', 'State', 'Grouptype', 'Group', 'Location', 
    'Textmessage', 'User', 'UserRole', 'Observation', 'ContactLink',
    'DailyRecord', 'KeyPopulation', 'PortaTestagem','Resource','ResourceType',
    'FormaPrestacaoServico','Person', 'Patent', 'SyncStatusEnum','Ramo',
    'Subunidade', 'Especialidade', 'Subespecialidade', 'SituacaoGeral',
    'Funcao', 'SituacaoPrestacaoServico', 'Afetacao', 'Transferencia',
    'EspecialidadeSaude', 'Candidato', 'CandidatoEdicao', 'TipoLicenca',
    'Pais', 'Formacao'
]
