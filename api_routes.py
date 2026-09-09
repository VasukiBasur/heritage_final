from flask import Blueprint, request, jsonify, session
import mysql.connector
import os
from datetime import datetime

api_bp = Blueprint('api_bp', __name__)

from db_config import get_db_connection

# ==========================================
# PRODUCTS
# ==========================================
@api_bp.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    if not conn: return jsonify({"error": "DB connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, a.name as artisan_name 
        FROM product_catalog p
        LEFT JOIN artisans a ON p.artisan_id = a.artisan_id
    """)
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "data": products})

@api_bp.route('/products', methods=['POST'])
def add_product():
    data = request.json or request.form
    conn = get_db_connection()
    if not conn: return jsonify({"error": "DB connection failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO product_catalog (product_name, category, price, stock_quantity, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (data.get('product_name'), data.get('category'), data.get('price'), data.get('stock_quantity', 0), data.get('status', 'In Stock')))
        conn.commit()
        product_id = cursor.lastrowid
        return jsonify({"success": True, "message": "Product added", "id": product_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@api_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json or request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE product_catalog 
            SET product_name=%s, category=%s, price=%s, stock_quantity=%s, status=%s
            WHERE product_id=%s
        """, (data.get('product_name'), data.get('category'), data.get('price'), data.get('stock_quantity'), data.get('status'), id))
        conn.commit()
        return jsonify({"success": True, "message": "Product updated"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@api_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM product_catalog WHERE product_id=%s", (id,))
        conn.commit()
        return jsonify({"success": True, "message": "Product deleted"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# ==========================================
# ORDERS
# ==========================================
@api_bp.route('/orders', methods=['GET'])
def get_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders ORDER BY order_date DESC")
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "data": orders})

@api_bp.route('/orders', methods=['POST'])
def add_order():
    data = request.json or request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO orders (customer_name, total_amount, status, shipping_address)
            VALUES (%s, %s, %s, %s)
        """, (data.get('customer_name'), data.get('total_amount'), data.get('status', 'Pending'), data.get('shipping_address')))
        conn.commit()
        return jsonify({"success": True, "message": "Order placed", "id": cursor.lastrowid})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@api_bp.route('/orders/<int:id>/status', methods=['PUT'])
def update_order_status(id):
    data = request.json or request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE orders SET status=%s WHERE order_id=%s", (data.get('status'), id))
        conn.commit()
        return jsonify({"success": True, "message": "Order status updated"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# ==========================================
# SUPPLIERS & INVENTORY
# ==========================================
@api_bp.route('/suppliers', methods=['GET'])
def get_suppliers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM suppliers")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "data": data})

@api_bp.route('/suppliers', methods=['POST'])
def add_supplier():
    data = request.json or request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO suppliers (company_name, contact_person, phone, material_type, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (data.get('company_name'), data.get('contact_person'), data.get('phone'), data.get('material_type'), data.get('status', 'Active')))
        conn.commit()
        return jsonify({"success": True, "message": "Supplier added"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@api_bp.route('/inventory', methods=['GET'])
def get_inventory():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM raw_materials")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "data": data})

@api_bp.route('/inventory/<int:id>/update', methods=['PUT'])
def update_inventory(id):
    data = request.json or request.form
    qty = int(data.get('quantity_change', 0))
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE raw_materials SET quantity_available = quantity_available + %s WHERE material_id=%s", (qty, id))
        conn.commit()
        return jsonify({"success": True, "message": "Inventory updated"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# ==========================================
# PAYMENTS & SHIPMENTS
# ==========================================
@api_bp.route('/payments', methods=['GET'])
def get_payments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM billing_payments")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "data": data})

@api_bp.route('/shipments', methods=['GET'])
def get_shipments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT l.*, o.customer_name, o.shipping_address 
        FROM logistics l
        JOIN orders o ON l.order_id = o.order_id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "data": data})

@api_bp.route('/shipments/<int:id>/status', methods=['PUT'])
def update_shipment_status(id):
    data = request.json or request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE logistics SET current_status=%s WHERE shipment_id=%s", (data.get('status'), id))
        conn.commit()
        return jsonify({"success": True, "message": "Shipment updated"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# ==========================================
# DASHBOARD STATS
# ==========================================
@api_bp.route('/dashboard/stats', methods=['GET'])
def dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT SUM(total_amount) as revenue FROM orders WHERE status != 'Cancelled'")
        revenue = cursor.fetchone()['revenue'] or 0
        
        cursor.execute("SELECT COUNT(*) as orders_count FROM orders")
        orders = cursor.fetchone()['orders_count']
        
        cursor.execute("SELECT COUNT(*) as artisans_count FROM artisans")
        artisans = cursor.fetchone()['artisans_count']
        
        cursor.execute("SELECT SUM(quantity_available) as inv_count FROM raw_materials")
        inventory = cursor.fetchone()['inv_count'] or 0

        return jsonify({
            "success": True,
            "data": {
                "revenue": float(revenue),
                "orders": orders,
                "artisans": artisans,
                "inventory": float(inventory)
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


# ==========================================
# QR CODE GENERATION
# ==========================================
import qrcode
from io import BytesIO
from flask import send_file

@api_bp.route('/products/<int:id>/qr', methods=['GET'])
def get_product_qr(id):
    conn = get_db_connection()
    if not conn: return jsonify({"error": "DB connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT product_name, artisan_id FROM product_catalog WHERE product_id=%s", (id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
        
    data = f"Heritage Handloom Authenticity\nProduct ID: {id}\nName: {product['product_name']}\nArtisan ID: {product['artisan_id'] or 'N/A'}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="#121212", back_color="#d4af37") # Gold background, black QR
    
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')
