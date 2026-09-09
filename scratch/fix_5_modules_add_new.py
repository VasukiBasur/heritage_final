import os

templates = {
    'order_module.html': """
    <!-- CRUD Modal -->
    <div id="crud-modal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-[999] flex items-center justify-center">
        <div class="bg-[#1a1a1a] border border-brand-gold/40 rounded-lg shadow-[0_0_40px_rgba(212,175,55,0.2)] w-full max-w-lg p-8 relative">
            <button onclick="document.getElementById('crud-modal').classList.add('hidden')" class="absolute top-4 right-4 text-brand-gold/50 hover:text-brand-gold">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
            <h3 class="text-2xl font-serif text-brand-gold mb-6">Add New Order</h3>
            <form action="/api/crud/order/add" method="POST" class="space-y-4">
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Customer ID</label>
                <input type="number" name="customer_id" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Product ID</label>
                <input type="number" name="product_id" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Quantity</label>
                <input type="number" name="quantity" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Total Price (₹)</label>
                <input type="number" step="0.01" name="total_price" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Delivery Date</label>
                <input type="date" name="delivery_date" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div class="pt-4"><button type="submit" class="w-full bg-brand-gold text-brand-black font-bold py-3 rounded hover:bg-yellow-500 transition-colors">Save Order</button></div>
            </form>
        </div>
    </div>
""",
    'customer_module.html': """
    <!-- CRUD Modal -->
    <div id="crud-modal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-[999] flex items-center justify-center">
        <div class="bg-[#1a1a1a] border border-brand-gold/40 rounded-lg shadow-[0_0_40px_rgba(212,175,55,0.2)] w-full max-w-lg p-8 relative">
            <button onclick="document.getElementById('crud-modal').classList.add('hidden')" class="absolute top-4 right-4 text-brand-gold/50 hover:text-brand-gold">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
            <h3 class="text-2xl font-serif text-brand-gold mb-6">Add New Customer</h3>
            <form action="/api/crud/customer/add" method="POST" class="space-y-4">
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Customer Name</label>
                <input type="text" name="name" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Email</label>
                <input type="email" name="email" class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Phone</label>
                <input type="text" name="phone" class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Buyer Type</label>
                <select name="buyer_type" class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none">
                    <option value="Retail">Retail</option><option value="Wholesale">Wholesale</option><option value="Exporter">Exporter</option>
                </select></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Location</label>
                <input type="text" name="location" class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div class="pt-4"><button type="submit" class="w-full bg-brand-gold text-brand-black font-bold py-3 rounded hover:bg-yellow-500 transition-colors">Save Customer</button></div>
            </form>
        </div>
    </div>
""",
    'inventory_module.html': """
    <!-- CRUD Modal -->
    <div id="crud-modal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-[999] flex items-center justify-center">
        <div class="bg-[#1a1a1a] border border-brand-gold/40 rounded-lg shadow-[0_0_40px_rgba(212,175,55,0.2)] w-full max-w-lg p-8 relative">
            <button onclick="document.getElementById('crud-modal').classList.add('hidden')" class="absolute top-4 right-4 text-brand-gold/50 hover:text-brand-gold">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
            <h3 class="text-2xl font-serif text-brand-gold mb-6">Add New Inventory Record</h3>
            <form action="/api/crud/inventory/add" method="POST" class="space-y-4">
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Product ID</label>
                <input type="number" name="product_id" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Warehouse Location</label>
                <input type="text" name="warehouse_location" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Stock In</label>
                <input type="number" name="stock_in" required value="0" class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div class="pt-4"><button type="submit" class="w-full bg-brand-gold text-brand-black font-bold py-3 rounded hover:bg-yellow-500 transition-colors">Save Inventory</button></div>
            </form>
        </div>
    </div>
""",
    'billing_module.html': """
    <!-- CRUD Modal -->
    <div id="crud-modal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-[999] flex items-center justify-center">
        <div class="bg-[#1a1a1a] border border-brand-gold/40 rounded-lg shadow-[0_0_40px_rgba(212,175,55,0.2)] w-full max-w-lg p-8 relative">
            <button onclick="document.getElementById('crud-modal').classList.add('hidden')" class="absolute top-4 right-4 text-brand-gold/50 hover:text-brand-gold">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
            <h3 class="text-2xl font-serif text-brand-gold mb-6">Add New Billing/Payment</h3>
            <form action="/api/crud/billing/add" method="POST" class="space-y-4">
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Entity Type</label>
                <select name="entity_type" class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none">
                    <option value="Artisan">Artisan</option><option value="Supplier">Supplier</option><option value="Customer">Customer</option>
                </select></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Entity ID</label>
                <input type="number" name="entity_id" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Amount (₹)</label>
                <input type="number" step="0.01" name="amount" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Payment Type</label>
                <select name="payment_type" class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none">
                    <option value="Wage">Wage</option><option value="Invoice">Invoice</option><option value="Purchase">Purchase</option>
                </select></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Status</label>
                <select name="status" class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none">
                    <option value="Completed">Completed</option><option value="Pending">Pending</option>
                </select></div>
                <div class="pt-4"><button type="submit" class="w-full bg-brand-gold text-brand-black font-bold py-3 rounded hover:bg-yellow-500 transition-colors">Save Payment</button></div>
            </form>
        </div>
    </div>
""",
    'logistics_module.html': """
    <!-- CRUD Modal -->
    <div id="crud-modal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-[999] flex items-center justify-center">
        <div class="bg-[#1a1a1a] border border-brand-gold/40 rounded-lg shadow-[0_0_40px_rgba(212,175,55,0.2)] w-full max-w-lg p-8 relative">
            <button onclick="document.getElementById('crud-modal').classList.add('hidden')" class="absolute top-4 right-4 text-brand-gold/50 hover:text-brand-gold">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
            <h3 class="text-2xl font-serif text-brand-gold mb-6">Add New Shipment</h3>
            <form action="/api/crud/logistics/add" method="POST" class="space-y-4">
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Order ID</label>
                <input type="number" name="order_id" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Transport Agency</label>
                <input type="text" name="transport_agency" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Tracking Number</label>
                <input type="text" name="tracking_number" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Estimated Delivery</label>
                <input type="date" name="estimated_delivery" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div class="pt-4"><button type="submit" class="w-full bg-brand-gold text-brand-black font-bold py-3 rounded hover:bg-yellow-500 transition-colors">Save Shipment</button></div>
            </form>
        </div>
    </div>
"""
}

