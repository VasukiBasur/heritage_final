import os
import re

# 1. Read edit_artisan.html to use as template
with open('d:\\dbmss\\templates\\edit_artisan.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Artisan specific strings with Supplier specific strings
html = html.replace('Edit Artisan', 'Edit Supplier')
html = html.replace('edit_artisan', 'edit_supplier')
html = html.replace('artisan.artisan_id', 'supplier.supplier_id')
html = html.replace('artisan.', 'supplier.')

# Form fields to replace
form_html = """
                <div>
                    <label for="supplier_name" class="block text-sm font-medium text-brand-lightgold/70 uppercase tracking-widest mb-2">Supplier Name</label>
                    <input type="text" id="supplier_name" name="supplier_name" value="{{ supplier.supplier_name }}" required class="w-full px-4 py-3 rounded-sm transition-all">
                </div>
                <div>
                    <label for="material_supplied" class="block text-sm font-medium text-brand-lightgold/70 uppercase tracking-widest mb-2">Material Supplied</label>
                    <input type="text" id="material_supplied" name="material_supplied" value="{{ supplier.material_supplied }}" required class="w-full px-4 py-3 rounded-sm transition-all">
                </div>
                <div>
                    <label for="cost" class="block text-sm font-medium text-brand-lightgold/70 uppercase tracking-widest mb-2">Cost (₹)</label>
                    <input type="number" step="0.01" id="cost" name="cost" value="{{ supplier.cost }}" required class="w-full px-4 py-3 rounded-sm transition-all">
                </div>
                <div>
                    <label for="delivery_dates" class="block text-sm font-medium text-brand-lightgold/70 uppercase tracking-widest mb-2">Delivery Dates</label>
                    <input type="text" id="delivery_dates" name="delivery_dates" value="{{ supplier.delivery_dates }}" required class="w-full px-4 py-3 rounded-sm transition-all">
                </div>
"""

# Extract the area between <form ...> and <div class="pt-8...
start_form = html.find('>', html.find('<form method="POST"')) + 1
end_form = html.find('<div class="pt-8 flex items-center justify-end')
html = html[:start_form] + form_html + html[end_form:]

# Remove image upload part
start_img = html.find('<div class="mt-4">')
end_img = html.find('<button type="submit"', start_img)
html = html[:start_img] + html[end_img:]

# Write edit_supplier.html
with open('d:\\dbmss\\templates\\edit_supplier.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Add route in app.py
route_code = """
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
        
        try:
            cursor.execute(\"\"\"
                UPDATE suppliers 
                SET supplier_name=%s, material_supplied=%s, cost=%s, delivery_dates=%s
                WHERE supplier_id=%s
            \"\"\", (supplier_name, material_supplied, cost, delivery_dates, id))
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
"""

with open('d:\\dbmss\\app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

if "def edit_supplier(" not in app_py:
    app_py = app_py.replace("def edit_artisan(id):", route_code + "\n\n@app.route('/edit_artisan/<int:id>', methods=['GET', 'POST'])\n@login_required\ndef edit_artisan(id):")
    with open('d:\\dbmss\\app.py', 'w', encoding='utf-8') as f:
        f.write(app_py)


# 3. Update supplier_module.html link
with open('d:\\dbmss\\templates\\supplier_module.html', 'r', encoding='utf-8') as f:
    supplier_module = f.read()

supplier_module = supplier_module.replace(
    "<a href='#' onclick='alert(\"Edit supplier page pending\")'",
    "<a href=\"{{ url_for('edit_supplier', id=s.supplier_id) }}\""
)

with open('d:\\dbmss\\templates\\supplier_module.html', 'w', encoding='utf-8') as f:
    f.write(supplier_module)

print("Edit supplier fully implemented.")
