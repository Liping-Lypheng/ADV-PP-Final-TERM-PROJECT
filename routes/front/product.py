from app import app
from flask import render_template
from model import Product
@app.get('/products')
def product():  # put application's code here
    products = Product.query.all()
    return render_template('products.html',products=products, module = 'products')
@app.route('/products/<int:id>')
def product_detail(id):
    products = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=products)
