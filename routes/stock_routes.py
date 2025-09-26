from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.models import db, StockItem, PartType, Machine
from flask import Response, render_template
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io


stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/')
def index():
    items = StockItem.query.all()
    return render_template('stock/index.html', items=items)


@stock_bp.route('/pdf')
def pdf_stock():
    items = StockItem.query.all()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Stock Report")

    p.setFont("Helvetica", 12)
    y = height - 80
    p.drawString(50, y, "ID")
    p.drawString(100, y, "Part Type")
    p.drawString(250, y, "Quantity")
    p.drawString(350, y, "Minimum")

    y -= 20
    for item in items:
        p.drawString(50, y, str(item.id))
        p.drawString(100, y, item.part_type.name)
        p.drawString(250, y, str(item.quantity))
        p.drawString(350, y, str(item.minimum))
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    return Response(pdf, mimetype="application/pdf",
                    headers={"Content-Disposition": "attachment;filename=stock.pdf"})
def api_get_stock_total_quantity_by_part_type(part_type_id):
    total_quantity = db.session.query(db.func.sum(StockItem.quantity)).filter(StockItem.part_type_id == part_type_id).scalar() or 0
    return {'total_quantity': total_quantity}   
