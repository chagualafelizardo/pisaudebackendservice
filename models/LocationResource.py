# from datetime import datetime
# from . import db

# class LocationResource(db.Model):
#     __tablename__ = 'location_resource'
#     __table_args__ = {'extend_existing': True}

#     # Primary Key única
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)

#     # ForeignKey
#     location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

#     # Dados do recurso
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(255), nullable=True)
#     recebidopor = db.Column(db.String(100), nullable=True)

#     # Imagens
#     imagem_principal = db.Column(db.Text, nullable=True)
#     imagens = db.Column(db.Text, nullable=True)

#     anexospdf = db.Column(db.Text, nullable=True)

#     datarecepcao = db.Column(db.Date, nullable=True)
#     quantidade = db.Column(db.Integer, nullable=False, default=0)

#     # Timestamps
#     createAt = db.Column(db.DateTime, default=datetime.utcnow)
#     updateAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Relacionamento reverso
#     location = db.relationship('Location', backref=db.backref('location_resources', lazy=True))

#     def __repr__(self):
#         return f'<LocationResource {self.name} | Location {self.location_id}>'
