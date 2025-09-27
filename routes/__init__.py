from .auth_routes import auth_bp
from .contacto_routes import contacto_bp
from .dashboard_routes import dashboard_bp
from .monitor_routes import monitor_bp
from .repuestos_routes import repuestos_bp
from .stock_routes import stock_bp

# routes/__init__.py


__all__ = [
    "auth_bp",
    "contacto_bp",
    "dashboard_bp",
    "monitor_bp",
    "repuestos_bp",
    "stock_bp",
]
