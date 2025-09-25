# routes/contacto_routes.py

from flask import Blueprint, render_template

contacto_bp = Blueprint("contacto", __name__, url_prefix="")

@contacto_bp.route("/contacto")

def contacto():
    contacto_info = {
        "email": "coloca_tu_email_aqui@ejemplo.com", # Reemplaza con un email real
        "telefono": "123-456-7890", # Reemplaza con un número real
        "direccion": "Calle Falsa 123, Ciudad, País"
    }
    return render_template("contacto.html", titulo="Contacto", contacto=contacto_info)