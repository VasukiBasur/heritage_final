html_content = """{% extends 'base_layout.html' %}

{% block title %}Enterprise Logistics Tracking{% endblock %}
{% block header_title %}Command Center - Live Tracking{% endblock %}

{% block content %}
<script async defer src="https://maps.googleapis.com/maps/api/js?callback=initMap"></script>

<style>
    /* Premium Glassmorphism & Glowing Effects */
    .glass-panel {
        background: rgba(20, 20, 20, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(212, 175, 55, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
    
    .glow-text {
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
    }
    
    .timeline-node {
        position: relative;
    }
    .timeline-node::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 100%;
        width: 100%;
        height: 2px;
        background: rgba(212, 175, 55, 0.2);
        transform: translateY(-50%);
        z-index: -1;
    }
    .timeline-node:last-child::after {
        display: none;
    }
    .timeline-node.active::after {
        background: linear-gradient(90deg, #d4af37 0%, rgba(212, 175, 55, 0.2) 100%);
    }

    /* Google Maps custom infowindow reset */
    .gm-style .gm-style-iw-c {
        background: transparent !important;
        box-shadow: none !important;
        padding: 0 !important;
        max-width: none !important;
    }
    .gm-style .gm-style-iw-tc::after {
        display: none !important; /* hide default arrow */
    }
    .gm-style-iw-d {
        overflow: hidden !important;
    }
    button.gm-ui-hover-effect {
        display: none !important; /* hide default close button */
    }
</style>

<div class="mb-6 flex justify-between items-end">
    <div>
        <h2 class="text-4xl font-serif text-[#f5ebd7] glow-text">Fleet Command Center</h2>
        <p class="text-sm text-[#d4af37]/70 mt-2 tracking-wide font-light flex items-center">
            <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse mr-2 shadow-[0_0_8px_#22c55e]"></span>
            AI-Powered Routing & Logistics Active
        </p>
    </div>
</div>

<!-- Full Screen Interactive Map Container -->
<div class="glass-panel rounded-2xl w-full relative overflow-hidden mb-8 shadow-[0_0_40px_rgba(212,175,55,0.05)] border border-[#d4af37]/30" style="height: calc(100vh - 200px); min-height: 700px;">
    
    <!-- Top Left Analytics Overlay -->
    <div class="absolute top-6 left-6 z-[1000] space-y-4 pointer-events-none">
        
        <div class="glass-panel p-4 rounded-xl flex items-center space-x-4 border-l-4 border-l-blue-500 pointer-events-auto hover:bg-[#1a1a1a]/90 transition-all cursor-pointer">
            <div class="p-3 bg-blue-500/10 rounded-lg">
                <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            </div>
            <div>
                <p class="text-[10px] uppercase tracking-widest text-[#d4af37]/70 font-bold">Active Routes</p>
                <h4 class="text-2xl font-bold text-white font-mono">14</h4>
            </div>
        </div>

        <div class="glass-panel p-4 rounded-xl flex items-center space-x-4 border-l-4 border-l-green-500 pointer-events-auto hover:bg-[#1a1a1a]/90 transition-all cursor-pointer">
            <div class="p-3 bg-green-500/10 rounded-lg">
                <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
            </div>
            <div>
                <p class="text-[10px] uppercase tracking-widest text-[#d4af37]/70 font-bold">Completed Today</p>
                <h4 class="text-2xl font-bold text-white font-mono">42</h4>
            </div>
        </div>

        <div class="glass-panel p-4 rounded-xl flex items-center space-x-4 border-l-4 border-l-red-500 pointer-events-auto hover:bg-[#1a1a1a]/90 transition-all cursor-pointer">
            <div class="p-3 bg-red-500/10 rounded-lg">
                <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            </div>
            <div>
                <p class="text-[10px] uppercase tracking-widest text-[#d4af37]/70 font-bold">Issues / Delayed</p>
                <h4 class="text-2xl font-bold text-white font-mono">1</h4>
            </div>
        </div>

    </div>

    <!-- Right Side Live Status Panel -->
    <div class="absolute top-6 right-6 bottom-6 w-80 z-[1000] flex flex-col pointer-events-none">
        
        <div class="glass-panel rounded-xl p-5 border border-[#d4af37]/20 flex-grow overflow-y-auto pointer-events-auto custom-scrollbar">
            <h4 class="text-xs font-bold text-[#d4af37] uppercase tracking-widest mb-4 flex justify-between items-center">
                Live Fleet Status
                <span class="w-2 h-2 rounded-full bg-blue-500 animate-ping"></span>
            </h4>
            
            <div class="space-y-4">
                <!-- Status Card 1 -->
                <div class="bg-gradient-to-r from-blue-900/20 to-black p-4 rounded-lg border border-blue-500/30 hover:border-blue-500 transition-colors cursor-pointer" onmouseover="focusRoute(0)" onmouseout="unfocusRoute()">
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs font-mono text-blue-400 bg-blue-900/30 px-2 py-0.5 rounded border border-blue-500/20">TRK-9021-A</span>
                        <span class="text-[10px] font-bold text-white uppercase tracking-wider">45 Mins</span>
                    </div>
                    <div class="text-sm font-semibold text-[#f5ebd7] truncate">Heritage Hub &rarr; Retail</div>
                    <div class="flex items-center mt-2">
                        <div class="w-full bg-black rounded-full h-1">
                            <div class="bg-blue-500 h-1 rounded-full relative" style="width: 70%">
                                <span class="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 bg-white rounded-full shadow-[0_0_5px_#fff]"></span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Status Card 2 -->
                <div class="bg-gradient-to-r from-[#8b4513]/20 to-black p-4 rounded-lg border border-[#d4af37]/30 hover:border-[#d4af37] transition-colors cursor-pointer" onmouseover="focusRoute(1)" onmouseout="unfocusRoute()">
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs font-mono text-[#d4af37] bg-[#d4af37]/10 px-2 py-0.5 rounded border border-[#d4af37]/20">VAN-4022</span>
                        <span class="text-[10px] font-bold text-white uppercase tracking-wider">12 Mins</span>
                    </div>
                    <div class="text-sm font-semibold text-[#f5ebd7] truncate">Udupi Artisan &rarr; Ctrl</div>
                    <div class="flex items-center mt-2">
                        <div class="w-full bg-black rounded-full h-1">
                            <div class="bg-[#d4af37] h-1 rounded-full relative" style="width: 90%">
                                <span class="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 bg-white rounded-full shadow-[0_0_5px_#fff]"></span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Status Card 3 -->
                <div class="bg-gradient-to-r from-red-900/20 to-black p-4 rounded-lg border border-red-500/30 hover:border-red-500 transition-colors cursor-pointer" onmouseover="focusRoute(2)" onmouseout="unfocusRoute()">
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs font-mono text-red-400 bg-red-900/30 px-2 py-0.5 rounded border border-red-500/20">BIKE-007</span>
                        <span class="text-[10px] font-bold text-red-400 uppercase tracking-wider animate-pulse">Delayed</span>
                    </div>
                    <div class="text-sm font-semibold text-[#f5ebd7] truncate">Hubli Zone &rarr; Mysore</div>
                    <div class="flex items-center mt-2">
                        <div class="w-full bg-black rounded-full h-1">
                            <div class="bg-red-500 h-1 rounded-full relative" style="width: 40%">
                                <span class="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 bg-red-200 rounded-full shadow-[0_0_5px_#ef4444]"></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mt-6 pt-4 border-t border-[#d4af37]/10">
                <p class="text-[10px] text-gray-400 text-center uppercase tracking-widest">Weather Status</p>
                <div class="flex items-center justify-center mt-2 text-[#d4af37]">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path></svg>
                    <span class="text-xs font-semibold">Clear Skies - Optimal Routing</span>
                </div>
            </div>

        </div>
    </div>

    <!-- The actual Google Map -->
    <div id="delivery-map" class="w-full h-full"></div>

</div>

<!-- Interactive Delivery Timeline -->
<div class="glass-panel rounded-2xl p-6 shadow-2xl relative overflow-hidden border border-[#d4af37]/20">
    <h4 class="text-sm font-bold text-[#f5ebd7] uppercase tracking-widest mb-6">Master Fulfillment Timeline</h4>
    <div class="flex justify-between items-center relative w-full px-4">
        
        <div class="timeline-node active flex flex-col items-center w-1/5 relative z-10 group cursor-pointer">
            <div class="w-10 h-10 rounded-full bg-[#d4af37] flex items-center justify-center shadow-[0_0_15px_rgba(212,175,55,0.6)] border-2 border-black group-hover:scale-110 transition-transform">
                <svg class="w-5 h-5 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path></svg>
            </div>
            <p class="text-xs font-bold text-[#d4af37] mt-3 uppercase tracking-wider text-center">Order Picked</p>
            <p class="text-[10px] text-gray-400 mt-1">08:00 AM</p>
        </div>

        <div class="timeline-node active flex flex-col items-center w-1/5 relative z-10 group cursor-pointer">
            <div class="w-10 h-10 rounded-full bg-[#d4af37] flex items-center justify-center shadow-[0_0_15px_rgba(212,175,55,0.6)] border-2 border-black group-hover:scale-110 transition-transform">
                <svg class="w-5 h-5 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
            </div>
            <p class="text-xs font-bold text-[#d4af37] mt-3 uppercase tracking-wider text-center">Left Warehouse</p>
            <p class="text-[10px] text-gray-400 mt-1">09:15 AM</p>
        </div>

        <div class="timeline-node flex flex-col items-center w-1/5 relative z-10 group cursor-pointer">
            <div class="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center shadow-[0_0_20px_rgba(59,130,246,0.8)] border-2 border-black group-hover:scale-110 transition-transform animate-pulse">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            </div>
            <p class="text-xs font-bold text-blue-400 mt-3 uppercase tracking-wider text-center">In Transit</p>
            <p class="text-[10px] text-blue-400/50 mt-1">Currently Active</p>
        </div>

        <div class="timeline-node flex flex-col items-center w-1/5 relative z-10 group cursor-pointer">
            <div class="w-10 h-10 rounded-full bg-[#1a1a1a] border-2 border-gray-600 flex items-center justify-center group-hover:border-[#d4af37] transition-colors">
                <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
            </div>
            <p class="text-xs font-bold text-gray-500 mt-3 uppercase tracking-wider text-center">Near Dest</p>
            <p class="text-[10px] text-gray-600 mt-1">Pending</p>
        </div>

        <div class="timeline-node flex flex-col items-center w-1/5 relative z-10 group cursor-pointer">
            <div class="w-10 h-10 rounded-full bg-[#1a1a1a] border-2 border-gray-600 flex items-center justify-center group-hover:border-[#d4af37] transition-colors">
                <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
            </div>
            <p class="text-xs font-bold text-gray-500 mt-3 uppercase tracking-wider text-center">Delivered</p>
            <p class="text-[10px] text-gray-600 mt-1">Pending</p>
        </div>
    </div>
</div>

<script>
    let mapInstance = null;
    let animationFrames = [];
    let polylineOverlays = []; // Used for hovering/focusing routes

    // OverlayView class for creating true CSS pulsing HTML markers
    class HTMLMarker extends google.maps.OverlayView {
        constructor(latlng, html, map) {
            super();
            this.latlng = latlng;
            this.html = html;
            this.div = null;
            this.setMap(map);
        }
        onAdd() {
            this.div = document.createElement('div');
            this.div.style.position = 'absolute';
            this.div.style.transform = 'translate(-50%, -50%)'; // Center precisely
            this.div.innerHTML = this.html;
            const panes = this.getPanes();
            panes.overlayMouseTarget.appendChild(this.div);
        }
        draw() {
            const overlayProjection = this.getProjection();
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

    function initMap() {
        if (mapInstance) return;

        // Premium Dark/Cyber theme
        const mapStyles = [
            { elementType: "geometry", stylers: [{ color: "#141414" }] },
            { elementType: "labels.text.stroke", stylers: [{ color: "#000000" }] },
            { elementType: "labels.text.fill", stylers: [{ color: "#808080" }] },
            { featureType: "administrative", elementType: "labels.text.fill", stylers: [{ color: "#d4af37" }] },
            { featureType: "road", elementType: "geometry", stylers: [{ color: "#1a1a1a" }] },
            { featureType: "road", elementType: "geometry.stroke", stylers: [{ color: "#333333" }] },
            { featureType: "road", elementType: "labels.text.fill", stylers: [{ color: "#555555" }] },
            { featureType: "road.highway", elementType: "geometry", stylers: [{ color: "#222222" }] },
            { featureType: "road.highway", elementType: "geometry.stroke", stylers: [{ color: "#333333" }] },
            { featureType: "water", elementType: "geometry", stylers: [{ color: "#0a0a0a" }] },
            { featureType: "water", elementType: "labels.text.fill", stylers: [{ color: "#333333" }] }
        ];

        mapInstance = new google.maps.Map(document.getElementById("delivery-map"), {
            center: { lat: 13.9, lng: 75.8 },
            zoom: 7,
            styles: mapStyles,
            disableDefaultUI: true,
            zoomControl: true,
            backgroundColor: '#141414'
        });

        const hubs = {
            mysore: { lat: 12.2958, lng: 76.6394 },
            bangalore: { lat: 12.9716, lng: 77.5946 },
            udupi: { lat: 13.3409, lng: 74.7421 },
            hubli: { lat: 15.3647, lng: 75.1240 }
        };

        // Vehicle Paths (SVG)
        const truckPath = "M17.4,0H5.6C2.5,0,0,3.5,0,6.6v34.8c0,3.1,2.5,5.6,5.6,5.6h11.8c3.1,0,5.6-2.5,5.6-5.6V6.6C23,3.5,20.5,0,17.4,0z M22.1,14.2v11.7l-2.7,0.4v-11.4L22.1,14.2z M20.6,10.8c-1,3.9-2.2,8.5-2.2,8.5H4.6l-2.2-8.5C2.4,10.8,11.3,7.8,20.6,10.8z M3.7,21.7v11.4l-2.7-0.4v-11.7L3.7,21.7z";
        const vanPath = "M28.4,15.2c-0.2-1.3-0.7-2.6-1.5-3.6c-0.8-1-1.8-1.7-2.9-2.2l-3-1.1c-1.3-0.5-2.6-0.7-4-0.7H13.6c-1.8,0-3.5,0.4-5.1,1.1 l-1.8,0.8c-1.7,0.7-3.2,1.8-4.5,3.2L1,14c-1,1.1-1.3,2.6-1,4.1l1.5,8c0.2,0.9,0.7,1.7,1.3,2.3c0.7,0.6,1.5,0.9,2.4,0.9h0.4 c0.8,2.7,3.3,4.6,6.3,4.6s5.5-1.9,6.3-4.6h3.4c0.8,2.7,3.3,4.6,6.3,4.6s5.5-1.9,6.3-4.6h1.2c1.3,0,2.3-1,2.3-2.3V18 C30,16.8,29.4,15.7,28.4,15.2z";
        const bikePath = "M19,13h-2v-2h-3v2H8.5c-1.5,0-2.8,1.1-3,2.5c-0.2,1.2,0.5,2.4,1.7,2.8L10.3,19l1.7-1l-3.3-1h3.1 c1.6,0,2.9-1.2,3-2.8l0-0.2H19v2h2v-4C21,13.4,20.1,13,19,13z M5.5,13C3.6,13,2,14.6,2,16.5S3.6,20,5.5,20S9,18.4,9,16.5 S7.4,13,5.5,13z M5.5,18C4.7,18,4,17.3,4,16.5S4.7,15,5.5,15S7,15.7,7,16.5S6.3,18,5.5,18z M18.5,13C16.6,13,15,14.6,15,16.5 S16.6,20,18.5,20S22,18.4,22,16.5S20.4,13,18.5,13z M18.5,18c-0.8,0-1.5-0.7-1.5-1.5s0.7-1.5,1.5-1.5s1.5,0.7,1.5,1.5 S19.3,18,18.5,18z";

        const deliveries = [
            {
                start: hubs.mysore,
                end: hubs.bangalore,
                color: '#3b82f6', // Neon Blue
                vehicle: truckPath,
                scale: 0.6,
                anchor: new google.maps.Point(12, 24),
                orderId: "TRK-9021-A",
                customer: "Heritage Hub → Retail",
                status: "In Transit",
                eta: "45 Mins",
                speed: 0.001, 
                progress: 0.2
            },
            {
                start: hubs.udupi,
                end: hubs.bangalore,
                color: '#d4af37', // Neon Gold
                vehicle: vanPath,
                scale: 0.8,
                anchor: new google.maps.Point(15, 15),
                orderId: "VAN-4022",
                customer: "Udupi Artisan → Ctrl",
                status: "Out for Delivery",
                eta: "12 Mins",
                speed: 0.002,
                progress: 0.7
            },
            {
                start: hubs.hubli,
                end: hubs.mysore,
                color: '#ef4444', // Neon Red
                vehicle: bikePath,
                scale: 1,
                anchor: new google.maps.Point(12, 16),
                orderId: "BIKE-007",
                customer: "Hubli Zone → Mysore",
                status: "Delayed (Traffic)",
                eta: "2 Hrs",
                speed: 0.0003,
                progress: 0.4
            }
        ];

        const infoWindow = new google.maps.InfoWindow({
            pixelOffset: new google.maps.Size(0, -30)
        });

        deliveries.forEach((delivery, index) => {
            // Glowing Route Effect using layered polylines
            // Base blur line
            const blurLine = new google.maps.Polyline({
                path: [delivery.start, delivery.end],
                geodesic: true,
                strokeColor: delivery.color,
                strokeOpacity: 0.2,
                strokeWeight: 12, // Thick blur
                map: mapInstance,
                clickable: false
            });
            // Core bright line
            const coreLine = new google.maps.Polyline({
                path: [delivery.start, delivery.end],
                geodesic: true,
                strokeColor: delivery.color,
                strokeOpacity: 1,
                strokeWeight: 3,
                map: mapInstance,
                clickable: false
            });
            polylineOverlays.push({blur: blurLine, core: coreLine});

            // HTML Pulsing Pickup Node
            const pickupHtml = `<div class="w-4 h-4 rounded-full border-2 shadow-[0_0_20px_10px_currentColor] animate-pulse" style="color: ${delivery.color}; background-color: #141414; border-color: ${delivery.color}; box-shadow: 0 0 15px 2px ${delivery.color}80;"></div>`;
            new HTMLMarker(delivery.start, pickupHtml, mapInstance);

            // HTML Destination Node
            const destHtml = `<div class="w-3 h-3 rounded-full border-2" style="background-color: #141414; border-color: ${delivery.color};"></div>`;
            new HTMLMarker(delivery.end, destHtml, mapInstance);

            // Animated Vehicle Marker
            const vehicleMarker = new google.maps.Marker({
                position: delivery.start,
                map: mapInstance,
                icon: {
                    path: delivery.vehicle,
                    scale: delivery.scale,
                    fillColor: "#ffffff",
                    fillOpacity: 1,
                    strokeWeight: 1.5,
                    strokeColor: delivery.color,
                    anchor: delivery.anchor,
                    rotation: Math.atan2(delivery.end.lng - delivery.start.lng, delivery.end.lat - delivery.start.lat) * 180 / Math.PI
                },
                zIndex: 999
            });

            const tooltipContent = `
                <div class="glass-panel" style="padding: 16px; border-radius: 12px; color: #f5ebd7; font-family: sans-serif; min-width: 240px; border: 1px solid ${delivery.color}50;">
                    <div style="color:${delivery.color}; font-size:10px; font-weight:bold; letter-spacing:1px; margin-bottom:4px;">${delivery.orderId}</div>
                    <div style="font-size:16px; font-weight:600; margin-bottom:12px; text-shadow: 0 0 5px ${delivery.color}50;">${delivery.customer}</div>
                    
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; font-size:12px;">
                        <span style="color:#888;">Status</span>
                        <span style="color:${delivery.color}; font-weight:bold; letter-spacing:0.5px;">${delivery.status}</span>
                    </div>
                    
                    <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                        <span style="color:#888;">ETA</span>
                        <span style="color:#fff; font-family:monospace; font-size:13px;">${delivery.eta}</span>
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

    // Simple interaction for the side panel to highlight routes
    window.focusRoute = function(index) {
        polylineOverlays.forEach((route, i) => {
            if(i !== index) {
                route.blur.setOptions({strokeOpacity: 0.05});
                route.core.setOptions({strokeOpacity: 0.2});
            } else {
                route.blur.setOptions({strokeOpacity: 0.5, strokeWeight: 20});
                route.core.setOptions({strokeOpacity: 1, strokeWeight: 5});
            }
        });
    };

    window.unfocusRoute = function() {
        polylineOverlays.forEach((route) => {
            route.blur.setOptions({strokeOpacity: 0.2, strokeWeight: 12});
            route.core.setOptions({strokeOpacity: 1, strokeWeight: 3});
        });
    };

</script>

{% endblock %}"""

with open('templates/supplier_tracking.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Successfully upgraded the live delivery map to premium UI.')
