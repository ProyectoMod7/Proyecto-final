class Maquina:
    def __init__(self, id, nombre, ubicacion):
        self.id = id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.piezas = []

    def agregar_pieza(self, pieza):
        self.piezas.append(pieza)

    def estado_general(self):
        estados = [pieza.estado() for pieza in self.piezas]
        if "rojo" in estados:
            return "rojo"
        elif "amarillo" in estados:
            return "amarillo"
        return "verde"
