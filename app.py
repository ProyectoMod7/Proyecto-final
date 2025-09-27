# app.py
from flask import Flask, render_template
from models import db
from routes import register_blueprints
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()  # carga variables del archivo .env
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback_key")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar base de datos
    db.init_app(app)

    # Registrar las rutas
    register_blueprints(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
