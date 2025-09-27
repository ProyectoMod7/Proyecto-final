# models/fabricante.py
from models.models import db

class Fabricante(db.Model):
    __tablename__ = "fabricantes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False, unique=True)
    contacto = db.Column(db.JSON, nullable=True)  # json con email/telefono/url

    def __repr__(self):
        return f"<Fabricante {self.nombre}>"
