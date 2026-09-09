import os
import re

template_dir = r"d:\dbmss\templates"

base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Heritage Handloom</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{ black: '#121212', dark: '#1a1a1a', brown: '#3e2723', gold: '#d4af37', lightgold: '#f0e6d2' }}
                    }},
                    fontFamily: {{ sans: ['Inter', 'sans-serif'], serif: ['Playfair Display', 'serif'] }}
                }}
            }}
        }}
    </script>
    <style>
        body {{ background-color: #121212; color: #e5e5e5; scrollbar-width: none; -ms-overflow-style: none; }}
        .glass-card {{ background: rgba(26, 26, 26, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(212, 175, 55, 0.2); }}
        ::-webkit-scrollbar {{ display: none; }}
        table {{ border-collapse: separate; border-spacing: 0; width: 100%; }}
        th {{ background-color: rgba(212, 175, 55, 0.1); color: #d4af37; text-transform: uppercase; font-size: 0.75rem; tracking: wider; padding: 1rem; text-align: left; border-bottom: 1px solid rgba(212, 175, 55, 0.3); }}
        td {{ padding: 1rem; border-bottom: 1px solid rgba(255, 255, 255, 0.05); font-size: 0.875rem; color: #f0e6d2; }}
        tr:hover td {{ background-color: rgba(255, 255, 255, 0.02); }}
    </style>
</head>
<body class="flex h-screen w-full overflow-hidden bg-[#121212] text-[#e5e5e5]">
    <div class="flex-1 flex flex-col h-full overflow-hidden">
        <!-- NAV PLACEHOLDER -->
        <header class="bg-brand-dark border-b border-brand-gold/30 h-16 flex items-center justify-between px-6 shadow-md w-full shrink-0 z-50">
            <h1 class="text-xl font-serif font-bold text-brand-gold"><a href="{{{{ url_for('dashboard') }}}}">Heritage Handloom</a></h1>
            <nav class="hidden md:flex space-x-6">
                <a href="{{{{ url_for('dashboard') }}}}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Dashboard</a>
                <a href="{{{{ url_for('artisans') }}}}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Artisans</a>
                <a href="{{{{ url_for('designs') }}}}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Designs</a>
                <a href="{{{{ url_for('materials') }}}}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Materials</a>
                {{% if session.get('role') == 'Admin' %}}
                <div class="relative group">
                    <button class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors flex items-center">
                        Modules <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </button>
                    <div class="absolute left-0 mt-2 w-48 bg-brand-dark border border-brand-gold/30 rounded-sm shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50">
                        <a href="{{{{ url_for('weaver_module') }}}}" class="block px-4 py-2 text-sm text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">Weaver Mgmt</a>
                        <a href="{{{{ url_for('raw_material_module') }}}}" class="block px-4 py-2 text-sm text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">Raw Materials</a>
                        <a href="{{{{ url_for('supplier_module') }}}}" class="block px-4 py-2 text-sm text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">Suppliers</a>
                        <a href="{{{{ url_for('production_module') }}}}" class="block px-4 py-2 text-sm text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">Production</a>
                        <a href="{{{{ url_for('product_catalog_module') }}}}" class="block px-4 py-2 text-sm text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">Product Catalog</a>
                    </div>
                </div>
                {{% endif %}}
                {{% if session.get('role') == 'Artisan' %}}
                <a href="{{{{ url_for('artisan_dashboard') }}}}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">My Workspace</a>
                {{% endif %}}
                {{% if session.get('role') == 'Buyer' %}}
                <a href="{{{{ url_for('buyer_marketplace') }}}}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Marketplace</a>
                {{% endif %}}
            </nav>
            <div class="flex items-center space-x-4">
                <span class="text-xs text-brand-lightgold hidden md:block">Logged in as <span class="font-bold text-brand-gold">{{{{ session.get('username', 'Guest') }}}}</span></span>
                <a href="{{{{ url_for('logout') }}}}" class="text-xs bg-brand-gold text-brand-black px-4 py-2 rounded font-semibold hover:bg-yellow-500 transition-colors">Logout</a>
            </div>
        </header>

        <main class="flex-1 overflow-y-auto p-6 lg:p-10 w-full relative">
            <div class="flex justify-between items-center mb-8 border-b border-brand-gold/20 pb-4">
                <h2 class="text-3xl font-serif font-bold text-brand-gold">{title}</h2>
                <button class="bg-brand-gold text-brand-black px-4 py-2 rounded text-sm font-bold hover:bg-yellow-500 transition-colors">+ Add New</button>
            </div>
            
            <div class="glass-card rounded-md overflow-hidden">
                <div class="overflow-x-auto">
                    {table_content}
                </div>
            </div>
        </main>
    </div>
</body>
</html>"""

# 1. Weaver Module
weaver_table = """
<table>
    <thead><tr><th>ID</th><th>Name</th><th>Village</th><th>Skill</th><th>Contact</th><th>Experience</th><th>Wage Details</th><th>Action</th></tr></thead>
    <tbody>
        {% for w in weavers %}
        <tr>
            <td>#{{ w.artisan_id }}</td>
            <td class="font-bold text-brand-gold">{{ w.name }}</td>
            <td>{{ w.village }}</td>
            <td><span class="px-2 py-1 bg-brand-gold/10 text-brand-gold border border-brand-gold/30 rounded-full text-xs">{{ w.skill_level }}</span></td>
            <td>{{ w.contact_number }}</td>
            <td>{{ w.experience_years }} Yrs</td>
            <td class="text-green-400">{{ w.wage_details }}</td>
            <td><a href="#" class="text-xs text-brand-gold hover:underline">Edit</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
"""
with open(os.path.join(template_dir, 'weaver_module.html'), 'w', encoding='utf-8') as f:
    f.write(base_template.format(title="Weaver Management", table_content=weaver_table))

# 2. Raw Material Module
material_table = """
<table>
    <thead><tr><th>ID</th><th>Material Name</th><th>Stock Available</th><th>Unit</th><th>Action</th></tr></thead>
    <tbody>
        {% for m in materials %}
        <tr>
            <td>#{{ m.material_id }}</td>
            <td class="font-bold text-brand-gold">{{ m.material_name }}</td>
            <td class="text-green-400 font-bold">{{ m.quantity_available }} Units</td>
            <td>Standard</td>
            <td><button class="text-xs bg-brand-gold/10 text-brand-gold px-2 py-1 border border-brand-gold/30 rounded hover:bg-brand-gold hover:text-brand-black">Update Stock</button></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
"""
with open(os.path.join(template_dir, 'raw_material_module.html'), 'w', encoding='utf-8') as f:
    f.write(base_template.format(title="Raw Material Inventory", table_content=material_table))

# 3. Supplier Module
supplier_table = """
<table>
    <thead><tr><th>ID</th><th>Supplier Name</th><th>Material Supplied</th><th>Cost</th><th>Delivery Schedule</th><th>Action</th></tr></thead>
    <tbody>
        {% for s in suppliers %}
        <tr>
            <td>#{{ s.supplier_id }}</td>
            <td class="font-bold text-brand-gold">{{ s.supplier_name }}</td>
            <td>{{ s.material_supplied }}</td>
            <td class="text-green-400">₹{{ s.cost }}</td>
            <td>{{ s.delivery_dates }}</td>
            <td><a href="#" class="text-xs text-brand-gold hover:underline">Manage</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
"""
with open(os.path.join(template_dir, 'supplier_module.html'), 'w', encoding='utf-8') as f:
    f.write(base_template.format(title="Supplier Management", table_content=supplier_table))

# 4. Production Tracking
prod_table = """
<table>
    <thead><tr><th>Batch ID</th><th>Design</th><th>Artisan</th><th>Start Date</th><th>Stage</th><th>Status</th><th>Action</th></tr></thead>
    <tbody>
        {% for log in logs %}
        <tr>
            <td>#BCH-{{ log.log_id }}</td>
            <td class="font-bold text-brand-gold">{{ log.design_name }}</td>
            <td>{{ log.artisan_name }}</td>
            <td>{{ log.start_date }}</td>
            <td>
                <select class="bg-brand-dark border border-brand-gold/30 text-xs px-2 py-1 rounded text-brand-lightgold focus:outline-none focus:border-brand-gold">
                    <option value="Dyeing" {% if log.stage == 'Dyeing' %}selected{% endif %}>Dyeing</option>
                    <option value="Spinning" {% if log.stage == 'Spinning' %}selected{% endif %}>Spinning</option>
                    <option value="Weaving" {% if log.stage == 'Weaving' %}selected{% endif %}>Weaving</option>
                    <option value="Finishing" {% if log.stage == 'Finishing' %}selected{% endif %}>Finishing</option>
                    <option value="Packaging" {% if log.stage == 'Packaging' %}selected{% endif %}>Packaging</option>
                </select>
            </td>
            <td><span class="px-2 py-1 bg-brand-gold/10 text-brand-gold border border-brand-gold/30 rounded-full text-[10px] uppercase">{{ log.status }}</span></td>
            <td><button class="text-xs text-green-400 hover:underline">Save Stage</button></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
"""
with open(os.path.join(template_dir, 'production_module.html'), 'w', encoding='utf-8') as f:
    f.write(base_template.format(title="Production Tracking", table_content=prod_table))

# 5. Product Catalog Module
catalog_table = """
<table>
    <thead><tr><th>Product ID</th><th>Name</th><th>Category</th><th>Price</th><th>Stock</th><th>Action</th></tr></thead>
    <tbody>
        {% for p in products %}
        <tr>
            <td>#{{ p.product_id }}</td>
            <td class="font-bold text-brand-gold">{{ p.product_name }}</td>
            <td><span class="px-2 py-1 bg-brand-black border border-brand-gold/30 rounded text-xs">{{ p.category }}</span></td>
            <td class="text-green-400">₹{{ p.price }}</td>
            <td class="font-bold {% if p.stock_quantity > 20 %}text-green-400{% else %}text-yellow-500{% endif %}">{{ p.stock_quantity }}</td>
            <td><a href="#" class="text-xs text-brand-gold hover:underline">View</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
"""
with open(os.path.join(template_dir, 'product_catalog_module.html'), 'w', encoding='utf-8') as f:
    f.write(base_template.format(title="Product Catalog Management", table_content=catalog_table))

print("Created 5 new module templates.")
