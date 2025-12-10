from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from supabase_client import supabase
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

piezas_bp = Blueprint("piezas", __name__, url_prefix="/piezas")

# =====================================================
#   INDEX – LISTA DE PIEZAS (CATÁLOGO)
# =====================================================
@piezas_bp.route("/", methods=["GET"])
def index():
    res = supabase.table("piezas").select("*").order("id", desc=False).execute()
    piezas = res.data or []

    # Obtener nombres adicionales (fabricante / material)
    for pz in piezas:

        # Fabricante
        if pz.get("fabricante_id"):
            fab = supabase.table("fabricantes").select("nombre") \
                  .eq("id", pz["fabricante_id"]).single().execute()
            pz["fabricante"] = fab.data.get("nombre") if fab and fab.data else "Desconocido"
        else:
            pz["fabricante"] = "N/A"

        # Material
        if pz.get("material_id"):
            mat = supabase.table("materiales").select("nombre") \
                  .eq("id", pz["material_id"]).single().execute()
            pz["material"] = mat.data.get("nombre") if mat and mat.data else "Desconocido"
        else:
            pz["material"] = "N/A"

    return render_template("piezas/index.html", piezas=piezas)


# =====================================================
#   CREAR PIEZA DEL CATÁLOGO
# =====================================================
@piezas_bp.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        data = {
            "nombre": request.form.get("nombre"),
            "sku": request.form.get("sku") or None,
            "descripcion": request.form.get("descripcion") or None,
            "fabricante_id": request.form.get("fabricante_id") or None,
            "material_id": request.form.get("material_id") or None,
            "vida_dias": int(request.form.get("vida_dias") or 0),
            "unidad": request.form.get("unidad") or None,
            "imagen_url": request.form.get("imagen_url") or None
        }

        supabase.table("piezas").insert(data).execute()
        flash("Pieza creada con éxito", "success")
        return redirect(url_for("piezas.index"))

    fabricantes = supabase.table("fabricantes").select("*").order("nombre").execute().data or []
    materiales = supabase.table("materiales").select("*").order("nombre").execute().data or []

    return render_template("piezas/form.html",
                           pieza=None,
                           fabricantes=fabricantes,
                           materiales=materiales)


# =====================================================
#   EDITAR PIEZA DEL CATÁLOGO
# =====================================================
@piezas_bp.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):
    if request.method == "POST":
        data = {
            "nombre": request.form.get("nombre"),
            "sku": request.form.get("sku") or None,
            "descripcion": request.form.get("descripcion") or None,
            "fabricante_id": request.form.get("fabricante_id") or None,
            "material_id": request.form.get("material_id") or None,
            "vida_dias": int(request.form.get("vida_dias") or 0),
            "unidad": request.form.get("unidad") or None,
            "imagen_url": request.form.get("imagen_url") or None
        }

        supabase.table("piezas").update(data).eq("id", id).execute()
        flash("Pieza actualizada", "success")
        return redirect(url_for("piezas.index"))

    pieza = supabase.table("piezas").select("*").eq("id", id).single().execute().data
    fabricantes = supabase.table("fabricantes").select("*").order("nombre").execute().data or []
    materiales = supabase.table("materiales").select("*").order("nombre").execute().data or []

    return render_template("piezas/form.html",
                           pieza=pieza,
                           fabricantes=fabricantes,
                           materiales=materiales)


# =====================================================
#   ELIMINAR PIEZA
# =====================================================
@piezas_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    supabase.table("piezas").delete().eq("id", id).execute()
    flash("Pieza eliminada", "info")
    return redirect(url_for("piezas.index"))


# =====================================================
#   PDF LISTA DE MODELOS DE PIEZA
# =====================================================
@piezas_bp.route("/pdf_reporte")
def pdf_reporte():
    response = supabase.table("piezas").select("*").execute()
    piezas = response.data or []
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, 750, "Catálogo de Piezas")

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    p.setFont("Helvetica", 10)
    p.drawString(50, 730, f"Generado el: {fecha_hora}")

    y = 700

    if not piezas:
        p.drawString(50, y, "⚠ No hay piezas registradas.")
    else:
        for pz in piezas:
            p.drawString(
                50, y,
                f"ID:{pz['id']} | {pz.get('nombre')} | SKU:{pz.get('sku')} | Vida:{pz.get('vida_dias')} días"
            )
            y -= 18

            if y < 50:
                p.showPage()
                y = 750

    p.save()
    buffer.seek(0)
    return send_file(buffer,
                     as_attachment=True,
                     download_name="piezas_catalogo.pdf",
                     mimetype="application/pdf")
