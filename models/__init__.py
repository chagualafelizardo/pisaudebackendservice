from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .PortaTestagem import PortaTestagem
from .ContactLink import ContactLink
from .Location import Location
from .User import User
from .DailyRecord import DailyRecord
from .PopulacaoChave import PopulacaoChave
# Importe todos os outros modelos necessários

__all__ = ['db', 'PortaTestagem', 'ContactLink', 'Location', 'User', 'DailyRecord', 'PopulacaoChave']