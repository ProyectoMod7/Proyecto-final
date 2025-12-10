# routes/stock_routes.py

from flask import Blueprint, render_template, send_file
from supabase_client import supabase
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

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

    return render_template("stock/index.html", piezas=stock)


@stock_bp.route("/imprimir")
def imprimir_stock():
    # --- Traer todas las piezas disponibles desde la vista stock ---
    res = supabase.table("stock").select("*").order("nombre").execute()
    stock = res.data if res.data else []

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()
    elements = []

    # Título con fecha
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    title = Paragraph(f"Reporte de Stock (Piezas NO instaladas) - {fecha_hora}", styles["Title"])
    elements.append(title)

    # Cabecera de tabla
    table_data = [["Nombre", "Vida útil (días)"]]

    # Filas con piezas
    for p in stock:
        table_data.append([
            p.get("nombre", "Sin nombre"),
            p.get("vida_dias", 0)
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (1, 1), (-1, -1), "CENTER")
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="stock_report.pdf", mimetype="application/pdf")
