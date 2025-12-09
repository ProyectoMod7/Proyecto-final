# routes/maquinas_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from supabase_client import supabase
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from datetime import datetime

# Declaración correcta del Blueprint (una sola vez)
maquinas_bp = Blueprint("maquinas", __name__, url_prefix="/maquinas")


# ===========================
# LISTAR MÁQUINAS
# ===========================
from helpers.piezas_estado import calcular_estado_maquina, calcular_estado_pieza

@maquinas_bp.route("/")
def index():
    # Todas las máquinas
    maquinas = supabase.table("maquinas").select("*").execute().data or []

    # Todas las piezas instaladas (para agrupar por máquina)
    piezas_inst = supabase.table("piezas_instaladas").select("*").execute().data or []

    # Agrupar piezas por máquina
    piezas_por_maquina = {}
    for p in piezas_inst:
        piezas_por_maquina.setdefault(p["maquina_id"], []).append(p)

    maquinas_final = []

    for m in maquinas:
        piezas = piezas_por_maquina.get(m["id"], [])

        piezas_info = []
        for p in piezas:
            estado_p = calcular_estado_pieza(p)
            piezas_info.append({
            "dias_restantes": estado_p.get("dias_restantes"),
            "estado_color": estado_p.get("estado_color"),
            "estado_texto": estado_p.get("estado_texto"),
            "rota": p.get("rota", False)
            })

        # Estado general de la máquina
        estado = calcular_estado_maquina(piezas_info)

        # Por seguridad: si la función devolviera un string por accidente, lo normalizamos
        if isinstance(estado, dict):
            estado_texto = estado.get("estado_texto", "Sin datos")
            estado_color = estado.get("estado_color", "gray")
        else:
            # fallback seguro
            estado_texto = str(estado)
            estado_color = "gray"

        # Agregar info de piezas al diccionario de la máquina
        m["estado"] = estado_texto
        m["estado_color"] = estado_color
        m["piezas"] = piezas_info

        maquinas_final.append(m)

    return render_template("maquinas/index.html", maquinas=maquinas_final)

# ===========================
# CREAR
# ===========================
@maquinas_bp.route("/crear", methods=["GET","POST"])
def crear():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        marca = request.form.get("marca")
        modelo = request.form.get("modelo")
        nro_serie = request.form.get("nro_serie")
        area_id = request.form.get("area_id") or None
        descripcion = request.form.get("descripcion") or ""

        supabase.table("maquinas").insert({
            "nombre": nombre,
            "marca": marca,
            "modelo": modelo,
            "nro_serie": nro_serie,
            "area_id": area_id,
            "descripcion": descripcion
        }).execute()

        flash("Máquina creada", "success")
        return redirect(url_for("maquinas.index"))

    areas = (supabase.table("areas").select("*").order("nombre").execute().data) or []
    return render_template("maquinas/form.html", maquina=None, areas=areas)


# ===========================
# EDITAR
# ===========================
@maquinas_bp.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):
    if request.method == "POST":
        nombre = request.form.get("nombre")
        marca = request.form.get("marca")
        modelo = request.form.get("modelo")
        nro_serie = request.form.get("nro_serie")
        area_id = request.form.get("area_id") or None
        descripcion = request.form.get("descripcion") or ""

        supabase.table("maquinas").update({
            "nombre": nombre,
            "marca": marca,
            "modelo": modelo,
            "nro_serie": nro_serie,
            "area_id": area_id,
            "descripcion": descripcion
        }).eq("id", id).execute()

        flash("Máquina actualizada", "success")
        return redirect(url_for("maquinas.index"))

    r = supabase.table("maquinas").select("*").eq("id", id).single().execute()
    maquina = r.data

    if not maquina:
        flash("Máquina no encontrada", "warning")
        return redirect(url_for("maquinas.index"))

    areas = (supabase.table("areas").select("*").order("nombre").execute().data) or []
    return render_template("maquinas/form.html", maquina=maquina, areas=areas)


# ===========================
# ELIMINAR
# ===========================
@maquinas_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    supabase.table("maquinas").delete().eq("id", id).execute()
    flash("Máquina eliminada", "info")
    return redirect(url_for("maquinas.index"))


# ===========================
# GENERAR PDF
# ===========================
@maquinas_bp.route("/pdf_reporte")
def pdf_reporte():

    try:
        response = supabase.table("maquinas").select("*").execute()
        maquinas = response.data
    except Exception:
        maquinas = []

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 750, "Reporte de Máquinas")

    p.setFont("Helvetica", 10)
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    p.drawString(50, 730, f"Generado el: {fecha_hora}")

    y = 700
    p.setFont("Helvetica", 10)

    if not maquinas:
        p.drawString(50, y, "ATENCIÓN: No hay datos de máquinas para mostrar.")
    else:
        for m in maquinas:
            descripcion = (m.get("descripcion") or "").replace("\n", " ")
            linea = f"ID: {m.get('id','')} | Nombre: {m.get('nombre','')} | Desc: {descripcion}"

            if len(linea) > 120:
                linea = linea[:117] + "..."

            p.drawString(50, y, linea)
            y -= 20

            if y < 60:
                p.showPage()
                p.setFont("Helvetica-Bold", 16)
                p.drawString(200, 750, "Reporte de Máquinas")
                p.setFont("Helvetica", 10)
                p.drawString(50, 730, f"Generado el: {fecha_hora}")
                y = 700

    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="reporte_maquinas.pdf", mimetype="application/pdf")
