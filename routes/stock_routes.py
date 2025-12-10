# routes/stock_routes.py
from flask import Blueprint, render_template, send_file
from supabase_client import supabase
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")

@stock_bp.route("/")
def ver_stock():
    # Traer todas las piezas NO instaladas
    data = supabase.table("piezas").select("*").eq("instalada", False).execute()
    piezas = data.data if data.data else []

    # Calcular si falta completar stock mínimo
    for p in piezas:
        try:
            p["stock_bajo"] = p["cantidad_actual"] < p["stock_minimo"]
        except:
            p["stock_bajo"] = False

    return render_template("stock/stock.html", piezas=piezas)


@stock_bp.route("/imprimir")
def imprimir_stock():
    data = supabase.table("piezas").select("*").eq("instalada", False).execute()
    piezas = data.data if data.data else []

    filename = "/mnt/data/stock_report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)

    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph("Reporte de Stock (Piezas no instaladas)", styles["Title"])
    elements.append(title)

    table_data = [["Nombre", "Cantidad", "Stock Mínimo", "Estado"]]

    for p in piezas:
        estado = "OK"
        if p["cantidad_actual"] < p["stock_minimo"]:
            estado = "STOCK BAJO"

        table_data.append([
            p.get("nombre", "Sin nombre"),
            p.get("cantidad_actual", 0),
            p.get("stock_minimo", 0),
            estado
        ])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (1, 1), (-1, -1), "CENTER")
    ]))

    elements.append(table)
    doc.build(elements)

    return send_file(filename, as_attachment=True)
