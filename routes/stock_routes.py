from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.models import db, StockItem, PartType

bp = Blueprint('stock', __name__)

@bp.route('/')
def index():
    items = StockItem.query.all()
    return render_template('stock/index.html', items=items)

@bp.route('/new', methods=['GET', 'POST'])
def new_stock():
    if request.method == 'POST':
        part_type_id = request.form['part_type_id']
        quantity = request.form['quantity']
        minimum = request.form['minimum']
        item = StockItem(part_type_id=part_type_id, quantity=quantity, minimum=minimum)
        db.session.add(item)
        db.session.commit()
        flash("Repuesto agregado al stock", "success")
        return redirect(url_for('stock.index'))
    part_types = PartType.query.all()
    return render_template('stock/new.html', part_types=part_types)

@bp.route('/<int:id>/delete')
def delete_stock(id):
    item = StockItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash("Repuesto eliminado del stock", "danger")
    return redirect(url_for('stock.index'))
@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_stock(id):
    item = StockItem.query.get_or_404(id)
    if request.method == 'POST':
        item.part_type_id = request.form['part_type_id']
        item.quantity = request.form['quantity']
        item.minimum = request.form['minimum']
        db.session.commit()
        flash("Repuesto actualizado", "success")
        return redirect(url_for('stock.index'))
    part_types = PartType.query.all()
    return render_template('stock/edit.html', item=item, part_types=part_types)
@bp.route('/low_stock')
def low_stock():
    items = StockItem.query.filter(StockItem.quantity < StockItem.minimum).all()
    return render_template('stock/low_stock.html', items=items)
@bp.route('/search', methods=['GET', 'POST'])
def search_stock(): 
    if request.method == 'POST':
        search_term = request.form['search_term']
        items = StockItem.query.join(PartType).filter(PartType.name.ilike(f'%{search_term}%')).all()
        return render_template('stock/index.html', items=items)
    return redirect(url_for('stock.index'))
@bp.route('/<int:id>')
def view_stock(id):
    item = StockItem.query.get_or_404(id)
    return render_template('stock/view.html', item=item)    
@bp.route('/<int:id>/adjust', methods=['GET', 'POST'])
def adjust_stock(id):
    item = StockItem.query.get_or_404(id)
    if request.method == 'POST':
        adjustment = int(request.form['adjustment'])
        item.quantity += adjustment
        db.session.commit()
        flash("Stock ajustado", "success")
        return redirect(url_for('stock.index'))
    return render_template('stock/adjust.html', item=item)  
@bp.route('/report')
def stock_report():
    items = StockItem.query.all()
    return render_template('stock/report.html', items=items)
@bp.route('/api/stock/<int:id>')
def api_get_stock(id):
    item = StockItem.query.get_or_404(id)
    return {
        'id': item.id,
        'part_type': item.part_type.name,
        'quantity': item.quantity,
        'minimum': item.minimum
    }   
@bp.route('/api/stock')
def api_get_all_stock():
    items = StockItem.query.all()
    return {
        'stock': [
            {
                'id': item.id,
                'part_type': item.part_type.name,
                'quantity': item.quantity,
                'minimum': item.minimum
            } for item in items
        ]
    }   
@bp.route('/api/stock/low')
def api_get_low_stock():
    items = StockItem.query.filter(StockItem.quantity < StockItem.minimum).all()
    return {
        'low_stock': [
            {
                'id': item.id,
                'part_type': item.part_type.name,
                'quantity': item.quantity,
                'minimum': item.minimum
            } for item in items
        ]
    }
from flask import Response, render_template
from weasyprint import HTML

@bp.route('/pdf')
def pdf_stock():
    items = StockItem.query.all()
    html = render_template('stock/pdf.html', items=items)
    pdf = HTML(string=html).write_pdf()
    return Response(pdf, mimetype="application/pdf",
                    headers={"Content-Disposition":"attachment;filename=stock.pdf"})
@bp.route('/api/stock/part_type/<int:part_type_id>')
def api_get_stock_by_part_type(part_type_id):
    items = StockItem.query.filter_by(part_type_id=part_type_id).all()
    return {
        'stock': [
            {
                'id': item.id,
                'part_type': item.part_type.name,
                'quantity': item.quantity,
                'minimum': item.minimum
            } for item in items
        ]
    }
@bp.route('/api/stock/brand/<int:brand_id>')
def api_get_stock_by_brand(brand_id):
    items = StockItem.query.join(PartType).filter(PartType.brand_id == brand_id).all()
    return {
        'stock': [
            {
                'id': item.id,
                'part_type': item.part_type.name,
                'quantity': item.quantity,
                'minimum': item.minimum
            } for item in items
        ]
    }
@bp.route('/api/stock/supplier/<int:supplier_id>')
def api_get_stock_by_supplier(supplier_id):
    items = StockItem.query.join(PartType).filter(PartType.supplier_id == supplier_id).all()
    return {
        'stock': [
            {
                'id': item.id,
                'part_type': item.part_type.name,
                'quantity': item.quantity,
                'minimum': item.minimum
            } for item in items
        ]
    }
