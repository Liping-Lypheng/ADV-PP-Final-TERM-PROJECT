from datetime import datetime

from flask import Flask, render_template, request, jsonify
import json
from app import app,mail,db
from FunctionSend import chat_id
from products import products_item
from flask_mail import Mail,Message
from tabulate import tabulate
import FunctionSend
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from model import Order,OrderItem,Product

@app.post('/proceed')
def proceed():
    form = request.form
    customer_name = form.get('name')
    email = form.get('email')
    phone = form.get('phone')
    address = form.get('address')
    created_at = form.get('created_at')
    cart_item_str = form.get('cart_item')
    if not cart_item_str:
        return jsonify({"error": "No cart data received"}), 400

    try:
        cart_item = json.loads(cart_item_str)
    except Exception:
        return jsonify({"error": "Invalid cart data"}), 400

    # ✅ Calculate total directly from cart_item
    total = sum(float(item.get('price', 0)) * float(item.get('qty', 1)) for item in cart_item)

    new_order = Order(
        user_id=1,
        name=customer_name,
        phone=phone,
        email=email,
        address=address,
        created_at=datetime.utcnow()
    )
    db.session.add(new_order)
    db.session.flush()

    for item in cart_item:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.get('id'),  # Assuming cart items have product IDs
            price=float(item['price']),
            qty=int(item['qty']),
            total=float(item['price']) * int(item['qty'])
        )
        db.session.add(order_item)

        # Commit all changes to database
    db.session.commit()

    # Build item rows for table
    item_row = []
    for item in cart_item:
        item_row.append(
            [
                f"{item['title'][0:15]}...",
                "$" + str(item["price"]),
                item["qty"],
                "$" + str(float(item["price"]) * float(item["qty"]))  # added per-item total
            ]
        )

    # Table
    table = tabulate(
        tabular_data=item_row,
        headers=['Product Name', 'Price', 'Qty', 'Total']
    )

    chat_id = '@lyphengchannel'
    html = f"<strong>Customer Name: {customer_name}</strong>\n"
    html += f"<strong>Customer Phone: {phone}</strong>\n"
    html += f"<i>Customer Address: {address}</i>\n"
    html += f"<i>Email: {email}</i>\n"
    html += f"<strong>------------------------------</strong>\n"
    html += f"<pre>{table}</pre>\n"
    html += f"<strong>Total: ${total}</strong>\n"
    html += f"<strong>Total:{format_khr(total* 4100)}</strong>"

    # Send to Telegram
    FunctionSend.sendmessage(message=html, chat_id=chat_id)

    # Send Email
    msg = Message('Invoice From SU4.13 Shop', recipients=[email])
    msg.body = 'This is a plain text email sent from Flask.'
    message = render_template(
        'invoice.html',
        cart_item=cart_item,
        customer_name=customer_name,
        phone=phone,
        address=address,
        email=email,
        total=total
    )
    msg.html = message
    mail.send(msg)

    return render_template('invoice.html',
                           cart_item=cart_item,
                           customer_name=customer_name,
                           phone=phone,
                           address=address,
                           email=email,
                           total=total)
def format_khr(amount):
    return f"{amount:,.0f} ៛"