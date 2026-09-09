import os

template_dir = r"d:\dbmss\templates"

trace_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Provenance Trace - Heritage Handloom</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: { brand: { black: '#121212', dark: '#1a1a1a', brown: '#3e2723', gold: '#d4af37', lightgold: '#f0e6d2' } },
                    fontFamily: { sans: ['Inter', 'sans-serif'], serif: ['Playfair Display', 'serif'] }
                }
            }
        }
    </script>
</head>
<body class="bg-brand-black text-brand-lightgold font-sans antialiased min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-brand-dark border border-brand-gold/30 rounded-xl shadow-2xl overflow-hidden">
        <div class="bg-brand-gold p-6 text-center text-brand-black relative">
            <svg class="w-12 h-12 mx-auto mb-2 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            <h1 class="text-2xl font-serif font-bold uppercase tracking-widest">Verified Authentic</h1>
            <p class="text-xs font-semibold mt-1 opacity-80">Heritage Handloom BlockChain</p>
        </div>
        
        <div class="p-6">
            <h2 class="text-3xl font-serif text-brand-gold mb-2">{{ product.product_name }}</h2>
            <p class="text-sm opacity-70 mb-6 border-b border-brand-gold/20 pb-4">Category: {{ product.category }} &bull; Value: ₹{{ product.price }}</p>
            
            <div class="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-brand-gold/50 before:via-brand-gold/50 before:to-transparent">
                
                <!-- Timeline Item 1 -->
                <div class="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                    <div class="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-brand-gold text-brand-black shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                    </div>
                    <div class="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded bg-brand-black border border-brand-gold/20 shadow">
                        <div class="flex items-center justify-between space-x-2 mb-1">
                            <div class="font-bold text-brand-gold text-sm">Crafted By</div>
                        </div>
                        <div class="text-brand-lightgold font-serif text-lg">{{ provenance.artisan_name }}</div>
                        <div class="text-xs opacity-60">Master Weaver</div>
                    </div>
                </div>
                
                <!-- Timeline Item 2 -->
                <div class="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                    <div class="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-brand-gold text-brand-black shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                    </div>
                    <div class="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded bg-brand-black border border-brand-gold/20 shadow">
                        <div class="flex items-center justify-between space-x-2 mb-1">
                            <div class="font-bold text-brand-gold text-sm">Origin</div>
                        </div>
                        <div class="text-brand-lightgold font-serif text-lg">{{ provenance.location }}</div>
                        <div class="text-xs opacity-60">Handloom Cluster</div>
                    </div>
                </div>

                <!-- Timeline Item 3 -->
                <div class="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                    <div class="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-brand-gold text-brand-black shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path></svg>
                    </div>
                    <div class="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded bg-brand-black border border-brand-gold/20 shadow">
                        <div class="flex items-center justify-between space-x-2 mb-1">
                            <div class="font-bold text-brand-gold text-sm">Materials & Design</div>
                        </div>
                        <div class="text-brand-lightgold font-serif text-lg">{{ provenance.material_type }}</div>
                        <div class="text-xs opacity-60">{{ provenance.design_name }}</div>
                    </div>
                </div>

            </div>
            
            <div class="mt-8 text-center">
                <p class="text-[10px] opacity-40">Scanned at {{ range(1000, 9999) | random }} &bull; Heritage Handloom ERP</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

