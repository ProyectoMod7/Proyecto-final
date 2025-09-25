from flask import Blueprint, render_template

# Creamos el Blueprint para el dashboard
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
def dashboard():
    # Datos de ejemplo (luego pueden venir de una DB o de sensores)
    maquinas = [
        {"nombre": "Máquina 1 - Rodamiento", "estado": "OK", "color": "success", "emoji": "🟢"},
        {"nombre": "Máquina 2 - Correa", "estado": "Pronto a fallo", "color": "warning", "emoji": "🟡"},
        {"nombre": "Máquina 3 - Motor", "estado": "Cambio urgente", "color": "danger", "emoji": "🔴"}
    ]
    return render_template("index.html", titulo="Panel de Mantenimiento", maquinas=maquinas)
