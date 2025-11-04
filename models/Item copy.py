from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum, LargeBinary, DateTime, Float, Integer, String
from datetime import datetime
import enum

# Enum para syncStatus
class SyncStatusEnum(enum.Enum):
    NotSyncronized = "Not Syncronized"
    Syncronized = "Syncronized"
    Updated = "Updated"


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(50), nullable=False, unique=True)
    designacao = db.Column(db.String(150), nullable=False)

    # 🔹 Relação com Armazém
    armazem_id = db.Column(db.Integer, db.ForeignKey('armazem.id'), nullable=False)
    armazem = relationship('Armazem', back_populates='itens')

    # 🔹 Relação com Porto de chegada (opcional)
    porto_id = db.Column(db.Integer, db.ForeignKey('porto.id'), nullable=True)
    porto = relationship('Porto', backref=db.backref('itens', lazy=True))

    # 🔹 Imagem do item (binário)
    imagem = db.Column(db.LargeBinary, nullable=True)

    # 🔹 Comprovativo de envio em PDF
    pdf_nome = db.Column(db.String(255), nullable=True)
    pdf_tipo = db.Column(db.String(50), nullable=True)
    pdf_dados = db.Column(db.LargeBinary, nullable=True)

    # 🔹 Campos de observações
    observacoes = db.Column(db.Text, nullable=True)

    # 🔹 Novos campos logísticos e comerciais
    hs_code = db.Column(db.String(50), nullable=True)                   # HS Code
    quantidade = db.Column(Integer, nullable=True)                      # Qty
    batch_no = db.Column(db.String(50), nullable=True)                  # Batch No
    data_fabricacao = db.Column(DateTime, nullable=True)                # MFG Date
    data_validade = db.Column(DateTime, nullable=True)                  # Expiry Date
    no_cartoes = db.Column(Integer, nullable=True)                      # No. of Cartons
    peso_bruto_total = db.Column(Float, nullable=True)                  # Total Gross Weight
    volume_total_cbm = db.Column(Float, nullable=True)                  # Total Volume (CBM)
    total_cartoes = db.Column(Integer, nullable=True)                   # Total No of Cartons
    total_paletes = db.Column(Integer, nullable=True)                   # Total No. of Pallets
    dimensoes_palete_cm = db.Column(String(100), nullable=True)         # Pallet Dimensions (CM)

    # 🔹 Campos de sincronização (Enum)
    syncStatus = db.Column(Enum(SyncStatusEnum), nullable=False, default=SyncStatusEnum.NotSyncronized)
    syncStatusDate = db.Column(db.DateTime, nullable=True)

    # 🔹 Timestamps
    createAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __repr__(self):
        return f'<Item {self.designacao}>'
