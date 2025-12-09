from flask import Blueprint, render_template, request, redirect, url_for, flash
from supabase_client import supabase
from datetime import datetime, date
from helpers.piezas_estado import calcular_estado_pieza, calcular_estado_maquina

piezas_instaladas_bp = Blueprint("piezas_instaladas", __name__, url_prefix="/piezas_instaladas")


# 📌 1) LISTAR piezas instaladas de una máquina específica
@piezas_instaladas_bp.route("/maquina/<int:maquina_id>")
def listar_por_maquina(maquina_id):
    # Obtener datos de la máquina
    maquina = supabase.table("maquinas").select("*").eq("id", maquina_id).single().execute().data

    if not maquina:
        flash("Máquina no encontrada", "warning")
        return redirect(url_for("maquinas.index"))

    # Obtener piezas instaladas
    res = (
        supabase.table("piezas_instaladas")
        .select("*")
        .eq("maquina_id", maquina_id)
        .order("id", desc=False)
        .execute()
    )
    piezas = res.data or []

    # Obtener listado de piezas (catálogo)
    catalogo = supabase.table("piezas").select("*").execute().data or []
    dict_catalogo = {p["id"]: p for p in catalogo}

    # Calcular estado de cada pieza
    piezas_info = []
    for p in piezas:
        pieza_catalogo = dict_catalogo.get(p["pieza_id"], {})
        estado = calcular_estado_pieza(p)

        piezas_info.append({
            "id": p["id"],
            "nombre": pieza_catalogo.get("nombre", "Pieza desconocida"),
            "fecha_instalacion": p["fecha_instalacion"],
            "vida_dias": p["vida_dias"],
            "rota": p["rota"],
            "notas": p.get("notas", ""),
            "dias_restantes": estado["dias_restantes"],
            "estado_color": estado["estado_color"],
            "estado_texto": estado["estado_texto"]
        })

    # Estado general de la máquina
    estado_maquina = calcular_estado_maquina(piezas_info)

    return render_template(
        "piezas_instaladas/lista_por_maquina.html",
        maquina=maquina,
        piezas=piezas_info,
        estado_maquina=estado_maquina
    )


# 📌 2) CREAR pieza instalada
@piezas_instaladas_bp.route("/crear/<int:maquina_id>", methods=["GET", "POST"])
def crear(maquina_id):
    if request.method == "POST":
        pieza_id = request.form.get("pieza_id")
        fecha_instalacion = request.form.get("fecha_instalacion")
        vida_dias = request.form.get("vida_dias")
        notas = request.form.get("notas")

        supabase.table("piezas_instaladas").insert({
            "maquina_id": maquina_id,
            "pieza_id": pieza_id,
            "fecha_instalacion": fecha_instalacion,
            "vida_dias": vida_dias,
            "rota": False,
            "notas": notas
        }).execute()

        flash("Pieza instalada correctamente", "success")
        return redirect(url_for("piezas_instaladas.listar_por_maquina", maquina_id=maquina_id))

    # GET
    piezas = supabase.table("piezas").select("*").execute().data
    return render_template("piezas_instaladas/form.html", piezas=piezas, maquina_id=maquina_id, pieza=None)


# 📌 3) EDITAR pieza instalada
@piezas_instaladas_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    # Obtener pieza instalada
    pieza = supabase.table("piezas_instaladas").select("*").eq("id", id).single().execute().data

    if not pieza:
        flash("Pieza no encontrada", "warning")
        return redirect(url_for("maquinas.index"))

    maquina_id = pieza["maquina_id"]

    if request.method == "POST":
        fecha_instalacion = request.form.get("fecha_instalacion")
        vida_dias = request.form.get("vida_dias")
        notas = request.form.get("notas")
        rota = request.form.get("rota") == "on"

        supabase.table("piezas_instaladas").update({
            "fecha_instalacion": fecha_instalacion,
            "vida_dias": vida_dias,
            "rota": rota,
            "notas": notas
        }).eq("id", id).execute()

        flash("Pieza actualizada", "success")
        return redirect(url_for("piezas_instaladas.listar_por_maquina", maquina_id=maquina_id))

    piezas = supabase.table("piezas").select("*").execute().data

    return render_template("piezas_instaladas/form.html", pieza=pieza, piezas=piezas, maquina_id=maquina_id)


# 📌 4) ELIMINAR pieza instalada
@piezas_instaladas_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    pieza = supabase.table("piezas_instaladas").select("*").eq("id", id).single().execute().data

    if not pieza:
        flash("Pieza no encontrada", "warning")
        return redirect(url_for("maquinas.index"))

    maquina_id = pieza["maquina_id"]

    supabase.table("piezas_instaladas").delete().eq("id", id).execute()

    flash("Pieza eliminada", "info")
    return redirect(url_for("piezas_instaladas.listar_por_maquina", maquina_id=maquina_id))
