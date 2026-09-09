import re

# 1. Update raw_material_module.html
with open('d:\\dbmss\\templates\\raw_material_module.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_form_field = """                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Material Name</label>"""
new_form_field = """                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Material ID (Optional)</label>
                <input type="number" name="material_id" placeholder="Auto-generated if left blank" class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none mb-2"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Material Name</label>"""

html = html.replace(old_form_field, new_form_field)

with open('d:\\dbmss\\templates\\raw_material_module.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update app.py
with open('d:\\dbmss\\app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

old_logic = """        elif module == 'raw_material' and action == 'add':
            cursor.execute('''INSERT INTO raw_materials (material_name, quantity_available) 
                              VALUES (%s, %s)''',
                           (data.get('name'), data.get('quantity')))"""

new_logic = """        elif module == 'raw_material' and action == 'add':
            material_id = data.get('material_id')
            if material_id:
                cursor.execute('''INSERT INTO raw_materials (material_id, material_name, quantity_available) 
                                  VALUES (%s, %s, %s)''',
                               (material_id, data.get('name'), data.get('quantity')))
            else:
                cursor.execute('''INSERT INTO raw_materials (material_name, quantity_available) 
                                  VALUES (%s, %s)''',
                               (data.get('name'), data.get('quantity')))"""

app_py = app_py.replace(old_logic, new_logic)

with open('d:\\dbmss\\app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)

print("Material ID added to Add New modal.")
