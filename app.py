from flask import Flask, render_template
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp
from routes.repuestos_routes import repuestos_bp
from routes.contacto_routes import contacto_bp



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecreto'  # cambiar en producción

    # Registrar los Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(repuestos_bp)
    app.register_blueprint(contacto_bp)
    
    @app.route("/")
    def index():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)