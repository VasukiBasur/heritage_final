import os
import re

# 1. Read edit_artisan.html to use as template
with open('d:\\dbmss\\templates\\edit_artisan.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Artisan specific strings with Material specific strings
html = html.replace('Edit Artisan', 'Edit Raw Material')
html = html.replace('edit_artisan', 'edit_raw_material')
html = html.replace('artisan.artisan_id', 'material.material_id')
html = html.replace('artisan.', 'material.')
html = html.replace("url_for('artisans')", "url_for('raw_material_module')")

# Form fields to replace
form_html = """
                <div>
                    <label for="material_name" class="block text-sm font-medium text-brand-lightgold/70 uppercase tracking-widest mb-2">Material Name</label>
                    <input type="text" id="material_name" name="material_name" value="{{ material.material_name }}" required class="w-full px-4 py-3 rounded-sm transition-all">
                </div>
                <div>
                    <label for="quantity_available" class="block text-sm font-medium text-brand-lightgold/70 uppercase tracking-widest mb-2">Quantity Available (kg)</label>
                    <input type="number" id="quantity_available" name="quantity_available" value="{{ material.quantity_available }}" required class="w-full px-4 py-3 rounded-sm transition-all">
                </div>
"""

# Extract the area between <form ...> and <div class="pt-8...
start_form = html.find('>', html.find('<form method="POST"')) + 1
end_form = html.find('<div class="pt-8 flex items-center justify-end')
html = html[:start_form] + form_html + html[end_form:]

# Write edit_raw_material.html (it retains the image upload from edit_artisan template!)
with open('d:\\dbmss\\templates\\edit_raw_material.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Add route in app.py
route_code = """
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
        
        try:
            if image_file:
                cursor.execute(\"\"\"
                    UPDATE raw_materials 
                    SET material_name=%s, quantity_available=%s, image_file=%s
                    WHERE material_id=%s
                \"\"\", (material_name, quantity, image_file, id))
            else:
                cursor.execute(\"\"\"
                    UPDATE raw_materials 
                    SET material_name=%s, quantity_available=%s
                    WHERE material_id=%s
                \"\"\", (material_name, quantity, id))
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
"""

with open('d:\\dbmss\\app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

if "def edit_raw_material(" not in app_py:
    app_py = app_py.replace("def edit_supplier(id):", route_code + "\n\n@app.route('/edit_supplier/<int:id>', methods=['GET', 'POST'])\n@login_required\ndef edit_supplier(id):")
    with open('d:\\dbmss\\app.py', 'w', encoding='utf-8') as f:
        f.write(app_py)


# 3. Update raw_material_module.html link
with open('d:\\dbmss\\templates\\raw_material_module.html', 'r', encoding='utf-8') as f:
    module = f.read()

module = module.replace(
    "<a href='#' onclick='alert(\"Edit material page pending\")'",
    "<a href=\"{{ url_for('edit_raw_material', id=m.material_id) }}\""
)

with open('d:\\dbmss\\templates\\raw_material_module.html', 'w', encoding='utf-8') as f:
    f.write(module)

print("Edit raw material fully implemented with image upload.")
