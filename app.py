from datetime import timedelta

from flask import Flask
from flask_mail import Mail

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'notraptor68@gmail.com'
app.config['MAIL_PASSWORD'] = 'quda efsc dkxw bplq'  # Use App Password from Google
app.config['MAIL_DEFAULT_SENDER'] = 'notraptor68@gmail.com'

mail = Mail(app)

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import model

import routes

if __name__ == '__main__':
    app.run()
