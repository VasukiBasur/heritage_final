import os
import glob

templates_dir = r'd:\dbmss\templates'
html_files = glob.glob(os.path.join(templates_dir, '*.html'))

replacements = {
    "url_for('dashboard')": "url_for('admin_dashboard')",
    'url_for("dashboard")': 'url_for("admin_dashboard")',
    "url_for('artisan_dashboard')": "url_for('weaver_dashboard')",
    'url_for("artisan_dashboard")': 'url_for("weaver_dashboard")',
    "url_for('supplier_dashboard')": "url_for('sup_dashboard')",
    'url_for("supplier_dashboard")': 'url_for("sup_dashboard")',
    "url_for('buyer_marketplace')": "url_for('shop_home')",
    'url_for("buyer_marketplace")': 'url_for("shop_home")',
    "url_for('shipment_dashboard')": "url_for('del_dashboard')",
    'url_for("shipment_dashboard")': 'url_for("del_dashboard")'
}

total_count = 0
for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    count = 0
    for old, new in replacements.items():
        if old in content:
            count += content.count(old)
            content = content.replace(old, new)
            
    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Replaced {count} instances in {os.path.basename(file_path)}")
        total_count += count

print(f"Total replacements in HTML templates: {total_count}")
