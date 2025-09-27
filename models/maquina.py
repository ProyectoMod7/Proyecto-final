# models/maquina.py
from . import db

class Maquina(db.Model):
    __tablename__ = "maquinas"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=True)
    nombre = db.Column(db.String(200), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey("areas.id"), nullable=True)
    marca = db.Column(db.String(100), nullable=True)
    modelo = db.Column(db.String(100), nullable=True)
    nro_serie = db.Column(db.String(100), nullable=True)

    # Relaciones
    area = db.relationship("Area", back_populates="maquinas", lazy=True)
    piezas_instaladas = db.relationship(
        "PiezaInstalada",
        back_populates="maquina",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        """Útil para serializar en templates o APIs si necesitás."""
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "area_id": self.area_id,
            "marca": self.marca,
            "modelo": self.modelo,
            "nro_serie": self.nro_serie,
        }

    def __repr__(self):
        return f"<Maquina {self.id} {self.nombre}>"
