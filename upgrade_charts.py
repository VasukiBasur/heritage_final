import os
import re

def update_dashboard():
    filepath = os.path.join("templates", "dashboard.html")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace the HTML structure
    old_html_pattern = r'<!-- Analytics Chart -->.*?<canvas id="productionChart"></canvas>.*?</div>.*?</div>'
    
    new_html = """<!-- Advanced Analytics Charts -->
                <div class="mb-10">
                    <h2 class="text-2xl font-serif text-brand-gold mb-6 border-b border-brand-gold/20 pb-4">Real-World Statistical Dashboard</h2>
                    
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                        <!-- Chart 1: Time Series Trend -->
                        <div class="glass-card rounded-sm p-6 shadow-xl flex flex-col justify-between h-[400px]">
                            <h3 class="text-sm tracking-widest uppercase text-brand-lightgold/70 mb-4">Supply Chain Output Trends (6 Months)</h3>
                            <div class="relative flex-1 w-full h-full">
                                <canvas id="trendChart"></canvas>
                            </div>
                        </div>

                        <!-- Chart 2: Artisan Performance -->
                        <div class="glass-card rounded-sm p-6 shadow-xl flex flex-col justify-between h-[400px]">
                            <h3 class="text-sm tracking-widest uppercase text-brand-lightgold/70 mb-4">Master Weaver Productivity Matrix</h3>
                            <div class="relative flex-1 w-full h-full">
                                <canvas id="artisanChart"></canvas>
                            </div>
                        </div>
                    </div>

                    <!-- Chart 3: Status Distribution -->
                    <div class="glass-card rounded-sm p-6 shadow-xl flex flex-col justify-between h-[400px] w-full lg:w-1/2 mx-auto">
                        <h3 class="text-sm tracking-widest uppercase text-brand-lightgold/70 mb-4 text-center">Global Order Fulfillment Status</h3>
                        <div class="relative flex-1 w-full h-full flex justify-center">
                            <canvas id="statusChart"></canvas>
                        </div>
                    </div>
                </div>"""
                
    content = re.sub(old_html_pattern, new_html, content, flags=re.DOTALL)

    # 2. Replace the JS structure
    old_js_pattern = r'fetch\(\'/api/production_stats\'\).*?\}\);.*?\}\);'
    
    new_js = """// Chart Defaults
            Chart.defaults.color = '#f0e6d2';
            Chart.defaults.font.family = "'Inter', sans-serif";
            Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(26, 26, 26, 0.9)';
            Chart.defaults.plugins.tooltip.titleColor = '#d4af37';
            Chart.defaults.plugins.tooltip.borderColor = 'rgba(212, 175, 55, 0.3)';
            Chart.defaults.plugins.tooltip.borderWidth = 1;

            // 1. Production Trend (Line Chart)
            fetch('/api/stats/production_trend')
                .then(response => response.json())
                .then(data => {
                    const ctx = document.getElementById('trendChart').getContext('2d');
                    let gradient = ctx.createLinearGradient(0, 0, 0, 400);
                    gradient.addColorStop(0, 'rgba(212, 175, 55, 0.6)');
                    gradient.addColorStop(1, 'rgba(212, 175, 55, 0.0)');

                    new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: data.map(item => item.month),
                            datasets: [{
                                label: 'Volume Produced',
                                data: data.map(item => item.volume),
                                borderColor: '#d4af37',
                                backgroundColor: gradient,
                                borderWidth: 3,
                                fill: true,
                                tension: 0.4,
                                pointBackgroundColor: '#121212',
                                pointBorderColor: '#d4af37',
                                pointBorderWidth: 2,
                                pointRadius: 5,
                                pointHoverRadius: 7
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: { legend: { display: false } },
                            scales: {
                                y: { beginAtZero: true, grid: { color: 'rgba(212, 175, 55, 0.1)' } },
                                x: { grid: { display: false } }
                            }
                        }
                    });
                });

            // 2. Artisan Performance (Horizontal Bar Chart)
            fetch('/api/stats/artisan_performance')
                .then(response => response.json())
                .then(data => {
                    const ctx = document.getElementById('artisanChart').getContext('2d');
                    new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: data.map(item => item.name),
                            datasets: [{
                                label: 'Total Logs Executed',
                                data: data.map(item => item.total_logs),
                                backgroundColor: 'rgba(34, 197, 94, 0.7)',
                                borderColor: '#22c55e',
                                borderWidth: 1,
                                borderRadius: 4
                            }]
                        },
                        options: {
                            indexAxis: 'y',
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: { legend: { display: false } },
                            scales: {
                                x: { beginAtZero: true, grid: { color: 'rgba(212, 175, 55, 0.1)' } },
                                y: { grid: { display: false } }
                            }
                        }
                    });
                });

            // 3. Status Distribution (Doughnut Chart)
            fetch('/api/stats/status_distribution')
                .then(response => response.json())
                .then(data => {
                    const ctx = document.getElementById('statusChart').getContext('2d');
                    const bgColors = data.map(item => {
                        if(item.status === 'Completed') return 'rgba(34, 197, 94, 0.8)';
                        if(item.status === 'Active') return 'rgba(234, 179, 8, 0.8)';
                        return 'rgba(212, 175, 55, 0.5)';
                    });

                    new Chart(ctx, {
                        type: 'doughnut',
                        data: {
                            labels: data.map(item => item.status),
                            datasets: [{
                                data: data.map(item => item.count),
                                backgroundColor: bgColors,
                                borderColor: '#121212',
                                borderWidth: 2,
                                hoverOffset: 10
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            cutout: '70%',
                            plugins: {
                                legend: { position: 'bottom', labels: { padding: 20, usePointStyle: true, pointStyle: 'circle' } }
                            }
                        }
                    });
                });"""
                
    content = re.sub(old_js_pattern, new_js, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Dashboard charts successfully upgraded!")

if __name__ == "__main__":
    update_dashboard()
