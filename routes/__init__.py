from .auth_routes import auth_bp
from .maquinas_routes import maquinas_bp
from .piezas_routes import piezas_bp
from .stock_routes import stock_bp
from .contacto_routes import contacto_bp
from .piezas_instaladas_routes import piezas_instaladas_bp   # 👈 IMPORTAMOS EL BLUEPRINT

# y cuando vayas agregando más:
# from .fabricantes_routes import fabricantes_bp
# from .materiales_routes import materiales_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(maquinas_bp)
    app.register_blueprint(piezas_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(contacto_bp)
    app.register_blueprint(piezas_instaladas_bp)  # 👈 LO REGISTRAMOS

    # app.register_blueprint(fabricantes_bp)
    # app.register_blueprint(materiales_bp)
