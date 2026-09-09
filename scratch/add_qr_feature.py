import os
import re

# 1. Update app.py with the new route
app_path = r'd:\dbmss\app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

new_route = """
@app.route('/scan/<log_id>')
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
        
    return render_template('product_scan.html', item=item)
"""

if "def scan_product" not in app_content:
    app_content = app_content.replace("if __name__ == '__main__':", new_route + "\nif __name__ == '__main__':")
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(app_content)

# 2. Update dashboard.html QR codes
dashboard_path = r'd:\dbmss\templates\dashboard.html'
with open(dashboard_path, 'r', encoding='utf-8') as f:
    dashboard_content = f.read()

# Replace static QR codes
dashboard_content = re.sub(r'data=(\d+)&color', r'data=http://127.0.0.1:5000/scan/\1&color', dashboard_content)

# Replace dynamic JS QR code
# Old: data=${newId}&color
# New: data=http%3A%2F%2F127.0.0.1%3A5000%2Fscan%2F${newId}%3Fdesign%3D${encodeURIComponent(design.name)}%26img%3D${encodeURIComponent(design.img)}&color
js_search = r'data=\$\{newId\}&color'
js_replace = r'data=http%3A%2F%2F127.0.0.1%3A5000%2Fscan%2F${newId}%3Fdesign%3D${encodeURIComponent(design.name)}%26img%3D${encodeURIComponent(design.img)}&color'
dashboard_content = re.sub(js_search, js_replace, dashboard_content)

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(dashboard_content)

print("Updated app.py and dashboard.html")
