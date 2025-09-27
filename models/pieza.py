from . import db

class Pieza(db.Model):
    __tablename__ = "piezas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    imagen_url = db.Column(db.String(255), nullable=True)

    # Relaciones
    stock_items = db.relationship("Stock", back_populates="pieza", lazy=True)
    piezas_instaladas = db.relationship("PiezaInstalada", back_populates="pieza", lazy=True)

    fabricante_id = db.Column(db.Integer, db.ForeignKey("fabricantes.id"))
    proveedor_id = db.Column(db.Integer, db.ForeignKey("proveedores.id"))
    material_id = db.Column(db.Integer, db.ForeignKey("materiales.id"))

    fabricante = db.relationship("Fabricante", back_populates="piezas")
    proveedor = db.relationship("Proveedor", back_populates="piezas")
    material = db.relationship("Material", back_populates="piezas")

    def __repr__(self):
        return f"<Pieza {self.nombre}>"

