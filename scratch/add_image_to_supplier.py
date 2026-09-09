import os
import re

# 1. Update edit_supplier.html
with open('d:\\dbmss\\templates\\edit_supplier.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Cancel link
html = html.replace('href="{{ url_for(\'artisans\') }}"', 'href="{{ url_for(\'supplier_module\') }}"')

# Add Image Input
img_html = """
            <div class="mt-4 mr-auto">
                <label for="image" class="block text-xs font-semibold text-brand-lightgold/70 uppercase tracking-widest mb-2">Upload Image</label>
                <input type="file" name="image" id="image" accept="image/*" class="mt-2 block w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-yellow-600 file:text-white hover:file:bg-yellow-700">
            </div>
"""

# Inject before the submit button
html = html.replace('<button type="submit"', img_html + '<button type="submit"')

with open('d:\\dbmss\\templates\\edit_supplier.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Update app.py's edit_supplier route
with open('d:\\dbmss\\app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

# Extract the existing edit_supplier block
# It starts at def edit_supplier(id): and ends right before def edit_artisan(id): or something else
start_idx = app_py.find("def edit_supplier(id):")
end_idx = app_py.find("@app.route", start_idx)

original_func = app_py[start_idx:end_idx]

new_func = """def edit_supplier(id):
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
                cursor.execute(\"\"\"
                    UPDATE suppliers 
                    SET supplier_name=%s, material_supplied=%s, cost=%s, delivery_dates=%s, image_file=%s
                    WHERE supplier_id=%s
                \"\"\", (supplier_name, material_supplied, cost, delivery_dates, image_file, id))
            else:
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

app_py = app_py.replace(original_func, new_func)

with open('d:\\dbmss\\app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)

print("Supplier edit image fully implemented.")
