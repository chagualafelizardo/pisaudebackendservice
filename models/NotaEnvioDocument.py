
from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum, LargeBinary, DateTime, Float, Integer, String, Text, ForeignKey
from datetime import datetime

# ===============================================================
# 🔹 Documentos anexos — NotaEnvioDocument (vários documentos por nota)
# ===============================================================
class NotaEnvioDocument(db.Model):
    __tablename__ = 'nota_envio_document'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nota_envio_id = db.Column(db.Integer, db.ForeignKey('nota_envio.id'), nullable=False)

    nome_arquivo = db.Column(db.String(255), nullable=False)
    tipo_mime = db.Column(db.String(100))
    dados_arquivo = db.Column(db.LargeBinary, nullable=False)
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)

    nota_envio = relationship('NotaEnvio', back_populates='documentos')

    def __repr__(self):
        return f'<NotaEnvioDocument {self.nome_arquivo}>'
