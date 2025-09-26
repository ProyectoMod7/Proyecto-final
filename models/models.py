# models/models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Sector(db.Model):
    __tablename__ = 'sectors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    location = db.Column(db.String(200))
    machines = db.relationship('Machine', back_populates='sector', cascade='all, delete-orphan')

class Machine(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    serial = db.Column(db.String(120))
    brand = db.Column(db.String(120))
    sector_id = db.Column(db.Integer, db.ForeignKey('sectors.id'), nullable=False)
    image = db.Column(db.String(300))
    start_monitor_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='operational')  # e.g. operational, stopped
    sector = db.relationship('Sector', back_populates='machines')
    pieces = db.relationship('MachinePiece', back_populates='machine', cascade='all, delete-orphan')

class PartType(db.Model):
    __tablename__ = 'part_types'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True, nullable=False)   # ej. ROD-6300-2RS
    name = db.Column(db.String(120), nullable=False)               # ej. Rodamiento
    description = db.Column(db.Text)
    measurement = db.Column(db.String(80))                         # ej. 20x47x14
    expected_life_hours = db.Column(db.Float)                      # vida esperada (h)
    stock_items = db.relationship('StockItem', back_populates='part_type')

class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(300))

class StockItem(db.Model):
    __tablename__ = 'stock_items'
    id = db.Column(db.Integer, primary_key=True)
    part_type_id = db.Column(db.Integer, db.ForeignKey('part_types.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    quantity = db.Column(db.Integer, nullable=False, default=0)
    minimum = db.Column(db.Integer, nullable=False, default=1)
    location = db.Column(db.String(120))
    image = db.Column(db.String(300))
    notes = db.Column(db.Text)
    part_type = db.relationship('PartType', back_populates='stock_items')
    brand = db.relationship('Brand')
    supplier = db.relationship('Supplier')

class MachinePiece(db.Model):
    __tablename__ = 'machine_pieces'
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), nullable=False)
    part_type_id = db.Column(db.Integer, db.ForeignKey('part_types.id'), nullable=False)
    installed_brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    install_date = db.Column(db.DateTime, default=datetime.utcnow)
    usage_seconds = db.Column(db.Integer, nullable=False, default=0)   # segundos de uso acumulados
    expected_life_seconds = db.Column(db.Integer)                      # (rellenar desde PartType)
    status = db.Column(db.String(20), default='ok')                    # ok, near_replace, urgent, broken
    machine = db.relationship('Machine', back_populates='pieces')
    part_type = db.relationship('PartType')
    brand = db.relationship('Brand')
    maintenance_events = db.relationship('MaintenanceEvent', back_populates='piece',
                                         cascade='all, delete-orphan')
    sensors = db.relationship('Sensor', back_populates='piece', cascade='all, delete-orphan')

    def life_percentage(self):
        if not self.expected_life_seconds or self.expected_life_seconds == 0:
            return None
        return (self.usage_seconds / self.expected_life_seconds) * 100.0

class MaintenanceEvent(db.Model):
    __tablename__ = 'maintenance_events'
    id = db.Column(db.Integer, primary_key=True)
    piece_id = db.Column(db.Integer, db.ForeignKey('machine_pieces.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String(50))   # replaced, inspected, repaired
    notes = db.Column(db.Text)
    replaced_with_stock_item_id = db.Column(db.Integer, db.ForeignKey('stock_items.id'))
    time_used_seconds = db.Column(db.Integer)  # tiempo de uso que tuvo la pieza antes del evento
    piece = db.relationship('MachinePiece', back_populates='maintenance_events')
    replaced_with = db.relationship('StockItem')

class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    sensor_type = db.Column(db.String(80))   # temp, vibration, rpm...
    unit = db.Column(db.String(30))
    piece_id = db.Column(db.Integer, db.ForeignKey('machine_pieces.id'))
    piece = db.relationship('MachinePiece', back_populates='sensors')
    readings = db.relationship('SensorReading', back_populates='sensor', cascade='all, delete-orphan')

class SensorReading(db.Model):
    __tablename__ = 'sensor_readings'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    value = db.Column(db.Float)
    sensor = db.relationship('Sensor', back_populates='readings')
    __table_args__ = (db.Index('idx_sensor_timestamp', 'sensor_id', 'timestamp'),)  # Index for faster queries

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maintenance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return db   

# Example usage:
# from flask import Flask   
# app = Flask(__name__)
# db = init_db(app)     
# Now you can use db.session to interact with the database
# and the models defined above.
# For example:
# new_sector = Sector(name='Manufacturing', location='Building A')
# db.session.add(new_sector)    
# db.session.commit()
# Remember to handle exceptions and edge cases in a production environment.
# Also, consider adding more validations and constraints as per your requirements.
# This is a basic structure to get you started with a maintenance tracking system.
# You can expand upon this by adding more features like user authentication,
# reporting, notifications, etc.
# Always test your models and database interactions thoroughly.
# End of models/models.py
# models/models.py
