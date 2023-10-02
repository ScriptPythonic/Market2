from flask import Flask,Blueprint,render_template
from flask_login import login_required,current_user
from .decorator import login_required
from .models import Product







views = Blueprint('views', __name__)






@views.route('/',methods=['GET'])
def landing():
        approved_product = Product.query.filter_by(status='Approved').all()

        return  render_template('Assest/landing_page.html',products = approved_product)
    
@views.route('/home',methods=['GET'])
@login_required('user')
def home():
   
    
    return  render_template('User/home.html', user=current_user)





