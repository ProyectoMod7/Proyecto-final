from . import db

class Material(db.Model):
    __tablename__ = "materiales"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)

    # Relación con piezas
    piezas = db.relationship("Pieza", back_populates="material")

    def __repr__(self):
        return f"<Material {self.nombre}>"
