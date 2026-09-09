import os

file_path = r'd:\dbmss\app.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

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

count = 0
for old, new in replacements.items():
    if old in content:
        count += content.count(old)
        content = content.replace(old, new)

if count > 0:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Replaced {count} instances of old url_for calls in app.py")
else:
    print("No old url_for calls found in app.py.")
