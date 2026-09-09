import re

with open('templates/supplier_tracking.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the deliveries array
new_deliveries = """const hubs = {
            mysore: { lat: 12.2958, lng: 76.6394 },
            bangalore: { lat: 12.9716, lng: 77.5946 },
            udupi: { lat: 13.3409, lng: 74.7421 },
            hubli: { lat: 15.3647, lng: 75.1240 },
            mangalore: { lat: 12.9141, lng: 74.8560 },
            belgaum: { lat: 15.8497, lng: 74.4977 },
            bellary: { lat: 15.1394, lng: 76.9214 }
        };

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
                color: '#f97316', // Neon Orange
                vehicle: vanPath,
                scale: 0.8,
                anchor: new google.maps.Point(15, 15),
                orderId: "VAN-4022",
                customer: "Udupi Artisan → Ctrl Hub",
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
            },
            {
                start: hubs.mangalore,
                end: hubs.hubli,
                color: '#d4af37', // Neon Gold
                vehicle: truckPath,
                scale: 0.6,
                anchor: new google.maps.Point(12, 24),
                orderId: "TRK-8014-X",
                customer: "Port Export → Hubli Base",
                status: "In Transit",
                eta: "3.5 Hrs",
                speed: 0.0008,
                progress: 0.15
            },
            {
                start: hubs.belgaum,
                end: hubs.bellary,
                color: '#a855f7', // Neon Purple
                vehicle: vanPath,
                scale: 0.8,
                anchor: new google.maps.Point(15, 15),
                orderId: "VAN-3099",
                customer: "Belgaum Weavers → Bellary",
                status: "In Transit",
                eta: "1 Hr 20 Mins",
                speed: 0.0012,
                progress: 0.6
            },
            {
                start: hubs.bellary,
                end: hubs.bangalore,
                color: '#10b981', // Neon Green
                vehicle: truckPath,
                scale: 0.6,
                anchor: new google.maps.Point(12, 24),
                orderId: "TRK-7711-Z",
                customer: "Bellary Hub → Flagship Store",
                status: "Near Destination",
                eta: "5 Mins",
                speed: 0.003,
                progress: 0.92
            }
        ];"""

# Replace the deliveries block
start = text.find('const hubs = {')
end = text.find('const infoWindow')
if start != -1 and end != -1:
    text = text[:start] + new_deliveries + '\n\n        ' + text[end:]

# 2. Update the Side Panel to match the new deliveries
new_side_panel = """<div class="space-y-4">
                <!-- Status Card 1 -->
                <div class="bg-gradient-to-r from-blue-900/20 to-black p-4 rounded-lg border border-blue-500/30 hover:border-blue-500 transition-colors cursor-pointer" onmouseover="focusRoute(0)" onmouseout="unfocusRoute()">
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs font-mono text-blue-400 bg-blue-900/30 px-2 py-0.5 rounded border border-blue-500/20">TRK-9021-A</span>
                        <span class="text-[10px] font-bold text-white uppercase tracking-wider">45 Mins</span>
                    </div>
                    <div class="text-sm font-semibold text-[#f5ebd7] truncate">Heritage Hub &rarr; Retail</div>
                    <div class="flex items-center mt-2">
                        <div class="w-full bg-black rounded-full h-1">
                            <div class="bg-blue-500 h-1 rounded-full relative" style="width: 20%">
                                <span class="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 bg-white rounded-full shadow-[0_0_5px_#fff]"></span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Status Card 2 -->
                <div class="bg-gradient-to-r from-orange-900/20 to-black p-4 rounded-lg border border-orange-500/30 hover:border-orange-500 transition-colors cursor-pointer" onmouseover="focusRoute(1)" onmouseout="unfocusRoute()">
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs font-mono text-orange-400 bg-orange-900/30 px-2 py-0.5 rounded border border-orange-500/20">VAN-4022</span>
                        <span class="text-[10px] font-bold text-white uppercase tracking-wider">12 Mins</span>
                    </div>
                    <div class="text-sm font-semibold text-[#f5ebd7] truncate">Udupi Artisan &rarr; Ctrl</div>
                    <div class="flex items-center mt-2">
                        <div class="w-full bg-black rounded-full h-1">
                            <div class="bg-orange-500 h-1 rounded-full relative" style="width: 70%">
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

                <!-- Status Card 4 -->
                <div class="bg-gradient-to-r from-purple-900/20 to-black p-4 rounded-lg border border-purple-500/30 hover:border-purple-500 transition-colors cursor-pointer" onmouseover="focusRoute(4)" onmouseout="unfocusRoute()">
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs font-mono text-purple-400 bg-purple-900/30 px-2 py-0.5 rounded border border-purple-500/20">VAN-3099</span>
                        <span class="text-[10px] font-bold text-white uppercase tracking-wider">1h 20m</span>
                    </div>
                    <div class="text-sm font-semibold text-[#f5ebd7] truncate">Belgaum &rarr; Bellary</div>
                    <div class="flex items-center mt-2">
                        <div class="w-full bg-black rounded-full h-1">
                            <div class="bg-purple-500 h-1 rounded-full relative" style="width: 60%">
                                <span class="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 bg-white rounded-full shadow-[0_0_5px_#fff]"></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>"""

start_panel = text.find('<div class="space-y-4">')
end_panel = text.find('<div class="mt-6 pt-4 border-t border-[#d4af37]/10">')
if start_panel != -1 and end_panel != -1:
    text = text[:start_panel] + new_side_panel + '\n            ' + text[end_panel:]


with open('templates/supplier_tracking.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Successfully added 6 distinct routes and updated side panel.')
