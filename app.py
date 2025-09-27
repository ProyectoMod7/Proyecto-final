import os
from flask import Flask, render_template
from dotenv import load_dotenv
from models import db  # importa db desde models/__init__.py

# Importar blueprints
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp
from routes.repuestos_routes import repuestos_bp
from routes.contacto_routes import contacto_bp
from routes.monitor_routes import monitor_bp
from routes.stock_routes import stock_bp

# Cargar variables de entorno
load_dotenv()


def create_app():
    app = Flask(__name__)

    # Configuración desde .env
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar SQLAlchemy
    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(repuestos_bp)
    app.register_blueprint(contacto_bp)
    app.register_blueprint(monitor_bp)
    app.register_blueprint(stock_bp, url_prefix="/stock")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    # Debug activado mientras desarrollás
    app.run(debug=True, host="0.0.0.0", port=5000)
