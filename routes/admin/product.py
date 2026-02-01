from werkzeug.utils import secure_filename

from app import app,db
from flask import request, render_template, redirect, url_for
from model import Category, Product
import os

@app.get('/admin/product')
def admin_product():
    module = 'product'
    products = Product.query.all()
    return render_template('admin/product/index.html', module=module, products=products)
@app.get('/admin/product/form')
def product_form():
    module = 'product'
    status = request.args.get('status')
    product = None
    categories = Category.query.all()
    if status == 'edit':
        product_id = request.args.get('product_id')
        if product_id:
            product = Product.query.get_or_404(int(product_id))

    return render_template(
        'admin/product/form.html',
        module=module,
        status=status,
        product=product,
        categories=categories
    )

@app.get('/admin/product/confirm')  # delete product
def product_confirm():
    module = 'product'
    product_id = int(request.args.get('product_id'))
    if not product_id:
        return redirect(url_for('product_form'))
    product = Product.query.filter_by(id=product_id).first()
    return render_template('admin/product/confirm.html', module=module, product=product)

@app.post('/admin/product/add')
def product_add():
    form = request.form
    file = request.files.get('image')

    category_id = form.get('category_id')
    if not category_id:
        return "Category is required", 400

    filename = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.root_path, 'static/product_upload', filename)
        file.save(upload_path)

    product = Product(
        name=form.get('name'),
        price=float(form.get('price')),
        cost=float(form.get('cost')),
        stock=int(form.get('stock')),
        description=form.get('description'),
        category_id=int(category_id),
        image=filename
    )

    db.session.add(product)
    db.session.commit()

    return redirect(url_for('admin_product'))


@app.post('/admin/product/updates')
def product_updates():
    form = request.form
    product_id = form.get('product_id')

    if not product_id:
        return "Product ID required", 400

    product = Product.query.get_or_404(int(product_id))

    product.name = form.get('name') or product.name
    product.cost = float(form.get('cost')) if form.get('cost') else product.cost
    product.price = float(form.get('price')) if form.get('price') else product.price
    product.stock = int(form.get('stock')) if form.get('stock') else product.stock
    product.description = form.get('description') or product.description

    category_id = form.get('category_id')
    if category_id:
        product.category_id = int(category_id)

    image = request.files.get('image')
    if image and image.filename:
        filename = secure_filename(image.filename)
        upload_path = os.path.join(app.root_path, 'static/product_upload', filename)
        image.save(upload_path)
        product.image = filename

    db.session.commit()
    return redirect(url_for('admin_product'))

@app.post('/admin/product/remove/')
def product_remove():
    module = 'product'
    product_id = int(request.form.get('product_id'))
    product = Product.query.get_or_404(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('admin_product'))