from models.models import db

class Stock(db.Model):
    __tablename__ = "stock"

    id = db.Column(db.Integer, primary_key=True)
    pieza_id = db.Column(db.Integer, db.ForeignKey("piezas.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    minimo = db.Column(db.Integer, nullable=False, default=0)

    # Relación con pieza
    pieza = db.relationship("Pieza", back_populates="stock_items")

    def __repr__(self):
        return f"<Stock {self.pieza.nombre} - {self.cantidad}>"
