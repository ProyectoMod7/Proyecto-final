from flask import Flask, render_template
from flask_migrate import Migrate
from models.models import db
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp
from routes.repuestos_routes import repuestos_bp
from routes.contacto_routes import contacto_bp
from routes.monitor_routes import monitor_bp
from routes.stock_routes import stock_bp
import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuración desde variables de entorno
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "clave_por_defecto")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.debug = os.getenv("DEBUG", "False") == "True"

    # Inicializar extensiones
    db.init_app(app)
    Migrate(app, db)

    # Registrar Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(repuestos_bp)
    app.register_blueprint(contacto_bp)
    app.register_blueprint(monitor_bp)
    app.register_blueprint(stock_bp, url_prefix="/stock")

    # Ruta principal
    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
# Nota: Para producción, usar un servidor WSGI como Gunicorn o uWSGI
# Ejemplo: gunicorn -w 4 app:app
# También configurar variables de entorno adecuadamente
# y manejar secretos con cuidado.