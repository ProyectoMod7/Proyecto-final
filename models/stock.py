from models.models import db

class Stock(db.Model):
    __tablename__ = "stock"

    id = db.Column(db.Integer, primary_key=True)
    pieza_id = db.Column(db.Integer, db.ForeignKey("piezas.id"), nullable=False)
    cantidad_actual = db.Column(db.Integer, default=0)
    minimo_requerido = db.Column(db.Integer, default=1)

    # Relación con pieza
    pieza = db.relationship("Pieza", back_populates="stock")

    def __repr__(self):
        return f"<Stock {self.pieza.nombre} - {self.cantidad_actual}>"
    def to_dict(self):
        return {
            "id": self.id,
            "pieza_id": self.pieza_id,
            "cantidad_actual": self.cantidad_actual,
            "minimo_requerido": self.minimo_requerido,
        }   
    def from_dict(self, data):
        for field in ["pieza_id", "cantidad_actual", "minimo_requerido"]:
            if field in data:
                setattr(self, field, data[field])   
        return self 
    def is_below_minimum(self):
        return self.cantidad_actual < self.minimo_requerido 
    def adjust_stock(self, cantidad):
        self.cantidad_actual += cantidad
        if self.cantidad_actual < 0:
            self.cantidad_actual = 0
        return self
    def set_minimo_requerido(self, minimo):
        if minimo < 0:
            minimo = 0
        self.minimo_requerido = minimo
        return self 
    def restock(self, cantidad):
        if cantidad > 0:
            self.cantidad_actual += cantidad
        return self
    def consume(self, cantidad):
        if cantidad > 0:
            self.cantidad_actual -= cantidad
            if self.cantidad_actual < 0:
                self.cantidad_actual = 0
        return self 
    def needs_restock(self):
        return self.cantidad_actual < self.minimo_requerido 
    def restock_to_minimum(self):
        if self.needs_restock():
            self.cantidad_actual = self.minimo_requerido
        return self     
    def clear_stock(self):
        self.cantidad_actual = 0
        return self 
    def increase_stock(self, cantidad):
        if cantidad > 0:
            self.cantidad_actual += cantidad
        return self 
    def decrease_stock(self, cantidad):
        if cantidad > 0:
            self.cantidad_actual -= cantidad
            if self.cantidad_actual < 0:
                self.cantidad_actual = 0
        return self 
    def update_from_dict(self, data):
        return self.from_dict(data) 
    def to_json(self):
        import json
        return json.dumps(self.to_dict())
    @staticmethod
    def from_json(json_str):
        import json
        data = json.loads(json_str)
        stock = Stock()
        return stock.from_dict(data)
    def clone(self):
        return Stock(
            pieza_id=self.pieza_id,
            cantidad_actual=self.cantidad_actual,
            minimo_requerido=self.minimo_requerido,
        )
    def summary(self):
        return f"Stock of {self.pieza.nombre}: {self.cantidad_actual} (Min: {self.minimo_requerido})"   
    def detailed_info(self):
        return {
            "id": self.id,
            "pieza": self.pieza.nombre if self.pieza else None,
            "cantidad_actual": self.cantidad_actual,
            "minimo_requerido": self.minimo_requerido,
            "is_below_minimum": self.is_below_minimum(),
        }   
    def __str__(self):
        return f"Stock(id={self.id}, pieza_id={self.pieza_id}, cantidad_actual={self.cantidad_actual}, minimo_requerido={self.minimo_requerido})"   
    def __eq__(self, other):
        if not isinstance(other, Stock):
            return False
        return (
            self.id == other.id and
            self.pieza_id == other.pieza_id and
            self.cantidad_actual == other.cantidad_actual and
            self.minimo_requerido == other.minimo_requerido
        )