from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(150), unique=True)
    user_password = db.Column(db.String(150))
    user_state = db.Column(db.String(120))
    user_role = 'user'
    role = db.Column(db.String(120), default='User')
  
    
    
class Seller(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    seller_name =  db.Column(db.String(50))
    seller_last_name =  db.Column(db.String(150), unique=True)
    seller_email =  db.Column(db.String(150), unique=True)
    seller_password = db.Column(db.String(150))
    seller_state = db.Column(db.String(120))
    user_role = 'seller' 
    role = db.Column(db.String(120), default='seller')
    
  
    
class Rider(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    rider_name =  db.Column(db.String(50))
    rider_last_name =  db.Column(db.String(150), unique=True)
    rider_email =  db.Column(db.String(150), unique=True)
    rider_password = db.Column(db.String(150))
    rider_state = db.Column(db.String(120))
    user_role = 'rider'
    role = db.Column(db.String(120), default='rider')
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(120))
    status = db.Column(db.String(120), default='Pending')
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    seller = db.relationship('Seller', backref=db.backref('products', lazy=True))

    def __init__(self, name, description, price, image_url, category, seller_id):
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url
        self.category = category
        self.seller_id = seller_id