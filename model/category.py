from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    products = db.relationship('Product', backref='category', cascade='all, delete-orphan',lazy=True)