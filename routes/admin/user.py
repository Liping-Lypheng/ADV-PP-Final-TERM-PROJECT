from werkzeug.security import generate_password_hash

from app import app,db
from flask import request, render_template, redirect, url_for
from model import User
@app.get('/admin/user')
def user():
    module = 'user'
    users = User.query.all()
    return render_template('admin/user/index.html', module=module,users=users)
@app.get('/admin/user/form')
def user_form():
    module = 'user'
    status = request.args.get('status')
    user = None
    if status == 'edit':
        user_id = int(request.args.get('user_id'))
        user = User.query.get(user_id)
    return render_template('admin/user/form.html', module=module, status=status,user=user)
@app.get('/admin/user/confirm')
def user_confirm():
    module = 'user'
    user_id = int(request.args.get('user_id'))
    user = User.query.get(user_id)
    return render_template('admin/user/confirm.html', module=module,user=user)

@app.post('/admin/user/add')
def user_add():
    form = request.form
    user = User(
        id=form.get('id'),
        username=form.get('username'),
        email=form.get('email'),
        password=generate_password_hash(form.get('password')),
        role = form.get('role')
    )
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('user'))

@app.post('/admin/user/updates')
def user_updates():
    form = request.form
    user_id = int(request.form.get('user_id'))
    user = User.query.get(user_id)
    if user:
        user.username = form.get('username')
        user.email = form.get('email')
        db.session.commit()
    return redirect(url_for('user'))


@app.post('/admin/user/remove')
def user_remove():
    module = 'user'
    user_id = int(request.form.get('user_id'))
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('user'))