import os
import re

template_dir = r"d:\dbmss\templates"

modules_dropdown = """
                {% if session.get('role') == 'Admin' %}
                <div class="relative group">
                    <button class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors flex items-center">
                        Modules <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </button>
                    <div class="absolute left-0 mt-2 w-48 bg-brand-dark border border-brand-gold/30 rounded-sm shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50">
                        <a href="{{ url_for('weaver_module') }}" class="block px-4 py-2 text-sm text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">Weaver Mgmt</a>
                        <a href="{{ url_for('raw_material_module') }}" class="block px-4 py-2 text-sm text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">Raw Materials</a>
                        <a href="{{ url_for('supplier_module') }}" class="block px-4 py-2 text-sm text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">Suppliers</a>
                        <a href="{{ url_for('production_module') }}" class="block px-4 py-2 text-sm text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">Production</a>
                        <a href="{{ url_for('product_catalog_module') }}" class="block px-4 py-2 text-sm text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">Product Catalog</a>
                    </div>
                </div>
                {% endif %}
                {% if session.get('role') == 'Artisan' %}
"""

for root, dirs, files in os.walk(template_dir):
    for f in files:
        if f.endswith('.html') and 'module' not in f:
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Replace the old Artisan condition with the new Modules + Artisan condition
            if "Modules <svg" not in content and "{% if session.get('role') == 'Artisan' %}" in content:
                new_content = content.replace(
                    "{% if session.get('role') == 'Artisan' %}",
                    modules_dropdown
                )
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Updated navbar in {f}")

print("Navigation update complete.")