@bp.route('/api/stock/sector/<int:sector_id>')
def api_get_stock_by_sector(sector_id):
    items = StockItem.query.join(PartType).join(Machine).filter(Machine.sector_id == sector_id).all()
    return {
        'stock': [
            {
                'id': item.id,
                'part_type': item.part_type.name,
                'quantity': item.quantity,
                'minimum': item.minimum
            } for item in items
        ]
    }   
@bp.route('/api/stock/machine/<int:machine_id>')
def api_get_stock_by_machine(machine_id):
    items = StockItem.query.join(PartType).filter(PartType.machine_id == machine_id).all()
    return {
        'stock': [
            {
                'id': item.id,
                'part_type': item.part_type.name,
                'quantity': item.quantity,
                'minimum': item.minimum
            } for item in items
        ]
    }   
@bp.route('/api/stock/count')
def api_get_stock_count():
    count = StockItem.query.count()
    return {'count': count} 
@bp.route('/api/stock/total_quantity')
def api_get_total_stock_quantity():
    total_quantity = db.session.query(db.func.sum(StockItem.quantity)).scalar() or 0
    return {'total_quantity': total_quantity}   
@bp.route('/api/stock/total_minimum')
def api_get_total_stock_minimum():
    total_minimum = db.session.query(db.func.sum(StockItem.minimum)).scalar() or 0
    return {'total_minimum': total_minimum} 
@bp.route('/api/stock/average_quantity')
def api_get_average_stock_quantity():
    average_quantity = db.session.query(db.func.avg(StockItem.quantity)).scalar() or 0
    return {'average_quantity': average_quantity}   
@bp.route('/api/stock/average_minimum')
def api_get_average_stock_minimum():
    average_minimum = db.session.query(db.func.avg(StockItem.minimum)).scalar() or 0
    return {'average_minimum': average_minimum}
@bp.route('/api/stock/part_type/<int:part_type_id>/count')
def api_get_stock_count_by_part_type(part_type_id):
    count = StockItem.query.filter_by(part_type_id=part_type_id).count()
    return {'count': count}
@bp.route('/api/stock/brand/<int:brand_id>/count')
def api_get_stock_count_by_brand(brand_id):
    count = StockItem.query.join(PartType).filter(PartType.brand_id == brand_id).count()
    return {'count': count}
@bp.route('/api/stock/supplier/<int:supplier_id>/count')
def api_get_stock_count_by_supplier(supplier_id):
    count = StockItem.query.join(PartType).filter(PartType.supplier_id == supplier_id).count()
    return {'count': count}
@bp.route('/api/stock/sector/<int:sector_id>/count')
def api_get_stock_count_by_sector(sector_id):
    count = StockItem.query.join(PartType).join(Machine).filter(Machine.sector_id == sector_id).count()
    return {'count': count} 
@bp.route('/api/stock/machine/<int:machine_id>/count')
def api_get_stock_count_by_machine(machine_id):
    count = StockItem.query.join(PartType).filter(PartType.machine_id == machine_id).count()
    return {'count': count}

@bp.route('/api/stock/low/count')
def api_get_low_stock_count():
    count = StockItem.query.filter(StockItem.quantity < StockItem.minimum).count()
    return {'count': count} 
@bp.route('/api/stock/low/total_quantity')
def api_get_low_stock_total_quantity():
    total_quantity = db.session.query(db.func.sum(StockItem.quantity)).filter(StockItem.quantity < StockItem.minimum).scalar() or 0
    return {'total_quantity': total_quantity}   

@bp.route('/api/stock/low/total_minimum')
def api_get_low_stock_total_minimum():
    total_minimum = db.session.query(db.func.sum(StockItem.minimum)).filter(StockItem.quantity < StockItem.minimum).scalar() or 0
    return {'total_minimum': total_minimum}
@bp.route('/api/stock/low/average_quantity')
def api_get_low_stock_average_quantity():
    average_quantity = db.session.query(db.func.avg(StockItem.quantity)).filter(StockItem.quantity < StockItem.minimum).scalar() or 0
    return {'average_quantity': average_quantity}   
@bp.route('/api/stock/low/average_minimum')
def api_get_low_stock_average_minimum():
    average_minimum = db.session.query(db.func.avg(StockItem.minimum)).filter(StockItem.quantity < StockItem.minimum).scalar() or 0
    return {'average_minimum': average_minimum} 
@bp.route('/api/stock/search/<string:search_term>')
def api_search_stock(search_term):
    items = StockItem.query.join(PartType).filter(PartType.name.ilike(f'%{search_term}%')).all()
    return {
        'stock': [
            {
                'id': item.id,
                'part_type': item.part_type.name,
                'quantity': item.quantity,
                'minimum': item.minimum
            } for item in items
        ]
    }
@bp.route('/api/stock/part_type/<int:part_type_id>/total_quantity')
def api_get_stock_total_quantity_by_part_type(part_type_id):
    total_quantity = db.session.query(db.func.sum(StockItem.quantity)).filter(StockItem.part_type_id == part_type_id).scalar() or 0
    return {'total_quantity': total_quantity}   
