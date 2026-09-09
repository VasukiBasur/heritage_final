import re

# 1. Update materials.html (Fix image height & Add file input to Modal)
with open('d:\\dbmss\\templates\\materials.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix image height
old_img = """                <div class="h-48 w-full">
                    <img src="{{ url_for('static', filename='uploads/' ~ material.image_file) }}" alt="Material" class="w-full h-56 object-cover object-center rounded-t-lg opacity-80 hover:opacity-100 transition-opacity">
                </div>"""

new_img = """                <div class="h-56 w-full overflow-hidden">
                    <img src="{{ url_for('static', filename='uploads/' ~ material.image_file) }}" alt="Material" class="w-full h-full object-cover object-center rounded-t-lg opacity-80 hover:opacity-100 transition-opacity">
                </div>"""

html = html.replace(old_img, new_img)

# Update Modal Form
old_form_start = """            <form action="/api/crud/raw_material/add" method="POST" class="space-y-4">"""
new_form_start = """            <form action="/api/crud/raw_material/add" method="POST" enctype="multipart/form-data" class="space-y-4">"""
html = html.replace(old_form_start, new_form_start)

# Add file input to Modal
old_qty_input = """                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Quantity (kg)</label>
                <input type="number" name="quantity" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>"""

new_qty_input = """                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Quantity (kg)</label>
                <input type="number" name="quantity" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Material Image</label>
                <input type="file" name="image" accept="image/*" class="w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-xs file:font-semibold file:bg-brand-gold file:text-brand-black hover:file:bg-yellow-500"></div>"""

html = html.replace(old_qty_input, new_qty_input)

with open('d:\\dbmss\\templates\\materials.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update raw_material_module.html (Modal ONLY)
with open('d:\\dbmss\\templates\\raw_material_module.html', 'r', encoding='utf-8') as f:
    html2 = f.read()

html2 = html2.replace(old_form_start, new_form_start)
html2 = html2.replace(old_qty_input, new_qty_input)

with open('d:\\dbmss\\templates\\raw_material_module.html', 'w', encoding='utf-8') as f:
    f.write(html2)

# 3. Update app.py api_crud (Handle image upload)
with open('d:\\dbmss\\app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

old_logic = """        elif module == 'raw_material' and action == 'add':
            material_id = data.get('material_id')
            if material_id:
                cursor.execute('''INSERT INTO raw_materials (material_id, material_name, quantity_available) 
                                  VALUES (%s, %s, %s)''',
                               (material_id, data.get('name'), data.get('quantity')))
            else:
                cursor.execute('''INSERT INTO raw_materials (material_name, quantity_available) 
                                  VALUES (%s, %s)''',
                               (data.get('name'), data.get('quantity')))"""

new_logic = """        elif module == 'raw_material' and action == 'add':
            material_id = data.get('material_id')
            
            image_file = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_file = filename
            
            if material_id:
                if image_file:
                    cursor.execute('''INSERT INTO raw_materials (material_id, material_name, quantity_available, image_file) 
                                      VALUES (%s, %s, %s, %s)''',
                                   (material_id, data.get('name'), data.get('quantity'), image_file))
                else:
                    cursor.execute('''INSERT INTO raw_materials (material_id, material_name, quantity_available) 
                                      VALUES (%s, %s, %s)''',
                                   (material_id, data.get('name'), data.get('quantity')))
            else:
                if image_file:
                    cursor.execute('''INSERT INTO raw_materials (material_name, quantity_available, image_file) 
                                      VALUES (%s, %s, %s)''',
                                   (data.get('name'), data.get('quantity'), image_file))
                else:
                    cursor.execute('''INSERT INTO raw_materials (material_name, quantity_available) 
                                      VALUES (%s, %s)''',
                                   (data.get('name'), data.get('quantity')))"""

app_py = app_py.replace(old_logic, new_logic)

with open('d:\\dbmss\\app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)

print("Images un-overlapped. File chooser added to Modal.")
