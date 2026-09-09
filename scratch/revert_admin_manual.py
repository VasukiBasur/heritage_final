import os

# 1. Read the current dashboard.html content block
current_dashboard_path = r'd:\dbmss\templates\dashboard.html'
with open(current_dashboard_path, 'r', encoding='utf-8') as f:
    current_content = f.read()

# Extract block content
content_start = current_content.find('{% block content %}') + len('{% block content %}')
content_end = current_content.find('{% endblock %}', content_start)
main_content = current_content[content_start:content_end].strip()

# Extract extra scripts
scripts_start = current_content.find('{% block extra_scripts %}')
scripts_end = -1
extra_scripts = ""
if scripts_start != -1:
    scripts_start += len('{% block extra_scripts %}')
    scripts_end = current_content.find('{% endblock %}', scripts_start)
    extra_scripts = current_content[scripts_start:scripts_end].strip()

# 2. Read base_layout.html head
base_layout_path = r'd:\dbmss\templates\base_layout.html'
with open(base_layout_path, 'r', encoding='utf-8') as f:
    base_content = f.read()

head_start = base_content.find('<!DOCTYPE html>')
head_end = base_content.find('</head>') + len('</head>')
head_html = base_content[head_start:head_end]
# Replace block title in head
head_html = head_html.replace('{% block title %}Dashboard{% endblock %}', 'Admin Dashboard')

# 3. Define the Original Top Navbar
original_layout = """<body class="flex justify-center h-screen w-full overflow-hidden bg-[#121212] text-[#e5e5e5]">

    <!-- Main Content Wrapper -->
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
"""

# 4. Define Flash Messages
flash_messages = """
                {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                {% for category, message in messages %}
                <div class="mb-4 p-4 rounded bg-[#1E1E1E] border-l-4 border-brand-gold shadow-lg flex items-center space-x-3 transition-transform transform hover:-translate-y-1 mx-6 mt-6">
                    <svg class="w-5 h-5 text-brand-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <span class="font-sans text-sm text-brand-lightgold">{{ message }}</span>
                </div>
                {% endfor %}
                {% endif %}
                {% endwith %}
"""

# 5. Combine everything
full_html = head_html + "\n\n" + original_layout + "\n" + flash_messages + "\n" + main_content + "\n\n        </main>\n    </div>\n\n    " + extra_scripts + "\n</body>\n</html>"

with open(current_dashboard_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print("Admin dashboard completely reverted to old Top Navbar layout.")
