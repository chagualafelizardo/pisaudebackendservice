from . import db
from datetime import datetime

class ResourceType(db.Model):
    __tablename__ = 'resourcetype'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=True)

    resources = db.relationship('Resource', back_populates='resourcetype')

    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<ResourceType {self.name}>'
