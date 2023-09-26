from flask import flash,redirect,url_for
from flask_login import current_user
from functools import wraps



def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Current User: {current_user}")
            if not current_user.is_authenticated:
                flash('You need to be logged in to access this page.', category='error')
                return redirect(url_for('auth.rider_login'))
            if hasattr(current_user, 'user_role') and current_user.user_role != role:
                flash(f'Access denied. You need to be a {role} to access this page.', category='error')
                return redirect(url_for('auth.rider_login')) 
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(route_func):
    @wraps(route_func)
    def decorated_route(*args, **kwargs):
        if current_user.is_anonymous:
            flash('You must log in to access this page.', category='error')
            return redirect(url_for('auth.login'))
        
        if current_user.role != 'admin':
            flash('You are not authorized to access this page.', category='error')
            return redirect(url_for('views.home'))  # Redirect non-admin users to a different page (if needed)

        return route_func(*args, **kwargs)

    return decorated_route