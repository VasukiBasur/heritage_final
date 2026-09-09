import re

# 1. Fix admin_base_layout.html (Remove duplicated heading)
with open('d:\\dbmss\\templates\\admin_base_layout.html', 'r', encoding='utf-8') as f:
    layout = f.read()

layout = re.sub(
    r'<div class="flex justify-between items-end mb-8 border-b border-brand-gold/20 pb-4">\s*<div>\s*<h1 class="text-3xl font-serif text-brand-gold">{% block header_title %}Module{% endblock %}</h1>\s*</div>\s*</div>',
    '',
    layout
)
with open('d:\\dbmss\\templates\\admin_base_layout.html', 'w', encoding='utf-8') as f:
    f.write(layout)

# 2. Fix frontend_api.js (Remove broken client-side overwrites)
with open('d:\\dbmss\\static\\frontend_api.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Just comment out the inventory/raw_material block
js = js.replace("else if (path.includes('inventory_module') || path.includes('raw_material_module')) {",
                "else if (false) {")
# Comment out supplier block
js = js.replace("else if (path.includes('supplier_module')) {",
                "else if (false) {")

with open('d:\\dbmss\\static\\frontend_api.js', 'w', encoding='utf-8') as f:
    f.write(js)

# 3. Add Delete Routes to app.py
with open('d:\\dbmss\\app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

if "def delete_supplier" not in app_py:
    delete_routes = """
@app.route('/delete_supplier/<int:id>', methods=['POST'])
@login_required
def delete_supplier(id):
    if session.get('role') != 'Admin': return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM suppliers WHERE supplier_id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Supplier deleted successfully', 'success')
    return redirect(url_for('supplier_module'))

@app.route('/delete_raw_material/<int:id>', methods=['POST'])
@login_required
def delete_raw_material(id):
    if session.get('role') != 'Admin': return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM raw_materials WHERE material_id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Raw material deleted successfully', 'success')
    return redirect(url_for('raw_material_module'))
"""
    app_py = app_py.replace("def api_crud(module, action):", delete_routes + "\ndef api_crud(module, action):")
    with open('d:\\dbmss\\app.py', 'w', encoding='utf-8') as f:
        f.write(app_py)

# 4. Update raw_material_module.html
with open('d:\\dbmss\\templates\\raw_material_module.html', 'r', encoding='utf-8') as f:
    raw_html = f.read()

if "<th>Actions</th>" not in raw_html:
    raw_html = raw_html.replace(
        "<th>ID</th><th>Material Name</th><th>Quantity Available (kg)</th>",
        "<th>ID</th><th>Material Name</th><th>Quantity Available (kg)</th><th class='text-right'>Actions</th>"
    )
    raw_html = raw_html.replace(
        "<td>#{{ m.material_id }}</td><td class='font-bold text-brand-gold'>{{ m.material_name }}</td><td class='text-blue-400 font-mono'>{{ m.quantity_available }} kg</td>",
        """<td>#{{ m.material_id }}</td><td class='font-bold text-brand-gold'>{{ m.material_name }}</td><td class='text-blue-400 font-mono'>{{ m.quantity_available }} kg</td>
        <td class='text-right'>
            <a href='#' onclick='alert(\"Edit material page pending\")' class='text-brand-gold hover:text-yellow-400 mr-3'>Edit</a>
            <form action="{{ url_for('delete_raw_material', id=m.material_id) }}" method="POST" class="inline" onsubmit="return confirm('Delete this material?');">
                <button type="submit" class="text-red-500 hover:text-red-400">Delete</button>
            </form>
        </td>"""
    )
    raw_html = raw_html.replace(
        '<td colspan="3" class="text-center',
        '<td colspan="4" class="text-center'
    )
    modal_html = """
    <!-- CRUD Modal -->
    <div id="crud-modal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-[999] flex items-center justify-center">
        <div class="bg-[#1a1a1a] border border-brand-gold/40 rounded-lg shadow-[0_0_40px_rgba(212,175,55,0.2)] w-full max-w-lg p-8 relative">
            <button onclick="document.getElementById('crud-modal').classList.add('hidden')" class="absolute top-4 right-4 text-brand-gold/50 hover:text-brand-gold">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
            <h3 class="text-2xl font-serif text-brand-gold mb-6">Add New Material</h3>
            <form action="/api/crud/raw_material/add" method="POST" class="space-y-4">
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Material Name</label>
                <input type="text" name="name" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Quantity (kg)</label>
                <input type="number" name="quantity" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div class="pt-4"><button type="submit" class="w-full bg-brand-gold text-brand-black font-bold py-3 rounded hover:bg-yellow-500 transition-colors">Save Material</button></div>
            </form>
        </div>
    </div>
"""
    raw_html = raw_html.replace("{% endblock %}", modal_html + "\n{% endblock %}")
    with open('d:\\dbmss\\templates\\raw_material_module.html', 'w', encoding='utf-8') as f:
        f.write(raw_html)


# 5. Update supplier_module.html
with open('d:\\dbmss\\templates\\supplier_module.html', 'r', encoding='utf-8') as f:
    sup_html = f.read()

if "<th>Actions</th>" not in sup_html:
    sup_html = sup_html.replace(
        "<th>ID</th><th>Supplier Name</th><th>Material Supplied</th><th>Cost (₹)</th><th>Delivery Dates</th>",
        "<th>ID</th><th>Supplier Name</th><th>Material Supplied</th><th>Cost (₹)</th><th>Delivery Dates</th><th class='text-right'>Actions</th>"
    )
    sup_html = sup_html.replace(
        "<td>#{{ s.supplier_id }}</td><td class='font-bold text-brand-gold'>{{ s.supplier_name }}</td><td>{{ s.material_supplied }}</td><td class='text-green-400 font-mono'>₹{{ s.cost }}</td><td>{{ s.delivery_dates }}</td>",
        """<td>#{{ s.supplier_id }}</td><td class='font-bold text-brand-gold'>{{ s.supplier_name }}</td><td>{{ s.material_supplied }}</td><td class='text-green-400 font-mono'>₹{{ s.cost }}</td><td>{{ s.delivery_dates }}</td>
        <td class='text-right'>
            <a href='#' onclick='alert(\"Edit supplier page pending\")' class='text-brand-gold hover:text-yellow-400 mr-3'>Edit</a>
            <form action="{{ url_for('delete_supplier', id=s.supplier_id) }}" method="POST" class="inline" onsubmit="return confirm('Delete this supplier?');">
                <button type="submit" class="text-red-500 hover:text-red-400">Delete</button>
            </form>
        </td>"""
    )
    sup_html = sup_html.replace(
        '<td colspan="5" class="text-center',
        '<td colspan="6" class="text-center'
    )
    modal_html_sup = """
    <!-- CRUD Modal -->
    <div id="crud-modal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-[999] flex items-center justify-center">
        <div class="bg-[#1a1a1a] border border-brand-gold/40 rounded-lg shadow-[0_0_40px_rgba(212,175,55,0.2)] w-full max-w-lg p-8 relative">
            <button onclick="document.getElementById('crud-modal').classList.add('hidden')" class="absolute top-4 right-4 text-brand-gold/50 hover:text-brand-gold">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
            <h3 class="text-2xl font-serif text-brand-gold mb-6">Add New Supplier</h3>
            <form action="/api/crud/supplier/add" method="POST" class="space-y-4">
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Supplier Name</label>
                <input type="text" name="name" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Material Supplied</label>
                <input type="text" name="material" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Cost (₹)</label>
                <input type="number" step="0.01" name="cost" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Delivery Dates</label>
                <input type="text" name="delivery_date" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div class="pt-4"><button type="submit" class="w-full bg-brand-gold text-brand-black font-bold py-3 rounded hover:bg-yellow-500 transition-colors">Save Supplier</button></div>
            </form>
        </div>
    </div>
"""
    sup_html = sup_html.replace("{% endblock %}", modal_html_sup + "\n{% endblock %}")
    with open('d:\\dbmss\\templates\\supplier_module.html', 'w', encoding='utf-8') as f:
        f.write(sup_html)

print("Modules Layout and CRUD Fixed!")
