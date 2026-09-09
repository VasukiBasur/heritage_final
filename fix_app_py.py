import os
import re

app_file = r"d:\dbmss\app.py"

with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix order_module
content = content.replace("c.name as customer_name, p.name as product_name", "c.name as customer_name, p.product_name as product_name")
# Fix inventory_module
content = content.replace("i.*, p.name as product_name", "i.*, p.product_name as product_name")

# Rewrite the entire api_crud function
new_api_crud = """@app.route('/api/crud/<module>/<action>', methods=['POST'])
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
            cursor.execute('''INSERT INTO raw_materials (material_name, quantity_available) 
                              VALUES (%s, %s)''',
                           (data.get('name'), data.get('quantity')))
                           
        elif module == 'supplier' and action == 'add':
            cursor.execute('''INSERT INTO suppliers (supplier_name, material_supplied, cost, delivery_dates) 
                              VALUES (%s, %s, %s, %s)''',
                           (data.get('name'), data.get('material'), data.get('cost'), data.get('delivery_date')))
                           
        elif module == 'product_catalog' and action == 'add':
            cursor.execute('''INSERT INTO product_catalog (product_name, category, price, stock_quantity) 
                              VALUES (%s, %s, %s, %s)''',
                           (data.get('name'), data.get('category'), data.get('price'), data.get('stock')))
                           
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
                           
        conn.commit()
        return redirect(request.referrer)
    except Exception as e:
        print(f"Error in API CRUD: {str(e)}")
        flash(f"Error saving data: {str(e)}", "error")
        return redirect(request.referrer)
    finally:
        cursor.close()
        conn.close()"""

# Replace old api_crud
# We will use regex to replace from @app.route('/api/crud/<module>/<action>', methods=['POST']) down to the finally block's conn.close()
pattern = r"@app\.route\('/api/crud/<module>/<action>', methods=\['POST'\]\).*?conn\.close\(\)"
content = re.sub(pattern, new_api_crud, content, flags=re.DOTALL)

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("app.py updated")
