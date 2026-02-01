from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.ForeignKey('branch.id'),index=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    remark = db.Column(db.String(256), nullable=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    image = db.Column(db.String(256), nullable=True)
    branch_table=db.relationship('Branch', backref='user', lazy=True)
    role = db.Column(db.String(20), default="user")
