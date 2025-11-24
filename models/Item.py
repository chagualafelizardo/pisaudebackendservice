from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import LargeBinary, DateTime, Float, Integer, String, Text, ForeignKey, UniqueConstraint
from datetime import datetime


class Item(db.Model):
    __tablename__ = 'item'

    # 🔹 Chave primária
    id = db.Column(Integer, primary_key=True, autoincrement=True)

    # 🔹 Campos únicos por combinação
    codigo = db.Column(String(50), nullable=False)
    designacao = db.Column(String(150), nullable=False)
    armazem_id = db.Column(Integer, ForeignKey('armazem.id'), nullable=False)
    armazem = relationship('Armazem', back_populates='itens')

    # 🔹 Combinação única
    __table_args__ = (
        UniqueConstraint('codigo', 'designacao', 'armazem_id', name='uq_item_codigo_designacao_armazem'),
    )

    # 🔹 Porto (opcional)
    porto_id = db.Column(Integer, ForeignKey('porto.id'), nullable=True)
    porto = relationship('Porto', backref=db.backref('itens', lazy=True))

    # 🔹 Nota de envio (opcional)
    nota_envio_id = db.Column(Integer, ForeignKey('nota_envio.id'), nullable=True)
    nota_envio = relationship('NotaEnvio', backref=db.backref('itens_envio', lazy=True))

    # 🔹 Anexos e documentos
    imagem = db.Column(LargeBinary, nullable=True)
    pdf_nome = db.Column(String(255), nullable=True)
    pdf_tipo = db.Column(String(50), nullable=True)
    pdf_dados = db.Column(LargeBinary, nullable=True)
    guia_assinada_nome = db.Column(String(255), nullable=True)
    guia_assinada_tipo = db.Column(String(50), nullable=True)
    guia_assinada_dados = db.Column(LargeBinary, nullable=True)

    # 🔹 Observação
    observacoes = db.Column(Text, nullable=True)

    # 🔹 Informações logísticas
    hs_code = db.Column(String(50), nullable=True)
    quantidade = db.Column(Integer, nullable=True)
    batch_no = db.Column(String(50), nullable=True)
    data_fabricacao = db.Column(DateTime, nullable=True)
    data_validade = db.Column(DateTime, nullable=True)
    no_cartoes = db.Column(Integer, nullable=True)
    peso_bruto_total = db.Column(Float, nullable=True)
    volume_total_cbm = db.Column(Float, nullable=True)
    total_cartoes = db.Column(Integer, nullable=True)
    total_paletes = db.Column(Integer, nullable=True)
    dimensoes_palete_cm = db.Column(String(100), nullable=True)

    # 🔹 Recepção
    data_recepcao = db.Column(DateTime, nullable=True)

    # 🔹 Sincronização
    syncStatus = db.Column(String(50), nullable=False, default='NotSyncronized')
    syncStatusDate = db.Column(DateTime, nullable=True)

    # 🔹 Utilizadores
    user = db.Column(String(150), nullable=True)
    recebeu = db.Column(String(150), nullable=True)

    # 🔹 Timestamps
    createAt = db.Column(DateTime, default=db.func.current_timestamp())
    updateAt = db.Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Item ID={self.id} | {self.codigo} - {self.designacao} - Armazém {self.armazem_id}>'
