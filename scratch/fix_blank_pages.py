import os

# 1. Wire Artisan links in base_layout.html
layout_path = r'd:\dbmss\templates\base_layout.html'
with open(layout_path, 'r', encoding='utf-8') as f:
    layout = f.read()

replacements = {
    "url_for('artisan_products')": "url_for('product_catalog_module')",
    "url_for('artisan_upload_product')": "url_for('product_catalog_module')",
    "url_for('artisan_production')": "url_for('production_module')",
    "url_for('artisan_orders')": "url_for('order_module')",
    "url_for('artisan_earnings')": "url_for('billing_module')",
    "url_for('artisan_qr_verification')": "url_for('trace')",
    "url_for('artisan_profile')": "url_for('weaver_module')"
}

for old, new in replacements.items():
    layout = layout.replace(old, new)

with open(layout_path, 'w', encoding='utf-8') as f:
    f.write(layout)
print("Updated base_layout.html with real routes.")


# 2. Add Leaflet JS to artisan_dashboard.html
artisan_path = r'd:\dbmss\templates\artisan_dashboard.html'
with open(artisan_path, 'r', encoding='utf-8') as f:
    artisan_content = f.read()

if 'unpkg.com/leaflet' not in artisan_content:
    leaflet_script = """
    <!-- Leaflet JS for Map -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var mapContainer = document.getElementById('artisan-map');
            if(mapContainer) {
                var map = L.map('artisan-map', {
                    zoomControl: false,
                    attributionControl: false
                }).setView([13.9299, 75.5681], 6); // Shivamogga coordinates
                
                L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                    maxZoom: 19
                }).addTo(map);

                // Add a pulse marker for Artisan Location
                var circle = L.circleMarker([13.9299, 75.5681], {
                    color: '#D4AF37',
                    fillColor: '#D4AF37',
                    fillOpacity: 0.5,
                    radius: 8
                }).addTo(map);
                circle.bindPopup('<div class="custom-map-popup"><b>Shivamogga Workshop</b><br>Active Looms: 87</div>');
            }
        });
    </script>
"""
    # Insert right after {% block extra_scripts %}
    extra_start = artisan_content.find('{% block extra_scripts %}')
    if extra_start != -1:
        insert_pos = extra_start + len('{% block extra_scripts %}')
        artisan_content = artisan_content[:insert_pos] + leaflet_script + artisan_content[insert_pos:]
        
        with open(artisan_path, 'w', encoding='utf-8') as f:
            f.write(artisan_content)
        print("Injected Leaflet JS into artisan_dashboard.html.")
    else:
        print("Could not find extra_scripts block.")
