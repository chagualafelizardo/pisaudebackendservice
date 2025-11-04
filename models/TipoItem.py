from . import db

class TipoItem(db.Model):
    __tablename__ = 'tipo_item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    # 🔹 Relacionamento com NotaEnvio
    notas_envio = db.relationship('NotaEnvio', back_populates='tipo_item')

    def __repr__(self):
        return f'<TipoItem {self.nome}>'
