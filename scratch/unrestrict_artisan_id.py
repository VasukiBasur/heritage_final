import re
import mysql.connector

# 1. First, make foreign keys cascade so we don't get errors!
try:
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='heritage_handloom')
    cursor = conn.cursor()
    # Update foreign keys for production_logs
    cursor.execute("ALTER TABLE production_logs DROP FOREIGN KEY production_logs_ibfk_1;")
    cursor.execute("ALTER TABLE production_logs ADD CONSTRAINT production_logs_ibfk_1 FOREIGN KEY (artisan_id) REFERENCES artisans(artisan_id) ON UPDATE CASCADE ON DELETE SET NULL;")
    # Update product_catalog
    cursor.execute("ALTER TABLE product_catalog DROP FOREIGN KEY product_catalog_ibfk_1;")
    cursor.execute("ALTER TABLE product_catalog ADD CONSTRAINT product_catalog_ibfk_1 FOREIGN KEY (artisan_id) REFERENCES artisans(artisan_id) ON UPDATE CASCADE ON DELETE SET NULL;")
    # Update payouts
    cursor.execute("ALTER TABLE payouts DROP FOREIGN KEY payouts_ibfk_1;")
    cursor.execute("ALTER TABLE payouts ADD CONSTRAINT payouts_ibfk_1 FOREIGN KEY (artisan_id) REFERENCES artisans(artisan_id) ON UPDATE CASCADE ON DELETE CASCADE;")
    conn.commit()
    cursor.close()
    conn.close()
    print("Foreign keys updated to CASCADE.")
except Exception as e:
    print("FK update failed or not needed:", e)

# 2. Update edit_artisan.html
with open('d:\\dbmss\\templates\\edit_artisan.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_id_block = """                <div>
                    <label class="block text-sm font-medium text-brand-lightgold/50 uppercase tracking-widest mb-2">Artisan ID (Read-Only)</label>
                    <input type="text" value="#ART-{{ artisan.artisan_id }}" readonly class="w-full px-4 py-3 rounded-sm transition-all bg-brand-dark/50 border-brand-gold/20 text-brand-lightgold/50 cursor-not-allowed">
                </div>"""

new_id_block = """                <div>
                    <label for="new_artisan_id" class="block text-sm font-medium text-brand-lightgold/70 uppercase tracking-widest mb-2">Artisan ID</label>
                    <input type="number" id="new_artisan_id" name="new_artisan_id" value="{{ artisan.artisan_id }}" required class="w-full px-4 py-3 rounded-sm transition-all">
                </div>"""

if old_id_block in html:
    html = html.replace(old_id_block, new_id_block)
else:
    # If indentation is different
    html = re.sub(r'<label class="block.*?Artisan ID \(Read-Only\).*?</div>', new_id_block, html, flags=re.DOTALL)

with open('d:\\dbmss\\templates\\edit_artisan.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 3. Update app.py
with open('d:\\dbmss\\app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

# Replace the artisan update logic
old_app_logic = """
        try:
            if image_file:
                cursor.execute(\"\"\"
                    UPDATE artisans 
                    SET name=%s, location=%s, contact_number=%s, skill_level=%s, image_file=%s, village=%s, experience_years=%s, wage_details=%s 
                    WHERE artisan_id=%s
                \"\"\", (name, location, contact, skill, image_file, village, experience_years, wage_details, id))
            else:
                cursor.execute(\"\"\"
                    UPDATE artisans 
                    SET name=%s, location=%s, contact_number=%s, skill_level=%s, village=%s, experience_years=%s, wage_details=%s 
                    WHERE artisan_id=%s
                \"\"\", (name, location, contact, skill, village, experience_years, wage_details, id))
            conn.commit()"""

new_app_logic = """
        new_artisan_id = request.form.get('new_artisan_id', id)
        try:
            if image_file:
                cursor.execute(\"\"\"
                    UPDATE artisans 
                    SET artisan_id=%s, name=%s, location=%s, contact_number=%s, skill_level=%s, image_file=%s, village=%s, experience_years=%s, wage_details=%s 
                    WHERE artisan_id=%s
                \"\"\", (new_artisan_id, name, location, contact, skill, image_file, village, experience_years, wage_details, id))
            else:
                cursor.execute(\"\"\"
                    UPDATE artisans 
                    SET artisan_id=%s, name=%s, location=%s, contact_number=%s, skill_level=%s, village=%s, experience_years=%s, wage_details=%s 
                    WHERE artisan_id=%s
                \"\"\", (new_artisan_id, name, location, contact, skill, village, experience_years, wage_details, id))
            conn.commit()"""

app_py = app_py.replace(old_app_logic, new_app_logic)

with open('d:\\dbmss\\app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)

print("Artisan ID unrestricted.")
