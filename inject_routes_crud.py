import os
import re

app_file = r"d:\dbmss\app.py"

with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

routes = """
# ==========================================
# MODULES 6-10 (GET ROUTES)
# ==========================================

@app.route('/customer_module')
@login_required
def customer_module():
    if session.get('role') != 'Admin': return redirect(url_for('dashboard'))
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
    if session.get('role') != 'Admin': return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT o.*, c.name as customer_name, p.name as product_name 
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
    if session.get('role') != 'Admin': return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT i.*, p.name as product_name 
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
    if session.get('role') != 'Admin': return redirect(url_for('dashboard'))
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
    if session.get('role') != 'Admin': return redirect(url_for('dashboard'))
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
            cursor.execute('''INSERT INTO artisans (name, skill_level, contact_number, village, experience_years, wage_details) 
                              VALUES (%s, %s, %s, %s, %s, %s)''', 
                           (data.get('name'), data.get('skill_level'), data.get('contact'), data.get('village'), data.get('experience'), data.get('wage')))
        
        elif module == 'raw_material' and action == 'add':
            cursor.execute('''INSERT INTO raw_materials (material_type, quantity_kg, source, quality_grade) 
                              VALUES (%s, %s, %s, %s)''',
                           (data.get('type'), data.get('quantity'), data.get('source'), data.get('grade')))
                           
        elif module == 'supplier' and action == 'add':
            cursor.execute('''INSERT INTO suppliers (supplier_name, material_supplied, cost_per_unit, next_delivery_date) 
                              VALUES (%s, %s, %s, %s)''',
                           (data.get('name'), data.get('material'), data.get('cost'), data.get('delivery_date')))
                           
        elif module == 'product_catalog' and action == 'add':
            cursor.execute('''INSERT INTO product_catalog (name, category, price, stock_quantity, description) 
                              VALUES (%s, %s, %s, %s, %s)''',
                           (data.get('name'), data.get('category'), data.get('price'), data.get('stock'), data.get('desc')))
                           
        elif module == 'customer' and action == 'add':
            cursor.execute('''INSERT INTO customers (name, email, phone, buyer_type, location, feedback) 
                              VALUES (%s, %s, %s, %s, %s, %s)''',
                           (data.get('name'), data.get('email'), data.get('phone'), data.get('buyer_type'), data.get('location'), data.get('feedback')))
                           
        elif module == 'order' and action == 'add':
            cursor.execute('''INSERT INTO orders (customer_id, product_id, quantity, total_price, status, delivery_date) 
                              VALUES (%s, %s, %s, %s, %s, %s)''',
                           (data.get('customer_id'), data.get('product_id'), data.get('quantity'), data.get('total_price'), data.get('status'), data.get('delivery_date')))
                           
        elif module == 'inventory' and action == 'add':
            cursor.execute('''INSERT INTO warehouse_inventory (product_id, warehouse_location, stock_in, stock_out, damaged_stock) 
                              VALUES (%s, %s, %s, %s, %s)''',
                           (data.get('product_id'), data.get('location'), data.get('stock_in'), data.get('stock_out'), data.get('damaged')))
                           
        elif module == 'billing' and action == 'add':
            cursor.execute('''INSERT INTO billing_payments (entity_type, entity_id, amount, payment_type, status) 
                              VALUES (%s, %s, %s, %s, %s)''',
                           (data.get('entity_type'), data.get('entity_id'), data.get('amount'), data.get('payment_type'), data.get('status')))
                           
        elif module == 'logistics' and action == 'add':
            cursor.execute('''INSERT INTO logistics (order_id, transport_agency, tracking_number, status, estimated_delivery) 
                              VALUES (%s, %s, %s, %s, %s)''',
                           (data.get('order_id'), data.get('agency'), data.get('tracking'), data.get('status'), data.get('delivery_date')))
                           
        # Additional handlers for 'edit' and 'delete' can be added here...
        
        conn.commit()
        # Return redirect back to the page they came from
        return redirect(request.referrer)
    except Exception as e:
        print(f"Error in API CRUD: {str(e)}")
        flash(f"Error saving data: {str(e)}", "error")
        return redirect(request.referrer)
    finally:
        cursor.close()
        conn.close()

"""

if "def customer_module():" not in content:
    content = content.replace("if __name__ == '__main__':", routes + "\nif __name__ == '__main__':")
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Routes injected successfully.")
else:
    print("Routes already exist.")
