from app import app
from flask import render_template
from products import products_item

@app.get('/checkout')
def checkout():  # put application's code here
    products = products_item
    return render_template('checkout.html',products=products_item, module = 'checkout')