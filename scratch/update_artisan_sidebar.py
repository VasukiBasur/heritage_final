import re

file_path = r'd:\dbmss\templates\artisan_dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the nav block in artisan_dashboard.html
new_nav = """        <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-1">
            <p class="px-3 text-xs font-bold text-brand-gold/50 uppercase tracking-widest mb-2">Main Menu</p>
            <a href="{{ url_for('weaver_dashboard') }}" class="block px-3 py-2 rounded-sm text-sm font-medium bg-brand-gold text-brand-black transition-colors">Dashboard</a>
            <a href="{{ url_for('admin_manage_users') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Manage Users</a>
            <a href="{{ url_for('admin_manage_artisans') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Manage Artisans</a>
            <a href="{{ url_for('admin_manage_suppliers') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Manage Suppliers</a>
            <a href="{{ url_for('admin_manage_products') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Manage Products</a>
            
            <p class="px-3 text-xs font-bold text-brand-gold/50 uppercase tracking-widest mt-6 mb-2">Operations</p>
            <a href="{{ url_for('admin_inventory') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Inventory</a>
            <a href="{{ url_for('admin_orders') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Orders</a>
            <a href="{{ url_for('admin_payments') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Payments</a>
            <a href="{{ url_for('admin_shipments') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Shipment Tracking</a>
            
            <p class="px-3 text-xs font-bold text-brand-gold/50 uppercase tracking-widest mt-6 mb-2">System</p>
            <a href="{{ url_for('admin_reports') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Reports & Analytics</a>
            <a href="{{ url_for('admin_settings') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Settings</a>
            <a href="{{ url_for('logout') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-red-400 hover:bg-red-400/10 transition-colors mt-4">Logout</a>
        </nav>"""

nav_start = content.find('<nav class="flex-1 overflow-y-auto py-4 px-3 space-y-1">')
nav_end = content.find('</nav>', nav_start) + 6

if nav_start != -1 and nav_end != -1:
    content = content[:nav_start] + new_nav + content[nav_end:]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Artisan Sidebar updated with Admin links.")
else:
    print("Failed to find nav block.")
