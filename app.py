from flask import Flask, render_template
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp
from routes.repuestos_routes import repuestos_bp
from routes.contacto_routes import contacto_bp
from flask_migrate import Migrate
from models.models import db
from routes.monitor_routes import bp as monitor_bp
from routes.stock_routes import bp as stock_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecreto'  # cambiar en producción
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user:password@localhost:5432/tu_basedatos"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "supersecretkey"

    db.init_app(app)
    Migrate(app, db)

    # Registrar todos los Blueprints
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
    app.run(debug=True)