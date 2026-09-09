import re

file_path = r'd:\dbmss\templates\artisan_dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    "url_for('admin_manage_users')": "url_for('customer_module')",
    "url_for('admin_manage_artisans')": "url_for('weaver_module')",
    "url_for('admin_manage_suppliers')": "url_for('supplier_module')",
    "url_for('admin_manage_products')": "url_for('product_catalog_module')",
    "url_for('admin_inventory')": "url_for('inventory_module')",
    "url_for('admin_orders')": "url_for('order_module')",
    "url_for('admin_payments')": "url_for('billing_module')",
    "url_for('admin_shipments')": "url_for('logistics_module')",
    "url_for('admin_reports')": "url_for('demand_prediction')"
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Linked Sidebar to real modules in artisan_dashboard.html")
