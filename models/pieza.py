from models.models import db

class Pieza(db.Model):
    __tablename__ = "piezas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100))
    fabricante = db.Column(db.String(100))
    material = db.Column(db.String(100))
    vida_util = db.Column(db.Integer)  # en horas o ciclos
    proveedor = db.Column(db.String(150))
    imagen_url = db.Column(db.String(255))  # URL en Supabase Storage

    # Relación con stock
    stock = db.relationship("Stock", back_populates="pieza", uselist=False)

    def __repr__(self):
        return f"<Pieza {self.nombre}>"
#    app.run(host='