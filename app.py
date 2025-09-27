# app.py
import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev_secret")
    # Si usás SQLAlchemy en otras partes podés dejar DATABASE_URL, si no no hace falta
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    from routes import register_blueprints
    register_blueprints(app)

    @app.route("/")
    def index():
        return render_template("base.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
