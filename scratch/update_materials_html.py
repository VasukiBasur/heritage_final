import re

with open('d:\\dbmss\\templates\\materials.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Title Header with Add New button
old_header = """        <div class="flex justify-between items-center mb-10 border-b border-brand-gold/20 pb-4">
            <h2 class="text-3xl font-serif font-bold text-brand-gold">Raw Materials Inventory</h2>
        </div>"""

new_header = """        <div class="flex justify-between items-center mb-10 border-b border-brand-gold/20 pb-4">
            <h2 class="text-3xl font-serif font-bold text-brand-gold">Raw Materials Inventory</h2>
            <button onclick="document.getElementById('crud-modal').classList.remove('hidden')" class="bg-brand-gold text-brand-black px-4 py-2 rounded text-sm font-bold hover:bg-yellow-500 transition-colors shadow-lg shadow-brand-gold/20">+ Add New</button>
        </div>"""

html = html.replace(old_header, new_header)

# 2. Add Material ID and Action buttons to card
old_card_content = """                    <div>
                        <h3 class="text-xl font-serif font-semibold text-brand-gold mb-4">{{ material.material_name }}</h3>
                        <div class="flex items-center justify-between">
                            <span class="text-sm text-gray-400">Current Stock:</span>
                            <span class="text-xl font-bold text-brand-lightgold">{{ material.quantity_available }} units</span>
                        </div>
                    </div>"""

new_card_content = """                    <div>
                        <h3 class="text-xl font-serif font-semibold text-brand-gold mb-4">{{ material.material_name }} <span class="text-[10px] text-brand-lightgold/50 align-top ml-2 font-mono bg-brand-gold/10 px-1.5 py-0.5 rounded border border-brand-gold/20 tracking-wider">#MAT-{{ material.material_id }}</span></h3>
                        <div class="flex items-center justify-between mb-4">
                            <span class="text-sm text-gray-400">Current Stock:</span>
                            <span class="text-xl font-bold text-brand-lightgold">{{ material.quantity_available }} units</span>
                        </div>
                    </div>
                    <div class="mt-auto pt-4 border-t border-brand-gold/10 flex justify-end space-x-4">
                        <a href="{{ url_for('edit_raw_material', id=material.material_id) }}" class="text-sm font-semibold text-brand-gold hover:text-yellow-400 transition-colors">Edit</a>
                        <form action="{{ url_for('delete_raw_material', id=material.material_id) }}" method="POST" class="inline" onsubmit="return confirm('Are you sure you want to delete this material?');">
                            <button type="submit" class="text-sm font-semibold text-red-500 hover:text-red-400 transition-colors">Delete</button>
                        </form>
                    </div>"""

html = html.replace(old_card_content, new_card_content)

# 3. Add CRUD Modal at the end of <main>
modal_html = """    <!-- CRUD Modal -->
    <div id="crud-modal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-[999] flex items-center justify-center">
        <div class="bg-[#1a1a1a] border border-brand-gold/40 rounded-lg shadow-[0_0_40px_rgba(212,175,55,0.2)] w-full max-w-lg p-8 relative">
            <button onclick="document.getElementById('crud-modal').classList.add('hidden')" class="absolute top-4 right-4 text-brand-gold/50 hover:text-brand-gold">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
            <h3 class="text-2xl font-serif text-brand-gold mb-6">Add New Material</h3>
            <form action="/api/crud/raw_material/add" method="POST" class="space-y-4">
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Material ID (Optional)</label>
                <input type="number" name="material_id" placeholder="Auto-generated if left blank" class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none mb-2"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Material Name</label>
                <input type="text" name="name" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Quantity (kg)</label>
                <input type="number" name="quantity" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                <div class="pt-4"><button type="submit" class="w-full bg-brand-gold text-brand-black font-bold py-3 rounded hover:bg-yellow-500 transition-colors">Save Material</button></div>
            </form>
        </div>
    </div>"""

# Insert just before <!-- Footer -->
html = html.replace("    <!-- Footer -->", modal_html + "\n    <!-- Footer -->")

with open('d:\\dbmss\\templates\\materials.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("materials.html updated.")
