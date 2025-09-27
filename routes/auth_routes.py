
from flask import Blueprint, render_template, redirect, url_for, session

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth")
def auth():
    return render_template("auth/index.html")

@auth_bp.route("/unlock")
def unlock():
    session["unlocked"] = True
    return redirect(url_for("maquinas.index"))
