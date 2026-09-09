import re

with open('templates/supplier_active.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove the openMapModal button
btn_regex = r'<button onclick="openMapModal\(\)".*?</button>'
text = re.sub(btn_regex, '', text, flags=re.DOTALL)

# 2. Extract the Map UI and put it where the modal button was (or just below the header)
map_ui = """
<!-- Inline Live Map -->
<div class="bg-[#141414] border border-[#d4af37]/30 rounded-xl w-full shadow-[0_0_20px_rgba(212,175,55,0.1)] mb-8 overflow-hidden relative">
    <div class="p-4 border-b border-[#d4af37]/20 flex justify-between items-center bg-gradient-to-r from-[#1a1a1a] to-black">
        <h3 class="text-xl font-serif text-[#f5ebd7] drop-shadow-md">Active Transits - Live Map</h3>
    </div>
    <div class="h-[500px] w-full relative z-0">
        <!-- Leaflet Map Container -->
        <div id="delivery-map" class="w-full h-full"></div>
        
        <!-- Map Overlay UI (Tracking Legend) -->
        <div class="absolute bottom-6 left-6 z-[1000] bg-[#1a1a1a]/90 backdrop-blur border border-[#d4af37]/30 p-4 rounded-lg shadow-2xl pointer-events-none">
            <h4 class="text-xs font-bold text-[#d4af37] uppercase tracking-widest mb-3">Live Fleet Status</h4>
            <div class="space-y-2">
                <div class="flex items-center text-xs text-white">
                    <div class="w-3 h-3 rounded-full bg-blue-500 mr-2 shadow-[0_0_8px_rgba(59,130,246,0.8)]"></div>
                    In Transit
                </div>
                <div class="flex items-center text-xs text-white">
                    <div class="w-3 h-3 rounded-full bg-[#d4af37] mr-2 shadow-[0_0_8px_rgba(212,175,55,0.8)]"></div>
                    Out for Delivery
                </div>
                <div class="flex items-center text-xs text-white">
                    <div class="w-3 h-3 rounded-full bg-red-500 mr-2 shadow-[0_0_8px_rgba(239,68,68,0.8)] animate-pulse"></div>
                    Delayed / Issue
                </div>
            </div>
        </div>
    </div>
</div>
"""

# Insert map_ui right after the header block
text = text.replace('<!-- End Header -->', '<!-- End Header -->\n' + map_ui)
# Wait, "<!-- End Header -->" might not exist. Let's insert it before <!-- Search and Filter -->
# Wait, let's see where to insert.
header_marker = '<div class="mb-8 flex justify-between items-end">'
# Wait, the structure is usually:
# <div class="mb-8 flex justify-between items-end">
#   <div>...</div>
#   <div class="flex space-x-4">...</div>
# </div>
# I'll insert the map right after this closing div.
# Instead of complex regex, let's just insert before the first Grid or Table.
text = text.replace('<!-- Grid of Active Shipments -->', map_ui + '\n<!-- Grid of Active Shipments -->')

# 3. Change initMap to run on load
js_mod = """
    document.addEventListener('DOMContentLoaded', () => {
        initMap();
    });
"""
text = text.replace('function openMapModal()', js_mod + '\n    function openMapModal()')

# 4. Remove the old Map Modal entirely
modal_regex = r'<!-- Live Map Modal -->.*</div>\n</div>'
text = re.sub(modal_regex, '', text, flags=re.DOTALL)

with open('templates/supplier_active.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Made map inline in supplier_active.html')
