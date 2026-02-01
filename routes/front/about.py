from app import app
from flask import render_template
from products import products_item

@app.get('/about')
def about():  # put application's code here
    products = products_item
    return render_template('about.html', products=products_item, module ='about')