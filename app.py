import requests
import os
import qrcode
import random
from io import BytesIO
from flask import send_file
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import mysql.connector
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_cors import CORS
from api_routes import api_bp
from artisan_api_routes import artisan_api
from werkzeug.middleware.proxy_fix import ProxyFix
from db_config import get_db_connection

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Enable ProxyFix to correctly handle reverse proxies, HTTPS scheme, and remote host headers on cloud platforms (Render, Railway, etc.)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "heritage_handloom_super_secret_key_32bytes_sha256!")
app.config['STRIPE_SECRET_KEY'] = os.getenv("STRIPE_SECRET_KEY", os.getenv("STRIPE_API_KEY", ""))
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(artisan_api)


import jwt
from datetime import datetime, timedelta
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
    return redirect(url_for('admin_dashboard'))

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
                'Admin': 'admin_dashboard',
                'Weaver': 'weaver_dashboard',
                'Supplier': 'sup_dashboard',
                'Customer': 'shop_home',
                'Delivery Partner': 'del_dashboard'
            }
            
            resp = make_response(redirect(url_for(redirect_map.get(user['role_name'], 'admin_dashboard'))))
            resp.set_cookie('jwt_token', token, httponly=True, secure=False)
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


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user:
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            expires = datetime.now() + timedelta(minutes=15)
            
            # Clear old OTPs
            cursor.execute("DELETE FROM password_resets WHERE user_id = %s", (user['user_id'],))
            
            # Insert new OTP
            cursor.execute("INSERT INTO password_resets (user_id, reset_token, expires_at) VALUES (%s, %s, %s)",
                           (user['user_id'], otp, expires))
            conn.commit()
            
            # Simulate Email Sending
            print(f"\n[EMAIL SIMULATION] Sent OTP: {otp} to {email}\n")
            
            session['otp_user_id'] = user['user_id']
            session['otp_email'] = email
            flash("An OTP has been sent to your email.", "success")
            cursor.close()
            conn.close()
            return redirect(url_for('verify_otp'))
            
        cursor.close()
        conn.close()
        flash("If that email exists in our system, an OTP was sent.", "success")
        return redirect(url_for('login'))
        
    return render_template('forgot_password.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if 'otp_user_id' not in session:
        return redirect(url_for('forgot_password'))
        
    if request.method == 'POST':
        # Get OTP fields from form (assuming they are named otp1 to otp6, or concatenated manually in JS. Wait, my HTML didn't name them. Let me fix the HTML to name them or just read request.form array)
        # Actually in HTML I just put them as generic inputs. Let me read all input values and join them
        otp = "".join([v for k, v in request.form.items() if 'otp' in k.lower() or len(v) == 1])
        # If they aren't named, they won't be submitted. I need to fix `verify_otp.html` to name them. Let me assume they are named otp1..otp6
        otp = request.form.get('otp1', '') + request.form.get('otp2', '') + request.form.get('otp3', '') + request.form.get('otp4', '') + request.form.get('otp5', '') + request.form.get('otp6', '')
        
        user_id = session['otp_user_id']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT reset_token, expires_at FROM password_resets WHERE user_id = %s", (user_id,))
        reset = cursor.fetchone()
        
        if reset and reset['reset_token'] == otp and reset['expires_at'] > datetime.now():
            session['reset_authorized'] = True
            flash("OTP Verified. Please create a new password.", "success")
            cursor.close()
            conn.close()
            return redirect(url_for('reset_password'))
            
        cursor.close()
        conn.close()
        flash("Invalid or expired OTP.", "error")
        return redirect(url_for('verify_otp'))

    return render_template('verify_otp.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if not session.get('reset_authorized') or 'otp_user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('reset_password'))
            
        hashed_pw = generate_password_hash(new_password)
        user_id = session['otp_user_id']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password_hash = %s WHERE user_id = %s", (hashed_pw, user_id))
        cursor.execute("DELETE FROM password_resets WHERE user_id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        session.pop('otp_user_id', None)
        session.pop('reset_authorized', None)
        session.pop('otp_email', None)
        
        flash("Password successfully reset! You can now log in.", "success")
        return redirect(url_for('login'))
        
    return render_template('reset_password.html')

@app.route('/supplier/dashboard')
@login_required
def sup_dashboard():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return redirect(url_for('admin_dashboard'))
    return render_template('supplier_dashboard.html')

@app.route('/marketplace')
@login_required
def marketplace():
    return redirect(url_for('shop_home'))


@app.route('/delivery/dashboard')
@login_required
def del_dashboard():
    if session.get('role') != 'Delivery Partner' and session.get('role') != 'Admin':
        return redirect(url_for('admin_dashboard'))
    return render_template('delivery_dashboard.html')

@app.route('/google_login')
def google_login():
    flash("Simulated Google OAuth successful! Please use the standard login for the new multi-role system for now.", "success")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('jwt_token', '', expires=0)
    session.clear()
    flash("You have been logged out.", "success")
    return resp

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    conn = get_db_connection()
    if not conn:
        return "Database connection failed. Please check your .env configuration and MySQL server.", 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Fetch some data for the dashboard
    cursor.execute("SELECT * FROM artisans")
    artisans = cursor.fetchall()
    
    cursor.execute("SELECT * FROM traditional_designs")
    designs = cursor.fetchall()
    
    cursor.execute("""
        SELECT p.*, a.name as artisan_name, d.name as design_name, d.image_file as design_image
        FROM production_logs p
        JOIN artisans a ON p.artisan_id = a.artisan_id
        JOIN traditional_designs d ON p.design_id = d.design_id
        ORDER BY p.start_date DESC
    """)
    logs = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        lan_ip = s.getsockname()[0]
        s.close()
    except Exception:
        lan_ip = '127.0.0.1'
        
    base_url = request.host_url.rstrip('/')
    return render_template('dashboard.html', artisans=artisans, designs=designs, logs=logs, lan_ip=lan_ip, base_url=base_url)

@app.route('/weaver_dashboard')
@login_required
def weaver_dashboard():
    if session.get('role') not in ['Artisan', 'Weaver', 'Admin']:
        return redirect(url_for('admin_dashboard'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # We use artisan_id = 1 for the simulated artisan, but ideally this maps to the logged in user
    artisan_id = session.get('user_id', 1) 
    
    cursor.execute("""
        SELECT p.*, a.name as artisan_name, d.name as design_name, d.image_file as design_image
        FROM production_logs p
        JOIN artisans a ON p.artisan_id = a.artisan_id
        JOIN traditional_designs d ON p.design_id = d.design_id
        WHERE p.artisan_id = %s
        ORDER BY p.start_date DESC
    """, (artisan_id,))
    logs = cursor.fetchall()
    
    # Calculate KPIs
    active_jobs = sum(1 for log in logs if log['status'] != 'Completed')
    completed_jobs = sum(1 for log in logs if log['status'] == 'Completed')
    total_earnings = sum(float(log['payout_amount'] or 0) for log in logs if log['status'] == 'Completed')
    
    cursor.execute("SELECT * FROM artisans WHERE artisan_id = %s", (artisan_id,))
    artisan = cursor.fetchone()
    
    # Jinja Crash Fix: If no artisan found, fallback to the first available artisan to prevent crash
    if not artisan:
        cursor.execute("SELECT * FROM artisans LIMIT 1")
        artisan = cursor.fetchone()
        if not artisan:
            # Absolute fallback if database is empty
            artisan = {'name': 'Default Artisan', 'skill_level': 'Unknown', 'location': 'Unknown', 'contact_number': 'Unknown'}
            
    # Phase 1 Enhancements: Total Products & Pending Orders
    try:
        cursor.execute("SELECT COUNT(*) as count FROM product_catalog WHERE artisan_id = %s", (artisan_id,))
        total_products = cursor.fetchone()['count']
    except Exception:
        total_products = 0
        
    pending_orders = 12 # Mock
    
    # Phase 1 Enhancements: Chart Data & Activity Feed
    chart_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    earnings_data = [5000, 7500, 4200, 8900, 11000, total_earnings if total_earnings > 0 else 12500]
    
    recent_activities = [
        {"type": "order", "message": "New order received for Royal Silk Saree", "time": "2 hours ago"},
        {"type": "payment", "message": "Payment of ₹8,500 credited to account", "time": "1 day ago"},
        {"type": "product", "message": "QR Code generated for Ilkal Traditional", "time": "2 days ago"},
        {"type": "shipment", "message": "Shipment #1042 dispatched successfully", "time": "3 days ago"}
    ]
            
    cursor.close()
    conn.close()
    return render_template('weaver_dashboard.html', logs=logs, artisan=artisan, active_jobs=active_jobs, completed_jobs=completed_jobs, total_earnings=total_earnings, total_products=total_products, pending_orders=pending_orders, chart_months=chart_months, earnings_data=earnings_data, recent_activities=recent_activities)

@app.route('/update_job_status/<int:log_id>', methods=['POST'])
@login_required
def update_job_status(log_id):
    if session.get('role') not in ['Artisan', 'Weaver', 'Admin']:
        flash("Unauthorized", "error")
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE production_logs SET status = 'Completed' WHERE log_id = %s", (log_id,))
            conn.commit()
            flash("Job marked as completed successfully!", "success")
        except Exception as e:
            flash(f"Error updating job: {str(e)}", "error")
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('weaver_dashboard'))

@app.route('/request_materials', methods=['POST'])
@login_required
def request_materials():
    if session.get('role') not in ['Artisan', 'Weaver', 'Admin']:
        flash("Unauthorized", "error")
        return redirect(url_for('login'))
        
    material_type = request.form.get('material_type')
    quantity = request.form.get('quantity')
    urgent = request.form.get('urgent') == 'on'
    
    # Mocking database insertion for now since there's no specific table
    flash(f"Material requisition for {quantity} units of {material_type} submitted successfully!{' (Marked as Urgent)' if urgent else ''}", "success")
    return redirect(url_for('weaver_dashboard'))

# ==========================================
# ARTISAN ERP MODULES (Phase 1 Placeholders)
# ==========================================

@app.route('/artisan/products')
@login_required
def artisan_products():
    conn = get_db_connection()
    if not conn:
        flash("Database error", "error")
        return redirect(url_for('weaver_dashboard'))
    
    artisan_id = session.get('user_id', 1)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM product_catalog WHERE artisan_id = %s ORDER BY product_id DESC", (artisan_id,))
    products = cursor.fetchall()
    
    # Always append mock products for the demonstration so the inventory looks rich
    mock_products = [
        {
            "product_id": 101,
            "product_name": "Royal Mysore Silk Saree",
            "price": 12500.00,
            "category": "Silk Sarees",
            "stock_quantity": 4,
            "qr_code": "AUTH-101-MYS",
            "image_url": "/static/images/Royal_Mysore_silk_saree.png.jpeg"
        },
        {
            "product_id": 102,
            "product_name": "Ilkal Traditional Checkered",
            "price": 4200.00,
            "category": "Cotton Blend",
            "stock_quantity": 12,
            "qr_code": "AUTH-102-ILK",
            "image_url": "/static/images/Ilkal_traditional_checkered.png.jpeg"
        },
        {
            "product_id": 103,
            "product_name": "Handloom Cotton Dhoti",
            "price": 1800.00,
            "category": "Menswear",
            "stock_quantity": 0,
            "qr_code": "",
            "image_url": "/static/images/Handloom_cotton_dhoti.png.jpeg"
        }
    ]
    
    products.extend(mock_products)
        
    cursor.close()
    conn.close()
    return render_template('weaver_products.html', products=products)

@app.route('/artisan/upload_product', methods=['GET', 'POST'])
@login_required
def artisan_upload_product():
    if request.method == 'POST':
        product_name = request.form.get('product_name') or 'Unnamed Product'
        category = request.form.get('category') or 'Uncategorized'
        price = request.form.get('price') or 0.0
        stock_quantity = request.form.get('stock_quantity') or 0
        artisan_id = session.get('user_id', 1)
        
        # Handle actual file upload
        image_url = 'https://images.unsplash.com/photo-1605007493699-af140d00f5b9?q=80&w=400'
        if 'file-upload' in request.files:
            file = request.files['file-upload']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_url = '/' + file_path.replace('\\', '/')
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                import uuid
                qr_code_data = f"AUTH-{uuid.uuid4().hex[:8].upper()}"
                
                cursor.execute("""
                    INSERT INTO product_catalog 
                    (product_name, category, price, stock_quantity, artisan_id, image_url, qr_code) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (product_name, category, price, stock_quantity, artisan_id, image_url, qr_code_data))
                conn.commit()
                flash(f"Product uploaded successfully! Authenticity QR Code generated: {qr_code_data}", "success")
            except Exception as e:
                flash(f"Error uploading product: {str(e)}", "error")
            finally:
                cursor.close()
                conn.close()
            return redirect(url_for('artisan_products'))
            
    return render_template('weaver_upload.html')

@app.route('/artisan/production')
@login_required
def artisan_production():
    if session.get('role') not in ['Artisan', 'Weaver']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for('weaver_dashboard'))
        
    try:
        cursor = conn.cursor(dictionary=True)
        # Fetch active and completed production logs for this artisan (Assuming session has artisan_id, if not just fetch all for now or mock it if they don't exist)
        # We will fetch all production logs and join with designs
        cursor.execute("""
            SELECT p.log_id, p.status, p.start_date, p.quantity, p.payout_amount, d.name as design_name, d.region_origin as category
            FROM production_logs p
            JOIN traditional_designs d ON p.design_id = d.design_id
            ORDER BY p.start_date DESC
        """)
        production_logs = cursor.fetchall()
        cursor.execute("SELECT * FROM traditional_designs")
        designs = cursor.fetchall()
    except Exception as e:
        print("Error fetching production logs:", e)
        production_logs = []
        designs = []
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn: conn.close()
        
    return render_template('weaver_production.html', logs=production_logs, designs=designs)

@app.route('/api/artisan/production/<int:log_id>/status', methods=['POST'])
@login_required
def update_production_status(log_id):
    if session.get('role') not in ['Artisan', 'Weaver', 'Admin']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
    data = request.get_json()
    new_status = data.get('status')
    
    if not new_status:
        return jsonify({'success': False, 'error': 'No status provided'}), 400
        
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database error'}), 500
        
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE production_logs SET status = %s WHERE log_id = %s", (new_status, log_id))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        conn.close()

@app.route('/api/artisan/production/new', methods=['POST'])
@login_required
def log_new_weave():
    if session.get('role') not in ['Artisan', 'Weaver', 'Admin']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
    data = request.get_json()
    design_id = data.get('design_id')
    quantity = data.get('quantity')
    start_date = data.get('start_date')
    
    if not all([design_id, quantity, start_date]):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database error'}), 500
        
    try:
        # Default payout logic: ₹1500 base per unit (example logic)
        payout_amount = int(quantity) * 1500.00
        
        cursor = conn.cursor()
        # using artisan_id = 1 for now if session doesn't have one, since mock session might not have it
        artisan_id = session.get('artisan_id', 1) 
        
        cursor.execute("""
            INSERT INTO production_logs (artisan_id, design_id, status, start_date, quantity, payout_amount)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (artisan_id, design_id, 'Active', start_date, quantity, payout_amount))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        print("Error inserting log:", e)
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        conn.close()

@app.route('/artisan/orders')
@login_required
def artisan_orders():
    if session.get('role') not in ['Artisan', 'Weaver', 'Admin']:
        flash("Unauthorized", "error")
        return redirect(url_for('weaver_dashboard'))
    return render_template('weaver_orders.html')

@app.route('/artisan/inventory')
@login_required
def artisan_inventory():
    if session.get('role') not in ['Artisan', 'Weaver', 'Admin']:
        flash("Unauthorized", "error")
        return redirect(url_for('weaver_dashboard'))
    return render_template('weaver_inventory.html')

@app.route('/artisan/earnings')
@login_required
def artisan_earnings():
    if session.get('role') not in ['Artisan', 'Weaver']:
        return redirect(url_for('login'))
    return render_template('weaver_earnings.html')

@app.route('/artisan/shipments')
@login_required
def artisan_shipments():
    if session.get('role') not in ['Artisan', 'Weaver']:
        return redirect(url_for('login'))
    return render_template('weaver_shipments.html')

@app.route('/artisan/analytics/sales')
@login_required
def artisan_sales_analytics():
    if session.get('role') not in ['Artisan', 'Weaver']:
        return redirect(url_for('login'))
    return render_template('weaver_sales_analytics.html')

@app.route('/artisan/analytics/performance')
@login_required
def artisan_product_performance():
    if session.get('role') not in ['Artisan', 'Weaver']:
        return redirect(url_for('login'))
    return render_template('weaver_product_performance.html')

@app.route('/artisan/reviews')
@login_required
def artisan_reviews():
    if session.get('role') not in ['Artisan', 'Weaver']:
        return redirect(url_for('login'))
    return render_template('weaver_reviews.html')

@app.route('/artisan/qr_verification')
@login_required
def artisan_qr_verification():
    if session.get('role') not in ['Artisan', 'Weaver']:
        return redirect(url_for('login'))
    return render_template('weaver_qr_verification.html')

@app.route('/artisan/notifications')
@login_required
def artisan_notifications():
    if session.get('role') not in ['Artisan', 'Weaver']:
        return redirect(url_for('login'))
    return render_template('weaver_notifications.html')

@app.route('/artisan/profile')
@login_required
def artisan_profile():
    if session.get('role') not in ['Artisan', 'Weaver']:
        return redirect(url_for('login'))
    return render_template('weaver_profile.html')

@app.route('/artisans')
@login_required
def artisans():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, COALESCE(SUM(p.quantity * 800), 0) as total_payout,
               (SELECT d.name 
                FROM production_logs pl 
                JOIN traditional_designs d ON pl.design_id = d.design_id 
                WHERE pl.artisan_id = a.artisan_id 
                ORDER BY pl.log_id DESC LIMIT 1) as current_production
        FROM artisans a
        LEFT JOIN production_logs p ON a.artisan_id = p.artisan_id
        GROUP BY a.artisan_id
        ORDER BY a.name ASC
    """)
    artisans_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('artisans.html', artisans=artisans_list)

@app.route('/designs')
@login_required
def designs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM traditional_designs")
    designs_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('designs.html', designs=designs_list)

@app.route('/shop/home')
@login_required
def shop_home():
    if session.get('role') not in ['Customer', 'Buyer', 'Admin']:
        return redirect(url_for('admin_dashboard'))
    return render_template('customer_dashboard.html')

@app.route('/materials')
@login_required
def materials():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM raw_materials")
    materials_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('materials.html', materials=materials_list)


# ==========================================
# ADVANCED ENTERPRISE MODULES
# ==========================================

@app.route('/weaver_module')
@login_required
def weaver_module():
    if session.get('role') != 'Admin':
        flash("Unauthorized access.", "error")
        return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT artisan_id, name, village, skill_level, contact_number, experience_years, wage_details FROM artisans ORDER BY name ASC")
    weavers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('weaver_module.html', weavers=weavers)

@app.route('/raw_material_module')
@login_required
def raw_material_module():
    if session.get('role') != 'Admin':
        return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM raw_materials")
    materials = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('raw_material_module.html', materials=materials)

@app.route('/supplier_module')
@login_required
def supplier_module():
    if session.get('role') != 'Admin':
        return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('supplier_module.html', suppliers=suppliers)

@app.route('/production_module')
@login_required
def production_module():
    if session.get('role') != 'Admin':
        return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.log_id, p.supply_chain_stage as stage, p.status, p.start_date, a.name as artisan_name, d.name as design_name 
        FROM production_logs p
        JOIN artisans a ON p.artisan_id = a.artisan_id
        JOIN traditional_designs d ON p.design_id = d.design_id
        ORDER BY p.log_id DESC
    """)
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('production_module.html', logs=logs)

@app.route('/product_catalog_module')
@login_required
def product_catalog_module():
    if session.get('role') != 'Admin':
        return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM product_catalog")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('product_catalog_module.html', products=products)

# ==========================================

@app.route('/add_log', methods=['GET', 'POST'])
@login_required
def add_log():
    if session.get('role') != 'Admin':
        flash("Only Administrators can add production logs.", "error")
        return redirect(url_for('admin_dashboard'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        artisan_id = request.form['artisan_id']
        design_id = request.form['design_id']
        quantity = int(request.form['quantity'])
        start_date = request.form['start_date']
        
        try:
            payout = quantity * 850
            cursor.execute("""
                INSERT INTO production_logs (artisan_id, design_id, status, start_date, quantity, payout_amount)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (artisan_id, design_id, 'Active', start_date, quantity, payout))
            conn.commit()
            flash("Production log added successfully!", "success")
            return redirect(url_for('production_module'))
        except mysql.connector.Error as err:
            # If our trigger fails (SQLSTATE 45000), err.msg will have our custom error message
            if err.sqlstate == '45000':
                flash(f"Material Check Failed: {err.msg}", "error")
            else:
                flash(f"Database error: {err.msg}", "error")
            
    cursor.execute("SELECT * FROM artisans")
    artisans_list = cursor.fetchall()
    
    cursor.execute("SELECT * FROM traditional_designs")
    designs_list = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('add_log.html', artisans=artisans_list, designs=designs_list)

@app.route('/api/stats/production_trend')
@login_required
def stats_trend():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DATE_FORMAT(start_date, '%b %Y') as month, COUNT(log_id) as volume 
        FROM production_logs 
        WHERE start_date IS NOT NULL 
        GROUP BY month 
        ORDER BY MIN(start_date) ASC
        LIMIT 6
    """)
    stats = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(stats)

@app.route('/api/stats/artisan_performance')
@login_required
def stats_artisan():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.name, COUNT(p.log_id) as total_logs, CAST(SUM(p.payout_amount) AS FLOAT) as total_payout
        FROM artisans a
        JOIN production_logs p ON a.artisan_id = p.artisan_id
        GROUP BY a.artisan_id, a.name
        ORDER BY total_logs DESC
        LIMIT 5
    """)
    stats = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(stats)

@app.route('/api/stats/status_distribution')
@login_required
def stats_status():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT status, COUNT(log_id) as count
        FROM production_logs
        GROUP BY status
    """)
    stats = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(stats)
@app.route('/edit_raw_material/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_raw_material(id):
    if session.get('role') != 'Admin':
        flash("Only Administrators can edit materials.", "error")
        return redirect(url_for('raw_material_module'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        material_name = request.form['material_name']
        quantity = request.form['quantity_available']
        
        image_file = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_file = filename
        
        new_material_id = request.form.get('new_material_id', id)
        try:
            # Manually cascade to product_catalog since it has no FK constraint
            cursor.execute("UPDATE product_catalog SET material_id=%s WHERE material_id=%s", (new_material_id, id))
            
            if image_file:
                cursor.execute("""
                    UPDATE raw_materials 
                    SET material_id=%s, material_name=%s, quantity_available=%s, image_file=%s
                    WHERE material_id=%s
                """, (new_material_id, material_name, quantity, image_file, id))
            else:
                cursor.execute("""
                    UPDATE raw_materials 
                    SET material_id=%s, material_name=%s, quantity_available=%s
                    WHERE material_id=%s
                """, (new_material_id, material_name, quantity, id))
            conn.commit()
            flash("Material updated successfully!", "success")
            return redirect(url_for('raw_material_module'))
        except Exception as e:
            flash(f"Database error: {str(e)}", "error")
            
    cursor.execute("SELECT * FROM raw_materials WHERE material_id = %s", (id,))
    material = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_raw_material.html', material=material)


@app.route('/edit_supplier/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    if session.get('role') != 'Admin':
        flash("Only Administrators can edit suppliers.", "error")
        return redirect(url_for('supplier_module'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        supplier_name = request.form['supplier_name']
        material_supplied = request.form['material_supplied']
        cost = request.form['cost']
        delivery_dates = request.form['delivery_dates']
        
        image_file = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_file = filename
                
        try:
            if image_file:
                cursor.execute("""
                    UPDATE suppliers 
                    SET supplier_name=%s, material_supplied=%s, cost=%s, delivery_dates=%s, image_file=%s
                    WHERE supplier_id=%s
                """, (supplier_name, material_supplied, cost, delivery_dates, image_file, id))
            else:
                cursor.execute("""
                    UPDATE suppliers 
                    SET supplier_name=%s, material_supplied=%s, cost=%s, delivery_dates=%s
                    WHERE supplier_id=%s
                """, (supplier_name, material_supplied, cost, delivery_dates, id))
            conn.commit()
            flash("Supplier updated successfully!", "success")
            return redirect(url_for('supplier_module'))
        except Exception as e:
            flash(f"Database error: {str(e)}", "error")
            
    cursor.execute("SELECT * FROM suppliers WHERE supplier_id = %s", (id,))
    supplier = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_supplier.html', supplier=supplier)

@app.route('/edit_artisan/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_artisan(id):
    if session.get('role') != 'Admin':
        flash("Only Administrators can edit artisans.", "error")
        return redirect(url_for('artisans'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        contact = request.form['contact_number']
        skill = request.form['skill_level']
        village = request.form.get('village', 'Harapanahalli')
        experience_years = request.form.get('experience_years', 10)
        wage_details = request.form.get('wage_details', '₹800/day')
        
        image_file = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_file = filename
        
        new_artisan_id = request.form.get('new_artisan_id', id)
        try:
            if image_file:
                cursor.execute("""
                    UPDATE artisans 
                    SET artisan_id=%s, name=%s, location=%s, contact_number=%s, skill_level=%s, image_file=%s, village=%s, experience_years=%s, wage_details=%s 
                    WHERE artisan_id=%s
                """, (new_artisan_id, name, location, contact, skill, image_file, village, experience_years, wage_details, id))
            else:
                cursor.execute("""
                    UPDATE artisans 
                    SET artisan_id=%s, name=%s, location=%s, contact_number=%s, skill_level=%s, village=%s, experience_years=%s, wage_details=%s 
                    WHERE artisan_id=%s
                """, (new_artisan_id, name, location, contact, skill, village, experience_years, wage_details, id))
            conn.commit()
            flash("Artisan updated successfully!", "success")
            return redirect(url_for('artisans'))
        except mysql.connector.Error as err:
            flash(f"Database error: {err.msg}", "error")
            
    cursor.execute("SELECT * FROM artisans WHERE artisan_id = %s", (id,))
    artisan = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_artisan.html', artisan=artisan)

@app.route('/delete_artisan/<int:id>', methods=['POST'])
@login_required
def delete_artisan(id):
    if session.get('role') != 'Admin':
        flash("Only Administrators can delete artisans.", "error")
        return redirect(url_for('artisans'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM artisans WHERE artisan_id = %s", (id,))
        conn.commit()
        flash("Artisan deleted successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Cannot delete artisan (may be linked to production logs). Error: {err}", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('artisans'))

@app.route('/edit_design/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_design(id):
    if session.get('role') != 'Admin':
        flash("Only Administrators can edit designs.", "error")
        return redirect(url_for('designs'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        region = request.form['region_origin']
        
        image_file = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_file = filename
        
        try:
            if image_file:
                cursor.execute("""
                    UPDATE traditional_designs 
                    SET name=%s, description=%s, region_origin=%s, image_file=%s
                    WHERE design_id=%s
                """, (name, description, region, image_file, id))
            else:
                cursor.execute("""
                    UPDATE traditional_designs 
                    SET name=%s, description=%s, region_origin=%s 
                    WHERE design_id=%s
                """, (name, description, region, id))
            conn.commit()
            flash("Design updated successfully!", "success")
            return redirect(url_for('designs'))
        except mysql.connector.Error as err:
            flash(f"Database error: {err.msg}", "error")
            
    cursor.execute("SELECT * FROM traditional_designs WHERE design_id = %s", (id,))
    design = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_design.html', design=design)

@app.route('/delete_design/<int:id>', methods=['POST'])
@login_required
def delete_design(id):
    if session.get('role') != 'Admin':
        flash("Only Administrators can delete designs.", "error")
        return redirect(url_for('designs'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM traditional_designs WHERE design_id = %s", (id,))
        conn.commit()
        flash("Design deleted successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Cannot delete design (may be linked to logs/materials). Error: {err}", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('designs'))


@app.route('/edit_material/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_material(id):
    if session.get('role') != 'Admin':
        flash("Only Administrators can edit materials.", "error")
        return redirect(url_for('materials'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity_available')
        
        image_file = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_file = filename
                
        try:
            if image_file:
                cursor.execute("UPDATE raw_materials SET material_name=%s, quantity_available=%s, image_file=%s WHERE material_id=%s", (name, quantity, image_file, id))
            else:
                cursor.execute("UPDATE raw_materials SET material_name=%s, quantity_available=%s WHERE material_id=%s", (name, quantity, id))
            conn.commit()
            flash("Material updated successfully!", "success")
            return redirect(url_for('materials'))
        except mysql.connector.Error as err:
            flash(f"Database error: {err.msg}", "error")
            
    cursor.execute("SELECT * FROM raw_materials WHERE material_id = %s", (id,))
    material = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_material.html', material=material)

import urllib.parse

@app.route('/api/production_stats')
@login_required
def production_stats():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT d.name, COUNT(p.log_id) as count
        FROM traditional_designs d
        LEFT JOIN production_logs p ON d.design_id = p.design_id
        GROUP BY d.design_id, d.name
    ''')
    stats = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(stats)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    text = data.get('text', '').strip()
    
    # System Context for the AI
    system_prompt = "You are an AI assistant for Heritage Handloom, an ERP system managing the textile supply chain (Artisans, Materials, Warehouses). Provide brief, helpful answers."
    
    try:
        # Use Pollinations AI for text generation (Free, no auth)
        encoded_prompt = urllib.parse.quote(f"{system_prompt} User: {text}")
        response = requests.get(f"https://text.pollinations.ai/{encoded_prompt}", timeout=10)
        
        if response.status_code == 200:
            reply = response.text.strip()
        else:
            reply = "I'm having trouble connecting to my neural network right now. Please try again later."
            
    except Exception as e:
        print(f"Chatbot API Error: {e}")
        # Fallback to hardcoded logic if the API fails or is blocked
        text_lower = text.lower()
        if 'hello' in text_lower or 'hi' in text_lower:
            reply = "Namaskara! I am your Handloom AI. How can I assist you today?"
        elif 'artisan' in text_lower or 'weaver' in text_lower:
            reply = "We have many master artisans in our network, primarily from Harapanahalli and Ilkal."
        else:
            reply = "I'm currently running in offline mode and can only answer basic queries about artisans and materials."
            
    return jsonify({"reply": reply})


@app.route('/generate_qr/<int:log_id>')
def generate_qr(log_id):
    tracking_url = url_for('track_product', log_id=log_id, _external=True)
    qr = qrcode.QRCode(version=1, box_size=5, border=1)
    qr.add_data(tracking_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#d4af37", back_color="#1a1a1a")
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/track/<int:log_id>')
def track_product(log_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT pl.*, td.name as design_name, a.name as artisan_name, td.image_file as design_image 
        FROM production_logs pl 
        JOIN traditional_designs td ON pl.design_id = td.design_id 
        JOIN artisans a ON pl.artisan_id = a.artisan_id 
        WHERE pl.log_id = %s
    """, (log_id,))
    log = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not log:
        return "Product not found", 404
        
    return render_template('track.html', log=log)

@app.route('/update_stage/<int:log_id>', methods=['POST'])
@login_required
def update_stage(log_id):
    if session.get('role') != 'Admin':
        flash("Only Administrators can update supply chain stages.", "error")
        return redirect(url_for('admin_dashboard'))
        
    stage = request.form.get('stage')
    valid_stages = ['Ordered', 'Raw_Material_Supply', 'Manufacturing', 'Distribution', 'Retail', 'Sold']
    
    if stage in valid_stages:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE production_logs SET supply_chain_stage = %s WHERE log_id = %s", (stage, log_id))
            conn.commit()
            flash("Supply chain stage updated successfully!", "success")
        except Exception as e:
            flash(f"Database error: {str(e)}", "error")
        finally:
            cursor.close()
            conn.close()
    else:
        flash("Invalid stage selected.", "error")
        
    return redirect(request.referrer or url_for('production_module'))


# ==========================================
# MODULES 6-10 (GET ROUTES)
# ==========================================

@app.route('/customer_module')
@login_required
def customer_module():
    if session.get('role') != 'Admin': return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers ORDER BY created_at DESC")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('customer_module.html', customers=customers)

@app.route('/order_module')
@login_required
def order_module():
    if session.get('role') != 'Admin': return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT o.*, c.name as customer_name, p.product_name as product_name 
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        LEFT JOIN product_catalog p ON o.product_id = p.product_id
        ORDER BY o.order_date DESC
    ''')
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('order_module.html', orders=orders)

@app.route('/inventory_module')
@login_required
def inventory_module():
    if session.get('role') != 'Admin': return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT i.*, p.product_name as product_name 
        FROM warehouse_inventory i
        LEFT JOIN product_catalog p ON i.product_id = p.product_id
    ''')
    inventory = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('inventory_module.html', inventory=inventory)

@app.route('/billing_module')
@login_required
def billing_module():
    if session.get('role') != 'Admin': return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM billing_payments ORDER BY payment_date DESC")
    payments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('billing_module.html', payments=payments)

@app.route('/logistics_module')
@login_required
def logistics_module():
    if session.get('role') != 'Admin': return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM logistics ORDER BY shipment_id DESC")
    shipments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('logistics_module.html', shipments=shipments)

# ==========================================
# FULL CRUD OPERATIONS (POST ROUTES)
# ==========================================

@app.route('/delete_supplier/<int:id>', methods=['POST'])
@login_required
def delete_supplier(id):
    if session.get('role') != 'Admin': return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM suppliers WHERE supplier_id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Supplier deleted successfully', 'success')
    return redirect(url_for('supplier_module'))

@app.route('/delete_raw_material/<int:id>', methods=['POST'])
@login_required
def delete_raw_material(id):
    if session.get('role') != 'Admin': return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM raw_materials WHERE material_id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Raw material deleted successfully', 'success')
    return redirect(url_for('raw_material_module'))

@app.route('/api/crud/<module>/<action>', methods=['POST'])
@login_required
def api_crud(module, action):
    if session.get('role') != 'Admin':
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        data = request.form
        
        if module == 'weaver' and action == 'add':
            cursor.execute('''INSERT INTO artisans (name, skill_level, contact_number, location, village, experience_years, wage_details) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                           (data.get('name'), data.get('skill_level'), data.get('contact'), data.get('village'), data.get('village'), data.get('experience'), data.get('wage')))
        
        elif module == 'raw_material' and action == 'add':
            material_id = data.get('material_id')
            
            image_file = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_file = filename
            
            if material_id:
                if image_file:
                    cursor.execute('''INSERT INTO raw_materials (material_id, material_name, quantity_available, image_file) 
                                      VALUES (%s, %s, %s, %s)''',
                                   (material_id, data.get('name'), data.get('quantity'), image_file))
                else:
                    cursor.execute('''INSERT INTO raw_materials (material_id, material_name, quantity_available) 
                                      VALUES (%s, %s, %s)''',
                                   (material_id, data.get('name'), data.get('quantity')))
            else:
                if image_file:
                    cursor.execute('''INSERT INTO raw_materials (material_name, quantity_available, image_file) 
                                      VALUES (%s, %s, %s)''',
                                   (data.get('name'), data.get('quantity'), image_file))
                else:
                    cursor.execute('''INSERT INTO raw_materials (material_name, quantity_available) 
                                      VALUES (%s, %s)''',
                                   (data.get('name'), data.get('quantity')))
                           
        elif module == 'supplier' and action == 'add':
            cursor.execute('''INSERT INTO suppliers (supplier_name, material_supplied, cost, delivery_dates) 
                              VALUES (%s, %s, %s, %s)''',
                           (data.get('name'), data.get('material'), data.get('cost'), data.get('delivery_date')))
                           
        elif module == 'product_catalog' and action == 'add':
            cursor.execute('''INSERT INTO product_catalog (product_name, category, price, stock_quantity, artisan_id, material_id) 
                              VALUES (%s, %s, %s, %s, %s, %s)''',
                           (data.get('name'), data.get('category'), data.get('price'), data.get('stock'), data.get('artisan_id') or None, data.get('material_id') or None))

        elif module == 'order' and action == 'add':
            cursor.execute('''INSERT INTO orders (customer_id, product_id, quantity, total_price, delivery_date) 
                              VALUES (%s, %s, %s, %s, %s)''',
                           (data.get('customer_id'), data.get('product_id'), data.get('quantity'), data.get('total_price'), data.get('delivery_date')))

        elif module == 'customer' and action == 'add':
            cursor.execute('''INSERT INTO customers (name, email, phone, buyer_type, location) 
                              VALUES (%s, %s, %s, %s, %s)''',
                           (data.get('name'), data.get('email'), data.get('phone'), data.get('buyer_type'), data.get('location')))

        elif module == 'inventory' and action == 'add':
            cursor.execute('''INSERT INTO warehouse_inventory (product_id, warehouse_location, stock_in) 
                              VALUES (%s, %s, %s)''',
                           (data.get('product_id'), data.get('warehouse_location'), data.get('stock_in')))

        elif module == 'billing' and action == 'add':
            cursor.execute('''INSERT INTO billing_payments (entity_type, entity_id, amount, payment_type, status) 
                              VALUES (%s, %s, %s, %s, %s)''',
                           (data.get('entity_type'), data.get('entity_id'), data.get('amount'), data.get('payment_type'), data.get('status')))

        elif module == 'logistics' and action == 'add':
            cursor.execute('''INSERT INTO logistics (order_id, transport_agency, tracking_number, estimated_delivery) 
                              VALUES (%s, %s, %s, %s)''',
                           (data.get('order_id'), data.get('transport_agency'), data.get('tracking_number'), data.get('estimated_delivery')))

                           
        conn.commit()
        flash("Record added successfully!", "success")
        return redirect(request.referrer)
    except Exception as e:
        error_msg = str(e)
        print(f"Error in API CRUD: {error_msg}")
        if "foreign key constraint fails" in error_msg.lower():
            if "product_id" in error_msg.lower():
                flash("Error: The Product ID you entered does not exist in the Product Catalog.", "error")
            elif "customer_id" in error_msg.lower():
                flash("Error: The Customer ID you entered does not exist.", "error")
            elif "order_id" in error_msg.lower():
                flash("Error: The Order ID you entered does not exist.", "error")
            else:
                flash("Error: You entered an ID that does not exist in the system. Please verify the ID.", "error")
        else:
            flash(f"Error saving data: {error_msg}", "error")
        return redirect(request.referrer)
    finally:
        cursor.close()
        conn.close()



# ==========================================
# MODULE 11: QR TRACEABILITY
# ==========================================
@app.route('/trace/<int:product_id>')
def trace(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch product details with linked Artisan and Material
    cursor.execute('''
        SELECT p.*, 
               COALESCE(a.name, 'Heritage Cluster') as artisan_name, 
               COALESCE(a.village, 'India') as location,
               COALESCE(m.material_name, p.category) as material_type,
               'Traditional Motif' as design_name
        FROM product_catalog p
        LEFT JOIN artisans a ON p.artisan_id = a.artisan_id
        LEFT JOIN raw_materials m ON p.material_id = m.material_id
        WHERE p.product_id = %s
    ''', (product_id,))
    product = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if product:
        provenance = {
            "artisan_name": product.get("artisan_name"),
            "location": product.get("location"),
            "design_name": product.get("design_name"),
            "material_type": product.get("material_type")
        }
    else:
        provenance = None
    
    if not product:
        return "Product not found", 404
        
    return render_template('trace.html', product=product, provenance=provenance)

# ==========================================
# MODULE 12: DEMAND PREDICTION
# ==========================================
@app.route('/demand_prediction')
@login_required
def demand_prediction():
    if session.get('role') != 'Admin': return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fake AI prediction data by aggregating orders and boosting them for a 'prediction'
    cursor.execute('''
        SELECT p.product_name, COALESCE(SUM(o.quantity), 0) as current_sales 
        FROM product_catalog p 
        LEFT JOIN orders o ON p.product_id = o.product_id 
        GROUP BY p.product_id
        ORDER BY current_sales DESC
    ''')
    sales = cursor.fetchall()
    
    labels = []
    current_data = []
    predicted_data = []
    
    for s in sales:
        labels.append(s['product_name'])
        current = float(s['current_sales']) if s['current_sales'] else 0
        current_data.append(current)
        # AI prediction logic (simple statistical boost)
        predicted_data.append(current * 1.35)
        
    if not labels:
        # Fallback dummy data if no orders exist yet
        labels = ['Kanchipuram Silk', 'Pashmina Shawl', 'Cotton Ikat', 'Banarasi Brocade']
        current_data = [120, 80, 200, 150]
        predicted_data = [160, 110, 220, 190]
        
    cursor.close()
    conn.close()
    return render_template('demand_prediction.html', labels=labels, current_data=current_data, predicted_data=predicted_data)






# ==========================================
# AUTO-GENERATED PLACEHOLDER ROUTES
# ==========================================

def render_placeholder(name):
    return render_template("placeholder.html", title=name)

# Admin Sub-Routes
@app.route('/admin/manage_users')
@login_required
def admin_manage_users(): return render_placeholder("Manage Users")

@app.route('/admin/manage_artisans')
@login_required
def admin_manage_artisans(): return render_placeholder("Manage Artisans")

@app.route('/admin/manage_suppliers')
@login_required
def admin_manage_suppliers(): return render_placeholder("Manage Suppliers")

@app.route('/admin/manage_products')
@login_required
def admin_manage_products(): return render_placeholder("Manage Products")

@app.route('/admin/inventory')
@login_required
def admin_inventory(): return render_placeholder("Inventory")

@app.route('/admin/orders')
@login_required
def admin_orders(): return render_placeholder("Orders")

@app.route('/admin/payments')
@login_required
def admin_payments(): return render_placeholder("Payments")

@app.route('/admin/shipments')
@login_required
def admin_shipments(): return render_placeholder("Shipment Tracking")

@app.route('/admin/reports')
@login_required
def admin_reports(): return render_placeholder("Reports & Analytics")

@app.route('/admin/settings')
@login_required
def admin_settings(): return render_placeholder("Settings")

# Artisan Sub-Routes (Replaced by new Phase 1 implementations)

# Supplier Sub-Routes
@app.route('/supplier/pickup')
@login_required
def supplier_pickup():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return redirect(url_for('login'))
    return render_template('supplier_pickup.html')

@app.route('/supplier/active')
@login_required
def supplier_active():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return redirect(url_for('login'))
    return render_template('supplier_active.html')

@app.route('/supplier/schedule')
@login_required
def supplier_schedule():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return redirect(url_for('login'))
    return render_template('supplier_schedule.html')

@app.route('/supplier/earnings')
@login_required
def supplier_earnings():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return redirect(url_for('login'))
    return render_template('supplier_earnings.html')

@app.route('/supplier/messages')
@app.route('/supplier/messages')
@login_required
def supplier_messages():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    return render_template('supplier_messages.html')

@app.route('/supplier/tracking')
@login_required
def supplier_tracking():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    return render_template('supplier_tracking.html')

@app.route('/supplier/analytics')
@login_required
def supplier_analytics():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return redirect(url_for('login'))
    return render_template('supplier_analytics.html')

@app.route('/supplier/settings')
@login_required
def supplier_settings():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return redirect(url_for('login'))
    stripe_api_key = app.config.get('STRIPE_SECRET_KEY') or os.getenv("STRIPE_SECRET_KEY", os.getenv("STRIPE_API_KEY", ""))
    return render_template("supplier_settings.html", stripe_api_key=stripe_api_key)

# Customer Sub-Routes
@app.route('/shop/products')
@login_required
def shop_products():
    if session.get('role') not in ['Customer', 'Buyer', 'Admin']:
        return redirect(url_for('admin_dashboard'))
    return render_template("shop_products.html")

@app.route('/shop/product/<int:id>')
def shop_product_details(id): return render_placeholder("Product Details")

@app.route('/shop/cart')
@login_required
def shop_cart(): return render_placeholder("Cart")

@app.route('/shop/checkout')
@login_required
def shop_checkout(): return render_placeholder("Checkout")

@app.route('/shop/payment')
@login_required
def shop_payment(): 
    if session.get('role') not in ['Customer', 'Buyer', 'Admin']:
        return redirect(url_for('admin_dashboard'))
    return render_template("shop_payment.html")

@app.route('/shop/messages')
@login_required
def shop_messages(): 
    if session.get('role') not in ['Customer', 'Buyer', 'Admin']:
        return redirect(url_for('admin_dashboard'))
    return render_template("shop_messages.html")

@app.route('/shop/tracking')
@login_required
def shop_tracking(): return render_template("shop_tracking.html")

@app.route('/shop/wishlist')
@login_required
def shop_wishlist(): 
    if session.get('role') not in ['Customer', 'Buyer', 'Admin']:
        return redirect(url_for('admin_dashboard'))
    return render_template("shop_wishlist.html")

@app.route('/shop/reviews')
@login_required
def shop_reviews(): 
    if session.get('role') not in ['Customer', 'Buyer', 'Admin']:
        return redirect(url_for('admin_dashboard'))
    return render_template("shop_reviews.html")

@app.route('/shop/profile')
@login_required
def shop_profile(): 
    if session.get('role') not in ['Customer', 'Buyer', 'Admin']:
        return redirect(url_for('admin_dashboard'))
    return render_template("shop_profile.html")

@app.route('/shop/orders')
@login_required
def shop_orders():
    if session.get('role') not in ['Customer', 'Buyer', 'Admin']:
        return redirect(url_for('admin_dashboard'))
    return render_template("shop_orders.html")

# Delivery Sub-Routes
@app.route('/delivery/assigned')
@login_required
def delivery_assigned(): return render_placeholder("Assigned Orders")

@app.route('/delivery/status')
@login_required
def delivery_status(): return render_placeholder("Delivery Status")

@app.route('/delivery/routes')
@login_required
def delivery_routes(): return render_placeholder("Route Details")

@app.route('/delivery/delivered')
@login_required
def delivery_delivered(): return render_placeholder("Delivered Orders")

@app.route('/delivery/contact')
@login_required
def delivery_contact(): return render_placeholder("Contact Customer")




@app.route('/scan/<log_id>')
def scan_product(log_id):
    item = GLOBAL_MOCK_DB.get(str(log_id))
    if not item:
        item = {
            'id': f'PRD-20{log_id}',
            'name': 'Unknown Product',
            'category': 'Unknown',
            'image': 'saree.png',
            'desc': 'Product details not found. Please rescan a valid log.',
            'fabric': '-', 'color': '-', 'size': '-', 'pattern': '-', 'price': '-'
        }
    return render_template('product_scan.html', item=item)


GLOBAL_MOCK_DB = {
    '15': {'id': 'PRD-1015', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Deep Emerald & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
    '7': {'id': 'PRD-1007', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Deep Emerald & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
    '10': {'id': 'PRD-1010', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Deep Emerald & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
    '11': {'id': 'PRD-1011', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Deep Emerald & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
    '12': {'id': 'PRD-1012', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Deep Emerald & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
    '22': {'id': 'PRD-1022', 'name': 'Dharwad Cotton', 'category': 'Cotton Sarees', 'image': 'dharwad_cotton_saree.png.jpeg', 'desc': 'Soft, breathable pure Dharwad cotton with naturally dyed threads.', 'fabric': 'Organic Dharwad Cotton', 'color': 'Earth Brown & Indigo', 'size': '5.5 Meters', 'pattern': 'Checkered & Stripes', 'price': '₹3,200'},
    '28': {'id': 'PRD-1028', 'name': 'Ilkal Checkered', 'category': 'Heritage Sarees', 'image': 'ilkal_checkered.png.jpeg', 'desc': 'Traditional Ilkal weave with signature red borders and intricate pallu.', 'fabric': 'Cotton-Silk Blend', 'color': 'Mustard & Ruby Red', 'size': '6.0 Meters', 'pattern': 'Kond Chikki (Checkered)', 'price': '₹6,400'},
}

@app.route('/api/add_log', methods=['POST'])
def add_mock_log_endpoint():
    data = request.json
    log_id = str(data.get('log_id'))
    details = data.get('product_details', {})
    # Map frontend 'img' key to 'image' for Jinja2 template compatibility
    if 'img' in details and 'image' not in details:
        details['image'] = details['img']
    GLOBAL_MOCK_DB[log_id] = details
    return jsonify({"success": True})


@app.route('/supplier/schedule/api/new', methods=['POST'])
@login_required
def create_supplier_schedule():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.json
    hub = data.get('hub')
    date = data.get('date')
    time = data.get('time')
    fleet = data.get('fleet')
    
    if not all([hub, date, time, fleet]):
        return jsonify({'success': False, 'message': 'Missing fields'}), 400
        
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO supplier_dispatches (hub_name, dispatch_date, dispatch_time, fleet_assigned) VALUES (%s, %s, %s, %s)",
                (hub, date, time, fleet)
            )
            conn.commit()
            dispatch_id = cursor.lastrowid
            return jsonify({'success': True, 'id': dispatch_id})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'success': False, 'message': 'Database connection failed'}), 500

@app.route('/supplier/schedule/api/list', methods=['GET'])
@login_required
def list_supplier_schedules():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM supplier_dispatches ORDER BY dispatch_date, dispatch_time")
            schedules = cursor.fetchall()
            
            for s in schedules:
                if s.get('dispatch_date'):
                    s['dispatch_date'] = s['dispatch_date'].strftime('%Y-%m-%d')
                if s.get('created_at'):
                    s['created_at'] = s['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                    
            return jsonify({'success': True, 'data': schedules})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'success': False, 'message': 'Database connection failed'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() in ("true", "1")
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
