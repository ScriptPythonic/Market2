from flask import Flask,Blueprint,render_template,request,flash,redirect,url_for,abort,session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,logout_user,login_user,current_user
from .models import User,Seller,Rider
from . import db 
import bcrypt 


auth = Blueprint('auth', __name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')
      
        user = User.query.filter_by(user_email=email).first()
        if user:
            if  bcrypt.checkpw(password.encode('utf-8'), user.user_password.encode('utf-8')):
                user.user_role = 'user'
                db.session.commit()
                flash('Logged in successfully!', category='success')
                login_user(user, remember=False)
                session.permanent = True
                session['type'] = 'user'
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template('Auth/login.html')

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        state = request.form.get('states')

        user = User.query.filter_by(user_email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = User(user_email=email,  user_state = state ,user_password= hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False)
            flash('User Account created!', category='success')
            return redirect(url_for('auth.login'))

    
    return render_template('Auth/sign-up.html')

@auth.route('/seller-login',methods=['GET','POST'])
def seller_login():
  
        if request.method == 'POST':
            email = request.form.get('email').lower()
            password = request.form.get('password')

            user = Seller.query.filter_by(seller_email=email).first()
           
              
            if user:
                if check_password_hash(user.seller_password, password):
                    user.user_role = 'seller'
                   
                    db.session.commit()
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=False)
                    session.permanent = True
                    session['type'] = 'seller'
                    return redirect(url_for('sellers.seller_home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')
           
        return render_template('Auth/seller-login.html')
   

@auth.route('/rider-login',methods=['GET','POST'])
def rider_login():
  
        if request.method == 'POST':
            email = request.form.get('email').lower()
            password = request.form.get('password')

            user = Rider.query.filter_by(rider_email=email).first()
            if user:
                if check_password_hash(user.rider_password, password):
                    user.user_role = 'rider'
                    db.session.commit()
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=False)
                    session.permanent = True
                    session['type'] = 'rider'
                    return 
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')
    
        return render_template('Auth/rider-login.html')
    
    
@auth.route('/seller-signUp', methods=['GET', 'POST'])
def seller_sign_up():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        name = request.form.get('name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        state = request.form.get('states')

        seller = Seller.query.filter_by(seller_email=email).first()
        if seller:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_seller = Seller(
                seller_email=email,
                seller_state=state,
                seller_name=name,
                seller_last_name=last_name,
                seller_password=generate_password_hash(password1, method='scrypt')
            )
            db.session.add(new_seller)
            db.session.commit()
            flash('Seller Account created!', category='success')
            return redirect(url_for('auth.seller_login'))

    return render_template('Auth/seller-sign-up.html')

@auth.route('/rider-signUp',methods=['GET','POST'])
def rider_sign_up():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        name = request.form.get('name').capitalize()
        last_name= request.form.get('last_name').capitalize()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        state = request.form.get('states')

        rider = Rider.query.filter_by(rider_email=email).first()
        if rider:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_rider = Rider(rider_email=email,
                                    rider_name = name ,
                                    rider_state = state ,
                                    rider_last_name = last_name, 
                                    rider_password=generate_password_hash(  password1, method='scrypt')
                              )
            db.session.add(new_rider)
            db.session.commit()
           
            flash('Rider Account created!', category='success')
            return redirect(url_for('auth.rider_login'))

    
    return render_template('Auth/rider-sign-up.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category= 'success')
    return redirect(url_for('auth.login'))

