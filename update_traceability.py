import os
import re
import mysql.connector
from dotenv import load_dotenv

# --- Database Schema Update for Real Traceability ---
load_dotenv()
try:
    db = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    cursor = db.cursor()
    # Add columns to product_catalog if they don't exist
    cursor.execute("SHOW COLUMNS FROM product_catalog LIKE 'artisan_id'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE product_catalog ADD COLUMN artisan_id INT")
    
    cursor.execute("SHOW COLUMNS FROM product_catalog LIKE 'material_id'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE product_catalog ADD COLUMN material_id INT")
    
    db.commit()
    cursor.close()
    db.close()
    print("Database schema updated for real traceability.")
except Exception as e:
    print(f"DB Error: {e}")

# --- Update app.py for Real Traceability Route ---
app_file = r"d:\dbmss\app.py"
with open(app_file, 'r', encoding='utf-8') as f:
    app_content = f.read()

old_trace = """@app.route('/trace/<int:product_id>')
def trace(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Fetch product details
    cursor.execute("SELECT * FROM product_catalog WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    
    # Fetch random provenance from the view as a demonstration (since product_id isn't directly linked to the view in the schema)
    cursor.execute("SELECT * FROM vw_textile_provenance LIMIT 1")
    provenance = cursor.fetchone()
    if not provenance:
        provenance = {"artisan_name": "Ramesh Weaver", "location": "Harapanahalli", "design_name": "Traditional Motif", "material_type": "Pure Silk"}
    
    cursor.close()
    conn.close()"""

new_trace = """@app.route('/trace/<int:product_id>')
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
        provenance = None"""

if old_trace in app_content:
    app_content = app_content.replace(old_trace, new_trace)
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(app_content)
    print("Trace route updated in app.py")

# --- Update product_catalog_module GET Route to pass artisans and materials for dropdowns ---
with open(app_file, 'r', encoding='utf-8') as f:
    app_content = f.read()

old_catalog_route = """@app.route('/product_catalog_module')
@login_required
def product_catalog_module():
    if session.get('role') != 'Admin': return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM product_catalog")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('product_catalog_module.html', products=data)"""

new_catalog_route = """@app.route('/product_catalog_module')
@login_required
def product_catalog_module():
    if session.get('role') != 'Admin': return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM product_catalog")
    data = cursor.fetchall()
    
    cursor.execute("SELECT artisan_id, name as artisan_name FROM artisans")
    artisans = cursor.fetchall()
    
    cursor.execute("SELECT material_id, material_name FROM raw_materials")
    materials = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('product_catalog_module.html', products=data, artisans=artisans, materials=materials)"""

if old_catalog_route in app_content:
    app_content = app_content.replace(old_catalog_route, new_catalog_route)
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(app_content)
    print("Product Catalog route updated in app.py")


# --- Update app.py CRUD for Product Catalog to include the foreign keys ---
with open(app_file, 'r', encoding='utf-8') as f:
    app_content = f.read()

old_catalog_add = """        elif module == 'product_catalog' and action == 'add':
            cursor.execute('''INSERT INTO product_catalog (product_name, category, price, stock_quantity) 
                              VALUES (%s, %s, %s, %s)''',
                           (data.get('name'), data.get('category'), data.get('price'), data.get('stock')))"""

new_catalog_add = """        elif module == 'product_catalog' and action == 'add':
            cursor.execute('''INSERT INTO product_catalog (product_name, category, price, stock_quantity, artisan_id, material_id) 
                              VALUES (%s, %s, %s, %s, %s, %s)''',
                           (data.get('name'), data.get('category'), data.get('price'), data.get('stock'), data.get('artisan_id') or None, data.get('material_id') or None))"""

if old_catalog_add in app_content:
    app_content = app_content.replace(old_catalog_add, new_catalog_add)
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(app_content)
    print("Product Catalog ADD logic updated in app.py")

print("Backend schema and routes updated.")
