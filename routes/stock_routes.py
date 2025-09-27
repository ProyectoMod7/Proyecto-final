# routes/stock_routes.py
from flask import Blueprint, render_template, Response, request, redirect, url_for, flash
from models.models import db
from models.stock import Stock
from models.pieza import Pieza
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")

@stock_bp.route("/")
def index():
    items = db.session.query(Stock).all()
    # debug simple: (se puede quitar después)
    # print("Stock items count:", len(items))
    return render_template("stock/index.html", items=items)

@stock_bp.route("/pdf")
def pdf_stock():
    items = db.session.query(Stock).all()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Reporte de Stock")

    p.setFont("Helvetica", 12)
    y = height - 80
    p.drawString(50, y, "ID")
    p.drawString(100, y, "Pieza")
    p.drawString(250, y, "Cantidad")
    p.drawString(350, y, "Mínimo")

    y -= 20
    for item in items:
        pieza = item.pieza  # gracias a la relación
        p.drawString(50, y, str(item.id))
        p.drawString(100, y, pieza.nombre if pieza else "N/A")
        p.drawString(250, y, str(item.cantidad))
        p.drawString(350, y, str(item.minimo))
        y -= 20
        if y < 60:
            p.showPage()
            y = height - 50

    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    return Response(pdf, mimetype="application/pdf",
                    headers={"Content-Disposition": "attachment;filename=stock.pdf"})
