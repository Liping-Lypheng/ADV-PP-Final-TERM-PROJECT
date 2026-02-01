from app import app
from flask import render_template, request
from products import products_item

@app.get('/contact')
def contact():  # put application's code here
    return render_template('contact.html', module = 'contact')

@app.post('/contactsuccess')
def contactsuccess():
    form = request.form
    customer_name = form.get('name')
    subject = form.get('subject')
    email = form.get('email')
    message = form.get('message')
    return render_template('contactsuccess.html',customer_name = customer_name, subject = subject, email = email, message = message)