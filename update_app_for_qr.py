import os

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
if 'import qrcode' not in content:
    content = content.replace('import os', 'import os\nimport qrcode\nfrom io import BytesIO\nfrom flask import send_file')

# Add QR and Stage routes
additions = """
@app.route('/generate_qr/<int:log_id>')
def generate_qr(log_id):
    tracking_url = url_for('track_product', log_id=log_id, _external=True)
    qr = qrcode.QRCode(version=1, box_size=5, border=1)
    qr.add_data(tracking_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#d4af37", back_color="#1a1a1a")
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/track/<int:log_id>')
def track_product(log_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(\"\"\"
        SELECT pl.*, td.name as design_name, a.name as artisan_name, td.image_file as design_image 
        FROM production_logs pl 
        JOIN traditional_designs td ON pl.design_id = td.design_id 
        JOIN artisans a ON pl.artisan_id = a.artisan_id 
        WHERE pl.log_id = %s
    \"\"\", (log_id,))
    log = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not log:
        return "Product not found", 404
        
    return render_template('track.html', log=log)

@app.route('/update_stage/<int:log_id>', methods=['POST'])
@login_required
def update_stage(log_id):
    if session.get('role') != 'Admin':
        flash("Only Administrators can update supply chain stages.", "error")
        return redirect(url_for('dashboard'))
        
    stage = request.form.get('stage')
    valid_stages = ['Ordered', 'Raw_Material_Supply', 'Manufacturing', 'Distribution', 'Retail', 'Sold']
    
    if stage in valid_stages:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE production_logs SET supply_chain_stage = %s WHERE log_id = %s", (stage, log_id))
            conn.commit()
            flash("Supply chain stage updated successfully!", "success")
        except Exception as e:
            flash(f"Database error: {str(e)}", "error")
        finally:
            cursor.close()
            conn.close()
    else:
        flash("Invalid stage selected.", "error")
        
    return redirect(request.referrer or url_for('dashboard'))

if __name__ == '__main__':
"""
if '@app.route(\'/generate_qr' not in content:
    content = content.replace("if __name__ == '__main__':", additions)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated app.py with QR and tracking routes.")
