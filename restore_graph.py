import re

app_file = r"d:\dbmss\templates\dashboard.html"

with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add the canvas for productionChart if it's missing. Let's replace trendChart or add it as a new card.
# Actually, the user has:
# <h3 class="text-sm tracking-widest uppercase text-brand-lightgold/70 mb-4">Supply Chain Output Trends (6 Months)</h3>
# Let's change this first chart to the Production Volume by Design Type chart.
if 'id="trendChart"' in content:
    content = content.replace('id="trendChart"', 'id="productionChart"')
    content = content.replace('Supply Chain Output Trends (6 Months)', 'Production Volume by Design Type')

# 2. Add the script to fetch /api/production_stats
script_code = """
    <!-- Production Volume Chart Script -->
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            fetch('/api/production_stats')
                .then(response => response.json())
                .then(data => {
                    const ctx = document.getElementById('productionChart');
                    if (!ctx) return;
                    
                    const labels = data.map(item => item.name);
                    const counts = data.map(item => item.count);

                    Chart.defaults.color = '#f0e6d2';
                    Chart.defaults.font.family = "'Inter', sans-serif";

                    new Chart(ctx.getContext('2d'), {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Production Volume',
                                data: counts,
                                backgroundColor: 'rgba(212, 175, 55, 0.7)',
                                borderColor: 'rgba(212, 175, 55, 1)',
                                borderWidth: 1,
                                borderRadius: 2
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: { display: false }
                            },
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    grid: { color: 'rgba(212, 175, 55, 0.1)' }
                                },
                                x: {
                                    grid: { display: false },
                                    ticks: { autoSkip: false, maxRotation: 45, minRotation: 45 }
                                }
                            }
                        }
                    });
                })
                .catch(error => console.error('Error fetching stats:', error));
        });
    </script>
"""

# Append script before </body>
if '/api/production_stats' not in content:
    content = content.replace('</body>', script_code + '\n</body>')

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Restored Production Volume Graph.")
