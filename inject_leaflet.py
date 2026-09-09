import os
import re

app_file = r"d:\dbmss\templates\dashboard.html"

with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Leaflet CSS and JS to the head
leaflet_head = """    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    <style>
        /* Custom Map Styles */
        .leaflet-popup-content-wrapper { background: rgba(26, 26, 26, 0.95); color: #d4af37; border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 4px; }
        .leaflet-popup-tip { background: rgba(26, 26, 26, 0.95); border: 1px solid rgba(212, 175, 55, 0.3); }
        .glowing-path { animation: dash 20s linear infinite; stroke-dasharray: 10; stroke-width: 3; filter: drop-shadow(0 0 4px red); }
        @keyframes dash { to { stroke-dashoffset: -100; } }
        .map-node { background: #d4af37; border: 2px solid #121212; border-radius: 50%; box-shadow: 0 0 10px #d4af37; }
        .map-node.hub { background: #ff0000; box-shadow: 0 0 15px #ff0000; }
    </style>
</head>"""

content = content.replace("</head>", leaflet_head)


# 2. Replace the old iframe with the new Leaflet container and logic
old_map_pattern = r'<div class="relative w-full h-80 rounded overflow-hidden border border-brand-gold/20 shadow-inner">.*?</div>'

new_map_container = """<div class="relative w-full h-96 rounded overflow-hidden border border-brand-gold/20 shadow-inner z-10" id="supplyChainMap"></div>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        // Initialize Map
        const map = L.map('supplyChainMap', {
            center: [14.0, 75.5], // Center of Karnataka
            zoom: 7,
            zoomControl: false
        });
        
        // Dark Theme Map Tiles
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://carto.com/">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(map);

        // Define Custom Icons
        const createIcon = (isHub) => L.divIcon({
            className: isHub ? 'map-node hub' : 'map-node',
            iconSize: [12, 12],
            iconAnchor: [6, 6]
        });

        // Geographic Nodes (Cities/Districts)
        const nodes = {
            supplier: { coords: [12.2958, 76.6394], name: "Mysore District", role: "Raw Material Supplier (Silk)" },
            artisan1: { coords: [15.9620, 76.1130], name: "Ilkal District", role: "Master Weavers (Saree)" },
            artisan2: { coords: [13.3409, 74.7421], name: "Udupi District", role: "Artisan Hub" },
            hub:      { coords: [13.9299, 75.5681], name: "Shivamogga", role: "Central Storage & Company Hub" },
            buyer:    { coords: [12.9716, 77.5946], name: "Bengaluru City", role: "Global Export & Retail" }
        };

        // Add Markers and Popups
        for (const key in nodes) {
            const node = nodes[key];
            const marker = L.marker(node.coords, {icon: createIcon(key === 'hub' || key === 'buyer')}).addTo(map);
            marker.bindPopup(`<b>${node.name}</b><br><span style="color:#f0e6d2; font-size:10px">${node.role}</span>`);
            // Keep Hub popup open
            if(key === 'hub') marker.openPopup();
        }

        // Draw Glowing Red Routes
        const routes = [
            [nodes.supplier.coords, nodes.artisan1.coords], // Supplier to Weaver
            [nodes.supplier.coords, nodes.artisan2.coords], // Supplier to Weaver
            [nodes.artisan1.coords, nodes.hub.coords],      // Weaver to Company Hub
            [nodes.artisan2.coords, nodes.hub.coords],      // Weaver to Company Hub
            [nodes.hub.coords, nodes.buyer.coords]          // Hub to Export
        ];

        routes.forEach(route => {
            L.polyline(route, {
                color: '#ff3333',
                weight: 3,
                opacity: 0.8,
                className: 'glowing-path'
            }).addTo(map);
        });
        
        // Fit bounds to show all markers
        const bounds = L.latLngBounds([nodes.supplier.coords, nodes.artisan1.coords, nodes.artisan2.coords, nodes.hub.coords, nodes.buyer.coords]);
        map.fitBounds(bounds, {padding: [50, 50]});
    });
</script>"""

# Find the div containing the iframe and replace it
content = re.sub(old_map_pattern, new_map_container, content, flags=re.DOTALL)

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Leaflet map injected successfully!")
