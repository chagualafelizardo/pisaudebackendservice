from . import db
from sqlalchemy import ForeignKey
from datetime import datetime

# ====================
# MODELO: Agendamento
# ====================
class Agendamento(db.Model):
    __tablename__ = 'agendamento'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Dados do paciente
    paciente_id = db.Column(db.Integer, ForeignKey('observation.id'), nullable=True)
    paciente_nome = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    
    # Dados do agendamento
    medico_id = db.Column(db.Integer, ForeignKey('medico.id'), nullable=False)
    data_consulta = db.Column(db.Date, nullable=False)
    hora_consulta = db.Column(db.Time, nullable=False)
    tipo_consulta = db.Column(db.String(50), default='Rotina')  # Rotina, Retorno, Emergência
    
    # Status
    status = db.Column(db.String(20), default='pendente')  # pendente, confirmado, cancelado, realizado
    observacoes = db.Column(db.Text, nullable=True)
    
    # Controle de SMS
    sms_enviado = db.Column(db.Boolean, default=False)
    sms_confirmacao_enviado = db.Column(db.Boolean, default=False)
    ultimo_sms_data = db.Column(db.DateTime, nullable=True)
    
    # Timestamps
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Agendamento {self.paciente_nome} - {self.data_consulta} {self.hora_consulta}>'