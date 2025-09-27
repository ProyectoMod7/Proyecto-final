# routes/maquinas_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import db
from models.maquina import Maquina

maquinas_bp = Blueprint("maquinas", __name__, url_prefix="/maquinas")

@maquinas_bp.route("/")
def index():
    maquinas = Maquina.query.all()
    return render_template("maquinas/index.html", maquinas=maquinas)

@maquinas_bp.route("/<int:id>")
def ver_maquina(id):
    maquina = Maquina.query.get_or_404(id)
    return render_template("maquinas/ver.html", maquina=maquina)