# 1. Update the HTML files by appending the modal before {% endblock %} for content
for tpl_name, modal_code in templates.items():
    path = os.path.join('d:\\dbmss\\templates', tpl_name)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Make sure we don't duplicate it
        if '<div id="crud-modal"' not in content:
            # Replace the first instance of {% endblock %} which closes the content block
            content = content.replace("{% endblock %}", modal_code + "\n{% endblock %}", 1)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added modal to {tpl_name}")

# 2. Update app.py api_crud
with open('d:\\dbmss\\app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

# We need to insert the logic for the 5 modules before the else: statement of api_crud
# Let's find "elif module == 'product_catalog' and action == 'add':" and the block after it
target_string = """        elif module == 'product_catalog' and action == 'add':
            cursor.execute('''INSERT INTO product_catalog (product_name, category, price, stock_quantity, artisan_id, material_id) 
                              VALUES (%s, %s, %s, %s, %s, %s)''',
                           (data.get('name'), data.get('category'), data.get('price'), data.get('stock'), data.get('artisan_id'), data.get('material_id')))"""

new_backend_logic = target_string + """
                           
        elif module == 'order' and action == 'add':
            cursor.execute('''INSERT INTO orders (customer_id, product_id, quantity, total_price, delivery_date) 
                              VALUES (%s, %s, %s, %s, %s)''',
                           (data.get('customer_id'), data.get('product_id'), data.get('quantity'), data.get('total_price'), data.get('delivery_date')))

        elif module == 'customer' and action == 'add':
            cursor.execute('''INSERT INTO customers (name, email, phone, buyer_type, location) 
                              VALUES (%s, %s, %s, %s, %s)''',
                           (data.get('name'), data.get('email'), data.get('phone'), data.get('buyer_type'), data.get('location')))

        elif module == 'inventory' and action == 'add':
            cursor.execute('''INSERT INTO warehouse_inventory (product_id, warehouse_location, stock_in) 
                              VALUES (%s, %s, %s)''',
                           (data.get('product_id'), data.get('warehouse_location'), data.get('stock_in')))

        elif module == 'billing' and action == 'add':
            cursor.execute('''INSERT INTO billing_payments (entity_type, entity_id, amount, payment_type, status) 
                              VALUES (%s, %s, %s, %s, %s)''',
                           (data.get('entity_type'), data.get('entity_id'), data.get('amount'), data.get('payment_type'), data.get('status')))

        elif module == 'logistics' and action == 'add':
            cursor.execute('''INSERT INTO logistics (order_id, transport_agency, tracking_number, estimated_delivery) 
                              VALUES (%s, %s, %s, %s)''',
                           (data.get('order_id'), data.get('transport_agency'), data.get('tracking_number'), data.get('estimated_delivery')))
"""

if target_string in app_py and "elif module == 'order' and action == 'add':" not in app_py:
    app_py = app_py.replace(target_string, new_backend_logic)
    with open('d:\\dbmss\\app.py', 'w', encoding='utf-8') as f:
        f.write(app_py)
    print("Updated app.py with all 5 new modules logic.")
else:
    print("app.py update skipped (already present or string mismatch).")
