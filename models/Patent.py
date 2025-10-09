from . import db
from sqlalchemy.orm import relationship
from .Person import person_patent  # importa a tabela associativa única

class Patent(db.Model):
    __tablename__ = 'patent'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100), nullable=False, unique=True)
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    persons = relationship('Person', secondary=person_patent, back_populates='patents')

    def __repr__(self):
        return f'<Patent {self.description}>'
