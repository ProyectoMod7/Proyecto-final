# routes/stock_routes.py
from flask import Blueprint, render_template, send_file
from supabase_client import supabase
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")

@stock_bp.route("/")
def index():
    # --- 1) OBTENER TODAS LAS PIEZAS ---
    piezas_data = supabase.table("piezas").select("*").execute()
    piezas = piezas_data.data if piezas_data.data else []

    # --- 2) OBTENER TODAS LAS PIEZAS INSTALADAS ---
    inst_data = supabase.table("piezas_instaladas").select("pieza_id").execute()
    instaladas_ids = [i["pieza_id"] for i in inst_data.data] if inst_data.data else []

    # --- 3) FILTRAR STOCK (piezas NO instaladas) ---
    stock = [p for p in piezas if p["id"] not in instaladas_ids]

    # --- 4) CALCULAR STOCK BAJO ---
    for p in stock:
        cantidad = p.get("cantidad_actual", 0)
        minimo = p.get("stock_minimo", 0)
        p["stock_bajo"] = cantidad < minimo

    return render_template("stock/index.html", piezas=stock)


@stock_bp.route("/imprimir")
def imprimir_stock():

    piezas_data = supabase.table("piezas").select("*").execute()
    piezas = piezas_data.data if piezas_data.data else []

    inst_data = supabase.table("piezas_instaladas").select("pieza_id").execute()
    instaladas_ids = [i["pieza_id"] for i in inst_data.data] if inst_data.data else []

    stock = [p for p in piezas if p["id"] not in instaladas_ids]

    filename = "/mnt/data/stock_report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)

    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph("Reporte de Stock (Piezas NO instaladas)", styles["Title"])
    elements.append(title)

    table_data = [["Nombre", "Cantidad", "Stock Mínimo", "Estado"]]

    for p in stock:
        cantidad = p.get("cantidad_actual", 0)
        minimo = p.get("stock_minimo", 0)
        estado = "STOCK BAJO" if cantidad < minimo else "OK"

        table_data.append([
            p.get("nombre", "Sin nombre"),
            cantidad,
            minimo,
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
