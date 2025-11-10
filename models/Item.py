from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import LargeBinary, DateTime, Float, Integer, String, Text, ForeignKey
from datetime import datetime


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(String(50), nullable=False, unique=True)
    designacao = db.Column(String(150), nullable=False)

    # 🔹 Relação com Armazém
    armazem_id = db.Column(Integer, ForeignKey('armazem.id'), nullable=False)
    armazem = relationship('Armazem', back_populates='itens')

    # 🔹 Relação com Porto de chegada (opcional)
    porto_id = db.Column(Integer, ForeignKey('porto.id'), nullable=True)
    porto = relationship('Porto', backref=db.backref('itens', lazy=True))

    # 🔹 Relação opcional com Nota de Envio
    nota_envio_id = db.Column(Integer, ForeignKey('nota_envio.id'), nullable=True)
    nota_envio = relationship('NotaEnvio', backref=db.backref('itens_envio', lazy=True))

    # 🔹 Imagem do item (binário)
    imagem = db.Column(LargeBinary, nullable=True)

    # 🔹 Comprovativo de envio em PDF
    pdf_nome = db.Column(String(255), nullable=True)
    pdf_tipo = db.Column(String(50), nullable=True)
    pdf_dados = db.Column(LargeBinary, nullable=True)

    # 🔹 Campos de observações
    observacoes = db.Column(Text, nullable=True)

    # 🔹 Novos campos logísticos e comerciais
    hs_code = db.Column(String(50), nullable=True)                   # HS Code
    quantidade = db.Column(Integer, nullable=True)                   # Qty
    batch_no = db.Column(String(50), nullable=True)                  # Batch No
    data_fabricacao = db.Column(DateTime, nullable=True)             # MFG Date
    data_validade = db.Column(DateTime, nullable=True)               # Expiry Date
    no_cartoes = db.Column(Integer, nullable=True)                   # No. of Cartons
    peso_bruto_total = db.Column(Float, nullable=True)               # Total Gross Weight
    volume_total_cbm = db.Column(Float, nullable=True)               # Total Volume (CBM)
    total_cartoes = db.Column(Integer, nullable=True)                # Total No of Cartons
    total_paletes = db.Column(Integer, nullable=True)                # Total No. of Pallets
    dimensoes_palete_cm = db.Column(String(100), nullable=True)      # Pallet Dimensions (CM)

    # 🔹 Campo de sincronização (agora String simples)
    syncStatus = db.Column(String(50), nullable=False, default='NotSyncronized')
    syncStatusDate = db.Column(DateTime, nullable=True)

    # 🔹 Novo campo para armazenar o nome do utilizador que adicionou o item
    user = db.Column(String(150), nullable=True)

    # 🔹 Timestamps
    createAt = db.Column(DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Item {self.designacao}>'
