import re

with open('templates/supplier_active.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove Leaflet CSS and JS
text = re.sub(r'<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"[^>]*>\s*', '', text)
text = re.sub(r'<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"[^>]*></script>\s*', '', text)

# 2. Add Google Maps JS CDN if missing
gm_script = '<script async defer src="https://maps.googleapis.com/maps/api/js?callback=initMap"></script>\n'
if 'maps.googleapis.com' not in text:
    text = text.replace('{% block content %}', '{% block content %}\n' + gm_script)

# 3. Replace the entire JS script block inside <script> that contains initMap
# The old script starts with `<script>\n    let mapInstance = null;` or similar
# Let's match from `<script>` up to `</script>` that contains `mapInstance = L.map`
script_pattern = r'<script>\s*let mapInstance = null;\s*function initMap\(\) \{.*?</script>'

gm_js = """<script>
    let mapInstance = null;
    let animationFrames = [];

    function initMap() {
        if (mapInstance) return;

        // Custom Dark Mode Map Theme (Uber/Swiggy style)
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
            mapId: "DEMO_MAP_ID" // Enables advanced markers
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
                color: '#3b82f6', // Blue (In Transit)
                orderId: "ORD-9021-A",
                customer: "Silk Emporium, Bangalore",
                status: "In Transit",
                eta: "45 Mins",
                speed: 0.002, // Animation speed
                progress: 0.2
            },
            {
                start: hubs.udupi,
                end: hubs.bangalore,
                color: '#d4af37', // Gold (Out for Delivery)
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
                color: '#ef4444', // Red (Delayed)
                orderId: "ORD-9055-E",
                customer: "Mysore Weavers Hub",
                status: "Delayed (Traffic)",
                eta: "2 Hrs",
                speed: 0.0005,
                progress: 0.4
            }
        ];

        // Shared InfoWindow for Tooltips
        const infoWindow = new google.maps.InfoWindow({
            pixelOffset: new google.maps.Size(0, -30)
        });

        deliveries.forEach((delivery, index) => {
            // Draw Route Line (Animated look by using dashed lines if possible, or just solid)
            new google.maps.Polyline({
                path: [delivery.start, delivery.end],
                geodesic: true,
                strokeColor: delivery.color,
                strokeOpacity: 0.4,
                strokeWeight: 4,
                map: mapInstance
            });

            // Pickup Marker
            new google.maps.Marker({
                position: delivery.start,
                map: mapInstance,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 7,
                    fillColor: "#141414",
                    fillOpacity: 1,
                    strokeWeight: 3,
                    strokeColor: "#ef4444" // Red Pin for start
                },
                title: "Pickup: " + delivery.orderId
            });

            // Destination Marker
            new google.maps.Marker({
                position: delivery.end,
                map: mapInstance,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 7,
                    fillColor: "#141414",
                    fillOpacity: 1,
                    strokeWeight: 3,
                    strokeColor: "#3b82f6" // Blue Pin for end
                },
                title: "Dropoff: " + delivery.customer
            });

            // Create Animated Vehicle Marker
            const vehicleMarker = new google.maps.Marker({
                position: delivery.start,
                map: mapInstance,
                icon: {
                    // SVG Truck/Car Icon
                    path: "M17.402,0H5.643C2.526,0,0,3.467,0,6.584v34.804c0,3.116,2.526,5.644,5.643,5.644h11.759c3.116,0,5.644-2.527,5.644-5.644 V6.584C23.044,3.467,20.518,0,17.402,0z M22.057,14.188v11.665l-2.729,0.351v-11.41L22.057,14.188z M20.625,10.773 c-1.016,3.9-2.219,8.51-2.219,8.51H4.638l-2.222-8.51C2.417,10.773,11.3,7.755,20.625,10.773z M3.748,21.713v11.41l-2.728-0.351 v-11.665L3.748,21.713z M1.02,34.403l2.728,0.352v7.712c0,0.589-0.478,1.066-1.066,1.066s-1.066-0.477-1.066-1.066V34.403z M22.057,42.467c0,0.589-0.478,1.066-1.066,1.066c-0.589,0-1.066-0.477-1.066-1.066v-7.711l2.729-0.352V42.467z M20.527,24.189H2.516 c0-0.589,0.478-1.066,1.066-1.066h15.879c0.588,0,1.066,0.477,1.066,1.066V24.189z",
                    scale: 0.6,
                    fillColor: "#ffffff",
                    fillOpacity: 1,
                    strokeWeight: 1,
                    strokeColor: "#000000",
                    anchor: new google.maps.Point(12, 24),
                    // Calculate heading
                    rotation: Math.atan2(delivery.end.lng - delivery.start.lng, delivery.end.lat - delivery.start.lat) * 180 / Math.PI
                },
                zIndex: 999
            });

            // Tooltip HTML
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

            // Hover event to show tooltip
            vehicleMarker.addListener('click', () => {
                infoWindow.setContent(tooltipContent);
                infoWindow.open(mapInstance, vehicleMarker);
            });

            // Animation Loop logic
            function animateVehicle() {
                delivery.progress += delivery.speed;
                
                // Ping-pong or loop effect
                if (delivery.progress >= 1.0) {
                    delivery.progress = 0; // Loop back to start for demo purposes
                }

                const currentLat = delivery.start.lat + (delivery.end.lat - delivery.start.lat) * delivery.progress;
                const currentLng = delivery.start.lng + (delivery.end.lng - delivery.start.lng) * delivery.progress;
                
                vehicleMarker.setPosition(new google.maps.LatLng(currentLat, currentLng));
                
                // Keep tooltip attached if open
                if (infoWindow.getAnchor() === vehicleMarker) {
                    infoWindow.setPosition(vehicleMarker.getPosition());
                }

                animationFrames[index] = requestAnimationFrame(animateVehicle);
            }
            
            // Start animation
            animateVehicle();
        });
    }

    // Since we use async defer for the Maps script with callback=initMap, it will auto-call.
</script>"""

text = re.sub(script_pattern, gm_js, text, flags=re.DOTALL)

with open('templates/supplier_active.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Successfully injected fully animated Google Map logic.')
