from app import app
from flask import render_template
from model import Product
@app.get('/admin/')
@app.get('/admin/dashboard')
def dashboard():
    module = 'dashboard'
    products = Product.query.all()
    return render_template('admin/dashboard/index.html', module=module, product=products)