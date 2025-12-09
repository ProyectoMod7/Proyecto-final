# routes/maquinas_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from supabase_client import supabase

maquinas_bp = Blueprint("maquinas", __name__, url_prefix="/maquinas")

@maquinas_bp.route("/", methods=["GET"])
def index():
    res = supabase.table("maquinas").select("*").order("id", desc=False).execute()
    maquinas = res.data or []
    return render_template("maquinas/index.html", maquinas=maquinas)

@maquinas_bp.route("/crear", methods=["GET","POST"])
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
    # GET -> formulario
    # opcional: cargar areas para select
    areas = (supabase.table("areas").select("*").order("nombre").execute().data) or []
    return render_template("maquinas/form.html", maquina=None, areas=areas)

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
    # GET -> obtener datos existentes
    r = supabase.table("maquinas").select("*").eq("id", id).single().execute()
    maquina = r.data

    if not maquina:
        flash("Máquina no encontrada", "warning")
        return redirect(url_for("maquinas.index"))

    areas = (supabase.table("areas").select("*").order("nombre").execute().data) or []
    return render_template("maquinas/form.html", maquina=maquina, areas=areas)

@maquinas_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    supabase.table("maquinas").delete().eq("id", id).execute()
    flash("Máquina eliminada", "info")
    return redirect(url_for("maquinas.index"))

from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from datetime import datetime


@maquinas_bp.route("/pdf_reporte")
def pdf_reporte():
    # Traer datos desde Supabase
    try:
        response = supabase.table("maquinas").select("*").execute()
        maquinas = response.data
    except Exception as e:
        maquinas = []

    # Crear PDF en memoria
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Título del reporte
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 750, "Reporte de Máquinas")

    # Fecha y hora actual
    p.setFont("Helvetica", 10)
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    p.drawString(50, 730, f"Generado el: {fecha_hora}")

    # Verificar si hay datos
    y = 700
    p.setFont("Helvetica", 10)
    if not maquinas:
        p.drawString(50, y, "ATENCIÓN: No hay datos de máquinas para mostrar.")
    else:
        for m in maquinas:
            descripcion = (m.get("descripcion") or "").replace("\n", " ")
            linea = f"ID: {m.get('id', '')} | Nombre: {m.get('nombre', '')} | Desc: {descripcion}"
            # Truncar línea para evitar desbordes
            max_len = 120
            if len(linea) > max_len:
                linea = linea[: max_len - 3] + "..."
            p.drawString(50, y, linea)
            y -= 20
            if y < 60:  # salto de página si se llena
                p.showPage()
                # redraw header on new page
                p.setFont("Helvetica-Bold", 16)
                p.drawString(200, 750, "Reporte de Máquinas")
                p.setFont("Helvetica", 10)
                p.drawString(50, 730, f"Generado el: {fecha_hora}")
                y = 700

    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="reporte_maquinas.pdf", mimetype="application/pdf")
