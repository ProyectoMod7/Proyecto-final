from datetime import datetime, date

def calcular_estado_pieza(p):
    """Devuelve estado de una pieza instalada: dias restantes, color, texto."""

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


def calcular_estado_maquina(lista_piezas):
    """
    Devuelve estado general de la máquina según sus piezas.
    Prioridad:
    negro > rojo > amarillo > verde
    """

    colores = [p["estado_color"] for p in lista_piezas]

    if "black" in colores:
        return "black"
    if "red" in colores:
        return "red"
    if "yellow" in colores:
        return "yellow"
    return "green"
