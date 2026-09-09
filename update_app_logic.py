import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
content = content.replace('from werkzeug.security import check_password_hash', 
                          'from werkzeug.security import check_password_hash\nfrom werkzeug.utils import secure_filename')

# Add UPLOAD_FOLDER
upload_config = """app.secret_key = os.getenv("SECRET_KEY", "super_secret_key_123")
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
"""
content = content.replace('app.secret_key = os.getenv("SECRET_KEY", "super_secret_key_123")', upload_config)

# Update edit_artisan POST logic
edit_artisan_target = """        name = request.form['name']
        location = request.form['location']
        contact = request.form['contact_number']
        skill = request.form['skill_level']
        
        try:
            cursor.execute(\"\"\"
                UPDATE artisans 
                SET name=%s, location=%s, contact_number=%s, skill_level=%s 
                WHERE artisan_id=%s
            \"\"\", (name, location, contact, skill, id))"""

edit_artisan_replace = """        name = request.form['name']
        location = request.form['location']
        contact = request.form['contact_number']
        skill = request.form['skill_level']
        
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
                    UPDATE artisans 
                    SET name=%s, location=%s, contact_number=%s, skill_level=%s, image_file=%s 
                    WHERE artisan_id=%s
                \"\"\", (name, location, contact, skill, image_file, id))
            else:
                cursor.execute(\"\"\"
                    UPDATE artisans 
                    SET name=%s, location=%s, contact_number=%s, skill_level=%s 
                    WHERE artisan_id=%s
                \"\"\", (name, location, contact, skill, id))"""

content = content.replace(edit_artisan_target, edit_artisan_replace)


# Update edit_design POST logic
edit_design_target = """        name = request.form['name']
        description = request.form['description']
        region = request.form['region_origin']
        
        try:
            cursor.execute(\"\"\"
                UPDATE traditional_designs 
                SET name=%s, description=%s, region_origin=%s 
                WHERE design_id=%s
            \"\"\", (name, description, region, id))"""

edit_design_replace = """        name = request.form['name']
        description = request.form['description']
        region = request.form['region_origin']
        
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
                    UPDATE traditional_designs 
                    SET name=%s, description=%s, region_origin=%s, image_file=%s
                    WHERE design_id=%s
                \"\"\", (name, description, region, image_file, id))
            else:
                cursor.execute(\"\"\"
                    UPDATE traditional_designs 
                    SET name=%s, description=%s, region_origin=%s 
                    WHERE design_id=%s
                \"\"\", (name, description, region, id))"""

content = content.replace(edit_design_target, edit_design_replace)


# Add edit_material and api/chat
additions = """
@app.route('/edit_material/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_material(id):
    if session.get('role') != 'Admin':
        flash("Only Administrators can edit materials.", "error")
        return redirect(url_for('materials'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity_available')
        
        image_file = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_file = filename
                
        try:
            if image_file:
                cursor.execute("UPDATE raw_materials SET material_name=%s, quantity_available=%s, image_file=%s WHERE material_id=%s", (name, quantity, image_file, id))
            else:
                cursor.execute("UPDATE raw_materials SET material_name=%s, quantity_available=%s WHERE material_id=%s", (name, quantity, id))
            conn.commit()
            flash("Material updated successfully!", "success")
            return redirect(url_for('materials'))
        except mysql.connector.Error as err:
            flash(f"Database error: {err.msg}", "error")
            
    cursor.execute("SELECT * FROM raw_materials WHERE material_id = %s", (id,))
    material = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_material.html', material=material)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    text = data.get('text', '').lower()
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    reply = "I didn't quite catch that. Could you ask about our artisans or materials?"
    
    try:
        if 'hello' in text or 'hi' in text:
            reply = "Namaskara! I am your Handloom AI. I track the threads and tales of our weavers. What shall we look up today?"
        elif 'artisan' in text or 'weaver' in text:
            cursor.execute("SELECT COUNT(*) as c FROM artisans")
            count = cursor.fetchone()['c']
            reply = f"We currently have {count} master and novice artisans actively weaving in our network."
        elif 'material' in text or 'silk' in text or 'yarn' in text:
            cursor.execute("SELECT SUM(quantity_available) as s FROM raw_materials")
            res = cursor.fetchone()
            total = res['s'] if res['s'] else 0
            reply = f"Our current inventory holds {total} kg of raw materials, carefully sourced for production."
        elif 'design' in text or 'saree' in text:
            cursor.execute("SELECT name FROM traditional_designs LIMIT 1")
            res = cursor.fetchone()
            name = res['name'] if res else 'Mysore Silk Zari'
            reply = f"The {name} is our most active production line this week."
    except Exception as e:
        reply = f"Error querying database: {str(e)}"
    finally:
        cursor.close()
        conn.close()
        
    return jsonify({"reply": reply})

if __name__ == '__main__':
"""
content = content.replace("if __name__ == '__main__':", additions)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("app.py updated successfully.")
