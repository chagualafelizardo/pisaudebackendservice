from . import db
from datetime import datetime

class Resource(db.Model):
    __tablename__ = 'resource'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=True)

    resourcetypeId = db.Column(db.Integer, db.ForeignKey('resourcetype.id'), nullable=False)
    resourcetype = db.relationship('ResourceType', back_populates='resources')

    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Resource {self.name}>'
