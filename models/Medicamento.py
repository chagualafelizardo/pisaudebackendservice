from sqlalchemy import UniqueConstraint
from datetime import datetime
from . import db

class Medicamento(db.Model):
    __tablename__ = 'medicamento'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    nome_padronizado = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.Enum('TARV', 'PrEP', 'TB Sensível', 'TB-DR', 'Profilaxia', 'Testes Rápidos', name='categoria_enum'), nullable=False)
    forma_farmaceutica = db.Column(db.Enum('Comprimido', 'Suspensão', 'Kit', 'Frasco', name='forma_farmaceutica_enum'), nullable=False)
    unidade_medida = db.Column(db.Enum('Comprimido', 'Frasco', 'Kit', 'ml', name='unidade_medida_enum'), nullable=False)
    apresentacao = db.Column(db.String(50), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    # Campos de controlo (padrão do exemplo)
    syncStatus = db.Column(db.String(50), nullable=False, default='Not Syncronized')
    syncStatusDate = db.Column(db.DateTime, nullable=True)
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    locations = db.relationship('MedicamentoLocation', backref='medicamento', lazy='dynamic', cascade='all, delete-orphan')

    # Restrição única para (nome_padronizado, apresentacao)
    __table_args__ = (
        UniqueConstraint('nome_padronizado', 'apresentacao', name='uq_medicamento_nome_apresentacao'),
    )

    def __repr__(self):
        return f'<Medicamento {self.id} - {self.nome_padronizado} - {self.apresentacao}>'