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
from .Candidato import Candidato, CandidatoEdicao
from .TipoLicenca import TipoLicenca
from .Pais import Pais, SyncStatusEnum
from .Formacao import Formacao
from .Licenca import Licenca, EstadoLicencaEnum
from .Despacho import Despacho, EstadoDespachoEnum
from .Provincia import Provincia
from .Item import Item
from .Armazem import Armazem
from .Componente import Componente
from .UserComponente import UserComponente
from .Porto import Porto
from .ItemHistorico import ItemHistorico
from .ItemLocationNecessidade import ItemLocationNecessidade
from .Distribuicao import Distribuicao
from .TipoItem import TipoItem
from .NotaEnvio import NotaEnvio, SyncStatusEnum
from .NotaEnvioItem import NotaEnvioItem
from .NotaEnvioDocument import NotaEnvioDocument
from .ItemPendente import ItemPendente

__all__ = [
    'db', 'Role', 'State', 'Grouptype', 'Group', 'Location', 
    'Textmessage', 'User', 'UserRole', 'Observation', 'ContactLink',
    'DailyRecord', 'KeyPopulation', 'PortaTestagem','Resource','ResourceType',
    'FormaPrestacaoServico','Person', 'Patent', 'SyncStatusEnum','Ramo',
    'Subunidade', 'Especialidade', 'Subespecialidade', 'SituacaoGeral',
    'Funcao', 'SituacaoPrestacaoServico', 'Afetacao', 'Transferencia',
    'EspecialidadeSaude', 'Candidato', 'CandidatoEdicao', 'TipoLicenca',
    'Pais', 'Formacao', 'Licenca','EstadoLicencaEnum', 'Despacho','EstadoDespachoEnum',
    'Provincia','Item','Armazem', 'Componente','UserComponente', 'Porto',
    'ItemHistorico','ItemLocationNecessidade', 'Distribuicao','TipoItem','NotaEnvio',
    'NotaEnvioItem', 'NotaEnvioDocument', 'ItemPendente'
]
