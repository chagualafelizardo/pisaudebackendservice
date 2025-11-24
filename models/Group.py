from datetime import datetime
from . import db

class Group(db.Model):
    __tablename__ = 'group'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Nome do grupo / descrição
    description = db.Column(db.String(150), nullable=False, unique=True)

    # Novos campos
    dateStart = db.Column(db.Date, nullable=True)
    dateEnd = db.Column(db.Date, nullable=True)
    observation = db.Column(db.Text, nullable=True)

    # Relacionamento com Observation
    observations = db.relationship('Observation', back_populates='group')

    createAt = db.Column(db.DateTime, default=db.func.now())
    updateAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<Group {self.description}>'
