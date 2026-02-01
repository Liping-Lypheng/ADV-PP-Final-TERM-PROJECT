from datetime import timedelta

from werkzeug.security import check_password_hash

from app import app,db
from flask import request, render_template, redirect, url_for, session
from model import User

app.config["SECRET_KEY"] = "yd3op2wu@e2d5ke"  # Change this!
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)

@app.get('/login')
def admin_login():
    return render_template('admin/login.html')

# @app.before_request
# def before_request():
#     from flask import request, session, url_for,redirect
#     admin_url = request.path
#     is_admin = 'admin' in admin_url
#     if is_admin:
#         if not session.get("user_id"):
#             return redirect(url_for('admin_login'))

@app.post('/admin/do_login')
def do_login():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    user = db.session.query(User).filter_by(username=username).first()
    if not user:
        return redirect(url_for('admin_login'))
    hash_password = user.password
    if check_password_hash(hash_password, password):
        session["user_id"] = user.id
        session["username"] = user.username
        session["email"] = user.email
        return redirect(url_for('dashboard'))

@app.get('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))
