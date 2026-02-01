from app import app
from flask import render_template



@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_page/404.html'), 404

@app.errorhandler(500)
def error_505(e):
    return render_template('error_page/505.html'), 505

@app.errorhandler(Exception)
def goble_error(e):
    return f"<center><h1>Some error from server side: {e}</h1></center>"
