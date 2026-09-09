import re

path = r'd:\dbmss\templates\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Map Section
old_map_start = "<!-- Geographic Distribution -->"
old_map_end = "<!-- Charts & Graphs Section -->"
start_idx = content.find(old_map_start)
end_idx = content.find(old_map_end)

new_map_html = """<!-- Geographic Distribution -->
<div class="glass-card p-6 mt-8 shadow-lg border border-brand-gold/20 mb-8 bg-[#1a1a1a]">
    <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-serif text-brand-gold flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path></svg>
            Global Supply Chain & Logistics Network
        </h2>
        <div class="flex space-x-3 text-xs font-bold bg-[#121212] p-2 rounded border border-white/5">
            <div class="flex items-center"><span class="w-3 h-3 rounded-full bg-red-500 mr-1 shadow-[0_0_5px_rgba(239,68,68,0.8)]"></span> Artisans</div>
            <div class="flex items-center"><span class="w-3 h-3 rounded-full bg-blue-500 mr-1 shadow-[0_0_5px_rgba(59,130,246,0.8)]"></span> Suppliers</div>
            <div class="flex items-center"><span class="w-3 h-3 rounded-full bg-yellow-500 mr-1 shadow-[0_0_5px_rgba(234,179,8,0.8)]"></span> Warehouses</div>
            <div class="flex items-center"><span class="w-3 h-3 rounded-full bg-green-500 mr-1 shadow-[0_0_5px_rgba(34,197,94,0.8)]"></span> Customers</div>
        </div>
    </div>
    <div id="supplyChainMap" class="w-full h-[500px] rounded bg-[#121212] z-10 border border-brand-gold/10"></div>
</div>
"""
content = content[:start_idx] + new_map_html + content[end_idx:]

# 2. Update Map Javascript
old_js_map_start = "// 1. Initialize Map"
old_js_map_end = "// 2. Initialize Analytics Charts"
start_idx = content.find(old_js_map_start)
end_idx = content.find(old_js_map_end)

