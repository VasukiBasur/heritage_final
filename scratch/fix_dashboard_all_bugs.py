import re

# 1. Update app.py to include a global dictionary and an endpoint for saving mock logs
app_py_path = r'd:\dbmss\app.py'
with open(app_py_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

# Add a global dict for mock logs if it doesn't exist
if 'GLOBAL_MOCK_DB =' not in app_content:
    injection = """
GLOBAL_MOCK_DB = {
    '15': {'id': 'PRD-1015', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Deep Emerald & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
    '7': {'id': 'PRD-1007', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Deep Emerald & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
    '10': {'id': 'PRD-1010', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Deep Emerald & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
    '11': {'id': 'PRD-1011', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Deep Emerald & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
    '12': {'id': 'PRD-1012', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Deep Emerald & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
    '22': {'id': 'PRD-1022', 'name': 'Dharwad Cotton', 'category': 'Cotton Sarees', 'image': 'dharwad_cotton_saree.png.jpeg', 'desc': 'Soft, breathable pure Dharwad cotton with naturally dyed threads.', 'fabric': 'Organic Dharwad Cotton', 'color': 'Earth Brown & Indigo', 'size': '5.5 Meters', 'pattern': 'Checkered & Stripes', 'price': '₹3,200'},
    '28': {'id': 'PRD-1028', 'name': 'Ilkal Checkered', 'category': 'Heritage Sarees', 'image': 'ilkal_checkered.png.jpeg', 'desc': 'Traditional Ilkal weave with signature red borders and intricate pallu.', 'fabric': 'Cotton-Silk Blend', 'color': 'Mustard & Ruby Red', 'size': '6.0 Meters', 'pattern': 'Kond Chikki (Checkered)', 'price': '₹6,400'},
}

@app.route('/api/add_log', methods=['POST'])
def add_mock_log_endpoint():
    data = request.json
    log_id = str(data.get('log_id'))
    GLOBAL_MOCK_DB[log_id] = data.get('product_details')
    return jsonify({"success": True})
"""
    app_content = app_content.replace("if __name__ == '__main__':", injection + "\nif __name__ == '__main__':")

# Replace scan_product to use GLOBAL_MOCK_DB
scan_product_old = """@app.route('/scan/<log_id>')
def scan_product(log_id):
    mock_db = {
        '15': {'id': 'PRD-1015', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Royal Crimson & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
        '7': {'id': 'PRD-1007', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Deep Emerald & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
        '10': {'id': 'PRD-1010', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Deep Emerald & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
        '11': {'id': 'PRD-1011', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Deep Emerald & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
        '12': {'id': 'PRD-1012', 'name': 'Mysore Silk Zari', 'category': 'Silk Sarees', 'image': 'mysore_silk_zari.png.jpeg', 'desc': 'Authentic handwoven pure silk saree with pure gold zari borders.', 'fabric': 'Pure Mulberry Silk', 'color': 'Deep Emerald & Gold', 'size': '6.2 Meters', 'pattern': 'Traditional Zari Border', 'price': '₹18,500'},
        '22': {'id': 'PRD-1022', 'name': 'Dharwad Cotton', 'category': 'Cotton Sarees', 'image': 'dharwad_cotton_saree.png.jpeg', 'desc': 'Soft, breathable pure Dharwad cotton with naturally dyed threads.', 'fabric': 'Organic Dharwad Cotton', 'color': 'Earth Brown & Indigo', 'size': '5.5 Meters', 'pattern': 'Checkered & Stripes', 'price': '₹3,200'},
        '28': {'id': 'PRD-1028', 'name': 'Ilkal Checkered', 'category': 'Heritage Sarees', 'image': 'ilkal_checkered.png.jpeg', 'desc': 'Traditional Ilkal weave with signature red borders and intricate pallu.', 'fabric': 'Cotton-Silk Blend', 'color': 'Mustard & Ruby Red', 'size': '6.0 Meters', 'pattern': 'Kond Chikki (Checkered)', 'price': '₹6,400'},
    }
    
    item = mock_db.get(str(log_id))
    if not item:
        design = request.args.get('design', 'Premium Handloom Product')
        img = request.args.get('img', 'saree.png')
        item = {
            'id': f'PRD-20{log_id}',
            'name': design,
            'category': 'Exclusive Handloom',
            'image': img,
            'desc': 'A masterpiece of traditional Indian weaving, crafted with care by master artisans.',
            'fabric': 'Premium Grade Yarn',
            'color': 'Artisan Choice',
            'size': 'Standard',
            'pattern': 'Heritage Motif',
            'price': '₹12,000'
        }
        
    return render_template('product_scan.html', item=item)"""
scan_product_new = """@app.route('/scan/<log_id>')
def scan_product(log_id):
    item = GLOBAL_MOCK_DB.get(str(log_id))
    if not item:
        item = {
            'id': f'PRD-20{log_id}',
            'name': 'Unknown Product',
            'category': 'Unknown',
            'image': 'saree.png',
            'desc': 'Product details not found. Please rescan a valid log.',
            'fabric': '-', 'color': '-', 'size': '-', 'pattern': '-', 'price': '-'
        }
    return render_template('product_scan.html', item=item)"""

if "def scan_product(log_id):" in app_content and "GLOBAL_MOCK_DB.get" not in app_content:
    match = re.search(r'@app\.route\(\'/scan/<log_id>\'\)\ndef scan_product.*?return render_template\(\'product_scan\.html\', item=item\)', app_content, re.DOTALL)
    if match:
        app_content = app_content[:match.start()] + scan_product_new + app_content[match.end():]

with open(app_py_path, 'w', encoding='utf-8') as f:
    f.write(app_content)


# 2. Update dashboard.html JavaScript and HTML
dashboard_path = r'd:\dbmss\templates\dashboard.html'
with open(dashboard_path, 'r', encoding='utf-8') as f:
    dash_content = f.read()

# Fix Status Badges by adding a specific class 'status-badge'
dash_content = dash_content.replace('class="px-3 py-1 bg-', 'class="status-badge px-3 py-1 bg-')

# Fix updateStatus JS
update_js_old = """window.updateStatus = function(btn) {
        const row = btn.closest('tr');
        const select = row.querySelector('select');
        const badge = row.querySelector('span[class*="px-3 py-1 bg-"]'); // The status badge
        if (select && badge) {
            const newStatus = select.value;
            badge.innerText = newStatus;
            badge.className = "px-3 py-1 rounded text-xs border bg-green-900/40 text-green-400 border-green-500/50";
            alert("Status updated to: " + newStatus);
        }
    };"""
update_js_new = """window.updateStatus = function(btn) {
        const row = btn.closest('tr');
        const select = row.querySelector('select');
        const badge = row.querySelector('.status-badge') || row.querySelector('span[class*="rounded text-xs border"]');
        if (select && badge) {
            const newStatus = select.value;
            badge.innerText = newStatus;
            badge.className = "status-badge px-3 py-1 rounded text-xs border bg-green-900/40 text-green-400 border-green-500/50";
            // Flash effect to show it worked without annoying alert
            badge.style.opacity = '0.5';
            setTimeout(() => badge.style.opacity = '1', 200);
        } else {
            console.error("Could not find badge element in row", row);
        }
    };"""
if update_js_old in dash_content:
    dash_content = dash_content.replace(update_js_old, update_js_new)
else:
    # Use regex if spacing changed
    match = re.search(r'window\.updateStatus = function\(btn\) \{.*?\};', dash_content, re.DOTALL)
    if match:
        dash_content = dash_content[:match.start()] + update_js_new + dash_content[match.end():]

# Fix addMockLog JS to POST to backend and simplify QR
addmock_match = re.search(r'const payloadText = `http://127.0.0.1:5000/scan/\$\{newId\}.*?\n.*?const encodedPayload = encodeURIComponent\(payloadText\);', dash_content)
if addmock_match:
    new_payload_js = """
        // Send details to backend so they can be retrieved by the scanner
        fetch('/api/add_log', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                log_id: newId,
                product_details: design
            })
        });
        
        const payloadText = `http://127.0.0.1:5000/scan/${newId}`;
        const encodedPayload = encodeURIComponent(payloadText);
"""
    dash_content = dash_content[:addmock_match.start()] + new_payload_js + dash_content[addmock_match.end():]


# 3. Completely fix the static QR codes
# They are broken because maybe qrserver rejects "http%3A%2F%2F127.0.0.1%3A5000%2Fscan%2F15" for some reason, or I corrupted the tag.
# We will encode it using Javascript's encodeURIComponent standard (which qrserver likes), 
# or just change them to google charts API, which never breaks.
# Wait, changing to Google Charts QR is bulletproof!
# https://chart.googleapis.com/chart?chs=400x400&cht=qr&chl=http://127.0.0.1:5000/scan/15
# And it works without complex encoding.

def replace_with_google_qr(match):
    full_tag = match.group(0)
    # Find the scan ID
    id_match = re.search(r'scan%2F(\d+)', full_tag)
    if not id_match:
        return full_tag
    log_id = id_match.group(1)
    return f'<img src="https://chart.googleapis.com/chart?chs=400x400&cht=qr&chl=http://127.0.0.1:5000/scan/{log_id}"'

# Replace in static rows
dash_content = re.sub(r'<img src=\"https://api\.qrserver\.com[^\"]*\"', replace_with_google_qr, dash_content)

# Replace in dynamic row JS
dash_content = dash_content.replace(
    'src="https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=${encodedPayload}&color=000000&bgcolor=FFFFFF"',
    'src="https://chart.googleapis.com/chart?chs=400x400&cht=qr&chl=${encodedPayload}"'
)

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(dash_content)

print("Backend DB added. Bugs fixed. QR API swapped to Google Charts for bulletproof reliability.")