demand_prediction_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Demand Prediction - Heritage Handloom</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: { brand: { black: '#121212', dark: '#1a1a1a', brown: '#3e2723', gold: '#d4af37', lightgold: '#f0e6d2' } },
                    fontFamily: { sans: ['Inter', 'sans-serif'], serif: ['Playfair Display', 'serif'] }
                }
            }
        }
    </script>
    <style>
        body { background-color: #121212; color: #e5e5e5; scrollbar-width: none; -ms-overflow-style: none; }
        ::-webkit-scrollbar { display: none; }
    </style>
</head>
<body class="flex flex-col min-h-screen bg-[#121212] text-[#e5e5e5]">
    
    <header class="bg-brand-dark border-b border-brand-gold/30 h-16 flex items-center px-6 shadow-md w-full shrink-0 z-50">
        <a href="{{ url_for('dashboard') }}" class="text-brand-lightgold hover:text-brand-gold mr-4">&larr; Back</a>
        <h1 class="text-xl font-serif font-bold text-brand-gold">AI Demand Prediction Engine</h1>
    </header>

    <main class="flex-1 p-6 lg:p-10 w-full max-w-[1500px] mx-auto">
        <div class="mb-8 border-b border-brand-gold/20 pb-4">
            <h2 class="text-3xl font-serif font-bold text-brand-gold">Market Analytics</h2>
            <p class="text-sm opacity-70 mt-2">Machine Learning analysis of historical order data to forecast next month's textile demand.</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Main Chart Area -->
            <div class="lg:col-span-2 bg-brand-dark border border-brand-gold/20 rounded-xl p-6 shadow-2xl">
                <h3 class="text-xl font-serif text-brand-gold mb-6 border-b border-brand-gold/10 pb-2">Sales Forecast vs Current Volume</h3>
                <div class="relative h-96 w-full">
                    <canvas id="demandChart"></canvas>
                </div>
            </div>

            <!-- Insights Panel -->
            <div class="bg-brand-dark border border-brand-gold/20 rounded-xl p-6 shadow-2xl flex flex-col">
                <h3 class="text-xl font-serif text-brand-gold mb-4 border-b border-brand-gold/10 pb-2 flex items-center justify-between">
                    AI Insights <span class="bg-blue-900/30 text-blue-400 text-[10px] px-2 py-1 rounded-full border border-blue-500/30 uppercase tracking-widest font-bold">Active</span>
                </h3>
                
                <div class="flex-1 space-y-4">
                    <div class="p-4 rounded-lg bg-green-900/10 border border-green-500/20">
                        <p class="text-xs text-green-400 font-bold uppercase tracking-wider mb-1">Top Trending</p>
                        <p class="text-lg font-serif text-white">{{ labels[0] if labels else 'N/A' }}</p>
                        <p class="text-xs opacity-70 mt-1">Expected 35% MoM growth driven by seasonal demand.</p>
                    </div>

                    <div class="p-4 rounded-lg bg-brand-gold/5 border border-brand-gold/20">
                        <p class="text-xs text-brand-gold font-bold uppercase tracking-wider mb-1">Production Recommendation</p>
                        <p class="text-sm text-white">Increase raw material procurement (Silk) by 20% to avoid supply chain bottlenecks in the upcoming quarter.</p>
                    </div>

                    <div class="p-4 rounded-lg bg-red-900/10 border border-red-500/20">
                        <p class="text-xs text-red-400 font-bold uppercase tracking-wider mb-1">Risk Alert</p>
                        <p class="text-sm text-white">Low stock quantity detected for fast-moving items. Expedite weaver assignments.</p>
                    </div>
                </div>
                
                <button onclick="alert('Exporting PDF Report...')" class="w-full mt-6 bg-brand-gold/10 hover:bg-brand-gold text-brand-gold hover:text-brand-black border border-brand-gold/50 transition-all font-bold py-3 rounded-lg shadow-lg">Export Report</button>
            </div>
        </div>
    </main>

    <script>
        const ctx = document.getElementById('demandChart').getContext('2d');
        const data = {
            labels: {{ labels | tojson }},
            datasets: [
                {
                    label: 'Current Monthly Volume',
                    data: {{ current_data | tojson }},
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    borderWidth: 1,
                    borderRadius: 4
                },
                {
                    label: 'Predicted Next Month (AI Forecast)',
                    data: {{ predicted_data | tojson }},
                    backgroundColor: 'rgba(212, 175, 55, 0.6)',
                    borderColor: '#d4af37',
                    borderWidth: 2,
                    borderRadius: 4,
                    shadowBlur: 10,
                    shadowColor: 'rgba(212,175,55,0.5)'
                }
            ]
        };

        const config = {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { color: '#f0e6d2', font: { family: 'Inter', size: 12 } }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(18,18,18,0.9)',
                        titleColor: '#d4af37',
                        bodyColor: '#f0e6d2',
                        borderColor: 'rgba(212,175,55,0.3)',
                        borderWidth: 1,
                        padding: 12
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255,255,255,0.05)' },
                        ticks: { color: 'rgba(240,230,210,0.5)' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: 'rgba(240,230,210,0.7)', font: { family: 'Inter' } }
                    }
                }
            }
        };

        new Chart(ctx, config);
    </script>
</body>
</html>
"""

with open(os.path.join(template_dir, 'trace.html'), 'w', encoding='utf-8') as f:
    f.write(trace_html)

with open(os.path.join(template_dir, 'demand_prediction.html'), 'w', encoding='utf-8') as f:
    f.write(demand_prediction_html)

print("Generated trace.html and demand_prediction.html")
