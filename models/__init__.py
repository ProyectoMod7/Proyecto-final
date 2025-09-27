from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def init_app(app):
    db.init_app(app)
    app.db = db # Attach db to app for easy access
    with app.app_context():
        db.create_all()  # Create tables for all models 
        print("Database tables created.")
        db.session.commit()
    return db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar los modelos para que SQLAlchemy los registre
from .area import Area
from .fabricante import Fabricante
from .maquina import Maquina
from .material import Material
from .pieza import Pieza
from .pieza_instalada import PiezaInstalada
from .proveedor import Proveedor
from .stock import Stock

# Add any additional models here
# For example:
# from .new_model import NewModel
# from .another_model import AnotherModel
# etc.
