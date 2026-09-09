with open('templates/supplier_tracking.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_js = """<script>
    let mapInstance = null;
    let animationFrames = [];
    let polylineOverlays = []; // Used for hovering/focusing routes

    // OverlayView class for true CSS HTML markers
    class HTMLMarker extends google.maps.OverlayView {
        constructor(latlng, html, map, offset = {x: 0, y: 0}) {
            super();
            this.latlng = latlng;
            this.html = html;
            this.div = null;
            this.offset = offset;
            this.setMap(map);
        }
        onAdd() {
            this.div = document.createElement('div');
            this.div.style.position = 'absolute';
            this.div.style.transform = `translate(calc(-50% + ${this.offset.x}px), calc(-50% + ${this.offset.y}px))`;
            this.div.innerHTML = this.html;
            const panes = this.getPanes();
            panes.overlayMouseTarget.appendChild(this.div);
        }
        draw() {
            const overlayProjection = this.getProjection();
            if(!overlayProjection) return;
            const position = overlayProjection.fromLatLngToDivPixel(this.latlng);
            if (this.div) {
                this.div.style.left = position.x + 'px';
                this.div.style.top = position.y + 'px';
            }
        }
        onRemove() {
            if (this.div) {
                this.div.parentNode.removeChild(this.div);
                this.div = null;
            }
        }
    }

    // Bezier Curve Generator for Maps
    function getBezierCurve(p0, p1, p2, numPoints = 100) {
        const points = [];
        for (let i = 0; i <= numPoints; i++) {
            const t = i / numPoints;
            const lat = Math.pow(1 - t, 2) * p0.lat + 2 * (1 - t) * t * p1.lat + Math.pow(t, 2) * p2.lat;
            const lng = Math.pow(1 - t, 2) * p0.lng + 2 * (1 - t) * t * p1.lng + Math.pow(t, 2) * p2.lng;
            points.push({ lat, lng });
        }
        return points;
    }

    function initMap() {
        if (mapInstance) return;

        const mapStyles = [
            { elementType: "geometry", stylers: [{ color: "#141414" }] },
            { elementType: "labels.text.stroke", stylers: [{ color: "#000000" }] },
            { elementType: "labels.text.fill", stylers: [{ color: "#808080" }] },
            { featureType: "administrative", elementType: "labels.text.fill", stylers: [{ color: "#d4af37" }] },
            { featureType: "road", elementType: "geometry", stylers: [{ color: "#1a1a1a" }] },
            { featureType: "road", elementType: "geometry.stroke", stylers: [{ color: "#333333" }] },
            { featureType: "road", elementType: "labels.text.fill", stylers: [{ color: "#555555" }] },
            { featureType: "water", elementType: "geometry", stylers: [{ color: "#0a0a0a" }] },
            { featureType: "water", elementType: "labels.text.fill", stylers: [{ color: "#333333" }] }
        ];

        mapInstance = new google.maps.Map(document.getElementById("delivery-map"), {
            center: { lat: 14.5, lng: 76.0 },
            zoom: 6.8,
            styles: mapStyles,
            disableDefaultUI: true,
            zoomControl: true,
            backgroundColor: '#141414'
        });

        const hubs = {
            mysore: { lat: 12.2958, lng: 76.6394 },
            bangalore: { lat: 12.9716, lng: 77.5946 },
            udupi: { lat: 13.3409, lng: 74.7421 },
            hubli: { lat: 15.3647, lng: 75.1240 },
            mangalore: { lat: 12.9141, lng: 74.8560 },
            belgaum: { lat: 15.8497, lng: 74.4977 },
            bellary: { lat: 15.1394, lng: 76.9214 },
            hassan: { lat: 13.0068, lng: 76.1004 },
            shimoga: { lat: 13.9299, lng: 75.5681 },
            davangere: { lat: 14.4644, lng: 75.9218 },
            chitradurga: { lat: 14.2255, lng: 76.4010 }
        };

        const truckPath = "M17.4,0H5.6C2.5,0,0,3.5,0,6.6v34.8c0,3.1,2.5,5.6,5.6,5.6h11.8c3.1,0,5.6-2.5,5.6-5.6V6.6C23,3.5,20.5,0,17.4,0z M22.1,14.2v11.7l-2.7,0.4v-11.4L22.1,14.2z M20.6,10.8c-1,3.9-2.2,8.5-2.2,8.5H4.6l-2.2-8.5C2.4,10.8,11.3,7.8,20.6,10.8z M3.7,21.7v11.4l-2.7-0.4v-11.7L3.7,21.7z";
        const vanPath = "M28.4,15.2c-0.2-1.3-0.7-2.6-1.5-3.6c-0.8-1-1.8-1.7-2.9-2.2l-3-1.1c-1.3-0.5-2.6-0.7-4-0.7H13.6c-1.8,0-3.5,0.4-5.1,1.1 l-1.8,0.8c-1.7,0.7-3.2,1.8-4.5,3.2L1,14c-1,1.1-1.3,2.6-1,4.1l1.5,8c0.2,0.9,0.7,1.7,1.3,2.3c0.7,0.6,1.5,0.9,2.4,0.9h0.4 c0.8,2.7,3.3,4.6,6.3,4.6s5.5-1.9,6.3-4.6h3.4c0.8,2.7,3.3,4.6,6.3,4.6s5.5-1.9,6.3-4.6h1.2c1.3,0,2.3-1,2.3-2.3V18 C30,16.8,29.4,15.7,28.4,15.2z";
        const bikePath = "M19,13h-2v-2h-3v2H8.5c-1.5,0-2.8,1.1-3,2.5c-0.2,1.2,0.5,2.4,1.7,2.8L10.3,19l1.7-1l-3.3-1h3.1 c1.6,0,2.9-1.2,3-2.8l0-0.2H19v2h2v-4C21,13.4,20.1,13,19,13z M5.5,13C3.6,13,2,14.6,2,16.5S3.6,20,5.5,20S9,18.4,9,16.5 S7.4,13,5.5,13z M5.5,18C4.7,18,4,17.3,4,16.5S4.7,15,5.5,15S7,15.7,7,16.5S6.3,18,5.5,18z M18.5,13C16.6,13,15,14.6,15,16.5 S16.6,20,18.5,20S22,18.4,22,16.5S20.4,13,18.5,13z M18.5,18c-0.8,0-1.5-0.7-1.5-1.5s0.7-1.5,1.5-1.5s1.5,0.7,1.5,1.5 S19.3,18,18.5,18z";

        // Blue = Active, Red = Delayed, Green = Completed, Yellow = Pending
        const deliveries = [
            {
                start: hubs.mysore,
                mid: hubs.hassan,
                end: hubs.bangalore,
                color: '#3b82f6', // Blue - Active
                vehicle: truckPath,
                scale: 0.6,
                anchor: new google.maps.Point(12, 24),
                orderId: "TRK-9021",
                customer: "Heritage Hub",
                status: "In Transit",
                eta: "45 Mins",
                speed: 0.001, 
                progress: 0.2,
                dist: "120 km"
            },
            {
                start: hubs.udupi,
                mid: hubs.shimoga,
                end: hubs.bangalore,
                color: '#eab308', // Yellow - Pending
                vehicle: vanPath,
                scale: 0.8,
                anchor: new google.maps.Point(15, 15),
                orderId: "VAN-4022",
                customer: "Udupi Artisan",
                status: "Pending Pickup",
                eta: "4 Hrs",
                speed: 0.0015,
                progress: 0.0,
                dist: "340 km"
            },
            {
                start: hubs.hubli,
                mid: hubs.davangere,
                end: hubs.mysore,
                color: '#ef4444', // Red - Delayed
                vehicle: truckPath,
                scale: 0.6,
                anchor: new google.maps.Point(12, 24),
                orderId: "TRK-007",
                customer: "Hubli Zone",
                status: "Delayed",
                eta: "2 Hrs",
                speed: 0.0003,
                progress: 0.4,
                dist: "180 km"
            },
            {
                start: hubs.belgaum,
                mid: hubs.hubli,
                end: hubs.bellary,
                color: '#22c55e', // Green - Completed
                vehicle: bikePath,
                scale: 1,
                anchor: new google.maps.Point(12, 16),
                orderId: "BIKE-3099",
                customer: "Belgaum Weavers",
                status: "Delivered",
                eta: "0 Mins",
                speed: 0,
                progress: 1.0,
                dist: "0 km"
            }
        ];

        let lineAnimations = []; // Store lines for arrow animation

        deliveries.forEach((delivery, index) => {
            // Generate 100 points for a smooth curve
            const curvePoints = getBezierCurve(delivery.start, delivery.mid, delivery.end, 100);

            // Base thick blur line
            const blurLine = new google.maps.Polyline({
                path: curvePoints,
                geodesic: true,
                strokeColor: delivery.color,
                strokeOpacity: 0.15,
                strokeWeight: 14,
                map: mapInstance,
                clickable: false
            });

            // Core bright line with animated arrows
            const coreLine = new google.maps.Polyline({
                path: curvePoints,
                geodesic: true,
                strokeColor: delivery.color,
                strokeOpacity: 1,
                strokeWeight: 3,
                icons: [{
                    icon: {
                        path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
                        scale: 2,
                        strokeColor: "#ffffff",
                        fillColor: "#ffffff",
                        fillOpacity: 1
                    },
                    offset: '0%',
                    repeat: '100px'
                }],
                map: mapInstance,
                clickable: false
            });
            polylineOverlays.push({blur: blurLine, core: coreLine});
            lineAnimations.push(coreLine);

            // 3 Route Markers (Start, Mid, End)
            // Start - Pulsing Dot
            new HTMLMarker(delivery.start, `<div class="w-3 h-3 rounded-full border border-white" style="background-color: ${delivery.color}; box-shadow: 0 0 10px ${delivery.color};"></div>`, mapInstance);
            
            // Mid - Transit Hub Dot
            new HTMLMarker(delivery.mid, `<div class="w-2 h-2 rounded-full border border-white" style="background-color: ${delivery.color}; box-shadow: 0 0 10px ${delivery.color};"></div>`, mapInstance);

            // End - Pulsing Red Dot for destination
            new HTMLMarker(delivery.end, `<div class="w-4 h-4 rounded-full border-2 shadow-[0_0_15px_5px_currentColor] animate-pulse" style="color: #ef4444; background-color: #141414; border-color: #ef4444;"></div>`, mapInstance);

            // Floating Status Badge above the mid-point!
            const badgeHtml = `
                <div class="px-2 py-1 rounded shadow-lg border backdrop-blur text-[10px] font-bold uppercase tracking-widest pointer-events-none" 
                     style="background: rgba(20,20,20,0.8); border-color: ${delivery.color}50; color: ${delivery.color}; transform: translateY(-20px);">
                    ${delivery.status} <br/>
                    <span class="text-white text-[9px]">${delivery.eta} | ${delivery.dist}</span>
                </div>
            `;
            new HTMLMarker(delivery.mid, badgeHtml, mapInstance, {x: 0, y: -30});

            // Animated Vehicle Marker
            const vehicleMarker = new google.maps.Marker({
                position: curvePoints[0],
                map: mapInstance,
                icon: {
                    path: delivery.vehicle,
                    scale: delivery.scale,
                    fillColor: "#ffffff",
                    fillOpacity: 1,
                    strokeWeight: 1.5,
                    strokeColor: delivery.color,
                    anchor: delivery.anchor,
                    rotation: 0
                },
                zIndex: 999
            });

            // Math to get heading from point A to B
            function getHeading(p1, p2) {
                return Math.atan2(p2.lng - p1.lng, p2.lat - p1.lat) * 180 / Math.PI;
            }

            function animateVehicle() {
                if (delivery.speed > 0) {
                    delivery.progress += delivery.speed;
                    if (delivery.progress >= 1.0) delivery.progress = 0; 
                }
                
                // Find exact position on the 100-point curve
                const floatIndex = delivery.progress * (curvePoints.length - 1);
                const i = Math.floor(floatIndex);
                
                if (i < curvePoints.length - 1) {
                    const frac = floatIndex - i;
                    const p1 = curvePoints[i];
                    const p2 = curvePoints[i+1];
                    const currentLat = p1.lat + (p2.lat - p1.lat) * frac;
                    const currentLng = p1.lng + (p2.lng - p1.lng) * frac;
                    const pos = new google.maps.LatLng(currentLat, currentLng);
                    
                    vehicleMarker.setPosition(pos);
                    
                    // Update vehicle rotation to match curve trajectory
                    const heading = getHeading(p1, p2);
                    const icon = vehicleMarker.getIcon();
                    icon.rotation = heading;
                    vehicleMarker.setIcon(icon);
                }

                animationFrames[index] = requestAnimationFrame(animateVehicle);
            }
            animateVehicle();
        });

        // Global animation loop for directional arrows on the lines
        let offsetCount = 0;
        window.setInterval(() => {
            offsetCount = (offsetCount + 1) % 200;
            lineAnimations.forEach(line => {
                const icons = line.get('icons');
                icons[0].offset = (offsetCount / 2) + '%';
                line.set('icons', icons);
            });
        }, 50);
    }
    
    document.addEventListener('DOMContentLoaded', () => {
        initMap();
    });

    window.focusRoute = function(index) {
        polylineOverlays.forEach((route, i) => {
            if(i !== index) {
                route.blur.setOptions({strokeOpacity: 0.05});
                route.core.setOptions({strokeOpacity: 0.1});
            } else {
                route.blur.setOptions({strokeOpacity: 0.4, strokeWeight: 20});
                route.core.setOptions({strokeOpacity: 1, strokeWeight: 5});
            }
        });
    };

    window.unfocusRoute = function() {
        polylineOverlays.forEach((route) => {
            route.blur.setOptions({strokeOpacity: 0.15, strokeWeight: 14});
            route.core.setOptions({strokeOpacity: 1, strokeWeight: 3});
        });
    };
</script>"""

start = text.find('<script>')
end = text.find('</script>') + 9
if start != -1 and end != -1:
    text = text[:start] + new_js + text[end:]

with open('templates/supplier_tracking.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated advanced routes JS!')
