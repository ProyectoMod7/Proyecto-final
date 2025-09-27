from .maquinas_routes import maquinas_bp
from .piezas_routes import piezas_bp
from .stock_routes import stock_bp
from .misc_routes import misc_bp

def register_blueprints(app):
    app.register_blueprint(maquinas_bp)
    app.register_blueprint(piezas_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(misc_bp)
