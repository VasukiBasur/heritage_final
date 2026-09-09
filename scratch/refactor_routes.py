import os
import re

app_file = r"d:\dbmss\app.py"

with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update redirect map in login
old_redirect = """            redirect_map = {
                'Admin': 'dashboard',
                'Weaver': 'artisan_dashboard',
                'Supplier': 'supplier_dashboard',
                'Customer': 'buyer_marketplace',
                'Delivery Partner': 'shipment_dashboard'
            }"""
new_redirect = """            redirect_map = {
                'Admin': 'admin_dashboard',
                'Weaver': 'weaver_dashboard',
                'Supplier': 'sup_dashboard',
                'Customer': 'shop_home',
                'Delivery Partner': 'del_dashboard'
            }"""
if old_redirect in content:
    content = content.replace(old_redirect, new_redirect)
else:
    print("Warning: Could not find exact redirect map to replace. Will attempt regex.")
    content = re.sub(r"redirect_map\s*=\s*\{[^}]+\}", new_redirect, content)

# 2. Rename dashboard routes
# @app.route('/dashboard') -> @app.route('/admin/dashboard') and def dashboard() -> def admin_dashboard()
content = re.sub(r"@app\.route\('/dashboard'\)\s*\n@login_required\s*\ndef dashboard\(\):", "@app.route('/admin/dashboard')\n@login_required\ndef admin_dashboard():", content)

# @app.route('/artisan_dashboard') -> @app.route('/artisan/dashboard') and def artisan_dashboard() -> def weaver_dashboard()
content = re.sub(r"@app\.route\('/artisan_dashboard'\)\s*\n@login_required\s*\ndef artisan_dashboard\(\):", "@app.route('/artisan/dashboard')\n@login_required\ndef weaver_dashboard():", content)

# @app.route('/supplier_dashboard') -> @app.route('/supplier/dashboard') and def supplier_dashboard() -> def sup_dashboard()
content = re.sub(r"@app\.route\('/supplier_dashboard'\)\s*\n@login_required\s*\ndef supplier_dashboard\(\):", "@app.route('/supplier/dashboard')\n@login_required\ndef sup_dashboard():", content)

# @app.route('/buyer_marketplace') -> @app.route('/shop/home') and def buyer_marketplace() -> def shop_home()
content = re.sub(r"@app\.route\('/buyer_marketplace'\)\s*\n@login_required\s*\ndef buyer_marketplace\(\):", "@app.route('/shop/home')\n@login_required\ndef shop_home():", content)

# @app.route('/shipment_dashboard') -> @app.route('/delivery/dashboard') and def shipment_dashboard() -> def del_dashboard()
content = re.sub(r"@app\.route\('/shipment_dashboard'\)\s*\n@login_required\s*\ndef shipment_dashboard\(\):", "@app.route('/delivery/dashboard')\n@login_required\ndef del_dashboard():", content)


# 3. Append placeholder routes at the bottom
placeholder_routes = """
# ==========================================
# AUTO-GENERATED PLACEHOLDER ROUTES
# ==========================================

def render_placeholder(name):
    return f"<h1 style='color: white; background: #121212; height: 100vh; padding: 50px; font-family: sans-serif;'>{name} (Placeholder UI)</h1>"

# Admin Sub-Routes
@app.route('/admin/manage_users')
@login_required
def admin_manage_users(): return render_placeholder("Manage Users")

@app.route('/admin/manage_artisans')
@login_required
def admin_manage_artisans(): return render_placeholder("Manage Artisans")

@app.route('/admin/manage_suppliers')
@login_required
def admin_manage_suppliers(): return render_placeholder("Manage Suppliers")

@app.route('/admin/manage_products')
@login_required
def admin_manage_products(): return render_placeholder("Manage Products")

@app.route('/admin/inventory')
@login_required
def admin_inventory(): return render_placeholder("Inventory")

@app.route('/admin/orders')
@login_required
def admin_orders(): return render_placeholder("Orders")

@app.route('/admin/payments')
@login_required
def admin_payments(): return render_placeholder("Payments")

@app.route('/admin/shipments')
@login_required
def admin_shipments(): return render_placeholder("Shipment Tracking")

@app.route('/admin/reports')
@login_required
def admin_reports(): return render_placeholder("Reports & Analytics")

@app.route('/admin/settings')
@login_required
def admin_settings(): return render_placeholder("Settings")

# Artisan Sub-Routes
@app.route('/artisan/products')
@login_required
def artisan_products(): return render_placeholder("My Products")

@app.route('/artisan/upload_product')
@login_required
def artisan_upload_product(): return render_placeholder("Upload Product")

@app.route('/artisan/production')
@login_required
def artisan_production(): return render_placeholder("Production Status")

@app.route('/artisan/orders')
@login_required
def artisan_orders(): return render_placeholder("Orders Received")

@app.route('/artisan/earnings')
@login_required
def artisan_earnings(): return render_placeholder("Earnings")

@app.route('/artisan/qr_verification')
@login_required
def artisan_qr_verification(): return render_placeholder("QR Verification")

@app.route('/artisan/profile')
@login_required
def artisan_profile(): return render_placeholder("Profile")

# Supplier Sub-Routes
@app.route('/supplier/materials')
@login_required
def supplier_materials(): return render_placeholder("Raw Materials")

@app.route('/supplier/requests')
@login_required
def supplier_requests(): return render_placeholder("Material Requests")

@app.route('/supplier/deliveries')
@login_required
def supplier_deliveries(): return render_placeholder("Deliveries")

@app.route('/supplier/inventory')
@login_required
def supplier_inventory(): return render_placeholder("Inventory Supply")

@app.route('/supplier/profile')
@login_required
def supplier_profile(): return render_placeholder("Profile")

# Customer Sub-Routes
@app.route('/shop/products')
def shop_products(): return render_placeholder("Product Listing")

@app.route('/shop/product/<int:id>')
def shop_product_details(id): return render_placeholder("Product Details")

@app.route('/shop/cart')
@login_required
def shop_cart(): return render_placeholder("Cart")

@app.route('/shop/checkout')
@login_required
def shop_checkout(): return render_placeholder("Checkout")

@app.route('/shop/payment')
@login_required
def shop_payment(): return render_placeholder("Payment")

@app.route('/shop/tracking')
@login_required
def shop_tracking(): return render_placeholder("Order Tracking")

@app.route('/shop/wishlist')
@login_required
def shop_wishlist(): return render_placeholder("Wishlist")

@app.route('/shop/reviews')
@login_required
def shop_reviews(): return render_placeholder("Reviews")

@app.route('/shop/profile')
@login_required
def shop_profile(): return render_placeholder("Profile")

@app.route('/shop/orders')
@login_required
def shop_orders(): return render_placeholder("Previous Orders")

# Delivery Sub-Routes
@app.route('/delivery/assigned')
@login_required
def delivery_assigned(): return render_placeholder("Assigned Orders")

@app.route('/delivery/status')
@login_required
def delivery_status(): return render_placeholder("Delivery Status")

@app.route('/delivery/routes')
@login_required
def delivery_routes(): return render_placeholder("Route Details")

@app.route('/delivery/delivered')
@login_required
def delivery_delivered(): return render_placeholder("Delivered Orders")

@app.route('/delivery/contact')
@login_required
def delivery_contact(): return render_placeholder("Contact Customer")
"""

if "# AUTO-GENERATED PLACEHOLDER ROUTES" not in content:
    content += "\n" + placeholder_routes

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Routes refactored successfully.")
