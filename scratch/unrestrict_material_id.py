import re
import mysql.connector

# 1. Update foreign key to ON UPDATE CASCADE
try:
    conn = mysql.connector.connect(user='root', password='root@123', host='localhost', database='heritage_handloom')
    cursor = conn.cursor()
    cursor.execute('ALTER TABLE design_materials DROP FOREIGN KEY fk_dm_material')
    cursor.execute('ALTER TABLE design_materials ADD CONSTRAINT fk_dm_material FOREIGN KEY (material_id) REFERENCES raw_materials(material_id) ON UPDATE CASCADE ON DELETE CASCADE')
    conn.commit()
    cursor.close()
    conn.close()
except Exception as e:
    print("FK alter failed (might already be cascaded):", e)

# 2. Update edit_raw_material.html
with open('d:\\dbmss\\templates\\edit_raw_material.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_id_block = """                <div>
                    <label for="new_material_id" class="block text-sm font-medium text-brand-lightgold/70 uppercase tracking-widest mb-2">Material ID</label>
                    <input type="number" id="new_material_id" name="new_material_id" value="{{ material.material_id }}" required class="w-full px-4 py-3 rounded-sm transition-all bg-[#121212] border border-brand-gold/30 text-brand-lightgold focus:border-brand-gold focus:outline-none">
                </div>
                <div>"""

html = html.replace('                <div>\n                    <label for="material_name"', new_id_block + '\n                    <label for="material_name"')

with open('d:\\dbmss\\templates\\edit_raw_material.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 3. Update app.py
with open('d:\\dbmss\\app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

old_logic = """
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
            conn.commit()"""

new_logic = """
        new_material_id = request.form.get('new_material_id', id)
        try:
            # Manually cascade to product_catalog since it has no FK constraint
            cursor.execute("UPDATE product_catalog SET material_id=%s WHERE material_id=%s", (new_material_id, id))
            
            if image_file:
                cursor.execute(\"\"\"
                    UPDATE raw_materials 
                    SET material_id=%s, material_name=%s, quantity_available=%s, image_file=%s
                    WHERE material_id=%s
                \"\"\", (new_material_id, material_name, quantity, image_file, id))
            else:
                cursor.execute(\"\"\"
                    UPDATE raw_materials 
                    SET material_id=%s, material_name=%s, quantity_available=%s
                    WHERE material_id=%s
                \"\"\", (new_material_id, material_name, quantity, id))
            conn.commit()"""

app_py = app_py.replace(old_logic, new_logic)

with open('d:\\dbmss\\app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)

print("Material ID made editable.")
