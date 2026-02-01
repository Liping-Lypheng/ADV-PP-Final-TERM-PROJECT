from datetime import timedelta

from app import app , db
from flask import request, jsonify, redirect
from sqlalchemy import text
from model import User

from flask_jwt_extended import create_access_token, get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager, set_access_cookies, unset_jwt_cookies
from werkzeug.security import check_password_hash,generate_password_hash
from werkzeug.utils import secure_filename

import os

from flask import render_template

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "yd3op2wu@e2d5ke"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config['JWT_COOKIE_SECURE'] = False  # True in production (HTTPS)
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Enable later

jwt = JWTManager(app)

# blocklist for revoked JTIS
REVOKED_JTIS = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header , jwt_data):
    return jwt_data["jti"] in REVOKED_JTIS

# @app.get("api/login")
# def login_page():
#     return render_template("admin/login.html")

@app.post("/login_confirm")
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    sql_str = text("select * from user where username = :username")
    result = db.session.execute(sql_str, {"username": username}).fetchone()

    if not result:
        return jsonify({"msg": "Incorrect Username or Password"}), 401

    user_id = str(result[0])
    hash_password = result[3]
    if check_password_hash(hash_password,password):
        access_token = create_access_token(identity=user_id)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Incorrect Username or Password"}), 401

# 3. UPDATE LOGOUT TO CLEAR COOKIES
@app.post("/logout")
@jwt_required()  # revoke current access token
def logout():
    jti = get_jwt()["jti"]
    REVOKED_JTIS.add(jti)
    return jsonify(msg="Access token revoked")

@app.post("/me")
@jwt_required()
def me():
    user = get_jwt_identity()
    return jsonify(user=user)
