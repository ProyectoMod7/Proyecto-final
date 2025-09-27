# models/maquina.py
from models.models import db

class Maquina(db.Model):
    __tablename__ = "maquinas"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True)
    nombre = db.Column(db.String(200), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey("areas.id"), nullable=True)
    marca = db.Column(db.String(100))
    modelo = db.Column(db.String(100))
    nro_serie = db.Column(db.String(100), nullable=True)

    piezas_instaladas = db.relationship(
        "PiezaInstalada",
        back_populates="maquina",
        lazy=True,
        cascade="all,delete-orphan"
    )

    def __repr__(self):
        return f"<Maquina {self.nombre}>"
