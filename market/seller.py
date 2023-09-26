from flask import Blueprint,render_template,request,flash,redirect,url_for,jsonify
from .decorator import login_required
from flask_login import current_user
import cloudinary.uploader
from .models import Seller,Product
from . import db 


sellers = Blueprint('sellers', __name__)

@sellers.route('/seller-home', methods=['GET'])
@login_required('seller')
def seller_home():
    seller_id = current_user.id
    products = Product.query.filter_by(seller_id=seller_id).all()
    
    return render_template('Seller/seller_page.html',user = current_user,products=products)


@sellers.route('/seller-dashboard', methods =['GET'])
@login_required('seller')
def seller_dashboard():
    
    
    return render_template('Seller/seller-dashboard.html', user = current_user)

@sellers.route('/seller-upload', methods =['GET'])
@login_required('seller')
def seller_upload():
    
    return render_template('Seller/upload-product.html', user = current_user)

@sellers.route('/seller-order-overview', methods =['GET'])
@login_required('seller')
def seller_order():
    
    return render_template('Seller/order-product.html', user = current_user)

@sellers.route('/upload', methods=['POST'])
@login_required('seller')
def upload_product():
    try:
        seller_id = current_user.id
        uploaded_image = request.files['product-img']

        if uploaded_image:
            category = request.form['product-categories']

            result = cloudinary.uploader.upload(
                uploaded_image,
                folder=f'product-images/{category}',
            )

            product_name = request.form.get('product-name')
            product_price = request.form.get('product-price')
            product_description = request.form.get('product-description')

          
            new_product = Product(
                name=product_name,
                price=product_price,
                description=product_description,
                image_url=result['secure_url'],
                category=category,
                seller_id=seller_id
            )

            db.session.add(new_product)
            db.session.commit()

            flash(f'Product uploaded successfully and is pending approval!', category='success')

            return redirect(url_for('sellers.seller_home'))

        else:
            flash('No image file provided.', category='error')
            return redirect(url_for('sellers.seller_home'))

    except Exception as e:
        flash(f'Error uploading product: {str(e)}', category='error')
        return redirect(url_for('sellers.seller_home'))

@sellers.route('/delete_products/<int:product_id>', methods=['DELETE'])
@login_required('sellers')
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        seller_id = current_user.id
        if seller_id == current_user.id:
          
            db.session.delete(product)
            db.session.commit()

           
            flash('Product deleted successfully', category='success')
            return jsonify({'message': 'Product deleted successfully'}), 200
        else:
          
            flash('Product not found or unauthorized', 'error')
            return jsonify({'error': 'Product not found or unauthorized'}), 404
    except Exception as e:
       
        flash(str(e), 'error')
        return jsonify({'error': str(e)}), 500


