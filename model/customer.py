from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    remark = db.Column(db.String(256))
    cart_items = db.relationship('CustomerCart', backref='customer', lazy=True)