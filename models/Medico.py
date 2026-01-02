from . import db
from sqlalchemy import ForeignKey
from datetime import datetime

# ====================
# MODELO: Médico
# ====================
class Medico(db.Model):
    __tablename__ = 'medico'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(200), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    registro_profissional = db.Column(db.String(50), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    horario_trabalho = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    
    # Timestamps
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relacionamentos
    horarios = db.relationship('HorarioMedico', backref='medico', lazy=True, cascade='all, delete-orphan')
    agendamentos = db.relationship('Agendamento', backref='medico', lazy=True)

    def __repr__(self):
        return f'<Medico {self.nome}>'