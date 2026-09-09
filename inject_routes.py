import re

app_path = r"d:\dbmss\app.py"
with open(app_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

new_routes = """
# ==========================================
# ADVANCED ENTERPRISE MODULES
# ==========================================

@app.route('/weaver_module')
@login_required
def weaver_module():
    if session.get('role') != 'Admin':
        flash("Unauthorized access.", "error")
        return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT artisan_id, name, village, skill_level, contact_number, experience_years, wage_details FROM artisans")
    weavers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('weaver_module.html', weavers=weavers)

@app.route('/raw_material_module')
@login_required
def raw_material_module():
    if session.get('role') != 'Admin':
        return redirect(url_for('dashboard'))
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
        return redirect(url_for('dashboard'))
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
        return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(\"\"\"
        SELECT p.log_id, p.supply_chain_stage as stage, p.status, p.start_date, a.name as artisan_name, d.name as design_name 
        FROM production_logs p
        JOIN artisans a ON p.artisan_id = a.artisan_id
        JOIN traditional_designs d ON p.design_id = d.design_id
        ORDER BY p.log_id DESC
    \"\"\")
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('production_module.html', logs=logs)

@app.route('/product_catalog_module')
@login_required
def product_catalog_module():
    if session.get('role') != 'Admin':
        return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM product_catalog")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('product_catalog_module.html', products=products)

# ==========================================
"""

# Inject before the @app.route('/add_log', methods=['GET', 'POST'])
if '@app.route(\'/weaver_module\')' not in app_content:
    app_content = app_content.replace(
        "@app.route('/add_log', methods=['GET', 'POST'])",
        new_routes + "\n@app.route('/add_log', methods=['GET', 'POST'])"
    )
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(app_content)
    print("Injected routes into app.py")
else:
    print("Routes already exist in app.py")
