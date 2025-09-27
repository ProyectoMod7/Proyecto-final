from models.models import db

class Pieza(db.Model):
    __tablename__ = "piezas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    fabricante_id = db.Column(db.Integer, db.ForeignKey("fabricantes.id"), nullable=True)

    # Relación con fabricante
    fabricante = db.relationship("Fabricante", backref="piezas", lazy=True)

    # Relación con stock (una pieza puede estar en muchos registros de stock)
    stock_items = db.relationship("Stock", back_populates="pieza", lazy=True)

    def __repr__(self):
        return f"<Pieza {self.nombre}>"
