from flask import jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import func
from app import app, db
from model import *
# from model.all import Invoice, InvoiceItem, Product, Category
# from model.invoice import Invoice
# from model.invoice_item import InvoiceItem
# from model.products import Product
# from model.category import Category

# 1. Daily Sales
@app.get('/report/daily')
def report_daily_sales():
    today = datetime.utcnow().date()
    total = db.session.query(func.sum(Invoice.total_amount))\
        .filter(func.date(Invoice.created_at) == today)\
        .scalar() or 0

    return jsonify({
        'report_type': 'daily',
        'date': str(today),
        'total_sales': float(total)
    }), 200

# 2. Weekly Sales
@app.get('/report/weekly')
def report_weekly_sales():
    today = datetime.utcnow().date()
    start_week = today - timedelta(days=today.weekday())
    total = db.session.query(func.sum(Invoice.total_amount))\
        .filter(func.date(Invoice.created_at) >= start_week)\
        .filter(func.date(Invoice.created_at) <= today)\
        .scalar() or 0

    return jsonify({
        'report_type': 'weekly',
        'start_date': str(start_week),
        'end_date': str(today),
        'total_sales': float(total)
    }), 200

# 3. Monthly Sales
@app.get('/report/monthly')
def report_monthly_sales():
    today = datetime.utcnow().date()
    first_day = today.replace(day=1)
    total = db.session.query(func.sum(Invoice.total_amount))\
        .filter(func.date(Invoice.created_at) >= first_day)\
        .filter(func.date(Invoice.created_at) <= today)\
        .scalar() or 0

    return jsonify({
        'report_type': 'monthly',
        'month': today.strftime("%B %Y"),
        'total_sales': float(total)
    }), 200

# 4. Sales by Criteria
@app.post('/report/sales/by')
def report_sales_by_criteria():
    data = request.get_json()
    criteria = data.get('criteria')
    value = data.get('value')

    query = db.session.query(func.sum(InvoiceItem.subtotal))

    if criteria == 'product':
        query = query.filter(InvoiceItem.product_id == value)
    elif criteria == 'category':
        query = query.join(Product, Product.id == InvoiceItem.product_id)\
                     .filter(Product.category_id == value)
    elif criteria == 'user':
        query = query.join(Invoice, Invoice.id == InvoiceItem.invoice_id)\
                     .filter(Invoice.created_by == value)
    else:
        return jsonify({'message': 'Invalid criteria!'}), 400

    total = query.scalar() or 0

    return jsonify({
        'criteria': criteria,
        'value': value,
        'total_sales': float(total)
    }), 200
