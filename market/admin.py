from flask import Blueprint, render_template,redirect,url_for
from flask_login import login_required
from .decorator import admin_required
from .models import Product
from . import db

admin_panel = Blueprint('admin_panel', __name__)

@admin_panel.route('/admin', methods=['GET'])
@admin_required
@login_required
def admin():
   
    pending_products = Product.query.filter_by(status='Pending').all()

    return render_template('Admin/admin.html', products=pending_products)

@admin_panel.route('/approved-product',methods=['GET'])
@admin_required
@login_required
def appproved_product():
    approved_product = Product.query.filter_by(status='Approved').all()
    
    return render_template('Admin/approved.html',products= approved_product)

@admin_panel.route('/approve_product/<int:product_id>', methods=['GET'])
@admin_required
@login_required
def approve_product(product_id):
   
    product = Product.query.get(product_id)
    
    if product:
     
        product.status = 'Approved'
        db.session.commit()
    
  
    return redirect(url_for('admin_panel.admin'))

@admin_panel.route('/decline_product/<int:product_id>', methods=['GET'])
@admin_required
@login_required
def decline_product(product_id):
   
    product = Product.query.get(product_id)
    
    if product:
     
        product.status = 'Declined'
        db.session.commit()
    return redirect(url_for('admin_panel.admin'))

