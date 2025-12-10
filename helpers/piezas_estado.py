from datetime import datetime, date

def calcular_estado_pieza(fecha_caducidad: date):
    hoy = date.today()
    dias_restantes = (fecha_caducidad - hoy).days

    if dias_restantes >= 30:
        return dias_restantes, "verde", "En buen estado"
    elif dias_restantes >= 7:
        return dias_restantes, "amarillo", "Pronto a mantenimiento"
    elif dias_restantes >= 0:
        return dias_restantes, "rojo", "Mantenimiento urgente"
    else:
        return dias_restantes, "gris", "Vencida"


"""
def calcular_estado_pieza(p):
    ###  Devuelve estado de una pieza instalada: dias restantes, color, texto

    fecha_inst = p.get("fecha_instalacion")
    vida_dias = int(p.get("vida_dias") or 0)
    roto = p.get("rota", False)

    if fecha_inst:
        fecha_inst = datetime.fromisoformat(fecha_inst.replace("Z", "")).date()
    else:
        return {"dias_restantes": None, "estado_color": "black", "estado_texto": "Sin datos"}

    hoy = date.today()
    dias_usados = (hoy - fecha_inst).days
    dias_restantes = vida_dias - dias_usados

    # PIEZA ROTA
    if roto:
        return {
            "dias_restantes": dias_restantes,
            "estado_color": "black",
            "estado_texto": "ROTA"
        }

    # VENCIDA
    if dias_restantes <= 0:
        return {
            "dias_restantes": dias_restantes,
            "estado_color": "red",
            "estado_texto": "VENCIDA"
        }

    # MENOS DE 20% DE VIDA = AMARILLO
    if dias_restantes <= vida_dias * 0.20:
        return {
            "dias_restantes": dias_restantes,
            "estado_color": "yellow",
            "estado_texto": "ADVERTENCIA"
        }

    # OK
    return {
        "dias_restantes": dias_restantes,
        "estado_color": "green",
        "estado_texto": "OK"
    }
"""

def calcular_estado_maquina(lista_piezas):
    """
    Devuelve un diccionario con:
    - estado_texto
    - estado_color
    """

    if not lista_piezas:
        return {
            "estado_texto": "Sin piezas",
            "estado_color": "gray"
        }

    colores = [p.get("estado_color") for p in lista_piezas]

    # PRIORIDAD: black > red > yellow > green
    if "black" in colores:
        return {
            "estado_texto": "Pieza rota",
            "estado_color": "black"
        }

    if "red" in colores:
        return {
            "estado_texto": "Vencida",
            "estado_color": "red"
        }

    if "yellow" in colores:
        return {
            "estado_texto": "Advertencia",
            "estado_color": "yellow"
        }

    return {
        "estado_texto": "Óptima",
        "estado_color": "green"
    }
