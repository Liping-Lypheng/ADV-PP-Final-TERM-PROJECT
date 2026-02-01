from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate
import urllib.parse
app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'notraptor68@gmail.com'
app.config['MAIL_PASSWORD'] = 'quda efsc dkxw bplq'  # Use App Password from Google
app.config['MAIL_DEFAULT_SENDER'] = 'notraptor68@gmail.com'

mail = Mail(app)

#database

jwt = JWTManager(app)
# blocklist for revoked JTIS
REVOKED_JTIS = set()

# Your actual password
password = "Admin123@#"

# URL-encode the password
encoded_password = urllib.parse.quote_plus(password)

# Construct the URI
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://app:{encoded_password}@localhost/app"
DB_CONFIG= {
    'host': 'localhost',
    'user': 'root',
    'password': 'Admin123@#',
    'database': 'app',
}

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'


#session
app.config['SECRET_KEY'] = '1283asd213'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)

import model

import routes

if __name__ == '__main__':
    app.run()
