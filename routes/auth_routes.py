from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login")
def login():
    return "Página de login (en construcción)"
