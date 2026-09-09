import re

# 1. Update product_catalog_module.html
with open('d:\\dbmss\\templates\\product_catalog_module.html', 'r', encoding='utf-8') as f:
    catalog_html = f.read()

modal_html = """
    <!-- CRUD Modal -->
    <div id="crud-modal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-[999] flex items-center justify-center">
        <div class="bg-[#1a1a1a] border border-brand-gold/40 rounded-lg shadow-[0_0_40px_rgba(212,175,55,0.2)] w-full max-w-lg p-8 relative max-h-[90vh] overflow-y-auto">
            <button onclick="document.getElementById('crud-modal').classList.add('hidden')" class="absolute top-4 right-4 text-brand-gold/50 hover:text-brand-gold">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
            <h3 class="text-2xl font-serif text-brand-gold mb-6">Add New Product</h3>
            <form action="/api/crud/product_catalog/add" method="POST" class="space-y-4">
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Product Name</label>
                <input type="text" name="name" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                
                <div><label class="block text-xs text-brand-lightgold/70 mb-1">Category</label>
                <input type="text" name="category" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                
                <div class="grid grid-cols-2 gap-4">
                    <div><label class="block text-xs text-brand-lightgold/70 mb-1">Price (₹)</label>
                    <input type="number" step="0.01" name="price" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                    <div><label class="block text-xs text-brand-lightgold/70 mb-1">Stock Quantity</label>
                    <input type="number" name="stock" required class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                </div>
                
                <div class="grid grid-cols-2 gap-4">
                    <div><label class="block text-xs text-brand-lightgold/70 mb-1">Artisan ID (Optional)</label>
                    <input type="number" name="artisan_id" class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                    <div><label class="block text-xs text-brand-lightgold/70 mb-1">Material ID (Optional)</label>
                    <input type="number" name="material_id" class="w-full bg-[#121212] border border-brand-gold/30 rounded p-2 text-brand-lightgold focus:border-brand-gold focus:outline-none"></div>
                </div>
                
                <div class="pt-4"><button type="submit" class="w-full bg-brand-gold text-brand-black font-bold py-3 rounded hover:bg-yellow-500 transition-colors">Save Product</button></div>
            </form>
        </div>
    </div>
"""

if 'id="crud-modal"' not in catalog_html:
    catalog_html = catalog_html.replace('{% endblock %}', modal_html + '\n{% endblock %}')
    with open('d:\\dbmss\\templates\\product_catalog_module.html', 'w', encoding='utf-8') as f:
        f.write(catalog_html)


# 2. Update trace.html
with open('d:\\dbmss\\templates\\trace.html', 'r', encoding='utf-8') as f:
    trace_html = f.read()

new_timeline_items = """
                <!-- Timeline Item 4 -->
                <div class="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                    <div class="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-brand-gold text-brand-black shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    </div>
                    <div class="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded bg-brand-black border border-brand-gold/20 shadow">
                        <div class="flex items-center justify-between space-x-2 mb-1">
                            <div class="font-bold text-brand-gold text-sm">Quality Assurance</div>
                        </div>
                        <div class="text-brand-lightgold font-serif text-lg">Govt. Handloom Mark</div>
                        <div class="text-xs opacity-60">Verified Authentic Handwoven Product</div>
                    </div>
                </div>

                <!-- Timeline Item 5 -->
                <div class="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                    <div class="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-brand-gold text-brand-black shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                    </div>
                    <div class="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded bg-brand-black border border-brand-gold/20 shadow">
                        <div class="flex items-center justify-between space-x-2 mb-1">
                            <div class="font-bold text-brand-gold text-sm">Fair Trade Status</div>
                        </div>
                        <div class="text-brand-lightgold font-serif text-lg">Ethically Sourced</div>
                        <div class="text-xs opacity-60">100% Payout Distributed to Artisan</div>
                    </div>
                </div>
"""

# Insert right before the closing div of the space-y-6 container
if '<!-- Timeline Item 4 -->' not in trace_html:
    trace_html = trace_html.replace(
        '            </div>\n            \n            <div class="mt-8 text-center">',
        new_timeline_items + '            </div>\n            \n            <div class="mt-8 text-center">'
    )
    with open('d:\\dbmss\\templates\\trace.html', 'w', encoding='utf-8') as f:
        f.write(trace_html)

print("Product catalog and Traceability fixed.")
