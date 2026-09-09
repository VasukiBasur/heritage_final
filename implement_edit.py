import os
import re

app_file = r"d:\dbmss\app.py"
template_dir = r"d:\dbmss\templates"

# --- 1. Update app.py api_crud to handle 'edit' ---
with open(app_file, 'r', encoding='utf-8') as f:
    app_content = f.read()

# I will replace the entire api_crud function to support both 'add' and 'edit'
# This requires a massive rewrite of the function. Let's just append the edit logic.
# Wait, replacing the whole function is safer.

new_api_crud = """@app.route('/api/crud/<module>/<action>', methods=['POST'])
@login_required
def api_crud(module, action):
    if session.get('role') != 'Admin':
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        data = request.form
        record_id = data.get('id') # Used for edit
        
        # --- ADD LOGIC ---
        if action == 'add':
            if module == 'weaver':
                cursor.execute('''INSERT INTO artisans (name, skill_level, contact_number, village, experience_years, wage_details) 
                                  VALUES (%s, %s, %s, %s, %s, %s)''', 
                               (data.get('name'), data.get('skill_level'), data.get('contact'), data.get('village'), data.get('experience'), data.get('wage')))
            elif module == 'raw_material':
                cursor.execute('''INSERT INTO raw_materials (material_name, quantity_available) VALUES (%s, %s)''', (data.get('name'), data.get('quantity')))
            elif module == 'supplier':
                cursor.execute('''INSERT INTO suppliers (supplier_name, material_supplied, cost, delivery_dates) VALUES (%s, %s, %s, %s)''', (data.get('name'), data.get('material'), data.get('cost'), data.get('delivery_date')))
            elif module == 'product_catalog':
                cursor.execute('''INSERT INTO product_catalog (product_name, category, price, stock_quantity, artisan_id, material_id) VALUES (%s, %s, %s, %s, %s, %s)''', (data.get('name'), data.get('category'), data.get('price'), data.get('stock'), data.get('artisan_id') or None, data.get('material_id') or None))
            elif module == 'customer':
                cursor.execute('''INSERT INTO customers (name, email, phone, buyer_type, location, feedback) VALUES (%s, %s, %s, %s, %s, %s)''', (data.get('name'), data.get('email'), data.get('phone'), data.get('buyer_type'), data.get('location'), data.get('feedback')))
            elif module == 'order':
                cursor.execute('''INSERT INTO orders (customer_id, product_id, quantity, total_price, status, delivery_date) VALUES (%s, %s, %s, %s, %s, %s)''', (data.get('customer_id'), data.get('product_id'), data.get('quantity'), data.get('total_price'), data.get('status'), data.get('delivery_date')))
            elif module == 'inventory':
                cursor.execute('''INSERT INTO warehouse_inventory (product_id, warehouse_location, stock_in, stock_out, damaged_stock) VALUES (%s, %s, %s, %s, %s)''', (data.get('product_id'), data.get('location'), data.get('stock_in'), data.get('stock_out'), data.get('damaged')))
            elif module == 'billing':
                cursor.execute('''INSERT INTO billing_payments (entity_type, entity_id, amount, payment_type, status) VALUES (%s, %s, %s, %s, %s)''', (data.get('entity_type'), data.get('entity_id'), data.get('amount'), data.get('payment_type'), data.get('status')))
            elif module == 'logistics':
                cursor.execute('''INSERT INTO logistics (order_id, transport_agency, tracking_number, status, estimated_delivery) VALUES (%s, %s, %s, %s, %s)''', (data.get('order_id'), data.get('agency'), data.get('tracking'), data.get('status'), data.get('delivery_date')))
        
        # --- EDIT LOGIC ---
        elif action == 'edit' and record_id:
            if module == 'weaver':
                cursor.execute('''UPDATE artisans SET name=%s, skill_level=%s, contact_number=%s, village=%s, experience_years=%s, wage_details=%s WHERE artisan_id=%s''', (data.get('name'), data.get('skill_level'), data.get('contact'), data.get('village'), data.get('experience'), data.get('wage'), record_id))
            elif module == 'raw_material':
                cursor.execute('''UPDATE raw_materials SET material_name=%s, quantity_available=%s WHERE material_id=%s''', (data.get('name'), data.get('quantity'), record_id))
            elif module == 'supplier':
                cursor.execute('''UPDATE suppliers SET supplier_name=%s, material_supplied=%s, cost=%s, delivery_dates=%s WHERE supplier_id=%s''', (data.get('name'), data.get('material'), data.get('cost'), data.get('delivery_date'), record_id))
            elif module == 'product_catalog':
                cursor.execute('''UPDATE product_catalog SET product_name=%s, category=%s, price=%s, stock_quantity=%s, artisan_id=%s, material_id=%s WHERE product_id=%s''', (data.get('name'), data.get('category'), data.get('price'), data.get('stock'), data.get('artisan_id') or None, data.get('material_id') or None, record_id))
            elif module == 'customer':
                cursor.execute('''UPDATE customers SET name=%s, email=%s, phone=%s, buyer_type=%s, location=%s, feedback=%s WHERE customer_id=%s''', (data.get('name'), data.get('email'), data.get('phone'), data.get('buyer_type'), data.get('location'), data.get('feedback'), record_id))
            elif module == 'order':
                cursor.execute('''UPDATE orders SET customer_id=%s, product_id=%s, quantity=%s, total_price=%s, status=%s, delivery_date=%s WHERE order_id=%s''', (data.get('customer_id'), data.get('product_id'), data.get('quantity'), data.get('total_price'), data.get('status'), data.get('delivery_date'), record_id))
            elif module == 'inventory':
                cursor.execute('''UPDATE warehouse_inventory SET product_id=%s, warehouse_location=%s, stock_in=%s, stock_out=%s, damaged_stock=%s WHERE inventory_id=%s''', (data.get('product_id'), data.get('location'), data.get('stock_in'), data.get('stock_out'), data.get('damaged'), record_id))
            elif module == 'billing':
                cursor.execute('''UPDATE billing_payments SET entity_type=%s, entity_id=%s, amount=%s, payment_type=%s, status=%s WHERE payment_id=%s''', (data.get('entity_type'), data.get('entity_id'), data.get('amount'), data.get('payment_type'), data.get('status'), record_id))
            elif module == 'logistics':
                cursor.execute('''UPDATE logistics SET order_id=%s, transport_agency=%s, tracking_number=%s, status=%s, estimated_delivery=%s WHERE tracking_id=%s''', (data.get('order_id'), data.get('agency'), data.get('tracking'), data.get('status'), data.get('delivery_date'), record_id))
            
        conn.commit()
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
        conn.close()"""

