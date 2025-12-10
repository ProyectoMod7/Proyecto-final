from flask import Blueprint, render_template, request, redirect, url_for, flash
from supabase_client import supabase
from datetime import datetime, timedelta
from helpers.piezas_estado import calcular_estado_pieza, calcular_estado_maquina

piezas_instaladas_bp = Blueprint("piezas_instaladas", __name__, url_prefix="/piezas_instaladas")


# ============================================================
# 1) LISTAR piezas instaladas de una máquina
# ============================================================
@piezas_instaladas_bp.route("/maquina/<int:maquina_id>")
def listar_por_maquina(maquina_id):

    maquina = supabase.table("maquinas").select("*").eq("id", maquina_id).single().execute().data
    if not maquina:
        flash("Máquina no encontrada", "warning")
        return redirect(url_for("maquinas.index"))

    piezas_inst = (
        supabase.table("piezas_instaladas")
        .select("*")
        .eq("maquina_id", maquina_id)
        .order("id")
        .execute()
        .data
        or []
    )

    catalogo = {p["id"]: p for p in supabase.table("piezas").select("*").execute().data or []}

    piezas_info = []
    for p in piezas_inst:
        piezacat = catalogo.get(p["pieza_id"], {})
        estado = calcular_estado_pieza(p)

        piezas_info.append({
            "id": p["id"],
            "nombre": piezacat.get("nombre", "Pieza desconocida"),
            "fecha_instalacion": p["fecha_instalacion"],
            "vida_dias": p["vida_dias"],
            "rota": p.get("rota", False),
            "notas": p.get("notas", ""),
            "dias_restantes": estado["dias_restantes"],
            "estado_color": estado["estado_color"],
            "estado_texto": estado["estado_texto"],
        })

    estado_maquina = calcular_estado_maquina(piezas_info)

    return render_template(
        "piezas_instaladas/lista_por_maquina.html",
        maquina=maquina,
        piezas=piezas_info,
        estado_maquina=estado_maquina,
    )


# ============================================================
# 2) CREAR pieza instalada (instalar pieza en máquina)
# ============================================================
@piezas_instaladas_bp.route("/crear/<int:maquina_id>", methods=["GET", "POST"])
def crear(maquina_id):

    # validar máquina
    maquina = supabase.table("maquinas").select("*").eq("id", maquina_id).single().execute().data
    if not maquina:
        flash("Máquina no encontrada", "warning")
        return redirect(url_for("maquinas.index"))

    if request.method == "POST":

        pieza_id = int(request.form.get("pieza_id"))
        fecha_inst = request.form.get("fecha_instalacion")
        notas = request.form.get("notas") or ""

        # obtener vida útil desde el catálogo piezas
        pieza_cat = supabase.table("piezas").select("*").eq("id", pieza_id).single().execute().data
        vida_dias = pieza_cat.get("vida_dias", 0)

        # comprobar stock disponible
        stock_reg = supabase.table("stock").select("*").eq("pieza_id", pieza_id).single().execute().data
        if not stock_reg or stock_reg["cantidad"] <= 0:
            flash("No hay stock disponible de esta pieza.", "danger")
            return redirect(url_for("piezas_instaladas.crear", maquina_id=maquina_id))

        # restar 1 de stock
        supabase.table("stock").update({
            "cantidad": stock_reg["cantidad"] - 1
        }).eq("id", stock_reg["id"]).execute()

        # calcular fecha caducidad
        fecha_inst_dt = datetime.strptime(fecha_inst, "%Y-%m-%d").date()
        fecha_cad = fecha_inst_dt + timedelta(days=vida_dias)

        # guardar pieza instalada
        supabase.table("piezas_instaladas").insert({
            "maquina_id": maquina_id,
            "pieza_id": pieza_id,
            "fecha_instalacion": fecha_inst,
            "vida_dias": vida_dias,
            "fecha_caducidad": fecha_cad.strftime("%Y-%m-%d"),
            "rota": False,
            "notas": notas
        }).execute()

        flash("Pieza instalada correctamente", "success")
        return redirect(url_for("piezas_instaladas.listar_por_maquina", maquina_id=maquina_id))

    piezas = supabase.table("piezas").select("*").order("nombre").execute().data
    return render_template("piezas_instaladas/form.html", piezas=piezas, maquina_id=maquina_id, pieza=None)


# ============================================================
# 3) EDITAR pieza instalada (actualizar fecha, notas, etc)
# ============================================================
@piezas_instaladas_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    pieza = supabase.table("piezas_instaladas").select("*").eq("id", id).single().execute().data
    if not pieza:
        flash("Pieza no encontrada", "warning")
        return redirect(url_for("maquinas.index"))

    maquina_id = pieza["maquina_id"]

    if request.method == "POST":

        fecha_inst = request.form.get("fecha_instalacion")
        vida_dias = int(request.form.get("vida_dias"))
        notas = request.form.get("notas")
        rota = request.form.get("rota") == "on"

        fecha_inst_dt = datetime.strptime(fecha_inst, "%Y-%m-%d").date()
        fecha_cad = fecha_inst_dt + timedelta(days=vida_dias)

        supabase.table("piezas_instaladas").update({
            "fecha_instalacion": fecha_inst,
            "vida_dias": vida_dias,
            "fecha_caducidad": fecha_cad.strftime("%Y-%m-%d"),
            "rota": rota,
            "notas": notas
        }).eq("id", id).execute()

        flash("Pieza actualizada", "success")
        return redirect(url_for("piezas_instaladas.listar_por_maquina", maquina_id=maquina_id))

    piezas = supabase.table("piezas").select("*").execute().data
    return render_template("piezas_instaladas/form.html", pieza=pieza, piezas=piezas, maquina_id=maquina_id)


# ============================================================
# 4) ELIMINAR pieza instalada
# ============================================================
@piezas_instaladas_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):

    pieza = supabase.table("piezas_instaladas").select("*").eq("id", id).single().execute().data
    if not pieza:
        flash("Pieza no encontrada", "warning")
        return redirect(url_for("maquinas.index"))

    maquina_id = pieza["maquina_id"]

    # opcional: devolver 1 unidad al stock
    stock_reg = supabase.table("stock").select("*").eq("pieza_id", pieza["pieza_id"]).single().execute().data
    if stock_reg:
        supabase.table("stock").update({
            "cantidad": stock_reg["cantidad"] + 1
        }).eq("id", stock_reg["id"]).execute()

    supabase.table("piezas_instaladas").delete().eq("id", id).execute()

    flash("Pieza eliminada", "info")
    return redirect(url_for("piezas_instaladas.listar_por_maquina", maquina_id=maquina_id))
