from flask import Blueprint, jsonify, request, session, redirect, url_for
import mysql.connector
import os
import uuid
import jwt
from functools import wraps

JWT_SECRET = os.getenv("SECRET_KEY", "super_secret_key_123")
artisan_api = Blueprint('artisan_api', __name__, url_prefix='/api/artisan')

def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('jwt_token')
        if not token:
            return jsonify({'error': 'Unauthorized - Missing Token'}), 401
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            session['user_id'] = payload['user_id']
            session['role'] = payload['role']
            session['username'] = payload['username']
        except Exception as e:
            return jsonify({'error': f'Unauthorized - {str(e)}'}), 401
        return f(*args, **kwargs)
    return decorated_function

from db_config import get_db_connection

# ==========================================
# DASHBOARD ANALYTICS API
# ==========================================
@artisan_api.route('/dashboard/stats', methods=['GET'])
@api_login_required
def get_dashboard_stats():
    if session.get('role') not in ['Artisan', 'Weaver']:
        return jsonify({'error': 'Unauthorized'}), 403
        
    artisan_id = session.get('user_id', 1)
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database error'}), 500
        
    cursor = conn.cursor(dictionary=True)
    try:
        # Fetch actual earnings array (Mocking for now to match chart structure)
        # In a real scenario, this would group payouts by month
        cursor.execute("SELECT SUM(payout_amount) as total FROM production_logs WHERE artisan_id = %s AND status = 'Completed'", (artisan_id,))
        res = cursor.fetchone()
        total = float(res['total'] or 0)
        
        # We will dynamically return chart data here
        data = {
            'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'earnings': [total * 0.1, total * 0.2, total * 0.15, total * 0.3, total * 0.05, total * 0.2],
            'production': {
                'labels': ['Silk Sarees', 'Cotton Dhotis', 'Shawls', 'Fabrics'],
                'active': [2, 1, 0, 1],
                'completed': [4, 5, 2, 0]
            }
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ==========================================
# PRODUCTS API
# ==========================================
@artisan_api.route('/products', methods=['GET'])
@api_login_required
def get_products():
    if session.get('role') not in ['Artisan', 'Weaver']:
        return jsonify({'error': 'Unauthorized'}), 403
        
    artisan_id = session.get('user_id', 1)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM product_catalog WHERE artisan_id = %s ORDER BY product_id DESC", (artisan_id,))
        products = cursor.fetchall()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@artisan_api.route('/products/<int:product_id>', methods=['DELETE'])
@api_login_required
def delete_product(product_id):
    if session.get('role') not in ['Artisan', 'Weaver']:
        return jsonify({'error': 'Unauthorized'}), 403
        
    artisan_id = session.get('user_id', 1)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Ensure the product belongs to this artisan
        cursor.execute("DELETE FROM product_catalog WHERE product_id = %s AND artisan_id = %s", (product_id, artisan_id))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Product not found or unauthorized'}), 404
        conn.commit()
        return jsonify({'success': True, 'message': 'Product deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@artisan_api.route('/products/<int:product_id>', methods=['PUT'])
@api_login_required
def update_product(product_id):
    if session.get('role') not in ['Artisan', 'Weaver']:
        return jsonify({'error': 'Unauthorized'}), 403
        
    artisan_id = session.get('user_id', 1)
    data = request.json
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE product_catalog 
            SET price = %s, stock_quantity = %s 
            WHERE product_id = %s AND artisan_id = %s
        """, (data.get('price'), data.get('stock_quantity'), product_id, artisan_id))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Product not found or unauthorized'}), 404
        conn.commit()
        return jsonify({'success': True, 'message': 'Product updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ==========================================
# ORDERS API
# ==========================================
@artisan_api.route('/orders/<int:order_id>/status', methods=['PUT'])
@api_login_required
def update_order_status(order_id):
    if session.get('role') not in ['Artisan', 'Weaver']:
        return jsonify({'error': 'Unauthorized'}), 403
        
    data = request.json
    new_status = data.get('status')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s", (new_status, order_id))
        conn.commit()
        return jsonify({'success': True, 'message': f'Order status updated to {new_status}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
