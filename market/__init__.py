from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView
import os
import bcrypt
from os import path
from flask_admin import Admin



db = SQLAlchemy(session_options={"autocommit": False, "expire_on_commit": False})
DB_NAME = "market.db"
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}?mod=wal '
    db.init_app(app)
    migrate.init_app(app, db)
  
          
    cloudinary.config( 
    cloud_name = "dwxmvddcd", 
    api_key = "485855482193362", 
    api_secret = "hvZOVNA9eJ8UVhJo5v-dODXHxAQ" 
)
    
    from .views import views
    from .auth import auth
    from .seller import sellers
    from .admin import admin_panel
    
    app.register_blueprint(auth,url_prefix='/auth')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(sellers,url_prefix='/')
    app.register_blueprint(admin_panel,url_prefix='/')
    
    from .models import User,Seller,Rider
    
    admin = Admin(app)
    
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Rider, db.session))
    admin.add_view(ModelView(Seller, db.session))

    
    create_database(app)
    with app.app_context():
        
        if len(User.query.all()) < 1:
            # Encrypt the password and save it in a variable
            hashed_password = bcrypt.hashpw('Adetutu'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
          
            # Create the admin user
            admin_user = User(
                role='admin',
                user_email='Basitadmin@gmail.com',
                user_state = 'Ogun state',
                user_password=hashed_password
            )
            
            db.session.add(admin_user)
            db.session.commit()
           

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
       type = session.get('type')
       if type == 'user':
           user = User.query.get(int(user_id))
       elif type == 'seller':
           user = Seller.query.get(int(user_id))
       elif type == 'rider':
           user = Rider.query.get(int(user_id))
       else:
           user = None
           
       return user
           
       
        
    
        
    return app

def create_database(app):
    with app.app_context():
        if not path.exists('market/' + DB_NAME):
            db.create_all()
