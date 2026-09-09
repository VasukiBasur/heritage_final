// Mock Google Maps API to check for obvious runtime errors
global.google = {
    maps: {
        Map: class {},
        Polyline: class {
            constructor(opts) { this.opts = opts; }
            get(prop) { return this.opts[prop]; }
            set(prop, val) { this.opts[prop] = val; }
        },
        Marker: class {
            constructor(opts) { this.opts = opts; }
            setPosition() {}
            getIcon() { return this.opts.icon; }
            setIcon() {}
        },
        OverlayView: class {
            setMap() {}
            getPanes() { return { overlayMouseTarget: { appendChild: () => {} } }; }
            getProjection() { return { fromLatLngToDivPixel: () => ({ x: 0, y: 0 }) }; }
        },
        Point: class {},
        LatLng: class {},
        SymbolPath: { FORWARD_CLOSED_ARROW: 'arrow' }
    }
};

const mapInstance = new google.maps.Map();
let polylineOverlays = [];

class HTMLMarker extends google.maps.OverlayView {
    constructor(latlng, html, map, offset = {x: 0, y: 0}, zIndex = 0) {
        super();
        this.latlng = latlng;
        this.html = html;
        this.div = null;
        this.offset = offset;
        this.z = zIndex;
        this.setMap(map);
    }
}

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

const hubs = {
    bangalore: { lat: 12.9716, lng: 77.5946 },
    mysore: { lat: 12.2958, lng: 76.6394 },
    udupi: { lat: 13.3409, lng: 74.7421 },
    chitradurga: { lat: 14.2255, lng: 76.4010 },
    hubli: { lat: 15.3647, lng: 75.1240 },
    belgaum: { lat: 15.8497, lng: 74.4977 },
    bellary: { lat: 15.1394, lng: 76.9214 },
    shimoga: { lat: 13.9299, lng: 75.5681 },
    mangalore: { lat: 12.9141, lng: 74.8560 },
    chennai: { lat: 13.0827, lng: 80.2707 },
    hyderabad: { lat: 17.3850, lng: 78.4867 },
    kochi: { lat: 9.9312, lng: 76.2673 },
    goa: { lat: 15.2993, lng: 74.1240 }
};

const deliveries = [
    {
        start: hubs.bangalore,
        mid: hubs.hassan || { lat: 13.0068, lng: 76.1004 },
        end: hubs.mysore,
        color: '#3b82f6', // Blue
        vehicle: 'truckPath',
        scale: 0.6,
        id: 'TRK-101',
        title: 'Blr → Mysuru',
        status: 'In Transit',
        eta: '45 mins',
        dist: '120 km',
        progress: 0.3,
        speed: 0.002
    },
    {
        start: hubs.udupi,
        mid: hubs.shimoga,
        end: hubs.chitradurga,
        color: '#f97316', // Orange
        vehicle: 'vanPath',
        scale: 0.8,
        id: 'VAN-202',
        title: 'Udupi → Chitrad',
        status: 'In Transit',
        eta: '2 hrs 15m',
        dist: '210 km',
        progress: 0.6,
        speed: 0.0015
    },
    {
        start: hubs.hubli,
        mid: hubs.davangere || { lat: 14.4644, lng: 75.9218 },
        end: hubs.mysore,
        color: '#ef4444', // Red
        vehicle: 'truckPath',
        scale: 0.6,
        id: 'TRK-303',
        title: 'Hubli → Mysuru',
        status: 'Delayed',
        eta: 'Unknown',
        dist: '390 km',
        progress: 0.5,
        speed: 0.0005
    },
    {
        start: hubs.belgaum,
        mid: hubs.hubli,
        end: hubs.bellary,
        color: '#a855f7', // Purple
        vehicle: 'truckPath',
        scale: 0.6,
        id: 'TRK-404',
        title: 'Belagavi → Ballari',
        status: 'In Transit',
        eta: '4 hrs',
        dist: '280 km',
        progress: 0.2,
        speed: 0.001
    },
    {
        start: hubs.shimoga,
        mid: hubs.udupi,
        end: hubs.mangalore,
        color: '#22c55e', // Green
        vehicle: 'bikePath',
        scale: 1.0,
        id: 'BIKE-505',
        title: 'Shivamogga → Mangaluru',
        status: 'Completed',
        eta: 'Delivered',
        dist: '0 km',
        progress: 1.0,
        speed: 0
    },
    {
        start: hubs.chennai,
        mid: { lat: 12.9, lng: 79.1 }, // Vellore
        end: hubs.bangalore,
        color: '#eab308', // Yellow
        vehicle: 'vanPath',
        scale: 0.8,
        id: 'VAN-606',
        title: 'Chennai → Blr',
        status: 'Pending Pickup',
        eta: '6 hrs',
        dist: '350 km',
        progress: 0.05,
        speed: 0.001
    },
    {
        start: hubs.hyderabad,
        mid: { lat: 15.8, lng: 78.0 }, // Kurnool
        end: hubs.bangalore,
        color: '#ec4899', // Pink
        vehicle: 'truckPath',
        scale: 0.6,
        id: 'TRK-707',
        title: 'Hyderabad → Blr',
        status: 'In Transit',
        eta: '8 hrs',
        dist: '570 km',
        progress: 0.4,
        speed: 0.0012
    },
    {
        start: hubs.kochi,
        mid: { lat: 11.2, lng: 76.5 }, // Coimbatore area
        end: hubs.mysore,
        color: '#06b6d4', // Cyan
        vehicle: 'truckPath',
        scale: 0.6,
        id: 'TRK-808',
        title: 'Kochi → Mysuru',
        status: 'In Transit',
        eta: '5 hrs',
        dist: '380 km',
        progress: 0.7,
        speed: 0.0014
    }
];

