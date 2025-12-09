# routes/piezas_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from supabase_client import supabase
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime, date

piezas_bp = Blueprint("piezas", __name__, url_prefix="/piezas")

# ============================
#   INDEX – LISTA DE PIEZAS
# ============================
@piezas_bp.route("/", methods=["GET"])
def index():
    res = supabase.table("piezas").select("*").order("id", desc=False).execute()
    piezas = res.data or []

    hoy = date.today()

    for pz in piezas:
        # --- FABRICANTE ---
        fabricante_id = pz.get("fabricante_id")
        if fabricante_id:
            fab_res = supabase.table("fabricantes").select("nombre").eq("id", fabricante_id).single().execute()
            pz["fabricante"] = fab_res.data.get("nombre") if fab_res and fab_res.data else "Desconocido"
        else:
            pz["fabricante"] = "Sin fabricante"

        # --- MATERIAL ---
        material_id = pz.get("material_id")
        if material_id:
            mat_res = supabase.table("materiales").select("nombre").eq("id", material_id).single().execute()
            pz["material"] = mat_res.data.get("nombre") if mat_res and mat_res.data else "Desconocido"
        else:
            pz["material"] = "Sin material"

        # --- CALCULAR VIDA RESTANTE ---
        vida = pz.get("vida_dias") or 0
        fecha_inst = pz.get("fecha_instalacion")

        if fecha_inst:
            fecha_inst = datetime.strptime(fecha_inst, "%Y-%m-%d").date()
            dias_usados = (hoy - fecha_inst).days
        else:
            dias_usados = 0

        dias_restantes = vida - dias_usados

        # Estado visual
        if dias_restantes > vida * 0.3:
            estado = "🟢 OK"
        elif dias_restantes > 0:
            estado = "🟡 Próximo a vencer"
        else:
            estado = "🔴 Vencido"

        pz["dias_usados"] = dias_usados
        pz["dias_restantes"] = dias_restantes
        pz["estado"] = estado

    return render_template("piezas/index.html", piezas=piezas)

# ============================
#   CREAR PIEZA
# ============================
@piezas_bp.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        fecha_inst = request.form.get("fecha_instalacion")
        if not fecha_inst:  # Si no cargó fecha → usar hoy
            fecha_inst = date.today().strftime("%Y-%m-%d")

        data = {
            "nombre": request.form.get("nombre"),
            "fabricante_id": request.form.get("fabricante_id") or None,
            "material_id": request.form.get("material_id") or None,
            "vida_dias": request.form.get("vida_dias") or None,
            "imagen_url": request.form.get("imagen_url") or None,
            "fecha_instalacion": fecha_inst
        }

        supabase.table("piezas").insert(data).execute()
        flash("Pieza creada con éxito", "success")
        return redirect(url_for("piezas.index"))

    fabricantes = supabase.table("fabricantes").select("*").order("nombre").execute().data or []
    materiales = supabase.table("materiales").select("*").order("nombre").execute().data or []
    return render_template("piezas/form.html", pieza=None, fabricantes=fabricantes, materiales=materiales)

# ============================
#   EDITAR PIEZA
# ============================
@piezas_bp.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):
    if request.method == "POST":
        fecha_inst = request.form.get("fecha_instalacion")
        if not fecha_inst:
            fecha_inst = date.today().strftime("%Y-%m-%d")

        data = {
            "nombre": request.form.get("nombre"),
            "fabricante_id": request.form.get("fabricante_id") or None,
            "material_id": request.form.get("material_id") or None,
            "vida_dias": request.form.get("vida_dias") or None,
            "imagen_url": request.form.get("imagen_url") or None,
            "fecha_instalacion": fecha_inst
        }

        supabase.table("piezas").update(data).eq("id", id).execute()
        flash("Pieza actualizada", "success")
        return redirect(url_for("piezas.index"))

    pieza = supabase.table("piezas").select("*").eq("id", id).single().execute().data
    fabricantes = supabase.table("fabricantes").select("*").order("nombre").execute().data or []
    materiales = supabase.table("materiales").select("*").order("nombre").execute().data or []

    return render_template("piezas/form.html", pieza=pieza, fabricantes=fabricantes, materiales=materiales)

# ============================
#   ELIMINAR PIEZA
# ============================
@piezas_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    supabase.table("piezas").delete().eq("id", id).execute()
    flash("Pieza eliminada", "info")
    return redirect(url_for("piezas.index"))

# ============================
#   PDF REPORTE
# ============================
@piezas_bp.route("/pdf_reporte")
def pdf_reporte():
    response = supabase.table("piezas").select("*").execute()
    piezas = response.data or []
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 750, "Reporte de Piezas")

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    p.setFont("Helvetica", 10)
    p.drawString(50, 730, f"Generado el: {fecha_hora}")

    y = 700
    hoy = date.today()

    if not piezas:
        p.drawString(50, y, "⚠ No hay piezas registradas.")
    else:
        for pz in piezas:
            vida = pz.get("vida_dias") or 0
            fecha_inst = pz.get("fecha_instalacion")

            if fecha_inst:
                fecha_inst = datetime.strptime(fecha_inst, "%Y-%m-%d").date()
                dias_usados = (hoy - fecha_inst).days
            else:
                dias_usados = 0

            dias_restantes = vida - dias_usados

            p.drawString(
                50, y,
                f"ID:{pz['id']} | {pz['nombre']} | Vida:{vida}d | Usados:{dias_usados}d | Restan:{dias_restantes}d"
            )
            y -= 20

            if y < 50:
                p.showPage()
                y = 750

    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="reporte_piezas.pdf", mimetype="application/pdf")
