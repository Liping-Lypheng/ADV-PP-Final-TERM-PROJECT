from werkzeug.utils import secure_filename
import os
from app import app,db
from flask import request, render_template, redirect, url_for, flash
from model import Category
@app.get('/admin/category')
def admin_category():
    module = 'category'
    categories = Category.query.all()
    return render_template('admin/category/index.html', module=module, categories=categories)

@app.get('/admin/category/form')
def category_form():
    module = 'category'
    status = request.args.get('status')
    category = None
    if status == 'edit':
        category_id = int(request.args.get('category_id'))
        category = Category.query.get(category_id)
    return render_template('admin/category/form.html', module=module, status=status, category=category)


@app.get('/admin/category/confirm')  # delete category
def category_confirm():
    module = 'category'
    category_id = request.args.get('category_id')
    if not category_id:
        return "Category ID is required", 400

    category_id = int(category_id)
    category = Category.query.get_or_404(category_id)

    return render_template(
        'admin/category/confirm.html',
        module=module,
        category=category
    )

@app.post('/admin/category/add')
def category_add():
    form = request.form
    status = request.args.get('status')
    file = request.files.get('image')
    filename = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        upload_path = os.path.join('static/category_upload', filename)
        file.save(upload_path)

    category = Category(
        name=form.get('name'),
    )
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('admin_category'))

@app.post('/admin/category/updates')
def category_updates():
    category_id = request.form.get('category_id')
    status = request.args.get('status')
    if not category_id:
        flash('Invalid category', 'error')
        return redirect(url_for('admin_category'))

    category = Category.query.get_or_404(category_id)
    category.name = request.form.get('name')
    db.session.commit()

    flash('Category updated successfully', 'success')
    return redirect(url_for('admin_category'))

@app.post('/admin/category/remove')
def category_remove():
    module = 'category'
    category_id = int(request.form.get('category_id'))
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
    return render_template('admin/user/confirm.html', module=module, category=category)