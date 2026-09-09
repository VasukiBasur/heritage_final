import re

with open('templates/supplier_tracking.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Insert Inline Map HTML right below the header block
# Header ends at <div class="mb-8 flex justify-between items-end"> ... </div>
map_ui = """
<!-- Inline Live Map -->
<div class="bg-[#141414] border border-[#d4af37]/30 rounded-xl w-full shadow-[0_0_20px_rgba(212,175,55,0.1)] mb-8 overflow-hidden relative">
    <div class="p-4 border-b border-[#d4af37]/20 flex justify-between items-center bg-gradient-to-r from-[#1a1a1a] to-black">
        <h3 class="text-xl font-serif text-[#f5ebd7] drop-shadow-md">Active Transits - Live Map</h3>
    </div>
    <div class="h-[500px] w-full relative z-0">
        <!-- Google Map Container -->
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
if 'id="delivery-map"' not in text:
    text = text.replace('<div class="grid grid-cols-1', map_ui + '\n<div class="grid grid-cols-1')

# 2. Replace the Leaflet script block with Google Maps animation
script_start = text.find('let mapInstance = null;')
script_end = text.find('</script>', script_start)

gm_js = """let mapInstance = null;
    let animationFrames = [];

    function initMap() {
        if (mapInstance) return;

        // Custom Dark Mode Map Theme
        const mapStyles = [
            { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
            { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
            { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
            { featureType: "administrative.locality", elementType: "labels.text.fill", stylers: [{ color: "#d59563" }] },
            { featureType: "poi", elementType: "labels.text.fill", stylers: [{ color: "#d59563" }] },
            { featureType: "poi.park", elementType: "geometry", stylers: [{ color: "#263c3f" }] },
            { featureType: "poi.park", elementType: "labels.text.fill", stylers: [{ color: "#6b9a76" }] },
            { featureType: "road", elementType: "geometry", stylers: [{ color: "#38414e" }] },
            { featureType: "road", elementType: "geometry.stroke", stylers: [{ color: "#212a37" }] },
            { featureType: "road", elementType: "labels.text.fill", stylers: [{ color: "#9ca5b3" }] },
            { featureType: "road.highway", elementType: "geometry", stylers: [{ color: "#746855" }] },
            { featureType: "road.highway", elementType: "geometry.stroke", stylers: [{ color: "#1f2835" }] },
            { featureType: "road.highway", elementType: "labels.text.fill", stylers: [{ color: "#f3d19c" }] },
            { featureType: "transit", elementType: "geometry", stylers: [{ color: "#2f3948" }] },
            { featureType: "transit.station", elementType: "labels.text.fill", stylers: [{ color: "#d59563" }] },
            { featureType: "water", elementType: "geometry", stylers: [{ color: "#17263c" }] },
            { featureType: "water", elementType: "labels.text.fill", stylers: [{ color: "#515c6d" }] },
            { featureType: "water", elementType: "labels.text.stroke", stylers: [{ color: "#17263c" }] }
        ];

        mapInstance = new google.maps.Map(document.getElementById("delivery-map"), {
            center: { lat: 13.9, lng: 75.8 },
            zoom: 7,
            styles: mapStyles,
            disableDefaultUI: true,
            zoomControl: true,
            mapId: "DEMO_MAP_ID"
        });

        const hubs = {
            mysore: { lat: 12.2958, lng: 76.6394 },
            bangalore: { lat: 12.9716, lng: 77.5946 },
            udupi: { lat: 13.3409, lng: 74.7421 },
            hubli: { lat: 15.3647, lng: 75.1240 }
        };

        const deliveries = [
            {
                start: hubs.mysore,
                end: hubs.bangalore,
                color: '#3b82f6', 
                orderId: "ORD-9021-A",
                customer: "Silk Emporium, Bangalore",
                status: "In Transit",
                eta: "45 Mins",
                speed: 0.002, 
                progress: 0.2
            },
            {
                start: hubs.udupi,
                end: hubs.bangalore,
                color: '#d4af37', 
                orderId: "ORD-9022-B",
                customer: "Heritage Retail, MG Road",
                status: "Out for Delivery",
                eta: "15 Mins",
                speed: 0.003,
                progress: 0.7
            },
            {
                start: hubs.hubli,
                end: hubs.mysore,
                color: '#ef4444', 
                orderId: "ORD-9055-E",
                customer: "Mysore Weavers Hub",
                status: "Delayed (Traffic)",
                eta: "2 Hrs",
                speed: 0.0005,
                progress: 0.4
            }
        ];

        const infoWindow = new google.maps.InfoWindow({
            pixelOffset: new google.maps.Size(0, -30)
        });

        deliveries.forEach((delivery, index) => {
            new google.maps.Polyline({
                path: [delivery.start, delivery.end],
                geodesic: true,
                strokeColor: delivery.color,
                strokeOpacity: 0.4,
                strokeWeight: 4,
                map: mapInstance
            });

            new google.maps.Marker({
                position: delivery.start,
                map: mapInstance,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 7,
                    fillColor: "#141414",
                    fillOpacity: 1,
                    strokeWeight: 3,
                    strokeColor: "#ef4444" 
                },
                title: "Pickup: " + delivery.orderId
            });

            new google.maps.Marker({
                position: delivery.end,
                map: mapInstance,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 7,
                    fillColor: "#141414",
                    fillOpacity: 1,
                    strokeWeight: 3,
                    strokeColor: "#3b82f6" 
                },
                title: "Dropoff: " + delivery.customer
            });

            const vehicleMarker = new google.maps.Marker({
                position: delivery.start,
                map: mapInstance,
                icon: {
                    path: "M17.402,0H5.643C2.526,0,0,3.467,0,6.584v34.804c0,3.116,2.526,5.644,5.643,5.644h11.759c3.116,0,5.644-2.527,5.644-5.644 V6.584C23.044,3.467,20.518,0,17.402,0z M22.057,14.188v11.665l-2.729,0.351v-11.41L22.057,14.188z M20.625,10.773 c-1.016,3.9-2.219,8.51-2.219,8.51H4.638l-2.222-8.51C2.417,10.773,11.3,7.755,20.625,10.773z M3.748,21.713v11.41l-2.728-0.351 v-11.665L3.748,21.713z M1.02,34.403l2.728,0.352v7.712c0,0.589-0.478,1.066-1.066,1.066s-1.066-0.477-1.066-1.066V34.403z M22.057,42.467c0,0.589-0.478,1.066-1.066,1.066c-0.589,0-1.066-0.477-1.066-1.066v-7.711l2.729-0.352V42.467z M20.527,24.189H2.516 c0-0.589,0.478-1.066,1.066-1.066h15.879c0.588,0,1.066,0.477,1.066,1.066V24.189z",
                    scale: 0.6,
                    fillColor: "#ffffff",
                    fillOpacity: 1,
                    strokeWeight: 1,
                    strokeColor: "#000000",
                    anchor: new google.maps.Point(12, 24),
                    rotation: Math.atan2(delivery.end.lng - delivery.start.lng, delivery.end.lat - delivery.start.lat) * 180 / Math.PI
                },
                zIndex: 999
            });

            const tooltipContent = `
                <div style="background:#141414; padding: 12px; border: 1px solid #d4af37; border-radius: 8px; color: #f5ebd7; font-family: sans-serif; min-width: 200px;">
                    <div style="color:#d4af37; font-size:10px; font-weight:bold; letter-spacing:1px; margin-bottom:4px;">ORDER ${delivery.orderId}</div>
                    <div style="font-size:14px; font-weight:600; margin-bottom:8px;">${delivery.customer}</div>
                    
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; font-size:11px;">
                        <span style="color:#888;">Status</span>
                        <span style="color:${delivery.color}; font-weight:bold;">${delivery.status}</span>
                    </div>
                    
                    <div style="display:flex; justify-content:space-between; align-items:center; font-size:11px;">
                        <span style="color:#888;">ETA</span>
                        <span style="color:#fff;">${delivery.eta}</span>
                    </div>
                </div>
            `;

            vehicleMarker.addListener('click', () => {
                infoWindow.setContent(tooltipContent);
                infoWindow.open(mapInstance, vehicleMarker);
            });

            function animateVehicle() {
                delivery.progress += delivery.speed;
                if (delivery.progress >= 1.0) delivery.progress = 0; 
                const currentLat = delivery.start.lat + (delivery.end.lat - delivery.start.lat) * delivery.progress;
                const currentLng = delivery.start.lng + (delivery.end.lng - delivery.start.lng) * delivery.progress;
                vehicleMarker.setPosition(new google.maps.LatLng(currentLat, currentLng));
                if (infoWindow.getAnchor() === vehicleMarker) {
                    infoWindow.setPosition(vehicleMarker.getPosition());
                }
                animationFrames[index] = requestAnimationFrame(animateVehicle);
            }
            animateVehicle();
        });
    }
    
    document.addEventListener('DOMContentLoaded', () => {
        initMap();
    });
"""

text = text[:script_start] + gm_js + text[script_end:]

# 3. Remove old map modal 
text = re.sub(r'<!-- Live Map Modal -->.*?(?=</script>|{% endblock %})', '', text, flags=re.DOTALL)

with open('templates/supplier_tracking.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('supplier_tracking.html completely fixed.')
