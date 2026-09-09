import os
import re

app_file = r"d:\dbmss\app.py"

with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

new_auth_code = """
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import make_response

JWT_SECRET = os.getenv("SECRET_KEY", "super_secret_key_123")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('jwt_token')
        if not token:
            flash("Please log in to access this page.", "error")
            return redirect(url_for('login'))
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            session['user_id'] = payload['user_id']
            session['role'] = payload['role']
            session['username'] = payload['username']
        except jwt.ExpiredSignatureError:
            flash("Session expired. Please log in again.", "error")
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            flash("Invalid token. Please log in again.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role_selected = request.form.get('role', 'Admin')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT u.*, r.role_name FROM users u JOIN roles r ON u.role_id = r.role_id WHERE u.email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            if user['role_name'] != role_selected:
                flash(f"User is registered as {user['role_name']}, not {role_selected}. Please select correct role.", "error")
                return redirect(url_for('login'))
                
            payload = {
                'user_id': user['user_id'],
                'role': user['role_name'],
                'username': user['name'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }
            token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
            
            # Map role to correct dashboard
            redirect_map = {
                'Admin': 'dashboard',
                'Weaver': 'artisan_dashboard',
                'Supplier': 'supplier_dashboard',
                'Customer': 'marketplace',
                'Delivery Partner': 'shipment_dashboard'
            }
            
            resp = make_response(redirect(url_for(redirect_map.get(user['role_name'], 'dashboard'))))
            resp.set_cookie('jwt_token', token, httponly=True, secure=True)
            flash(f"Welcome {user['name']}! Authenticated successfully.", "success")
            return resp
        else:
            flash("Invalid email or password.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        role_name = request.form.get('role', 'Admin')
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        # Profile Data (from dynamic form fields)
        import json
        profile_data = {}
        for key, val in request.form.items():
            if key not in ['role', 'email', 'password', 'name']:
                profile_data[key] = val

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("Email already registered.", "error")
            return redirect(url_for('signup'))
            
        cursor.execute("SELECT role_id FROM roles WHERE role_name = %s", (role_name,))
        role = cursor.fetchone()
        if not role:
            flash("Invalid Role.", "error")
            return redirect(url_for('signup'))

        hashed_pw = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (role_id, email, password_hash, name) VALUES (%s, %s, %s, %s)",
            (role['role_id'], email, hashed_pw, name)
        )
        user_id = cursor.lastrowid
        
        cursor.execute(
            "INSERT INTO user_profiles (user_id, profile_data) VALUES (%s, %s)",
            (user_id, json.dumps(profile_data))
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')

@app.route('/verify_otp')
def verify_otp():
    return render_template('verify_otp.html')

@app.route('/supplier_dashboard')
@login_required
def supplier_dashboard():
    return render_template('dashboard.html') # Placeholder for now

@app.route('/marketplace')
@login_required
def marketplace():
    return render_template('dashboard.html') # Placeholder for now

@app.route('/shipment_dashboard')
@login_required
def shipment_dashboard():
    return render_template('dashboard.html') # Placeholder for now

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('jwt_token', '', expires=0)
    session.clear()
    flash("You have been logged out.", "success")
    return resp
"""

start_idx = content.find("# Decorator for requiring login")
end_idx = content.find("@app.route('/dashboard')")

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_auth_code + "\n" + content[end_idx:]
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Authentication logic updated.")
else:
    print("Could not find start/end bounds for replacement.")