new_js_map = """// 1. Initialize Advanced ERP Map (Leaflet)
        const map = L.map('supplyChainMap', { zoomControl: false }).setView([20.5, 78.9], 4);
        L.control.zoom({ position: 'topright' }).addTo(map);
        
        // Luxury Dark Theme Tiles
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; OpenStreetMap &copy; CartoDB',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(map);

        // Nodes data
        const nodes = [
            // Artisans (Red)
            { pos: [12.2958, 76.6394], title: "Mysore Silk Weavers", type: "artisan", color: "#ef4444", status: "Active Production" },
            { pos: [15.9613, 76.1158], title: "Ilkal Handloom Cluster", type: "artisan", color: "#ef4444", status: "High Output" },
            { pos: [25.3176, 82.9739], title: "Varanasi Zari Artisans", type: "artisan", color: "#ef4444", status: "Busy" },
            // Suppliers (Blue)
            { pos: [13.0827, 80.2707], title: "Chennai Silk Yarns Ltd", type: "supplier", color: "#3b82f6", status: "Stock: 4,000kg" },
            { pos: [21.1702, 72.8311], title: "Surat Textile Hub", type: "supplier", color: "#3b82f6", status: "Dispatching" },
            // Warehouses (Gold)
            { pos: [19.0760, 72.8777], title: "Mumbai Central Warehouse", type: "warehouse", color: "#eab308", status: "Capacity: 85%" },
            { pos: [28.7041, 77.1025], title: "Delhi Regional Hub", type: "warehouse", color: "#eab308", status: "Capacity: 60%" },
            // Customers (Green)
            { pos: [12.9716, 77.5946], title: "Boutique Order #ORD-991", type: "customer", color: "#22c55e", status: "Awaiting Delivery" },
            { pos: [22.5726, 88.3639], title: "Retail Order #ORD-990", type: "customer", color: "#22c55e", status: "Delivered" },
            { pos: [40.7128, -74.0060], title: "Global Export #EXP-402", type: "customer", color: "#22c55e", status: "In Transit (NY)" }
        ];

        // Add Markers
        nodes.forEach(m => {
            const icon = L.divIcon({
                className: 'custom-div-icon',
                html: `<div style="background-color:${m.color};width:14px;height:14px;border-radius:50%;box-shadow:0 0 15px ${m.color};border:2px solid #1a1a1a;"></div>`,
                iconSize: [14, 14]
            });
            const marker = L.marker(m.pos, {icon: icon}).addTo(map);
            marker.bindPopup(`
                <div style="background:#1a1a1a; padding:5px; border-radius:4px; border:1px solid ${m.color}; color:#fff; font-family:Inter,sans-serif;">
                    <strong style="color:${m.color}; font-size:14px; display:block; margin-bottom:4px;">${m.title}</strong>
                    <span style="font-size:11px; color:#aaa; display:block;">Role: ${m.type.toUpperCase()}</span>
                    <span style="font-size:11px; color:#fff; display:block; margin-top:4px;">Status: ${m.status}</span>
                </div>
            `);
        });

        // Delivery Routes (Animated Lines)
        const routes = [
            { from: [13.0827, 80.2707], to: [12.2958, 76.6394], color: "#3b82f6" }, // Supplier to Artisan
            { from: [12.2958, 76.6394], to: [19.0760, 72.8777], color: "#eab308" }, // Artisan to Warehouse
            { from: [19.0760, 72.8777], to: [12.9716, 77.5946], color: "#22c55e" }, // Warehouse to Customer
            { from: [15.9613, 76.1158], to: [19.0760, 72.8777], color: "#eab308" }, // Artisan to Warehouse
            { from: [19.0760, 72.8777], to: [40.7128, -74.0060], color: "#22c55e", dashArray: "5, 10" }, // Global Export
            { from: [21.1702, 72.8311], to: [25.3176, 82.9739], color: "#3b82f6" }  // Supplier to Artisan
        ];

        routes.forEach(r => {
            L.polyline([r.from, r.to], {
                color: r.color,
                weight: 2,
                opacity: 0.6,
                dashArray: r.dashArray || '4, 8',
                lineJoin: 'round'
            }).addTo(map);
        });

        // Heatmap Simulation (using colored circles for regions)
        const heatRegions = [
            { pos: [14.0, 76.0], radius: 150000, color: "#D4AF37", intensity: 0.2 }, // South India Handloom Belt
            { pos: [23.0, 72.0], radius: 120000, color: "#ef4444", intensity: 0.15 }, // West India Textile Hub
            { pos: [26.0, 81.0], radius: 100000, color: "#D4AF37", intensity: 0.1 }  // North India Zari Belt
        ];
        heatRegions.forEach(h => {
            L.circle(h.pos, {
                color: 'transparent',
                fillColor: h.color,
                fillOpacity: h.intensity,
                radius: h.radius
            }).addTo(map);
        });

        """
content = content[:start_idx] + new_js_map + content[end_idx:]

# 3. Update QR Codes colors for high contrast (color=000000&bgcolor=FFFFFF)
# This significantly improves camera contrast.
content = re.sub(r'color=[A-Fa-f0-9]+&bgcolor=[A-Fa-f0-9]+', 'color=000000&bgcolor=FFFFFF', content)

# 4. Trim payload in JS slightly to reduce density.
content = re.sub(
    r'const payloadText = `Product ID: \$\{design\.id\}\\nProduct Name: \$\{design\.name\}\\nCategory: \$\{design\.category\}\\nFabric Type: \$\{design\.fabric\}\\nColor: \$\{design\.color\}\\nSize: \$\{design\.size\}\\nDesign Pattern: \$\{design\.pattern\}\\nProduct Price: \$\{design\.price\}\\nDescription: \$\{design\.desc\}\\nImage URL: https://heritagehandloom\.com/static/images/\$\{design\.img\}`;',
    r'const payloadText = `ID:${design.id}\\nItem:${design.name}\\nFab:${design.fabric}\\nCol:${design.color}\\nSize:${design.size}\\nPat:${design.pattern}\\nRs:${design.price}`;',
    content
)

# And for static QR images in table, just change their color
# Already handled by the color=000000&bgcolor=FFFFFF regex replacement!

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated Map and QR Codes.")
