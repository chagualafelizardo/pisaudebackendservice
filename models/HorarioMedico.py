# models.py - Modelo HorarioMedico corrigido
from . import db
from sqlalchemy import ForeignKey
from datetime import datetime

class HorarioMedico(db.Model):
    __tablename__ = 'horario_medico'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    medico_id = db.Column(db.Integer, ForeignKey('medico.id'), nullable=False)
    
    # Configuração de horário
    dia_semana = db.Column(db.Integer, nullable=True)  # 1=Segunda, 2=Terça, etc. (nullable agora)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    duracao_consulta = db.Column(db.Integer, default=30)  # em minutos
    intervalo_almoco_inicio = db.Column(db.Time, nullable=True)
    intervalo_almoco_fim = db.Column(db.Time, nullable=True)
    
    # Data específica (se aplicável)
    data_especifica = db.Column(db.Date, nullable=True)
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    
    # Timestamps
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<HorarioMedico Medico:{self.medico_id} Dia:{self.dia_semana}>'