pattern = r"@app\.route\('/api/crud/<module>/<action>', methods=\['POST'\]\).*?conn\.close\(\)"
app_content = re.sub(pattern, new_api_crud, app_content, flags=re.DOTALL)

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(app_content)
print("app.py CRUD API updated for Edit functionality.")


# --- 2. Update generate_all_modules.py to add Edit button and JS ---
generate_file = r"d:\dbmss\generate_all_modules.py"
with open(generate_file, 'r', encoding='utf-8') as f:
    gen_content = f.read()

# Add hidden ID input to forms
gen_content = gen_content.replace("""<form action="{form_action}" method="POST">""", """<form action="{form_action}" method="POST" id="crud-form">
                    <input type="hidden" name="id" id="crud-id">""")

# Modify the add button to clear the form
gen_content = gen_content.replace("""onclick="document.getElementById('crud-modal').classList.remove('hidden')\"""", """onclick="openModal('add', null)\"""")

# Add the Edit JS script before </body>
edit_js = """
    <script>
        function openModal(mode, data) {
            const form = document.getElementById('crud-form');
            const modal = document.getElementById('crud-modal');
            const title = modal.querySelector('h3');
            
            // Set action URL correctly
            let baseAction = "{form_action}".replace('/add', '');
            form.action = baseAction + '/' + mode;
            
            if (mode === 'add') {
                title.innerText = "Add New Record";
                form.reset();
                document.getElementById('crud-id').value = '';
            } else {
                title.innerText = "Edit Record";
                document.getElementById('crud-id').value = data.id;
                // Dynamically populate fields
                for (const key in data) {
                    const input = form.elements[key];
                    if (input) {
                        input.value = data[key];
                    }
                }
            }
            modal.classList.remove('hidden');
        }
    </script>
</body>"""

gen_content = gen_content.replace("</body>", edit_js)
with open(generate_file, 'w', encoding='utf-8') as f:
    f.write(gen_content)
print("generate_all_modules.py updated with Edit JS.")
