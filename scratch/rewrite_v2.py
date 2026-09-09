import re

dashboard_path = r'd:\dbmss\templates\dashboard.html'
with open(dashboard_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Quick Actions Bar
quick_actions_html = """
<!-- Quick Actions & Search -->
<div class="glass-card p-4 mb-8 border border-brand-gold/20 shadow-lg bg-[#1a1a1a] flex flex-col md:flex-row justify-between items-center gap-4">
    <div class="flex-1 w-full relative">
        <input type="text" placeholder="Search orders, products, or artisans..." class="w-full bg-[#121212] border border-brand-gold/30 text-white text-sm rounded px-4 py-3 pl-10 focus:outline-none focus:border-brand-gold shadow-inner transition-colors">
        <svg class="w-5 h-5 absolute left-3 top-3 text-brand-gold/50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
    </div>
    <div class="flex flex-wrap gap-2 items-center justify-center">
        <button class="bg-[#121212] border border-brand-gold/50 text-brand-gold hover:bg-brand-gold hover:text-black px-4 py-2 rounded text-xs font-bold uppercase tracking-widest transition-colors shadow">Add Product</button>
        <button class="bg-[#121212] border border-brand-gold/50 text-brand-gold hover:bg-brand-gold hover:text-black px-4 py-2 rounded text-xs font-bold uppercase tracking-widest transition-colors shadow">Add Supplier</button>
        <button class="bg-[#121212] border border-brand-gold/50 text-brand-gold hover:bg-brand-gold hover:text-black px-4 py-2 rounded text-xs font-bold uppercase tracking-widest transition-colors shadow">Add Artisan</button>
        <button class="bg-[#121212] border border-brand-gold/50 text-brand-gold hover:bg-brand-gold hover:text-black px-4 py-2 rounded text-xs font-bold uppercase tracking-widest transition-colors shadow">View Reports</button>
        <button class="bg-[#121212] border border-brand-gold/50 text-brand-gold hover:bg-brand-gold hover:text-black px-4 py-2 rounded text-xs font-bold uppercase tracking-widest transition-colors shadow">Manage Inventory</button>
    </div>
</div>
"""

# Insert Quick Actions after 4 Image Cards Grid
img_cards_end = "<!-- 4 Stat Cards Grid -->"
content = content.replace(img_cards_end, quick_actions_html + "\n" + img_cards_end)

# 2. Replace 4 Stat Cards Grid with 9 KPI Cards
old_kpi_start = "<!-- 4 Stat Cards Grid -->"
old_kpi_end = "<!-- AI Supply Chain Insights -->"
start_idx = content.find(old_kpi_start)
end_idx = content.find(old_kpi_end)

new_kpi_html = """<!-- 9 KPI Cards Grid -->
<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-3 gap-6 mb-8">
    <div class="glass-card p-6 flex flex-col justify-center items-center h-32 border border-brand-gold/20 shadow-lg bg-[#1a1a1a]">
        <span class="text-[10px] font-bold tracking-widest text-brand-lightgold uppercase mb-2 opacity-70">Total Users</span>
        <span class="text-4xl font-serif text-brand-gold">1,245</span>
    </div>
    <div class="glass-card p-6 flex flex-col justify-center items-center h-32 border border-brand-gold/20 shadow-lg bg-[#1a1a1a]">
        <span class="text-[10px] font-bold tracking-widest text-brand-lightgold uppercase mb-2 opacity-70">Total Artisans</span>
        <span class="text-4xl font-serif text-brand-gold">342</span>
    </div>
    <div class="glass-card p-6 flex flex-col justify-center items-center h-32 border border-brand-gold/20 shadow-lg bg-[#1a1a1a]">
        <span class="text-[10px] font-bold tracking-widest text-brand-lightgold uppercase mb-2 opacity-70">Total Suppliers</span>
        <span class="text-4xl font-serif text-brand-gold">89</span>
    </div>
    <div class="glass-card p-6 flex flex-col justify-center items-center h-32 border border-brand-gold/20 shadow-lg bg-[#1a1a1a]">
        <span class="text-[10px] font-bold tracking-widest text-brand-lightgold uppercase mb-2 opacity-70">Total Customers</span>
        <span class="text-4xl font-serif text-brand-gold">814</span>
    </div>
    <div class="glass-card p-6 flex flex-col justify-center items-center h-32 border border-brand-gold/20 shadow-lg bg-[#1a1a1a]">
        <span class="text-[10px] font-bold tracking-widest text-brand-lightgold uppercase mb-2 opacity-70">Total Products</span>
        <span class="text-4xl font-serif text-brand-gold">456</span>
    </div>
    <div class="glass-card p-6 flex flex-col justify-center items-center h-32 border border-brand-gold/20 shadow-lg bg-[#1a1a1a]">
        <span class="text-[10px] font-bold tracking-widest text-brand-lightgold uppercase mb-2 opacity-70">Total Orders</span>
        <span class="text-4xl font-serif text-brand-gold">2,903</span>
    </div>
    <div class="glass-card p-6 flex flex-col justify-center items-center h-32 border border-brand-gold/20 shadow-lg bg-[#1a1a1a]">
        <span class="text-[10px] font-bold tracking-widest text-brand-lightgold uppercase mb-2 opacity-70">Revenue Generated</span>
        <span class="text-3xl font-serif text-brand-gold">₹8.4M</span>
    </div>
    <div class="glass-card p-6 flex flex-col justify-center items-center h-32 border border-brand-gold/20 shadow-lg bg-[#1a1a1a]">
        <span class="text-[10px] font-bold tracking-widest text-brand-lightgold uppercase mb-2 opacity-70">Pending Shipments</span>
        <span class="text-4xl font-serif text-brand-gold text-yellow-500">42</span>
    </div>
    <div class="glass-card p-6 flex flex-col justify-center items-center h-32 border border-brand-gold/20 shadow-lg bg-[#1a1a1a]">
        <span class="text-[10px] font-bold tracking-widest text-brand-lightgold uppercase mb-2 opacity-70">Low Inventory Alerts</span>
        <span class="text-4xl font-serif text-red-500">7</span>
    </div>
</div>
"""
content = content[:start_idx] + new_kpi_html + content[end_idx:]

# 3. Replace 5 Charts with 6 Charts and Activity Section
old_charts_start = "<!-- Order Fulfillment Section -->"
old_charts_end = "<!-- Shipment Updates & Tracking -->"
if old_charts_end not in content:
    old_charts_end = "<!-- Recent Production Logs -->"

start_idx = content.find(old_charts_start)
end_idx = content.find(old_charts_end)

new_charts_html = """<!-- Charts & Graphs Section -->
<div class="mt-8 mb-4">
    <h3 class="text-xl font-serif text-brand-gold mb-4 pb-2">Analytics Overview</h3>
    <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        <div class="glass-card p-6 shadow-lg border border-brand-gold/10 bg-[#151515]">
            <span class="text-[10px] tracking-widest text-brand-lightgold uppercase mb-6 opacity-70 block">Monthly Revenue Chart</span>
            <div class="h-64"><canvas id="revenueChart"></canvas></div>
        </div>
        <div class="glass-card p-6 shadow-lg border border-brand-gold/10 bg-[#151515]">
            <span class="text-[10px] tracking-widest text-brand-lightgold uppercase mb-6 opacity-70 block">Orders Analytics</span>
            <div class="h-64"><canvas id="ordersChart"></canvas></div>
        </div>
        <div class="glass-card p-6 shadow-lg border border-brand-gold/10 bg-[#151515]">
            <span class="text-[10px] tracking-widest text-brand-lightgold uppercase mb-6 opacity-70 block">Product Sales Graph</span>
            <div class="h-64 pb-4"><canvas id="salesChart"></canvas></div>
        </div>
        <div class="glass-card p-6 shadow-lg border border-brand-gold/10 bg-[#151515]">
            <span class="text-[10px] tracking-widest text-brand-lightgold uppercase mb-6 opacity-70 block">Shipment Status</span>
            <div class="h-64"><canvas id="shipmentChart"></canvas></div>
        </div>
        <div class="glass-card p-6 shadow-lg border border-brand-gold/10 bg-[#151515]">
            <span class="text-[10px] tracking-widest text-brand-lightgold uppercase mb-6 opacity-70 block">Inventory Trends</span>
            <div class="h-64"><canvas id="inventoryChart"></canvas></div>
        </div>
        <div class="glass-card p-6 shadow-lg border border-brand-gold/10 bg-[#151515]">
            <span class="text-[10px] tracking-widest text-brand-lightgold uppercase mb-6 opacity-70 block">User Growth Analytics</span>
            <div class="h-64"><canvas id="userGrowthChart"></canvas></div>
        </div>
    </div>
</div>

<!-- Recent Activities Section -->
<div class="mt-8 mb-8">
    <h3 class="text-xl font-serif text-brand-gold mb-4 pb-2">Recent Activities</h3>
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Latest Orders -->
        <div class="glass-card p-4 shadow-lg border border-brand-gold/10 bg-[#1a1a1a]">
            <span class="text-[10px] tracking-widest text-brand-lightgold uppercase mb-4 opacity-70 block">Latest Orders</span>
            <div class="space-y-3">
                <div class="flex justify-between items-center bg-[#121212] p-2 rounded border border-white/5">
                    <span class="text-xs text-brand-gold font-bold">#ORD-991</span>
                    <span class="text-xs text-gray-300">Mysore Silk Zari</span>
                    <span class="text-[10px] bg-blue-900/40 text-blue-400 px-2 py-0.5 rounded">Processing</span>
                </div>
                <div class="flex justify-between items-center bg-[#121212] p-2 rounded border border-white/5">
                    <span class="text-xs text-brand-gold font-bold">#ORD-990</span>
                    <span class="text-xs text-gray-300">Ilkal Checkered</span>
                    <span class="text-[10px] bg-green-900/40 text-green-400 px-2 py-0.5 rounded">Shipped</span>
                </div>
                <div class="flex justify-between items-center bg-[#121212] p-2 rounded border border-white/5">
                    <span class="text-xs text-brand-gold font-bold">#ORD-989</span>
                    <span class="text-xs text-gray-300">Dharwad Cotton</span>
                    <span class="text-[10px] bg-orange-900/40 text-orange-400 px-2 py-0.5 rounded">Pending</span>
                </div>
            </div>
        </div>
        <!-- Recently Added Products -->
        <div class="glass-card p-4 shadow-lg border border-brand-gold/10 bg-[#1a1a1a]">
            <span class="text-[10px] tracking-widest text-brand-lightgold uppercase mb-4 opacity-70 block">Recently Added Products</span>
            <div class="space-y-3">
                <div class="flex justify-between items-center bg-[#121212] p-2 rounded border border-white/5">
                    <div class="flex items-center gap-2">
                        <div class="w-6 h-6 bg-brand-gold/20 rounded-full flex items-center justify-center text-[10px]">👘</div>
                        <span class="text-xs text-gray-300">Banarasi Brocade</span>
                    </div>
                    <span class="text-[10px] text-gray-500">2 hrs ago</span>
                </div>
                <div class="flex justify-between items-center bg-[#121212] p-2 rounded border border-white/5">
                    <div class="flex items-center gap-2">
                        <div class="w-6 h-6 bg-brand-gold/20 rounded-full flex items-center justify-center text-[10px]">🧶</div>
                        <span class="text-xs text-gray-300">Organic Silk Yarn</span>
                    </div>
                    <span class="text-[10px] text-gray-500">5 hrs ago</span>
                </div>
                <div class="flex justify-between items-center bg-[#121212] p-2 rounded border border-white/5">
                    <div class="flex items-center gap-2">
                        <div class="w-6 h-6 bg-brand-gold/20 rounded-full flex items-center justify-center text-[10px]">🧵</div>
                        <span class="text-xs text-gray-300">Pure Gold Zari</span>
                    </div>
                    <span class="text-[10px] text-gray-500">1 day ago</span>
                </div>
            </div>
        </div>
        <!-- New User Registrations -->
        <div class="glass-card p-4 shadow-lg border border-brand-gold/10 bg-[#1a1a1a]">
            <span class="text-[10px] tracking-widest text-brand-lightgold uppercase mb-4 opacity-70 block">New User Registrations</span>
            <div class="space-y-3">
                <div class="flex justify-between items-center bg-[#121212] p-2 rounded border border-white/5">
                    <div class="flex items-center gap-2">
                        <div class="w-6 h-6 bg-brand-gold text-black rounded-full flex items-center justify-center text-xs font-bold">R</div>
                        <span class="text-xs text-gray-300">Rajesh K.</span>
                    </div>
                    <span class="text-[10px] text-brand-gold">Customer</span>
                </div>
                <div class="flex justify-between items-center bg-[#121212] p-2 rounded border border-white/5">
                    <div class="flex items-center gap-2">
                        <div class="w-6 h-6 bg-gray-500 text-white rounded-full flex items-center justify-center text-xs font-bold">S</div>
                        <span class="text-xs text-gray-300">Sunil T.</span>
                    </div>
                    <span class="text-[10px] text-blue-400">Supplier</span>
                </div>
                <div class="flex justify-between items-center bg-[#121212] p-2 rounded border border-white/5">
                    <div class="flex items-center gap-2">
                        <div class="w-6 h-6 bg-green-700 text-white rounded-full flex items-center justify-center text-xs font-bold">L</div>
                        <span class="text-xs text-gray-300">Lakshmi R.</span>
                    </div>
                    <span class="text-[10px] text-orange-400">Artisan</span>
                </div>
            </div>
        </div>
    </div>
</div>
"""
content = content[:start_idx] + new_charts_html + "\n" + content[end_idx:]

# Rename "Recent Production Logs" to "Shipment Updates & Tracking"
content = content.replace(">Recent Production Logs<", ">Shipment Updates & Tracking<")

# 4. Update the Javascript Charts
old_js_charts_start = "// 2. Initialize Advanced Charts"
old_js_charts_end = "// Add Mock Log Function"
if old_js_charts_start not in content:
    old_js_charts_start = "// 2. Initialize Analytics Charts"

start_idx = content.find(old_js_charts_start)
end_idx = content.find(old_js_charts_end)

new_js_charts = """// 2. Initialize Analytics Charts
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

        """
content = content[:start_idx] + new_js_charts + "\n    " + content[end_idx:]

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Dashboard completely rewritten to spec with NO Javascript syntax errors.")
