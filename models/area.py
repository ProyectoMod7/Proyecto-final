from . import db

class Area(db.Model):
    __tablename__ = "areas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    # Relación con máquinas
    maquinas = db.relationship("Maquina", back_populates="area")

    def __repr__(self):
        return f"<Area {self.nombre}>"