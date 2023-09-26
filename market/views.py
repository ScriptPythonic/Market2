from flask import Flask,Blueprint,render_template
from flask_login import login_required,current_user
from .decorator import login_required







views = Blueprint('views', __name__)






@views.route('/',methods=['GET'])
def landing():
   
    
        return  render_template('Assest/landing_page.html',user=current_user)
    
@views.route('/home',methods=['GET'])
@login_required('user')
def home():
   
    
    return  render_template('User/home.html', user=current_user)





