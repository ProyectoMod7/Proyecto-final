# routes/contacto_routes.py
from flask import Blueprint, render_template

contacto_bp = Blueprint("contacto", __name__)

@contacto_bp.route("/contacto")
def contacto():
    return render_template("contacto/index.html")
