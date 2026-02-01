from app import app
from flask import render_template
from model import Product
@app.route('/')
def home():  # put application's code here
    products = Product.query.all()
    return render_template('home.html',products=products, module = 'home')
