import re

with open('templates/supplier_active.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Define the new script and modal HTML
new_bottom = """<script>
    function updateDeliveryStatus(btn) {
        const card = btn.closest('.group');
        const badge = card.querySelector('span[class*="tracking-widest"]');
        badge.innerText = 'Delivered';
        badge.className = 'bg-green-900/30 text-green-400 text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded border border-green-500/30 shadow-[0_0_10px_rgba(74,222,128,0.2)]';
        btn.innerText = 'Completed';
        btn.className = 'text-green-400 bg-green-900/20 px-4 py-2 rounded border border-green-500/30 font-bold uppercase tracking-widest text-[10px] opacity-50 cursor-not-allowed';
        btn.disabled = true;
        if(card.classList.contains('border-red-500/20')) {
            card.classList.remove('border-red-500/20');
            card.classList.add('border-green-500/20');
            const delayText = card.querySelector('p.text-\\\\[\\\\#ff9999\\\\]\\\\/80');
            if (delayText) delayText.innerText = "Resolved & Delivered";
        }
        const bar = card.querySelector('.rounded-full.h-2 > div');
        if (bar) {
            bar.style.width = '100%';
            bar.className = 'bg-gradient-to-r from-green-600 to-green-400 h-full rounded-full shadow-[0_0_8px_rgba(74,222,128,0.6)] relative transition-all duration-1000';
            const pulse = bar.querySelector('span');
            if(pulse) pulse.remove();
        }
        const remaining = card.querySelector('.font-mono:last-of-type');
        if(remaining) remaining.innerText = "0.0 km remaining";
    }

    let mapInstance = null;

    function initMap() {
        if (mapInstance !== null) return; // Already initialized

        // Initialize map centered on Karnataka
        mapInstance = L.map('delivery-map').setView([14.1670, 75.0403], 7);

        // CartoDB Dark Matter tiles
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(mapInstance);

        // Define Icons
        const pickupIcon = L.divIcon({
            html: `<div class="w-4 h-4 rounded-full bg-[#8b4513] border-2 border-[#d4af37] shadow-[0_0_10px_rgba(212,175,55,0.8)]"></div>`,
            className: '',
            iconSize: [16, 16],
            iconAnchor: [8, 8]
        });

        const destIcon = L.divIcon({
            html: `<div class="w-4 h-4 rounded-full bg-blue-600 border-2 border-white shadow-[0_0_10px_rgba(59,130,246,0.8)]"></div>`,
            className: '',
            iconSize: [16, 16],
            iconAnchor: [8, 8]
        });

        const truckIcon = L.divIcon({
            html: `<div class="w-6 h-6 bg-white rounded-full flex items-center justify-center shadow-[0_0_15px_rgba(255,255,255,1)] border-2 border-[#d4af37] animate-pulse"><svg class="w-3 h-3 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path></svg></div>`,
            className: '',
            iconSize: [24, 24],
            iconAnchor: [12, 12]
        });

        // Hub Coordinates
        const hubs = {
            mysore: [12.2958, 76.6394],
            bangalore: [12.9716, 77.5946],
            udupi: [13.3409, 74.7421],
            hubli: [15.3647, 75.1240],
            mangalore: [12.9141, 74.8560]
        };

        // Routes Data
        const routes = [
            {
                start: hubs.mysore,
                end: hubs.bangalore,
                color: '#3b82f6', // Blue (In Transit)
                label: "TRK-9021-A | Cargo: 140kg Textiles",
                eta: "01:30 PM",
                progress: 0.6
            },
            {
                start: hubs.udupi,
                end: hubs.bangalore,
                color: '#d4af37', // Gold (Out for Delivery)
                label: "TRK-9022-B | Cargo: 28kg Stoles",
                eta: "12:15 PM",
                progress: 0.9
            },
            {
                start: hubs.hubli,
                end: hubs.mysore,
                color: '#ef4444', // Red (Delayed)
                label: "TRK-9055-E | Vehicle Breakdown",
                eta: "Unknown",
                progress: 0.55
            }
        ];

        routes.forEach(route => {
            // Draw Polyline
            L.polyline([route.start, route.end], {
                color: route.color,
                weight: 3,
                opacity: 0.5,
                dashArray: '10, 10'
            }).addTo(mapInstance);

            // Add Pickup Pin
            L.marker(route.start, {icon: pickupIcon})
                .bindTooltip("Pickup Point", {direction: 'top', className: 'dark-tooltip'})
                .addTo(mapInstance);

            // Add Destination Pin
            L.marker(route.end, {icon: destIcon})
                .bindTooltip("Delivery Hub", {direction: 'top', className: 'dark-tooltip'})
                .addTo(mapInstance);

            // Calculate current truck position based on progress
            const lat = route.start[0] + (route.end[0] - route.start[0]) * route.progress;
            const lng = route.start[1] + (route.end[1] - route.start[1]) * route.progress;

            // Add Animated Truck Pin
            const truck = L.marker([lat, lng], {icon: truckIcon}).addTo(mapInstance);
            
            // Add rich tooltip to truck
            const tooltipContent = `
                <div class="font-sans text-xs">
                    <strong class="text-[#d4af37] uppercase tracking-widest block mb-1 font-mono">${route.label.split('|')[0]}</strong>
                    <div class="mb-1">${route.label.split('|')[1]}</div>
                    <div class="text-gray-400">ETA: <span class="text-white">${route.eta}</span></div>
                </div>
            `;
            truck.bindTooltip(tooltipContent, {direction: 'auto', className: 'dark-tooltip', permanent: false});
        });
    }

    function openMapModal() {
        const modal = document.getElementById('map-modal');
        const content = document.getElementById('map-modal-content');
        
        modal.classList.remove('opacity-0', 'pointer-events-none');
        modal.classList.add('opacity-100');
        
        setTimeout(() => {
            content.classList.remove('scale-95', 'opacity-0');
            content.classList.add('scale-100', 'opacity-100');
            
            // Initialize Leaflet Map safely after modal renders
            initMap();
            // Force Leaflet to recalculate container size so tiles load correctly
            setTimeout(() => {
                if(mapInstance) mapInstance.invalidateSize();
            }, 300);
            
        }, 50);
    }

    function closeMapModal() {
        const modal = document.getElementById('map-modal');
        const content = document.getElementById('map-modal-content');
        
        content.classList.remove('scale-100', 'opacity-100');
        content.classList.add('scale-95', 'opacity-0');
        
        setTimeout(() => {
            modal.classList.remove('opacity-100');
            modal.classList.add('opacity-0', 'pointer-events-none');
        }, 300);
    }
</script>

<!-- Live Map Modal -->
<div id="map-modal" class="fixed inset-0 z-50 flex items-center justify-center opacity-0 pointer-events-none transition-opacity duration-300">
    <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" onclick="closeMapModal()"></div>
    <div class="bg-[#141414] border border-[#d4af37]/30 rounded-xl w-full max-w-5xl shadow-[0_0_50px_rgba(212,175,55,0.15)] relative z-10 transform scale-95 opacity-0 transition-all duration-300" id="map-modal-content">
        <div class="p-4 border-b border-[#d4af37]/20 flex justify-between items-center bg-gradient-to-r from-[#1a1a1a] to-black rounded-t-xl">
            <h3 class="text-xl font-serif text-[#f5ebd7] drop-shadow-md">Active Transits - Live Map</h3>
            <button onclick="closeMapModal()" class="text-[#d4af37]/60 hover:text-[#d4af37] transition-colors">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
        </div>
        <div class="h-[600px] w-full relative rounded-b-xl overflow-hidden z-0">
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
</div>
{% endblock %}
"""

# replace everything from <script> to {% endblock %} with new_bottom
pattern = re.compile(r'<script>.*{% endblock %}', re.DOTALL)
new_text = pattern.sub(new_bottom.strip(), text)

with open('templates/supplier_active.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Map logic injected.")
