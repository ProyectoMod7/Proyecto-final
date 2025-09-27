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

# No usamos create_all() porque ya tenemos las tablas en Supabase
# SQLAlchemy solo va a mapear los modelos a las tablas existentes