let lineAnimations = [];
const cardsHtml = [];

deliveries.forEach((delivery, index) => {
    console.log(`Processing delivery ${index}...`);
    const curvePoints = getBezierCurve(delivery.start, delivery.mid, delivery.end, 100);

    const blurLine = new google.maps.Polyline({
        path: curvePoints,
        geodesic: true,
        strokeColor: delivery.color,
        strokeOpacity: 0.25,
        strokeWeight: 16,
        map: mapInstance,
        clickable: false
    });

    const coreLine = new google.maps.Polyline({
        path: curvePoints,
        geodesic: true,
        strokeColor: delivery.color,
        strokeOpacity: 1,
        strokeWeight: 3,
        icons: [{
            icon: {
                path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
                scale: 2.5,
                strokeColor: "#ffffff",
                fillColor: "#ffffff",
                fillOpacity: 1
            },
            offset: '0%',
            repeat: '120px'
        }],
        map: mapInstance,
        clickable: false
    });
    polylineOverlays.push({blur: blurLine, core: coreLine});
    lineAnimations.push(coreLine);

    new HTMLMarker(delivery.start, `html1`, mapInstance, {x:0,y:0}, 1);
    new HTMLMarker(delivery.end, `html2`, mapInstance, {x:0,y:0}, 2);
    new HTMLMarker(delivery.mid, `html3`, mapInstance, {x: 0, y: -25}, 10);

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
            anchor: new google.maps.Point(12, 12),
            rotation: 0
        },
        zIndex: 999
    });

    function getHeading(p1, p2) {
        return Math.atan2(p2.lng - p1.lng, p2.lat - p1.lat) * 180 / Math.PI;
    }

    function animateVehicle() {
        if (delivery.speed > 0) {
            delivery.progress += delivery.speed;
            if (delivery.progress >= 1.0) delivery.progress = 0; 
        }
        
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
            
            const heading = getHeading(p1, p2);
            const icon = vehicleMarker.getIcon();
            icon.rotation = heading;
            vehicleMarker.setIcon(icon);
        }
    }
    if(delivery.speed > 0) {
        animateVehicle();
    } else {
        vehicleMarker.setPosition(curvePoints[curvePoints.length-1]);
        const p1 = curvePoints[curvePoints.length-2];
        const p2 = curvePoints[curvePoints.length-1];
        const heading = getHeading(p1, p2);
        const icon = vehicleMarker.getIcon();
        icon.rotation = heading;
        vehicleMarker.setIcon(icon);
    }
    
    cardsHtml.push(`success`);
});
console.log("SUCCESS!");
