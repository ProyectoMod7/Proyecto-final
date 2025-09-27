from flask import Blueprint, render_template, request, redirect, url_for
from models import db
from models.maquina import Maquina

maquinas_bp = Blueprint("maquinas", __name__, url_prefix="/maquinas")

@maquinas_bp.route("/")
def index():
    maquinas = Maquina.query.all()
    return render_template("maquinas/index.html", maquinas=maquinas)

@maquinas_bp.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        nombre = request.form["nombre"]
        nueva = Maquina(nombre=nombre)
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for("maquinas.index"))
    return render_template("maquinas/new.html")

@maquinas_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    maquina = Maquina.query.get_or_404(id)
    if request.method == "POST":
        maquina.nombre = request.form["nombre"]
        db.session.commit()
        return redirect(url_for("maquinas.index"))
    return render_template("maquinas/edit.html", maquina=maquina)

@maquinas_bp.route("/delete/<int:id>")
def delete(id):
    maquina = Maquina.query.get_or_404(id)
    db.session.delete(maquina)
    db.session.commit()
    return redirect(url_for("maquinas.index"))
