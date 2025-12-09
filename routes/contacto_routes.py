# routes/contacto_routes.py
from flask import Blueprint, render_template, request, redirect, url_for

contacto_bp = Blueprint("contacto", __name__)

@contacto_bp.route("/contacto")
def contacto():
    return render_template("contacto/index.html")

@contacto_bp.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')
    # Aquí irá la lógica para guardar o enviar el mensaje
    return redirect(url_for('contacto.index'))