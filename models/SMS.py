from . import db
from sqlalchemy import ForeignKey
from datetime import datetime

# ====================
# MODELO: SMS
# ====================
class SMS(db.Model):
    __tablename__ = 'sms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Destinatário
    destinatario = db.Column(db.String(15), nullable=False)
    destinatario_nome = db.Column(db.String(200), nullable=True)
    
    # Mensagem
    mensagem = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # lembrete, confirmacao, cancelamento, educativo, personalizado
    
    # Status
    status = db.Column(db.String(20), default='pendente')  # pendente, enviado, falha
    resposta = db.Column(db.Text, nullable=True)
    mensagem_id = db.Column(db.String(100), nullable=True)  # ID da mensagem no provedor SMS
    
    # Referência ao agendamento (se aplicável)
    agendamento_id = db.Column(db.Integer, ForeignKey('agendamento.id'), nullable=True)
    
    # Timestamps
    data_envio = db.Column(db.DateTime, default=db.func.current_timestamp())
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<SMS para {self.destinatario} - {self.status}>'