from sqlalchemy import UniqueConstraint
from datetime import datetime
from . import db

class MedicamentoLocation(db.Model):
    __tablename__ = 'medicamento_location'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    medicamento_id = db.Column(db.Integer, db.ForeignKey('medicamento.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    stock_minimo = db.Column(db.Integer, nullable=False, default=0)
    stock_maximo = db.Column(db.Integer, nullable=False, default=0)

    # Campos de controlo
    syncStatus = db.Column(db.String(50), nullable=False, default='Not Syncronized')
    syncStatusDate = db.Column(db.DateTime, nullable=True)
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    __table_args__ = (
        UniqueConstraint('medicamento_id', 'location_id', name='uq_medicamento_location'),
    )

    def __repr__(self):
        return f'<MedicamentoLocation med={self.medicamento_id} loc={self.location_id}>'