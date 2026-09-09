import re

dashboard_path = r'd:\dbmss\templates\dashboard.html'
with open(dashboard_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the Charts HTML
old_charts_html = """<!-- Real World Statistical Dashboard -->
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
    <div class="glass-card p-6 shadow-lg border border-brand-gold/20 bg-[#1a1a1a]">
        <h3 class="text-lg font-serif text-brand-gold mb-4">Production Output Trends</h3>
        <canvas id="productionTrendChart" class="w-full h-64"></canvas>
    </div>
    <div class="glass-card p-6 shadow-lg border border-brand-gold/20 bg-[#1a1a1a]">
        <h3 class="text-lg font-serif text-brand-gold mb-4">Order Fulfillment Status</h3>
        <canvas id="fulfillmentChart" class="w-full h-64"></canvas>
    </div>
</div>"""

new_charts_html = """<!-- Order Fulfillment Section -->
<div class="mt-8 mb-4">
    <h3 class="text-xl font-serif text-brand-gold mb-4 pb-2">Order Fulfillment</h3>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="glass-card p-6 shadow-lg border border-brand-gold/10 bg-[#151515]">
            <span class="text-[10px] tracking-widest text-brand-lightgold uppercase mb-6 opacity-70 block">Fulfillment Status</span>
            <div class="h-64"><canvas id="fulfillmentStatusChart"></canvas></div>
        </div>
        <div class="glass-card p-6 shadow-lg border border-brand-gold/10 bg-[#151515]">
            <span class="text-[10px] tracking-widest text-brand-lightgold uppercase mb-6 opacity-70 block">Volume By Category</span>
            <div class="h-64"><canvas id="volumeCategoryChart"></canvas></div>
        </div>
    </div>
</div>

<!-- Resources & Logistics Section -->
<div class="mt-8 mb-4">
    <h3 class="text-xl font-serif text-brand-gold mb-4 pb-2">Resources & Logistics</h3>
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="glass-card p-6 shadow-lg border border-brand-gold/10 bg-[#151515]">
            <span class="text-[10px] tracking-widest text-brand-lightgold uppercase mb-6 opacity-70 block">User Demographics</span>
            <div class="h-64"><canvas id="userDemoChart"></canvas></div>
        </div>
        <div class="glass-card p-6 shadow-lg border border-brand-gold/10 bg-[#151515]">
            <span class="text-[10px] tracking-widest text-brand-lightgold uppercase mb-6 opacity-70 block">Top Stock Availability</span>
            <div class="h-64 pb-4"><canvas id="topStockChart"></canvas></div>
        </div>
        <div class="glass-card p-6 shadow-lg border border-brand-gold/10 bg-[#151515]">
            <span class="text-[10px] tracking-widest text-brand-lightgold uppercase mb-6 opacity-70 block">Delivery Performance</span>
            <div class="h-64"><canvas id="deliveryPerfChart"></canvas></div>
        </div>
    </div>
</div>"""

if old_charts_html in content:
    content = content.replace(old_charts_html, new_charts_html)

# 2. Replace the Chart JS logic
old_js_start = "// 2. Initialize Charts"
old_js_end = "// Chatbot Logic"

js_start_idx = content.find(old_js_start)
js_end_idx = content.find(old_js_end)

new_js = """// 2. Initialize Advanced Charts
        Chart.defaults.color = '#f0e6d2';
        Chart.defaults.borderColor = 'rgba(212,175,55,0.05)';
        Chart.defaults.font.family = 'Inter';

        // Custom legend labels plugin
        const legendOptions = {
            display: true,
            position: 'top',
            labels: { boxWidth: 30, color: '#f0e6d2', padding: 15, usePointStyle: false, borderRadius: 0 }
        };

        // 1. Fulfillment Status (Bar)
        new Chart(document.getElementById('fulfillmentStatusChart'), {
            type: 'bar',
            data: {
                labels: ['Processing', 'Shipped'],
                datasets: [{
                    label: 'Orders',
                    data: [1.0, 1.0],
                    backgroundColor: ['#D4AF37', '#A3A3A3'],
                    barPercentage: 0.6
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: true, position: 'top', align: 'end', labels: { boxWidth: 20 } } },
                scales: {
                    y: { beginAtZero: true, max: 1.0, ticks: { stepSize: 0.1 } },
                    x: { grid: { display: false } }
                }
            }
        });

        // 2. Volume by Category (Pie)
        new Chart(document.getElementById('volumeCategoryChart'), {
            type: 'pie',
            data: {
                labels: ['Silk Sarees', 'Cotton Sarees', 'Shawls', 'Fabrics'],
                datasets: [{
                    data: [45, 30, 15, 10],
                    backgroundColor: ['#D4AF37', '#B8860B', '#CD853F', '#DEB887'],
                    borderColor: '#151515',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: legendOptions }
            }
        });

        // 3. User Demographics (Pie)
        new Chart(document.getElementById('userDemoChart'), {
            type: 'pie',
            data: {
                labels: ['Admin', 'Customer', 'Delivery Partner', 'Supplier', 'Weaver'],
                datasets: [{
                    data: [5, 40, 15, 10, 30],
                    backgroundColor: ['#D4AF37', '#A3A3A3', '#65a30d', '#3b82f6', '#ea580c'],
                    borderColor: '#151515',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: true, position: 'top', labels: { boxWidth: 20, padding: 10 } } }
            }
        });

        // 4. Top Stock Availability (Horizontal Bar)
        new Chart(document.getElementById('topStockChart'), {
            type: 'bar',
            data: {
                labels: ['Banarasi Zari Dupatta', 'Mysore Royal Saree', 'Kashmiri Pashmina Shawl', 'Navalgund Geometric Carpet'],
                datasets: [{
                    label: 'Stock Units',
                    data: [80, 45, 10, 5],
                    backgroundColor: 'rgba(212, 175, 55, 0.2)',
                    borderColor: '#D4AF37',
                    borderWidth: 1,
                    barPercentage: 0.5
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: true, position: 'top', align: 'end' } },
                scales: {
                    x: { beginAtZero: true, max: 80, ticks: { stepSize: 20 } },
                    y: { grid: { display: false }, ticks: { color: '#f0e6d2', font: { size: 10 } } }
                }
            }
        });

        // 5. Delivery Performance (Doughnut)
        new Chart(document.getElementById('deliveryPerfChart'), {
            type: 'doughnut',
            data: {
                labels: ['Delivered On Time', 'Delayed', 'Pending'],
                datasets: [{
                    data: [75, 5, 20],
                    backgroundColor: ['#22c55e', '#ef4444', '#eab308'],
                    borderColor: '#151515',
                    borderWidth: 4
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                cutout: '80%',
                plugins: { legend: { display: true, position: 'top', labels: { boxWidth: 20, padding: 10 } } }
            }
        });
    });

    """

if js_start_idx != -1 and js_end_idx != -1:
    content = content[:js_start_idx] + new_js + content[js_end_idx:]

# 3. Simplify Production Logs QR styling back to "previous"
# The user didn't like the over-styled version.
old_qr = '<td class="p-3 text-center flex justify-center"><img src="https://api.qrserver.com/v1/create-qr-code/?size=40x40&data=LOG001-COMPLETED-RAMESH" alt="QR" class="rounded shadow border border-brand-gold/50 hover:scale-150 transition-transform cursor-pointer"></td>'
new_qr = '<td class="p-3"><img src="https://api.qrserver.com/v1/create-qr-code/?size=50x50&data=LOG001-COMPLETED-RAMESH" alt="QR"></td>'
content = content.replace(old_qr, new_qr)

old_qr2 = '<td class="p-3 text-center flex justify-center"><img src="https://api.qrserver.com/v1/create-qr-code/?size=40x40&data=LOG002-ACTIVE-LAKSHMI" alt="QR" class="rounded shadow border border-brand-gold/50 hover:scale-150 transition-transform cursor-pointer"></td>'
new_qr2 = '<td class="p-3"><img src="https://api.qrserver.com/v1/create-qr-code/?size=50x50&data=LOG002-ACTIVE-LAKSHMI" alt="QR"></td>'
content = content.replace(old_qr2, new_qr2)

old_qr3 = '<td class="p-3 text-center flex justify-center"><img src="https://api.qrserver.com/v1/create-qr-code/?size=40x40&data=LOG003-QC-BASA" alt="QR" class="rounded shadow border border-brand-gold/50 hover:scale-150 transition-transform cursor-pointer"></td>'
new_qr3 = '<td class="p-3"><img src="https://api.qrserver.com/v1/create-qr-code/?size=50x50&data=LOG003-QC-BASA" alt="QR"></td>'
content = content.replace(old_qr3, new_qr3)

# Remove the "text-center" from the QR Tracking header
content = content.replace('<th class="p-3 text-brand-gold font-serif text-center">QR Tracking</th>', '<th class="p-3 text-brand-gold font-serif">QR Tracking</th>')


with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Charts and QR logs successfully updated.")
