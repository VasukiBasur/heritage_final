import os

dashboard_path = r'd:\dbmss\templates\dashboard.html'
with open(dashboard_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Insert before {% endblock %}
append_html = """
<!-- Geographic Distribution -->
<div class="glass-card p-6 mt-8 shadow-lg border border-brand-gold/20">
    <h2 class="text-xl font-serif text-brand-gold mb-4 flex items-center">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path></svg>
        Supply Chain Geographic Distribution
    </h2>
    <div id="supplyChainMap" class="w-full h-96 rounded bg-[#121212] z-10 border border-brand-gold/10"></div>
</div>

<!-- Real World Statistical Dashboard -->
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
    <div class="glass-card p-6 shadow-lg border border-brand-gold/20 bg-[#1a1a1a]">
        <h3 class="text-lg font-serif text-brand-gold mb-4">Production Output Trends</h3>
        <canvas id="productionTrendChart" class="w-full h-64"></canvas>
    </div>
    <div class="glass-card p-6 shadow-lg border border-brand-gold/20 bg-[#1a1a1a]">
        <h3 class="text-lg font-serif text-brand-gold mb-4">Order Fulfillment Status</h3>
        <canvas id="fulfillmentChart" class="w-full h-64"></canvas>
    </div>
</div>

<!-- Recent Production Logs with QR -->
<div class="glass-card p-6 mt-8 shadow-lg border border-brand-gold/20 bg-[#1a1a1a] overflow-x-auto">
    <h2 class="text-xl font-serif text-brand-gold mb-4">Recent Production Logs & Tracking</h2>
    <table class="w-full text-left border-collapse min-w-[600px]">
        <thead>
            <tr class="bg-[#121212] border-b border-brand-gold/30">
                <th class="p-3 text-brand-gold font-serif">Log ID</th>
                <th class="p-3 text-brand-gold font-serif">Artisan</th>
                <th class="p-3 text-brand-gold font-serif">Design</th>
                <th class="p-3 text-brand-gold font-serif">Status</th>
                <th class="p-3 text-brand-gold font-serif text-center">QR Tracking</th>
            </tr>
        </thead>
        <tbody>
            <tr class="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td class="p-3 font-bold text-brand-lightgold">#LOG-001</td>
                <td class="p-3">Ramesh Kumar</td>
                <td class="p-3">Mysore Silk Zari</td>
                <td class="p-3"><span class="px-2 py-1 bg-green-900/50 text-green-400 rounded text-[10px] uppercase tracking-wider border border-green-500/20">Completed</span></td>
                <td class="p-3 text-center flex justify-center"><img src="https://api.qrserver.com/v1/create-qr-code/?size=40x40&data=LOG001-COMPLETED-RAMESH" alt="QR" class="rounded shadow border border-brand-gold/50 hover:scale-150 transition-transform cursor-pointer"></td>
            </tr>
            <tr class="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td class="p-3 font-bold text-brand-lightgold">#LOG-002</td>
                <td class="p-3">Lakshmi Devi</td>
                <td class="p-3">Ilkal Checkered</td>
                <td class="p-3"><span class="px-2 py-1 bg-yellow-900/50 text-yellow-400 rounded text-[10px] uppercase tracking-wider border border-yellow-500/20">Active</span></td>
                <td class="p-3 text-center flex justify-center"><img src="https://api.qrserver.com/v1/create-qr-code/?size=40x40&data=LOG002-ACTIVE-LAKSHMI" alt="QR" class="rounded shadow border border-brand-gold/50 hover:scale-150 transition-transform cursor-pointer"></td>
            </tr>
            <tr class="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td class="p-3 font-bold text-brand-lightgold">#LOG-003</td>
                <td class="p-3">Basavaraj</td>
                <td class="p-3">Udupi Cotton</td>
                <td class="p-3"><span class="px-2 py-1 bg-blue-900/50 text-blue-400 rounded text-[10px] uppercase tracking-wider border border-blue-500/20">Quality Check</span></td>
                <td class="p-3 text-center flex justify-center"><img src="https://api.qrserver.com/v1/create-qr-code/?size=40x40&data=LOG003-QC-BASA" alt="QR" class="rounded shadow border border-brand-gold/50 hover:scale-150 transition-transform cursor-pointer"></td>
            </tr>
        </tbody>
    </table>
</div>

<!-- Chatbot Widget -->
<div class="fixed bottom-6 right-6 z-[100]">
    <div id="chat-window" class="hidden mb-4 w-80 h-96 bg-[#1a1a1a] border border-brand-gold/30 rounded shadow-[0_0_30px_rgba(0,0,0,0.8)] flex flex-col overflow-hidden">
        <div class="bg-brand-dark p-3 border-b border-brand-gold/20 flex justify-between items-center">
            <span class="font-serif text-brand-gold font-bold">Heritage AI Assistant</span>
            <button onclick="document.getElementById('chat-window').classList.add('hidden')" class="text-brand-lightgold hover:text-white">&times;</button>
        </div>
        <div id="chat-messages" class="flex-1 p-4 overflow-y-auto space-y-3 text-sm">
            <div class="bg-[#121212] p-2 rounded text-brand-lightgold inline-block max-w-[85%] border border-white/5">
                Hello! I am your AI supply chain assistant. How can I help you today?
            </div>
        </div>
        <div class="p-3 bg-brand-dark border-t border-brand-gold/20 flex">
            <input type="text" id="chat-input" placeholder="Ask about inventory..." class="flex-1 bg-[#121212] border border-brand-gold/30 text-white text-sm rounded-l px-3 py-2 focus:outline-none focus:border-brand-gold m-0">
            <button onclick="sendMessage()" class="bg-brand-gold text-black px-4 py-2 rounded-r font-bold hover:bg-yellow-500">Send</button>
        </div>
    </div>
    <button onclick="document.getElementById('chat-window').classList.toggle('hidden')" class="w-14 h-14 bg-brand-gold text-brand-black rounded-full shadow-[0_0_15px_rgba(212,175,55,0.6)] flex items-center justify-center hover:scale-110 transition-transform float-right">
        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"></path></svg>
        <span class="absolute top-0 right-0 w-3 h-3 bg-red-500 rounded-full border-2 border-[#121212]"></span>
    </button>
</div>
"""

extra_scripts = """
{% block extra_scripts %}
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', () => {
        // 1. Initialize Map
        const map = L.map('supplyChainMap', { zoomControl: false }).setView([14.5, 76.5], 6);
        L.control.zoom({ position: 'topright' }).addTo(map);
        
        // CartoDB Dark Matter theme
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; OpenStreetMap &copy; CartoDB',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(map);

        // Map Markers
        const markers = [
            { pos: [12.2958, 76.6394], title: "Mysore Hub (Silk)", color: "#D4AF37" },
            { pos: [15.9613, 76.1158], title: "Ilkal Weavers", color: "#D4AF37" },
            { pos: [13.3409, 74.7421], title: "Udupi Cotton", color: "#D4AF37" }
        ];

        markers.forEach(m => {
            const icon = L.divIcon({
                className: 'custom-div-icon',
                html: `<div style="background-color:${m.color};width:12px;height:12px;border-radius:50%;box-shadow:0 0 10px ${m.color}"></div>`,
                iconSize: [12, 12]
            });
            L.marker(m.pos, {icon: icon}).addTo(map).bindPopup(`<strong style="color:black">${m.title}</strong>`);
        });

        // 2. Initialize Charts
        Chart.defaults.color = '#f0e6d2';
        Chart.defaults.borderColor = 'rgba(212,175,55,0.1)';

        new Chart(document.getElementById('productionTrendChart'), {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Sarees Produced',
                    data: [120, 150, 180, 140, 200, 230],
                    borderColor: '#D4AF37',
                    backgroundColor: 'rgba(212,175,55,0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } },
                    x: { grid: { display: false } }
                }
            }
        });

        new Chart(document.getElementById('fulfillmentChart'), {
            type: 'doughnut',
            data: {
                labels: ['Delivered', 'In Transit', 'Processing'],
                datasets: [{
                    data: [65, 20, 15],
                    backgroundColor: ['#22c55e', '#3b82f6', '#eab308'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: { legend: { position: 'bottom' } }
            }
        });
    });

    // Chatbot Logic
    function sendMessage() {
        const input = document.getElementById('chat-input');
        const text = input.value.trim();
        if(!text) return;
        
        const msgs = document.getElementById('chat-messages');
        
        // Add user msg
        msgs.innerHTML += `<div class="bg-brand-gold text-black p-2 rounded inline-block max-w-[85%] self-end ml-auto mb-3 shadow">${text}</div>`;
        input.value = '';
        msgs.scrollTop = msgs.scrollHeight;

        // Mock AI response
        setTimeout(() => {
            msgs.innerHTML += `<div class="bg-[#121212] p-2 rounded text-brand-lightgold inline-block max-w-[85%] border border-white/5 mb-3 shadow">Checking database... Currently, Mysore Silk Zari production is running at 92% capacity.</div>`;
            msgs.scrollTop = msgs.scrollHeight;
        }, 1000);
    }
</script>
{% endblock %}
"""

if "supplyChainMap" not in content:
    content = content.replace('{% endblock %}', append_html + "\n" + extra_scripts)
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Dashboard fully restored with Map, Charts, QR logs, and Chatbot.")
else:
    print("Already restored.")
