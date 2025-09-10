from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Importe modelos BASE primeiro (que não dependem de outros)
from .Role import Role
from .State import State
from .Grouptype import Grouptype
from .Group import Group
from .Location import Location
from .Textmessage import Textmessage
from .User import User  # User antes de UserRole

# Depois importe modelos que dependem de outros
from .UserRole import UserRole
from .Observation import Observation
from .ContactLink import ContactLink
from .DailyRecord import DailyRecord
from .keyPopulation import keyPopulation
from .PortaTestagem import PortaTestagem

__all__ = [
    'db', 'Role', 'State', 'Grouptype', 'Group', 'Location', 
    'Textmessage', 'User', 'userRole', 'Observation', 'ContactLink',
    'DailyRecord', 'keyPopulation', 'PortaTestagem'
]