import os

template_dir = r"d:\dbmss\templates"

# The master navigation HTML (updated for all 10 modules)
nav_html = """
        <header class="bg-brand-dark border-b border-brand-gold/30 h-16 flex items-center justify-between px-6 shadow-md w-full shrink-0 z-50">
            <h1 class="text-xl font-serif font-bold text-brand-gold"><a href="{{ url_for('dashboard') }}">Heritage Handloom</a></h1>
            <nav class="hidden md:flex space-x-6">
                <a href="{{ url_for('dashboard') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Dashboard</a>
                <a href="{{ url_for('artisans') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Artisans</a>
                <a href="{{ url_for('designs') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Designs</a>
                <a href="{{ url_for('materials') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Materials</a>
                
                {% if session.get('role') == 'Admin' %}
                <div class="relative group">
                    <button class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors flex items-center">
                        Modules <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </button>
                    <!-- Mega Dropdown for 10 Modules -->
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
                    </div>
                </div>
                {% endif %}
                {% if session.get('role') == 'Artisan' %}
                <a href="{{ url_for('artisan_dashboard') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">My Workspace</a>
                {% endif %}
                {% if session.get('role') == 'Buyer' %}
                <a href="{{ url_for('buyer_marketplace') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Marketplace</a>
                {% endif %}
            </nav>
            <div class="flex items-center space-x-4">
                <span class="text-xs text-brand-lightgold hidden md:block">Logged in as <span class="font-bold text-brand-gold">{{ session.get('username', 'Guest') }}</span></span>
                <a href="{{ url_for('logout') }}" class="text-xs bg-brand-gold text-brand-black px-4 py-2 rounded font-semibold hover:bg-yellow-500 transition-colors">Logout</a>
            </div>
        </header>
"""

# Base HTML generator for a module
def get_module_html(title, iter_var, data_var, headers, columns_html, form_action, form_inputs):
    return f"""<!DOCTYPE html>
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
                    colors: {{ brand: {{ black: '#121212', dark: '#1a1a1a', brown: '#3e2723', gold: '#d4af37', lightgold: '#f0e6d2' }} }},
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
        th {{ background-color: rgba(212, 175, 55, 0.1); color: #d4af37; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; padding: 1rem; text-align: left; border-bottom: 1px solid rgba(212, 175, 55, 0.3); }}
        td {{ padding: 1rem; border-bottom: 1px solid rgba(255, 255, 255, 0.05); font-size: 0.875rem; color: #f0e6d2; }}
        tr:hover td {{ background-color: rgba(255, 255, 255, 0.02); }}
        input, select, textarea {{ background-color: rgba(0,0,0,0.5); border: 1px solid rgba(212,175,55,0.3); color: #f0e6d2; border-radius: 4px; padding: 0.5rem; width: 100%; margin-bottom: 1rem; font-size: 0.875rem; }}
        input:focus, select:focus, textarea:focus {{ outline: none; border-color: #d4af37; }}
        label {{ display: block; font-size: 0.75rem; color: #d4af37; margin-bottom: 0.25rem; text-transform: uppercase; }}
    </style>
</head>
<body class="flex justify-center h-screen w-full overflow-hidden bg-[#121212] text-[#e5e5e5]">
    <div class="flex flex-col h-full overflow-hidden w-full max-w-[1500px] mx-auto relative shadow-[0_0_50px_rgba(0,0,0,0.8)] border-x border-brand-gold/10">
{nav_html}
        <main class="flex-1 overflow-y-auto p-6 lg:p-10 w-full relative">
            <div class="flex justify-between items-center mb-8 border-b border-brand-gold/20 pb-4">
                <h2 class="text-3xl font-serif font-bold text-brand-gold">{title}</h2>
                <button onclick="document.getElementById('crud-modal').classList.remove('hidden')" class="bg-brand-gold text-brand-black px-4 py-2 rounded text-sm font-bold hover:bg-yellow-500 transition-colors shadow-lg shadow-brand-gold/20">+ Add New</button>
            </div>
            
            <!-- Table Data -->
            <div class="glass-card rounded-md overflow-hidden">
                <div class="overflow-x-auto">
                    <table>
                        <thead><tr>
                            {"".join([f"<th>{h}</th>" for h in headers])}
                        </tr></thead>
                        <tbody>
                            {{% for {iter_var} in {data_var} %}}
                            <tr>
                                {columns_html}
                            </tr>
                            {{% else %}}
                            <tr><td colspan="{len(headers)}" class="text-center italic opacity-50 py-8">No records found. Click '+ Add New' to create one.</td></tr>
                            {{% endfor %}}
                        </tbody>
                    </table>
                </div>
            </div>
        </main>
    </div>

    <!-- CRUD Modal -->
    <div id="crud-modal" class="hidden fixed inset-0 z-[9999] flex items-center justify-center bg-black/80 backdrop-blur-sm">
        <div class="bg-brand-dark border border-brand-gold/30 rounded-lg shadow-[0_10px_50px_rgba(212,175,55,0.15)] w-full max-w-lg overflow-hidden flex flex-col max-h-[90vh]">
            <div class="px-6 py-4 border-b border-brand-gold/20 flex justify-between items-center bg-brand-black/50">
                <h3 class="text-xl font-serif text-brand-gold font-bold">Add New Record</h3>
                <button onclick="document.getElementById('crud-modal').classList.add('hidden')" class="text-brand-lightgold/50 hover:text-brand-gold transition-colors text-2xl leading-none">&times;</button>
            </div>
            <div class="p-6 overflow-y-auto flex-1">
                <form action="{form_action}" method="POST">
                    {form_inputs}
                    <div class="mt-6 flex justify-end space-x-3">
                        <button type="button" onclick="document.getElementById('crud-modal').classList.add('hidden')" class="px-4 py-2 border border-brand-gold/30 text-brand-lightgold rounded text-sm hover:bg-brand-gold/10 transition-colors">Cancel</button>
                        <button type="submit" class="bg-brand-gold text-brand-black px-6 py-2 rounded font-bold text-sm hover:bg-yellow-500 transition-colors shadow-lg">Save Record</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
"""

