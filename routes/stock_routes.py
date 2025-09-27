from flask import Blueprint, render_template, Response
from models.models import db
from models.stock import Stock
from models.pieza import Pieza
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")

# Página principal: muestra tabla de stock
@stock_bp.route("/")
def index():
    items = db.session.query(Stock).all()
    return render_template("stock/index.html", items=items)

# Exportar stock a PDF
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
        pieza = Pieza.query.get(item.pieza_id)
        p.drawString(50, y, str(item.id))
        p.drawString(100, y, pieza.nombre if pieza else "N/A")
        p.drawString(250, y, str(item.cantidad))
        p.drawString(350, y, str(item.minimo))
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment;filename=stock.pdf"}
    )

# API: total de stock por pieza
def api_get_stock_total_quantity_by_pieza(pieza_id):
    total = (
        db.session.query(db.func.sum(Stock.cantidad))
        .filter(Stock.pieza_id == pieza_id)
        .scalar()
        or 0
    )
    return {"total_cantidad": total}
stock_bp.add_url_rule(
    "/api/stock/total/<int:pieza_id>",  
    view_func=api_get_stock_total_quantity_by_pieza,
    methods=["GET"]
)
# Nota: La ruta API no está registrada en el blueprint para evitar conflictos con rutas web.
# Se puede registrar en la aplicación principal si es necesario.  
