# routes/stock_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from supabase_client import supabase
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")

@stock_bp.route("/")
def index():
    res = supabase.table("stock").select("*").order("id", desc=False).execute()
    items = res.data or []
    for it in items:
        p = supabase.table("piezas").select("nombre").eq("id", it.get("pieza_id")).single().execute()
        it["pieza_nombre"] = p.data.get("nombre") if p and p.data else "N/A"
    return render_template("stock/index.html", items=items)

@stock_bp.route("/crear", methods=["GET","POST"])
def crear():
    if request.method == "POST":
        data = {
            "pieza_id": request.form.get("pieza_id"),
            "cantidad": request.form.get("cantidad"),
            "stock_minimo": request.form.get("stock_minimo"),
            "ubicacion": request.form.get("ubicacion")
        }
        supabase.table("stock").insert(data).execute()
        flash("Item de stock creado", "success")
        return redirect(url_for("stock.index"))
    piezas = supabase.table("piezas").select("*").order("nombre").execute().data or []
    return render_template("stock/form.html", item=None, piezas=piezas)

@stock_bp.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):
    if request.method == "POST":
        data = {
            "pieza_id": request.form.get("pieza_id"),
            "cantidad": request.form.get("cantidad"),
            "stock_minimo": request.form.get("stock_minimo"),
            "ubicacion": request.form.get("ubicacion")
        }
        supabase.table("stock").update(data).eq("id", id).execute()
        flash("Item actualizado", "success")
        return redirect(url_for("stock.index"))
    item = supabase.table("stock").select("*").eq("id", id).single().execute().data
    piezas = supabase.table("piezas").select("*").order("nombre").execute().data or []
    return render_template("stock/form.html", item=item, piezas=piezas)

@stock_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    supabase.table("stock").delete().eq("id", id).execute()
    flash("Item eliminado", "info")
    return redirect(url_for("stock.index"))

@stock_bp.route("/pdf")
def pdf_stock():
    res = supabase.table("stock").select("*").order("id", desc=False).execute()
    items = res.data or []
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    p.setFont("Helvetica-Bold", 14)
    p.drawString(40, height-40, "Reporte de Stock")
    y = height - 70
    p.setFont("Helvetica", 10)
    for it in items:
        pieza = supabase.table("piezas").select("nombre").eq("id", it.get("pieza_id")).single().execute()
        pieza_nombre = pieza.data.get("nombre") if pieza and pieza.data else "N/A"
        p.drawString(40, y, f"{pieza_nombre} | Cant: {it.get('cantidad')} | Min: {it.get('minimo')} | Ubicación: {it.get('ubicacion')}")
        y -= 15
        if y < 60:
            p.showPage()
            y = height - 40
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    return Response(pdf, mimetype="application/pdf", headers={"Content-Disposition":"attachment; filename=stock.pdf"})
