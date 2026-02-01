from flask import render_template, redirect, url_for, flash
from app import app, db
from model import Order

@app.get('/admin/order')
def admin_order():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/order/index.html', orders=orders)

@app.get('/admin/order/<int:order_id>')
def admin_order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order/detail.html', order=order)

@app.post('/admin/order/<int:order_id>/delete')
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Order deleted successfully.', 'info')
    return redirect(url_for('admin_order'))