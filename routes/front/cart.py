from app import app
from flask import render_template
from products import products_item

@app.get('/cart')
def cart():  # put application's code here
    products = products_item
    return render_template('cart.html', products=products_item, module ='cart')