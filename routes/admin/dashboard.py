from app import app
from flask import request,render_template

@app.get('/admin/')
@app.get('/admin/dashboard')
def dashboard():
    module = 'dashboard'
    return render_template('admin/dashboard/index.html', module=module)