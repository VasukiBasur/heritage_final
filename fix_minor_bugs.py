import os
import re

template_dir = r"d:\dbmss\templates"
app_file = r"d:\dbmss\app.py"

# --- 1. Fix artisans.html search ---
artisans_file = os.path.join(template_dir, "artisans.html")
with open(artisans_file, "r", encoding="utf-8") as f:
    artisans_content = f.read()

search_script = """
    <!-- Search Script -->
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const searchInput = document.getElementById("searchArtisans");
            const filterSelect = document.getElementById("filterSkill");
            const cards = document.querySelectorAll(".glass-card");

            function filterCards() {
                const query = searchInput.value.toLowerCase();
                const skill = filterSelect ? filterSelect.value : "All";
                
                cards.forEach(card => {
                    // Only filter artisan cards, not the "Total Artisans" summary cards
                    if(!card.querySelector("h3")) return;
                    
                    const name = card.querySelector("h3").innerText.toLowerCase();
                    const location = card.innerText.toLowerCase();
                    const cardSkillElement = card.querySelector(".text-[10px]");
                    const cardSkill = cardSkillElement ? cardSkillElement.innerText : "";
                    
                    const matchesSearch = name.includes(query) || location.includes(query);
                    const matchesSkill = (skill === "All") || cardSkill.includes(skill.toUpperCase());
                    
                    if (matchesSearch && matchesSkill) {
                        card.parentElement.style.display = "block";
                    } else {
                        card.parentElement.style.display = "none";
                    }
                });
            }

            if(searchInput) searchInput.addEventListener("input", filterCards);
            if(filterSelect) filterSelect.addEventListener("change", filterCards);
        });
    </script>
</body>
"""
if "filterCards()" not in artisans_content:
    artisans_content = artisans_content.replace("</body>", search_script)
    with open(artisans_file, "w", encoding="utf-8") as f:
        f.write(artisans_content)


# --- 2. Fix order_module.html and app.py ---
with open(app_file, "r", encoding="utf-8") as f:
    app_content = f.read()

# Update order_module route in app.py to fetch customers and products
old_route = """@app.route('/order_module')
@login_required
def order_module():
    if session.get('role') != 'Admin': return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''SELECT o.*, c.name as customer_name, p.product_name as product_name 
                      FROM orders o 
                      LEFT JOIN customers c ON o.customer_id = c.customer_id 
                      LEFT JOIN product_catalog p ON o.product_id = p.product_id''')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('order_module.html', orders=data)"""

new_route = """@app.route('/order_module')
@login_required
def order_module():
    if session.get('role') != 'Admin': return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''SELECT o.*, c.name as customer_name, p.product_name as product_name 
                      FROM orders o 
                      LEFT JOIN customers c ON o.customer_id = c.customer_id 
                      LEFT JOIN product_catalog p ON o.product_id = p.product_id''')
    data = cursor.fetchall()
    
    cursor.execute("SELECT customer_id, name FROM customers")
    customers = cursor.fetchall()
    
    cursor.execute("SELECT product_id, product_name FROM product_catalog")
    products = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('order_module.html', orders=data, customers=customers, products=products)"""

app_content = app_content.replace(old_route, new_route)

with open(app_file, "w", encoding="utf-8") as f:
    f.write(app_content)

# Update order_module.html to use dropdowns
order_file = os.path.join(template_dir, "order_module.html")
with open(order_file, "r", encoding="utf-8") as f:
    order_content = f.read()

old_inputs = """<label>Customer ID</label><input type="number" name="customer_id" required>
<label>Product ID</label><input type="number" name="product_id" required>"""

new_inputs = """<label>Customer</label>
<select name="customer_id" required>
    {% for c in customers %}
    <option value="{{ c.customer_id }}">{{ c.name }}</option>
    {% endfor %}
</select>
<label>Product</label>
<select name="product_id" required>
    {% for p in products %}
    <option value="{{ p.product_id }}">{{ p.product_name }}</option>
    {% endfor %}
</select>"""

if old_inputs in order_content:
    order_content = order_content.replace(old_inputs, new_inputs)
    with open(order_file, "w", encoding="utf-8") as f:
        f.write(order_content)

print("Fixes applied.")
