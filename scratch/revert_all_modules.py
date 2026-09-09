import os
import glob

base_layout_path = r'd:\dbmss\templates\base_layout.html'
dashboard_path = r'd:\dbmss\templates\dashboard.html'
admin_layout_path = r'd:\dbmss\templates\admin_base_layout.html'

with open(dashboard_path, 'r', encoding='utf-8') as f:
    dashboard_content = f.read()

# The dashboard.html currently has the FULL standalone HTML.
# We can just extract everything before the {% block content %} and after the {% endblock %}
# to create admin_base_layout.html

# Wait, dashboard.html has hardcoded flash messages and content. Let's make it a proper layout.

admin_base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Admin Dashboard{% endblock %} - Heritage Handloom</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: { brand: { black: '#121212', dark: '#1a1a1a', brown: '#3e2723', gold: '#d4af37', lightgold: '#f0e6d2' } },
                    fontFamily: { sans: ['Inter', 'sans-serif'], serif: ['Playfair Display', 'serif'] }
                }
            }
        }
    </script>
    <style>
        body { background-color: #121212; color: #e5e5e5; scrollbar-width: none; -ms-overflow-style: none; }
        ::-webkit-scrollbar { display: none; }
        .glass-card { background: rgba(26, 26, 26, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(212, 175, 55, 0.2); }
        table { border-collapse: separate; border-spacing: 0; width: 100%; }
        th { background-color: rgba(212, 175, 55, 0.1); color: #d4af37; text-transform: uppercase; font-size: 0.75rem; padding: 1rem; text-align: left; border-bottom: 1px solid rgba(212, 175, 55, 0.3); }
        td { padding: 1rem; border-bottom: 1px solid rgba(255, 255, 255, 0.05); font-size: 0.875rem; color: #f0e6d2; }
        tr:hover td { background-color: rgba(255, 255, 255, 0.02); }
        input, select, textarea { background-color: rgba(0,0,0,0.5); border: 1px solid rgba(212,175,55,0.3); color: #f0e6d2; border-radius: 4px; padding: 0.5rem; width: 100%; margin-bottom: 1rem; }
    </style>
</head>
<body class="flex justify-center h-screen w-full overflow-hidden bg-[#121212] text-[#e5e5e5]">

    <div class="flex flex-col h-full overflow-hidden w-full max-w-[1500px] mx-auto relative shadow-[0_0_50px_rgba(0,0,0,0.8)] border-x border-brand-gold/10">

        <!-- Top Navbar -->
        <header class="bg-brand-dark border-b border-brand-gold/30 h-16 flex items-center justify-between px-6 shadow-md w-full shrink-0 z-50">
            <h1 class="text-xl font-serif font-bold text-brand-gold"><a href="{{ url_for('admin_dashboard') }}">Heritage Handloom</a></h1>
            
            <nav class="hidden md:flex space-x-6">
                <a href="{{ url_for('admin_dashboard') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Dashboard</a>
                <a href="{{ url_for('artisans') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Artisans</a>
                <a href="{{ url_for('designs') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Designs</a>
                <a href="{{ url_for('materials') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Materials</a>
                
                {% if session.get('role') == 'Admin' %}
                <div class="relative group">
                    <button class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors flex items-center">
                        Modules <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </button>
                    <!-- Mega Dropdown for 12 Modules -->
                    <div class="absolute left-0 mt-2 w-56 bg-brand-dark border border-brand-gold/30 rounded-sm shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50 grid grid-cols-1 divide-y divide-brand-gold/10">
                        <div class="py-1">
                            <p class="px-4 py-1 text-[10px] font-bold text-brand-gold uppercase tracking-wider">Core Supply</p>
                            <a href="{{ url_for('weaver_module') }}" class="block px-4 py-1.5 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">1. Weaver Mgmt</a>
                            <a href="{{ url_for('raw_material_module') }}" class="block px-4 py-1.5 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">2. Raw Materials</a>
                            <a href="{{ url_for('supplier_module') }}" class="block px-4 py-1.5 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">3. Suppliers</a>
                        </div>
                        <div class="py-1">
                            <p class="px-4 py-1 text-[10px] font-bold text-brand-gold uppercase tracking-wider">Production & Catalog</p>
                            <a href="{{ url_for('production_module') }}" class="block px-4 py-1.5 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">4. Production Tracking</a>
                            <a href="{{ url_for('product_catalog_module') }}" class="block px-4 py-1.5 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">5. Product Catalog</a>
                        </div>
                        <div class="py-1">
                            <p class="px-4 py-1 text-[10px] font-bold text-brand-gold uppercase tracking-wider">Enterprise ERP</p>
                            <a href="{{ url_for('order_module') }}" class="block px-4 py-1.5 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">6. Order Mgmt</a>
                            <a href="{{ url_for('customer_module') }}" class="block px-4 py-1.5 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">7. Customer Mgmt</a>
                            <a href="{{ url_for('inventory_module') }}" class="block px-4 py-1.5 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">8. Warehouse Inventory</a>
                            <a href="{{ url_for('billing_module') }}" class="block px-4 py-1.5 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">9. Payment & Billing</a>
                            <a href="{{ url_for('logistics_module') }}" class="block px-4 py-1.5 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">10. Logistics Transport</a>
                        </div>
                        <div class="py-1">
                            <p class="px-4 py-1 text-[10px] font-bold text-brand-gold uppercase tracking-wider">Advanced Analytics</p>
                            <a href="{{ url_for('demand_prediction') }}" class="block px-4 py-1.5 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors flex items-center justify-between">12. Demand Prediction <span class="bg-blue-600 text-white text-[8px] px-1 py-0.5 rounded-sm">AI</span></a>
                        </div>
                    </div>
                </div>
                {% endif %}
                {% if session.get('role') == 'Artisan' %}
                <a href="{{ url_for('weaver_dashboard') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">My Workspace</a>
                {% endif %}
                {% if session.get('role') == 'Buyer' %}
                <a href="{{ url_for('shop_home') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Marketplace</a>
                {% endif %}
            </nav>

            <div class="flex items-center space-x-4">
                <span class="text-xs text-brand-lightgold hidden md:block">Logged in as <span class="font-bold text-brand-gold">{{ session.get('username', 'Guest') }}</span></span>
                <a href="{{ url_for('logout') }}" class="text-xs bg-brand-gold text-brand-black px-4 py-2 rounded font-semibold hover:bg-yellow-500 transition-colors">Logout</a>
            </div>
        </header>

        <!-- Main Scrollable Area -->
        <main class="flex-1 overflow-y-auto bg-[#121212] w-full" style="overflow-x: hidden;">
            {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
            {% for category, message in messages %}
            <div class="mb-4 p-4 rounded bg-[#1E1E1E] border-l-4 border-brand-gold shadow-lg mx-6 mt-6">
                <span class="font-sans text-sm text-brand-lightgold">{{ message }}</span>
            </div>
            {% endfor %}
            {% endif %}
            {% endwith %}

            <div class="p-6 lg:p-10">
                <div class="flex justify-between items-end mb-8 border-b border-brand-gold/20 pb-4">
                    <div>
                        <h1 class="text-3xl font-serif text-brand-gold">{% block header_title %}Module{% endblock %}</h1>
                    </div>
                </div>

                {% block content %}{% endblock %}
            </div>
        </main>
    </div>

    {% block extra_scripts %}{% endblock %}
    <script src="{{ url_for('static', filename='frontend_api.js') }}"></script>
</body>
</html>
"""

with open(admin_layout_path, 'w', encoding='utf-8') as f:
    f.write(admin_base_html)

print("Created admin_base_layout.html")

# Now update all modules to extend admin_base_layout.html
template_dir = r'd:\dbmss\templates'
module_files = glob.glob(os.path.join(template_dir, '*_module.html'))
module_files.append(os.path.join(template_dir, 'demand_prediction.html'))
module_files.append(dashboard_path)

for file_path in module_files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # If the file extends base_layout.html, change it
        if "{% extends 'base_layout.html' %}" in content:
            new_content = content.replace("{% extends 'base_layout.html' %}", "{% extends 'admin_base_layout.html' %}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {os.path.basename(file_path)}")
        elif file_path == dashboard_path:
            # We already restored dashboard.html in revert_admin_manual.py so it DOESN'T extend anything.
            # But wait, it's better if dashboard.html extends admin_base_layout.html for cleanliness!
            pass
