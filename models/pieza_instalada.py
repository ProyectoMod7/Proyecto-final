# models/pieza_instalada.py
from models.models import db
from datetime import datetime

class PiezaInstalada(db.Model):
    __tablename__ = "piezas_instaladas"

    id = db.Column(db.Integer, primary_key=True)
    maquina_id = db.Column(db.Integer, db.ForeignKey("maquinas.id"), nullable=False)
    pieza_id = db.Column(db.Integer, db.ForeignKey("piezas.id"), nullable=False)
    instalada_en = db.Column(db.DateTime, default=datetime.utcnow)
    horas_uso = db.Column(db.Integer, default=0)
    vida_horas = db.Column(db.Integer, nullable=True)
    rota = db.Column(db.Boolean, default=False)
    notas = db.Column(db.Text, nullable=True)

    maquina = db.relationship("Maquina", back_populates="piezas_instaladas")
    pieza = db.relationship("Pieza", back_populates="piezas_instaladas")

    def __repr__(self):
        return f"<PiezaInstalada maquina={self.maquina_id} pieza={self.pieza_id}>"
