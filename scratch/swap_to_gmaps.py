import re

with open('templates/supplier_active.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove Leaflet CSS and JS
text = re.sub(r'<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css".*?/>\n', '', text)
text = re.sub(r'<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js".*?></script>\n', '', text)

# 2. Add Google Maps JS
gm_script = '<script async defer src="https://maps.googleapis.com/maps/api/js?callback=initMap"></script>\n'
if 'maps.googleapis.com' not in text:
    text = text.replace('{% block content %}', '{% block content %}\n' + gm_script)

# 3. Replace the entire JS script block inside <script> that contains initMap
# First, let's find the script block
script_pattern = r'<script>\n    let mapInstance = null;.*?</script>'

gm_js = """<script>
    let mapInstance = null;

    function initMap() {
        if (mapInstance) return;

        const mapStyles = [
            { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
            { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
            { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
            {
                featureType: "administrative.locality",
                elementType: "labels.text.fill",
                stylers: [{ color: "#d59563" }],
            },
            {
                featureType: "road",
                elementType: "geometry",
                stylers: [{ color: "#38414e" }],
            },
            {
                featureType: "road",
                elementType: "geometry.stroke",
                stylers: [{ color: "#212a37" }],
            },
            {
                featureType: "road",
                elementType: "labels.text.fill",
                stylers: [{ color: "#9ca5b3" }],
            },
            {
                featureType: "water",
                elementType: "geometry",
                stylers: [{ color: "#17263c" }],
            },
            {
                featureType: "water",
                elementType: "labels.text.fill",
                stylers: [{ color: "#515c6d" }],
            },
            {
                featureType: "water",
                elementType: "labels.text.stroke",
                stylers: [{ color: "#17263c" }],
            },
        ];

        mapInstance = new google.maps.Map(document.getElementById("delivery-map"), {
            center: { lat: 14.1670, lng: 75.0403 },
            zoom: 7,
            styles: mapStyles,
            disableDefaultUI: true,
            zoomControl: true,
        });

        // Hub Coordinates
        const hubs = {
            mysore: { lat: 12.2958, lng: 76.6394 },
            bangalore: { lat: 12.9716, lng: 77.5946 },
            udupi: { lat: 13.3409, lng: 74.7421 },
            hubli: { lat: 15.3647, lng: 75.1240 }
        };

        const routes = [
            { start: hubs.mysore, end: hubs.bangalore, color: '#3b82f6', progress: 0.6, label: 'TRK-9021-A' },
            { start: hubs.udupi, end: hubs.bangalore, color: '#d4af37', progress: 0.9, label: 'TRK-9022-B' },
            { start: hubs.hubli, end: hubs.mysore, color: '#ef4444', progress: 0.55, label: 'TRK-9055-E' }
        ];

        routes.forEach(route => {
            // Draw Route Line
            new google.maps.Polyline({
                path: [route.start, route.end],
                geodesic: true,
                strokeColor: route.color,
                strokeOpacity: 0.5,
                strokeWeight: 4,
                map: mapInstance
            });

            // Hub Markers
            new google.maps.Marker({
                position: route.start,
                map: mapInstance,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 6,
                    fillColor: "#8b4513",
                    fillOpacity: 1,
                    strokeWeight: 2,
                    strokeColor: "#d4af37"
                },
                title: "Pickup Point"
            });

            new google.maps.Marker({
                position: route.end,
                map: mapInstance,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 6,
                    fillColor: "#2563eb",
                    fillOpacity: 1,
                    strokeWeight: 2,
                    strokeColor: "#ffffff"
                },
                title: "Delivery Hub"
            });

            // Calculate current truck position
            const lat = route.start.lat + (route.end.lat - route.start.lat) * route.progress;
            const lng = route.start.lng + (route.end.lng - route.start.lng) * route.progress;

            // Truck Marker
            new google.maps.Marker({
                position: { lat: lat, lng: lng },
                map: mapInstance,
                icon: {
                    path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
                    scale: 5,
                    fillColor: "#ffffff",
                    fillOpacity: 1,
                    strokeWeight: 2,
                    strokeColor: route.color,
                    rotation: Math.atan2(route.end.lng - route.start.lng, route.end.lat - route.start.lat) * 180 / Math.PI
                },
                title: route.label
            });
        });
    }

    // Since we use async defer for the Maps script with callback=initMap, it will auto-call.
</script>"""

text = re.sub(script_pattern, gm_js, text, flags=re.DOTALL)

with open('templates/supplier_active.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Replaced Leaflet with Google Maps in supplier_active.html')
