from . import db

class Proveedor(db.Model):
    __tablename__ = "proveedores"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False, unique=True)
    contacto = db.Column(db.String(150), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)

    # Relación con piezas o stock
    piezas = db.relationship("Pieza", back_populates="proveedor")

    def __repr__(self):
        return f"<Proveedor {self.nombre}>"
