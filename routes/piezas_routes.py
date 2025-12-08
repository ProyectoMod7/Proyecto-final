# routes/piezas_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from supabase_client import supabase

piezas_bp = Blueprint("piezas", __name__, url_prefix="/piezas")

@piezas_bp.route("/", methods=["GET"])
def index():
    res = supabase.table("piezas").select("*").order("id", desc=False).execute()
    piezas = res.data or []
    # enriquecer con fabricante y material
    for pz in piezas:
        # Fabricante
        fabricante_id = pz.get("fabricante_id")
        if fabricante_id:
            fab_res = supabase.table("fabricantes").select("nombre").eq("id", fabricante_id).single().execute()
            nombre_fabricante = fab_res.data.get("nombre") if fab_res and fab_res.data else "Desconocido"
        else:
            nombre_fabricante = "Sin fabricante"

        # Material
        material_id = pz.get("material_id")
        if material_id:
            mat_res = supabase.table("materiales").select("nombre").eq("id", material_id).single().execute()
            nombre_material = mat_res.data.get("nombre") if mat_res and mat_res.data else "Desconocido"
        else:
            nombre_material = "Sin material"

        pz["fabricante"] = nombre_fabricante
        pz["material"] = nombre_material

    return render_template("piezas/index.html", piezas=piezas)

@piezas_bp.route("/crear", methods=["GET","POST"])
def crear():
    if request.method == "POST":
        data = {
            "nombre": request.form.get("nombre"),
            "fabricante_id": request.form.get("fabricante_id") or None,
            "material_id": request.form.get("material_id") or None,
            "vida_horas": request.form.get("vida_horas") or None,
            "imagen_url": request.form.get("imagen_url") or None
        }
        supabase.table("piezas").insert(data).execute()
        flash("Pieza creada", "success")
        return redirect(url_for("piezas.index"))
    fabricantes = supabase.table("fabricantes").select("*").order("nombre").execute().data or []
    materiales = supabase.table("materiales").select("*").order("nombre").execute().data or []
    return render_template("piezas/form.html", pieza=None, fabricantes=fabricantes, materiales=materiales)

@piezas_bp.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):
    if request.method == "POST":
        data = {
            "nombre": request.form.get("nombre"),
            "fabricante_id": request.form.get("fabricante_id") or None,
            "material_id": request.form.get("material_id") or None,
            "vida_horas": request.form.get("vida_horas") or None,
            "imagen_url": request.form.get("imagen_url") or None
        }
        supabase.table("piezas").update(data).eq("id", id).execute()
        flash("Pieza actualizada", "success")
        return redirect(url_for("piezas.index"))
    pieza = supabase.table("piezas").select("*").eq("id", id).single().execute().data
    fabricantes = supabase.table("fabricantes").select("*").order("nombre").execute().data or []
    materiales = supabase.table("materiales").select("*").order("nombre").execute().data or []
    return render_template("piezas/form.html", pieza=pieza, fabricantes=fabricantes, materiales=materiales)

@piezas_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    supabase.table("piezas").delete().eq("id", id).execute()
    flash("Pieza eliminada", "info")
    return redirect(url_for("piezas.index"))

from flask import send_file
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

@piezas_bp.route("/pdf_reporte")
def pdf_reporte():
    # Traer datos desde Supabase
    try:
        response = supabase.table("piezas").select("*").execute()
        piezas = response.data
    except Exception as e:
        piezas = []

    # Crear PDF en memoria
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Título del reporte
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 750, "Reporte de Piezas")

    # Fecha y hora actual
    p.setFont("Helvetica", 10)
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    p.drawString(50, 730, f"Generado el: {fecha_hora}")

    # Verificar si hay datos
    y = 700
    if not piezas:
        p.drawString(50, y, "⚠ No hay datos de piezas para mostrar.")
    else:
        for pz in piezas:
            p.drawString(
                50, y,
                f"ID: {pz['id']} | Nombre: {pz['nombre']} | Vida útil: {pz.get('vida_util', 'N/A')} días"
            )
            y -= 20
            if y < 50:  # salto de página si se llena
                p.showPage()
                y = 750

    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="reporte_piezas.pdf", mimetype="application/pdf")
