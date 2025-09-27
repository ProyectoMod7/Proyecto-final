# models/pieza.py
from models.models import db

class Pieza(db.Model):
    __tablename__ = "piezas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    imagen_url = db.Column(db.String(255), nullable=True)
    fabricante_id = db.Column(db.Integer, db.ForeignKey("fabricantes.id"), nullable=True)

    # Relaciones
    fabricante = db.relationship("Fabricante", backref="piezas", lazy=True)
    stock_items = db.relationship("Stock", back_populates="pieza", lazy=True)
    piezas_instaladas = db.relationship("PiezaInstalada", back_populates="pieza", lazy=True)

    def __repr__(self):
        return f"<Pieza {self.nombre} ({self.codigo})>"
