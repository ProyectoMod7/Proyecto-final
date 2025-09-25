# routes/repuestos_routes.py
from flask import Blueprint, render_template

repuestos_bp = Blueprint("repuestos", __name__, url_prefix="")

@repuestos_bp.route("/repuestos")
def repuestos():
    piezas = [
        {"nombre": "Rodamiento 6203", "stock": 12, "minimo": 5},
        {"nombre": "Correa A-42", "stock": 3, "minimo": 5},
        {"nombre": "Filtro aceite XZ", "stock": 0, "minimo": 2},
    ]
    return render_template("repuestos.html", titulo="Repuestos", piezas=piezas)
