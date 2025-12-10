# helpers/piezas_estado.py
from datetime import datetime, date

# ----------------------------
# Normalizador de fecha seguro
# ----------------------------
def normalizar_fecha(fecha):
    if fecha is None:
        return None

    # string: "YYYY-MM-DD"
    if isinstance(fecha, str):
        try:
            return datetime.strptime(fecha[:10], "%Y-%m-%d").date()
        except:
            pass

    # date ya válido
    if isinstance(fecha, date):
        return fecha

    # datetime
    if isinstance(fecha, datetime):
        return fecha.date()

    # dict del tipo {"year": 2025, "month": 1, "day": 15}
    if isinstance(fecha, dict):
        try:
            return date(
                fecha.get("year"),
                fecha.get("month"),
                fecha.get("day")
            )
        except:
            pass

    raise ValueError(f"Formato de fecha no reconocido: {fecha}")


# ----------------------------
# Estado de pieza instalada
# ----------------------------
def calcular_estado_pieza(p):
    """
    p es un diccionario con:
    - fecha_instalacion
    - vida_dias
    - rota
    - fecha_caducidad (opcional)
    """

    fecha_inst = p.get("fecha_instalacion")
    vida_dias = int(p.get("vida_dias") or 0)
    roto = p.get("rota", False)

    fecha_inst = normalizar_fecha(fecha_inst)

    if not fecha_inst:
        return {
            "dias_restantes": None,
            "estado_color": "black",
            "estado_texto": "Sin fecha"
        }

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

    # 20% restante = amarillo
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


# ----------------------------
# Estado general de máquina
# ----------------------------
def calcular_estado_maquina(lista_piezas):
    if not lista_piezas:
        return {
            "estado_texto": "Sin piezas",
            "estado_color": "gray"
        }

    colores = [p.get("estado_color") for p in lista_piezas]

    if "black" in colores:
        return {"estado_texto": "Pieza rota", "estado_color": "black"}

    if "red" in colores:
        return {"estado_texto": "Vencida", "estado_color": "red"}

    if "yellow" in colores:
        return {"estado_texto": "Advertencia", "estado_color": "yellow"}

    return {"estado_texto": "Óptima", "estado_color": "green"}
