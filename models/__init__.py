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
from .ContactLink import ContactLink        # ✅ Adicionado
from .DailyRecord import DailyRecord        # ✅ Adicionado

__all__ = [
    'db', 'Role', 'State', 'Grouptype', 'Group', 'Location', 
    'Textmessage', 'User', 'UserRole', 'Observation', 'ContactLink',
    'DailyRecord', 'KeyPopulation', 'PortaTestagem'
]
