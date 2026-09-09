
    document.addEventListener('DOMContentLoaded', () => {
        // 1. Initialize Advanced ERP Map (Leaflet)
        const map = L.map('supplyChainMap', { zoomControl: false, scrollWheelZoom: false }).setView([20.5, 78.9], 4);
        L.control.zoom({ position: 'topright' }).addTo(map);
        
        // Luxury Dark Theme Tiles
        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
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

        // 2. Initialize Analytics Charts
        Chart.defaults.color = '#f0e6d2';
        Chart.defaults.borderColor = 'rgba(212,175,55,0.05)';
        Chart.defaults.font.family = 'Inter';

        const legendOptions = {
            display: true, position: 'top', labels: { boxWidth: 15, color: '#f0e6d2', padding: 10 }
        };

        // 1. Monthly Revenue Chart (Line)
        new Chart(document.getElementById('revenueChart'), {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Revenue (in Millions)',
                    data: [1.2, 1.5, 1.4, 1.8, 1.9, 2.3],
                    borderColor: '#D4AF37', backgroundColor: 'rgba(212,175,55,0.1)',
                    borderWidth: 2, fill: true, tension: 0.4
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: legendOptions }, scales: { x: { grid: { display: false } }, y: { beginAtZero: true } } }
        });

        // 2. Orders Analytics (Bar)
        new Chart(document.getElementById('ordersChart'), {
            type: 'bar',
            data: {
                labels: ['Silk', 'Cotton', 'Linen', 'Wool', 'Zari'],
                datasets: [{
                    label: 'Orders',
                    data: [450, 320, 150, 90, 120],
                    backgroundColor: ['#D4AF37', '#A3A3A3', '#8B6508', '#CD853F', '#DEB887'],
                    barPercentage: 0.6
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: legendOptions }, scales: { x: { grid: { display: false } } } }
        });

        // 3. Product Sales Graph (Horizontal Bar)
        new Chart(document.getElementById('salesChart'), {
            type: 'bar',
            data: {
                labels: ['Mysore Silk', 'Ilkal', 'Banarasi', 'Dharwad'],
                datasets: [{
                    label: 'Units Sold',
                    data: [1200, 850, 640, 520],
                    backgroundColor: 'rgba(212, 175, 55, 0.4)',
                    borderColor: '#D4AF37', borderWidth: 1
                }]
            },
            options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: legendOptions }, scales: { x: { beginAtZero: true }, y: { grid: { display: false } } } }
        });

        // 4. Shipment Status Pie Chart
        new Chart(document.getElementById('shipmentChart'), {
            type: 'pie',
            data: {
                labels: ['Delivered', 'In Transit', 'Pending', 'Delayed'],
                datasets: [{
                    data: [65, 20, 10, 5],
                    backgroundColor: ['#22c55e', '#3b82f6', '#eab308', '#ef4444'],
                    borderColor: '#151515', borderWidth: 2
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: legendOptions } }
        });

        // 5. Inventory Trends (Line)
        new Chart(document.getElementById('inventoryChart'), {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                datasets: [{
                    label: 'Raw Silk',
                    data: [500, 480, 420, 350],
                    borderColor: '#3b82f6', tension: 0.2
                }, {
                    label: 'Zari Thread',
                    data: [200, 190, 150, 180],
                    borderColor: '#D4AF37', tension: 0.2
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: legendOptions }, scales: { x: { grid: { display: false } } } }
        });

        // 6. User Growth Analytics (Doughnut)
        new Chart(document.getElementById('userGrowthChart'), {
            type: 'doughnut',
            data: {
                labels: ['New Customers', 'Returning Customers', 'New Artisans'],
                datasets: [{
                    data: [40, 55, 5],
                    backgroundColor: ['#A3A3A3', '#D4AF37', '#65a30d'],
                    borderColor: '#151515', borderWidth: 3
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, cutout: '75%', plugins: { legend: legendOptions } }
        });

        
        });


        
    
    // Table Search Filter
    window.handleSearch = function() {
        const input = document.getElementById("dashboardSearch").value.toLowerCase();
        const resultsContainer = document.getElementById("searchResults");
        const resultsList = document.getElementById("searchResultsList");
        
        if (input.length < 2) {
            resultsContainer.classList.add("hidden");
            return;
        }
        
        resultsContainer.classList.remove("hidden");
        
        // Mock database for global search
        const mockData = [
            { name: "Kavitha Weavers", type: "Artisan", desc: "Expert in Kanchipuram Silk", icon: "🧶" },
            { name: "Order #ORD-KAV99", type: "Order", desc: "Pending Shipment to Kavitha R.", icon: "📦" },
            { name: "Kavi Gold Zari", type: "Raw Material", desc: "Supplier: Surat Hub", icon: "✨" },
            { name: "Mysore Silk Zari", type: "Product", desc: "Active Production", icon: "👘" },
            { name: "Abdul Kareem", type: "Artisan", desc: "Master Weaver", icon: "🧶" },
            { name: "Order #ORD-991", type: "Order", desc: "Delivered", icon: "📦" },
            { name: "Surat Textile Hub", type: "Supplier", desc: "Premium Zari Yarns", icon: "🧵" }
        ];
        
        const filtered = mockData.filter(item => item.name.toLowerCase().includes(input) || item.desc.toLowerCase().includes(input));
        
        if (filtered.length === 0) {
            resultsList.innerHTML = `<li class="p-4 text-center text-gray-500 text-sm">No results found for "${input}"</li>`;
            return;
        }
        
        resultsList.innerHTML = filtered.map(item => `
            <li class="p-3 border-b border-white/5 hover:bg-brand-gold/10 cursor-pointer flex items-center gap-3 transition-colors" onclick=\"document.getElementById('searchResults').classList.add('hidden'); window.addMockLog('${item.name}'); document.querySelector('table').scrollIntoView({behavior: 'smooth'});\">
                <div class="w-8 h-8 rounded-full bg-[#121212] border border-brand-gold/20 flex items-center justify-center text-lg">${item.icon}</div>
                <div>
                    <p class="text-brand-gold font-bold text-sm">${item.name}</p>
                    <p class="text-gray-400 text-xs">${item.type} &bull; ${item.desc}</p>
                </div>
            </li>
        `).join("");
    };
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('#dashboardSearch') && !e.target.closest('#searchResults')) {
            const resultsContainer = document.getElementById("searchResults");
            if(resultsContainer) resultsContainer.classList.add("hidden");
        }
    });

    
    window.updateStatus = function(btn) {
        const row = btn.closest('tr');
        const select = row.querySelector('select');
        const badge = row.querySelector('.status-badge') || row.querySelector('span[class*="rounded text-xs border"]');
        if (select && badge) {
            const newStatus = select.value;
            badge.innerText = newStatus;
            badge.className = "status-badge px-3 py-1 rounded text-xs border bg-green-900/40 text-green-400 border-green-500/50";
            // Flash effect to show it worked without annoying alert
            badge.style.opacity = '0.5';
            setTimeout(() => badge.style.opacity = '1', 200);
        } else {
            console.error("Could not find badge element in row", row);
        }
    };

    // Add Mock Log Function
    window.addMockLog = function() {
        const tbody = document.querySelector('table tbody');
        const newId = Math.floor(Math.random() * 100) + 30;
        

        const designs = [
            {
                name: 'Mysore Silk Zari', img: 'mysore_silk_zari.png.jpeg',
                id: 'PRD-MYS-01', category: 'Sarees', fabric: 'Pure Silk',
                color: 'Royal Blue & Gold', size: '6.2 Meters', pattern: 'Solid with Zari Border',
                price: '₹8500.00', desc: 'Authentic handwoven Mysore silk saree with pure gold zari borders.'
            },
            {
                name: 'Ilkal Checkered', img: 'ilkal_checkered.png.jpeg',
                id: 'PRD-ILK-02', category: 'Sarees', fabric: 'Cotton Silk Blend',
                color: 'Red & Black Checkered', size: '6.0 Meters', pattern: 'Checkered',
                price: '₹3200.00', desc: 'Traditional Ilkal saree featuring iconic red borders and checkered body.'
            },
            {
                name: 'Dharwad Cotton', img: 'dharwad_cotton_saree.png.jpeg',
                id: 'PRD-DHA-03', category: 'Sarees', fabric: 'Pure Cotton',
                color: 'Earth Brown & Green', size: '5.5 Meters', pattern: 'Earthy Stripes',
                price: '₹2400.00', desc: 'Soft, breathable pure Dharwad cotton with naturally dyed threads.'
            },
            {
                name: 'Udupi Cotton', img: 'udupi_silk.png.jpeg',
                id: 'PRD-UDU-04', category: 'Sarees', fabric: 'Fine Cotton',
                color: 'Mustard Yellow', size: '5.5 Meters', pattern: 'Minimalist Border',
                price: '₹1800.00', desc: 'Classic Udupi weave, lightweight and perfect for daily wear.'
            },
            {
                name: 'Banarasi Brocade', img: 'banarasi_brocode_saree.png.jpeg',
                id: 'PRD-BAN-05', category: 'Sarees', fabric: 'Brocade Silk',
                color: 'Crimson Red', size: '6.5 Meters', pattern: 'Floral Brocade',
                price: '₹12500.00', desc: 'Opulent Banarasi silk woven with intricate golden floral motifs.'
            }
        ];

        
        const artisans = ['Ramesh Kumar', 'Lakshmi Devi', 'Basavaraj', 'Sunitha Reddy', 'Abdul Kareem', 'Savitri Bai', 'Gowramma', 'Manjunath'];
        
        let design = designs[Math.floor(Math.random() * designs.length)];
        if (customName) {
            design = { ...design, name: customName }; // Override name with searched item
        }
        const artisan = artisans[Math.floor(Math.random() * artisans.length)];
        const qty = Math.floor(Math.random() * 5) + 1;
        const payout = (qty * 850).toFixed(2);
        
        
        
        // Send details to backend so they can be retrieved by the scanner
        fetch('/api/add_log', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                log_id: newId,
                product_details: design
            })
        });
        
        const payloadText = `http://{{ lan_ip }}:5000/scan/${newId}`;
        const encodedPayload = encodeURIComponent(payloadText);

        const newRow = document.createElement('tr');
        newRow.className = "border-b border-white/5 hover:bg-white/5 transition-colors bg-brand-gold/20";
        newRow.innerHTML = `
            <td class="p-3"><img src="/static/images/${design.img}" class="w-10 h-10 object-cover rounded border border-brand-gold/30" alt="${design.name}"></td>
            <td class="p-3 font-bold text-brand-gold">#${newId}</td>
            <td class="p-3 font-bold text-gray-200">${artisan}</td>
            <td class="p-3 font-bold text-gray-200">${design.name}</td>
            <td class="p-3"><span class="status-badge px-3 py-1 bg-blue-900/40 text-blue-400 rounded text-xs border border-blue-500/50">Pending</span></td>
            <td class="p-3">
                <div class="flex items-center space-x-2">
                    <select class="bg-[#121212] border border-brand-gold/30 text-gray-300 text-xs rounded px-2 py-1 outline-none font-bold">
                        <option>Order Placed</option>
                        <option>Raw Material Supply</option>
                        <option>Weaving</option>
                        <option>Quality Check</option>
                        <option>Shipped</option>
                        <option>Delivered</option>
                    </select>
                    <button class="bg-brand-gold text-brand-black px-2 py-1 rounded text-xs font-bold hover:bg-yellow-500" onclick="updateStatus(this)">Update</button>
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=http%3A%2F%2F{{ (lan_ip ~ ':5000') | urlencode }}%2Fscan%2F28&color=000000&bgcolor=FFFFFF" alt="QR" class="w-8 h-8 object-contain border border-brand-gold/50 rounded cursor-pointer transition-transform duration-300 hover:scale-[6] hover:-translate-x-12 hover:-translate-y-8 relative z-50 shadow-2xl">
                </div>
            </td>
            <td class="p-3 text-gray-200 font-bold">${qty}</td>
            <td class="p-3 text-brand-gold font-bold">₹${payout}</td>
        `;
        tbody.insertBefore(newRow, tbody.firstChild);
        setTimeout(() => {
            newRow.classList.remove('bg-brand-gold/20');
        }, 1000);
    };

    // Chatbot Logic
    function sendMessage() {
        const input = document.getElementById('chat-input');
        const text = input.value.trim();
        if(!text) return;
        
        const msgs = document.getElementById('chat-messages');
        
        msgs.innerHTML += `<div class="bg-brand-gold text-black p-2 rounded inline-block max-w-[85%] self-end ml-auto mb-3 shadow">${text}</div>`;
        input.value = '';
        msgs.scrollTop = msgs.scrollHeight;

        setTimeout(() => {
            msgs.innerHTML += `<div class="bg-[#121212] p-2 rounded text-brand-lightgold inline-block max-w-[85%] border border-white/5 mb-3 shadow">Checking database... Currently, Mysore Silk Zari production is running at 92% capacity.</div>`;
            msgs.scrollTop = msgs.scrollHeight;
        }, 1000);
    }