modules_def = [
    {
        "filename": "weaver_module.html", "title": "Weaver Management", "iter_var": "w", "data_var": "weavers",
        "headers": ["ID", "Name", "Village", "Skill", "Contact", "Experience", "Wage Details"],
        "columns_html": "<td>#{{ w.artisan_id }}</td><td class='font-bold text-brand-gold'>{{ w.name }}</td><td>{{ w.village }}</td><td><span class='px-2 py-1 bg-brand-gold/10 text-brand-gold border border-brand-gold/30 rounded-full text-xs'>{{ w.skill_level }}</span></td><td>{{ w.contact_number }}</td><td>{{ w.experience_years }} Yrs</td><td class='text-green-400'>{{ w.wage_details }}</td>",
        "form_action": "/api/crud/weaver/add",
        "form_inputs": """<label>Name</label><input type="text" name="name" required>
<label>Village</label><input type="text" name="village" required>
<label>Skill Level</label><select name="skill_level"><option value="Master">Master</option><option value="Apprentice">Apprentice</option></select>
<label>Contact Number</label><input type="text" name="contact" required>
<label>Experience (Years)</label><input type="number" name="experience" required>
<label>Wage Details</label><input type="text" name="wage" placeholder="e.g. ₹800/day" required>"""
    },
    {
        "filename": "raw_material_module.html", "title": "Raw Material Management", "iter_var": "m", "data_var": "materials",
        "headers": ["ID", "Type", "Quantity (kg)", "Source", "Quality Grade", "Updated At"],
        "columns_html": "<td>#{{ m.material_id }}</td><td class='font-bold text-brand-gold'>{{ m.material_type }}</td><td class='text-blue-400 font-mono'>{{ m.quantity_kg }} kg</td><td>{{ m.source }}</td><td><span class='px-2 py-1 bg-brand-gold/10 text-brand-gold border border-brand-gold/30 rounded-full text-xs'>{{ m.quality_grade }}</span></td><td class='text-xs text-brand-lightgold/50'>{{ m.last_updated }}</td>",
        "form_action": "/api/crud/raw_material/add",
        "form_inputs": """<label>Material Type</label><input type="text" name="type" placeholder="Silk, Cotton, Dye..." required>
<label>Quantity (kg)</label><input type="number" step="0.01" name="quantity" required>
<label>Source</label><input type="text" name="source" required>
<label>Quality Grade</label><select name="grade"><option value="Premium">Premium</option><option value="Standard">Standard</option><option value="Economy">Economy</option></select>"""
    },
    {
        "filename": "supplier_module.html", "title": "Supplier Management", "iter_var": "s", "data_var": "suppliers",
        "headers": ["ID", "Supplier Name", "Material Supplied", "Cost/Unit (₹)", "Next Delivery Date"],
        "columns_html": "<td>#{{ s.supplier_id }}</td><td class='font-bold text-brand-gold'>{{ s.supplier_name }}</td><td>{{ s.material_supplied }}</td><td class='text-green-400 font-mono'>₹{{ s.cost_per_unit }}</td><td>{{ s.next_delivery_date }}</td>",
        "form_action": "/api/crud/supplier/add",
        "form_inputs": """<label>Supplier Name</label><input type="text" name="name" required>
<label>Material Supplied</label><input type="text" name="material" required>
<label>Cost per Unit (₹)</label><input type="number" step="0.01" name="cost" required>
<label>Next Delivery Date</label><input type="date" name="delivery_date" required>"""
    },
    {
        "filename": "product_catalog_module.html", "title": "Product Catalog Management", "iter_var": "p", "data_var": "products",
        "headers": ["ID", "Product Name", "Category", "Price (₹)", "Stock Qty"],
        "columns_html": "<td>#{{ p.product_id }}</td><td class='font-bold text-brand-gold'>{{ p.name }}</td><td>{{ p.category }}</td><td class='text-green-400 font-mono'>₹{{ p.price }}</td><td class='text-blue-400'>{{ p.stock_quantity }}</td>",
        "form_action": "/api/crud/product_catalog/add",
        "form_inputs": """<label>Product Name</label><input type="text" name="name" required>
<label>Category</label><input type="text" name="category" placeholder="Saree, Shawl, Carpet..." required>
<label>Price (₹)</label><input type="number" step="0.01" name="price" required>
<label>Stock Quantity</label><input type="number" name="stock" required>
<label>Description</label><textarea name="desc"></textarea>"""
    },
    {
        "filename": "customer_module.html", "title": "Customer Management", "iter_var": "c", "data_var": "customers",
        "headers": ["ID", "Name", "Email", "Phone", "Type", "Location", "Feedback"],
        "columns_html": "<td>#{{ c.customer_id }}</td><td class='font-bold text-brand-gold'>{{ c.name }}</td><td>{{ c.email }}</td><td>{{ c.phone }}</td><td><span class='px-2 py-1 bg-blue-900/40 text-blue-300 border border-blue-500/30 rounded-full text-[10px] uppercase font-bold tracking-wider'>{{ c.buyer_type }}</span></td><td>{{ c.location }}</td><td class='text-xs italic opacity-70 truncate max-w-[150px]'>{{ c.feedback }}</td>",
        "form_action": "/api/crud/customer/add",
        "form_inputs": """<label>Customer/Business Name</label><input type="text" name="name" required>
<label>Email</label><input type="email" name="email" required>
<label>Phone</label><input type="text" name="phone">
<label>Buyer Type</label><select name="buyer_type"><option value="Retail">Retail</option><option value="Wholesale">Wholesale</option><option value="Exporter">Exporter</option></select>
<label>Location</label><input type="text" name="location">
<label>Feedback/Notes</label><textarea name="feedback"></textarea>"""
    },
    {
        "filename": "order_module.html", "title": "Order Management", "iter_var": "o", "data_var": "orders",
        "headers": ["Order ID", "Customer", "Product", "Qty", "Total (₹)", "Status", "Delivery Date"],
        "columns_html": "<td>#{{ o.order_id }}</td><td class='font-bold text-brand-gold'>{{ o.customer_name }}</td><td>{{ o.product_name }}</td><td class='text-blue-400'>{{ o.quantity }}</td><td class='text-green-400 font-mono'>₹{{ o.total_price }}</td><td><span class='px-2 py-1 rounded-sm text-xs border border-brand-gold/30 bg-brand-gold/10 text-brand-gold'>{{ o.status }}</span></td><td>{{ o.delivery_date }}</td>",
        "form_action": "/api/crud/order/add",
        "form_inputs": """<label>Customer ID</label><input type="number" name="customer_id" required>
<label>Product ID</label><input type="number" name="product_id" required>
<label>Quantity</label><input type="number" name="quantity" required>
<label>Total Price (₹)</label><input type="number" step="0.01" name="total_price" required>
<label>Status</label><select name="status"><option value="Placed">Placed</option><option value="Processing">Processing</option><option value="Shipped">Shipped</option><option value="Delivered">Delivered</option></select>
<label>Delivery Date</label><input type="date" name="delivery_date">"""
    },
    {
        "filename": "inventory_module.html", "title": "Warehouse Inventory", "iter_var": "i", "data_var": "inventory",
        "headers": ["Inv ID", "Product", "Location", "Stock In", "Stock Out", "Damaged"],
        "columns_html": "<td>#{{ i.inventory_id }}</td><td class='font-bold text-brand-gold'>{{ i.product_name }}</td><td>{{ i.warehouse_location }}</td><td class='text-green-400'>+{{ i.stock_in }}</td><td class='text-yellow-500'>-{{ i.stock_out }}</td><td class='text-red-500'>{{ i.damaged_stock }}</td>",
        "form_action": "/api/crud/inventory/add",
        "form_inputs": """<label>Product ID</label><input type="number" name="product_id" required>
<label>Warehouse Location</label><input type="text" name="location" required>
<label>Stock In</label><input type="number" name="stock_in" value="0">
<label>Stock Out</label><input type="number" name="stock_out" value="0">
<label>Damaged Stock</label><input type="number" name="damaged" value="0">"""
    },
    {
        "filename": "billing_module.html", "title": "Payment & Billing", "iter_var": "b", "data_var": "payments",
        "headers": ["Payment ID", "Entity", "Amount (₹)", "Type", "Status", "Date"],
        "columns_html": "<td>#{{ b.payment_id }}</td><td class='font-bold text-brand-gold'>{{ b.entity_type }} (ID: {{ b.entity_id }})</td><td class='text-green-400 font-mono'>₹{{ b.amount }}</td><td><span class='px-2 py-1 bg-purple-900/40 text-purple-300 border border-purple-500/30 rounded-full text-[10px] uppercase font-bold tracking-wider'>{{ b.payment_type }}</span></td><td>{{ b.status }}</td><td class='text-xs text-brand-lightgold/50'>{{ b.payment_date }}</td>",
        "form_action": "/api/crud/billing/add",
        "form_inputs": """<label>Entity Type</label><select name="entity_type"><option value="Artisan">Artisan</option><option value="Supplier">Supplier</option><option value="Customer">Customer</option></select>
<label>Entity ID</label><input type="number" name="entity_id" required>
<label>Amount (₹)</label><input type="number" step="0.01" name="amount" required>
<label>Payment Type</label><select name="payment_type"><option value="Wage">Wage</option><option value="Invoice">Invoice</option><option value="Purchase">Purchase</option></select>
<label>Status</label><select name="status"><option value="Pending">Pending</option><option value="Completed">Completed</option><option value="Failed">Failed</option></select>"""
    },
    {
        "filename": "logistics_module.html", "title": "Logistics & Transport", "iter_var": "l", "data_var": "shipments",
        "headers": ["Shipment ID", "Order ID", "Agency", "Tracking #", "Status", "Est. Delivery"],
        "columns_html": "<td>#{{ l.shipment_id }}</td><td class='font-bold text-brand-gold'>#{{ l.order_id }}</td><td>{{ l.transport_agency }}</td><td class='font-mono'>{{ l.tracking_number }}</td><td><span class='px-2 py-1 rounded-sm text-xs border border-blue-500/30 bg-blue-900/20 text-blue-400'>{{ l.status }}</span></td><td>{{ l.estimated_delivery }}</td>",
        "form_action": "/api/crud/logistics/add",
        "form_inputs": """<label>Order ID</label><input type="number" name="order_id" required>
<label>Transport Agency</label><input type="text" name="agency" required>
<label>Tracking Number</label><input type="text" name="tracking" required>
<label>Status</label><select name="status"><option value="Dispatched">Dispatched</option><option value="In Transit">In Transit</option><option value="Delivered">Delivered</option><option value="Delayed">Delayed</option></select>
<label>Estimated Delivery</label><input type="date" name="delivery_date">"""
    }
]

for mod in modules_def:
    filename = mod.pop('filename'); html_content = get_module_html(**mod); mod['filename'] = filename
    filepath = os.path.join(template_dir, mod['filename'])
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated {mod['filename']}")

print("All 9 specific modules generated successfully.")
