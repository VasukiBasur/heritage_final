import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delivery Partner - Heritage Handloom</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brand: {
                            gold: '#D4AF37',
                            lightgold: '#F3E5AB',
                            dark: '#0a0a0a',
                            panel: '#151515',
                            border: '#333333'
                        }
                    },
                    fontFamily: {
                        serif: ['"Playfair Display"', 'serif'],
                        sans: ['"Inter"', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    
    <style>
        body {
            background-color: #050505;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
            background-image: radial-gradient(rgba(212, 175, 55, 0.05) 1px, transparent 1px);
            background-size: 30px 30px;
            overflow-x: hidden;
        }
        
        .glass-panel {
            background: rgba(20, 20, 20, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(212, 175, 55, 0.15);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        }
        
        .nav-link.active {
            background: rgba(212, 175, 55, 0.1);
            color: #D4AF37;
            border-left: 3px solid #D4AF37;
        }

        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #0a0a0a; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #D4AF37; }

        @keyframes pulse-ring { 0% { transform: scale(0.8); opacity: 0.5; } 100% { transform: scale(2.5); opacity: 0; } }
        .map-marker::before {
            content: ''; position: absolute; left: -100%; top: -100%; right: -100%; bottom: -100%;
            border-radius: 50%; animation: pulse-ring 2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
            border: 2px solid #D4AF37;
        }

        .tab-content { display: none; }
        .tab-content.active { display: block; animation: fadeIn 0.4s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body class="flex h-screen overflow-hidden">
    <div id="toast-container" class="fixed bottom-5 right-5 z-[9999] flex flex-col gap-2 pointer-events-none"></div>

    <!-- SIDEBAR -->
    <aside class="w-64 glass-panel border-r border-brand-border flex flex-col z-20 flex-shrink-0">
        <div class="p-6 border-b border-brand-border/50">
            <h1 class="text-xl font-serif text-brand-gold font-bold flex items-center">
                <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                Heritage Logistics
            </h1>
        </div>
        
        <div class="flex-1 overflow-y-auto py-4">
            <nav class="space-y-1">
                <a href="#" onclick="switchTab('dashboard', this)" class="nav-link active flex items-center px-6 py-3 text-sm text-gray-400 hover:text-brand-gold transition-all border-l-3 border-transparent">
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6z"></path></svg>
                    Dashboard Overview
                </a>
                <a href="#" onclick="switchTab('tracking', this)" class="nav-link flex items-center px-6 py-3 text-sm text-gray-400 hover:text-brand-gold transition-all border-l-3 border-transparent">
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path></svg>
                    Live Tracking & Routes
                </a>
                <a href="#" onclick="switchTab('verification', this)" class="nav-link flex items-center px-6 py-3 text-sm text-gray-400 hover:text-brand-gold transition-all border-l-3 border-transparent">
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Delivery Verification
                </a>
                <a href="#" onclick="switchTab('history', this)" class="nav-link flex items-center px-6 py-3 text-sm text-gray-400 hover:text-brand-gold transition-all border-l-3 border-transparent">
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Delivery History
                </a>
                <a href="#" onclick="switchTab('earnings', this)" class="nav-link flex items-center px-6 py-3 text-sm text-gray-400 hover:text-brand-gold transition-all border-l-3 border-transparent">
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Earnings Dashboard
                </a>
                <a href="#" onclick="switchTab('messages', this)" class="nav-link flex items-center px-6 py-3 text-sm text-gray-400 hover:text-brand-gold transition-all border-l-3 border-transparent">
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
                    Messages
                    <span class="ml-auto bg-brand-gold text-black text-xs font-bold px-2 py-0.5 rounded-full">3</span>
                </a>
            </nav>
        </div>
        
        <div class="p-6 border-t border-brand-border/50">
            <a href="/" class="flex items-center text-sm text-gray-500 hover:text-red-400 transition-colors">
                <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
                Logout
            </a>
        </div>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="flex-1 flex flex-col h-full overflow-hidden relative">
        <header class="h-16 glass-panel border-b border-brand-border/50 flex items-center justify-between px-8 z-10 shrink-0">
            <div class="flex items-center w-1/3">
                <div class="relative w-full max-w-md">
                    <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                    <input type="text" placeholder="Search orders, locations, IDs..." class="w-full bg-[#111] border border-brand-border rounded-full py-1.5 pl-10 pr-4 text-sm text-white focus:outline-none focus:border-brand-gold transition-colors">
                </div>
            </div>
            
            <div class="flex items-center space-x-6">
                <div class="relative cursor-pointer hover:text-brand-gold transition-colors text-gray-400">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
                    <span class="absolute -top-1 -right-1 w-3 h-3 bg-brand-gold border-2 border-[#0a0a0a] rounded-full"></span>
                </div>
                <div class="flex items-center space-x-3 border-l border-brand-border pl-6">
                    <div class="text-right">
                        <p class="text-sm font-bold text-white">Rahul Verma</p>
                        <p class="text-xs text-green-500 flex items-center justify-end"><span class="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5"></span> On Duty</p>
                    </div>
                    <div class="w-10 h-10 rounded-full border-2 border-brand-gold/50 bg-[#111] flex items-center justify-center font-serif text-brand-gold font-bold">RV</div>
                </div>
            </div>
        </header>

        <div class="flex-1 overflow-y-auto p-6 relative" id="main-scroll">
            
            <!-- 1. DASHBOARD OVERVIEW -->
            <div id="tab-dashboard" class="tab-content active space-y-6">
                <div class="flex justify-between items-end">
                    <div>
                        <h2 class="text-3xl font-serif text-brand-lightgold mb-1">Welcome back, Rahul</h2>
                        <p class="text-sm text-gray-400">Here is your high-level logistics overview.</p>
                    </div>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
                    <div class="glass-panel p-4 rounded-xl border border-gray-800 hover:border-brand-gold/30">
                        <p class="text-xs text-gray-400 mb-1 uppercase tracking-wider font-bold">Assigned Orders</p>
                        <h3 class="text-2xl font-serif font-bold text-white">24</h3>
                    </div>
                    <div class="glass-panel p-4 rounded-xl border border-brand-gold/40 shadow-[0_0_15px_rgba(212,175,55,0.1)]">
                        <p class="text-xs text-brand-gold mb-1 uppercase tracking-wider font-bold">In Progress</p>
                        <h3 class="text-2xl font-serif font-bold text-white">4</h3>
                    </div>
                    <div class="glass-panel p-4 rounded-xl border border-gray-800 hover:border-blue-500/30">
                        <p class="text-xs text-blue-400 mb-1 uppercase tracking-wider font-bold">Pending Pickups</p>
                        <h3 class="text-2xl font-serif font-bold text-white">6</h3>
                    </div>
                    <div class="glass-panel p-4 rounded-xl border border-gray-800 hover:border-green-500/30">
                        <p class="text-xs text-green-500 mb-1 uppercase tracking-wider font-bold">Delivered Today</p>
                        <h3 class="text-2xl font-serif font-bold text-white">14</h3>
                    </div>
                    <div class="glass-panel p-4 rounded-xl border border-gray-800 hover:border-purple-500/30">
                        <p class="text-xs text-purple-400 mb-1 uppercase tracking-wider font-bold">On-Time Rate</p>
                        <h3 class="text-2xl font-serif font-bold text-white">99.1%</h3>
                    </div>
                    <div class="glass-panel p-4 rounded-xl border border-gray-800 hover:border-brand-gold/30">
                        <p class="text-xs text-gray-400 mb-1 uppercase tracking-wider font-bold">Monthly Earnings</p>
                        <h3 class="text-2xl font-serif font-bold text-brand-lightgold">₹41.2k</h3>
                    </div>
                </div>

                <div class="grid grid-cols-1 xl:grid-cols-3 gap-6 h-[400px]">
                    <div class="xl:col-span-2 glass-panel rounded-2xl border border-gray-800 flex flex-col relative overflow-hidden group">
                        <div class="p-4 border-b border-gray-800 flex justify-between items-center z-10 bg-[#0a0a0a]/80 backdrop-blur">
                            <h3 class="text-lg font-serif text-white">Live Logistics Map</h3>
                            <div class="flex space-x-4 text-xs font-bold text-gray-300">
                                <span class="bg-[#111] border border-gray-700 px-3 py-1 rounded">Dist: 14 km</span>
                                <span class="bg-[#111] border border-brand-gold/30 text-brand-gold px-3 py-1 rounded">ETA: 45 min</span>
                                <span class="bg-green-500/10 border border-green-500/30 text-green-400 px-3 py-1 rounded">Efficiency: 94%</span>
                            </div>
                        </div>
                        <div class="flex-1 relative">
                            <div class="absolute inset-0 opacity-20 pointer-events-none" style="background-image: linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px); background-size: 50px 50px;"></div>
                            <svg class="absolute inset-0 w-full h-full" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
                                <defs><linearGradient id="dashPath2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#4B5563" /><stop offset="50%" stop-color="#D4AF37" /><stop offset="100%" stop-color="#10B981" /></linearGradient></defs>
                                <path d="M 100 80 C 200 80, 250 200, 350 250 S 550 150, 700 200" fill="none" stroke="url(#dashPath2)" stroke-width="3" stroke-linecap="round" class="map-path"/>
                                <g><circle r="6" fill="#ffffff" filter="drop-shadow(0 0 8px rgba(255,255,255,1))"/><animateMotion dur="10s" repeatCount="indefinite" path="M 100 80 C 200 80, 250 200, 350 250 S 550 150, 700 200" /></g>
                            </svg>
                            <div class="absolute top-[60px] left-[80px] flex flex-col items-center"><div class="w-4 h-4 bg-gray-600 rounded-full border-2 border-white z-10"></div><div class="mt-1 px-2 py-0.5 bg-black border border-gray-700 rounded text-[9px] text-gray-300">Supplier HQ</div></div>
                            <div class="absolute top-[230px] left-[330px] flex flex-col items-center"><div class="relative map-marker w-5 h-5 bg-blue-500 rounded-full border-2 border-white z-10"></div><div class="mt-1 px-2 py-0.5 bg-black border border-blue-500/50 rounded text-[9px] text-blue-400">Warehouse 4</div></div>
                            <div class="absolute top-[180px] left-[680px] flex flex-col items-center"><div class="relative map-marker w-6 h-6 bg-brand-gold rounded-full border-2 border-white z-10 shadow-[0_0_15px_#D4AF37]"></div><div class="mt-1 px-2 py-0.5 bg-black border border-brand-gold rounded text-[10px] text-brand-lightgold font-bold">Delivery Dropoff</div></div>
                        </div>
                    </div>

                    <div class="glass-panel p-5 rounded-2xl border border-gray-800 flex flex-col">
                        <h3 class="text-lg font-serif text-white mb-4">Active Tasks</h3>
                        <div class="flex-1 overflow-y-auto space-y-3 pr-2">
                            <div class="bg-[#111] border border-brand-gold/30 rounded-xl p-4">
                                <div class="flex justify-between items-center mb-2">
                                    <span class="text-xs font-bold text-white">#ORD-8921</span>
                                    <span class="text-[10px] bg-brand-gold/20 text-brand-gold px-2 py-0.5 rounded border border-brand-gold/30">In Transit</span>
                                </div>
                                <h4 class="text-sm font-bold text-gray-200 truncate">Kanchipuram Silk Saree</h4>
                                <p class="text-xs text-gray-500 mb-3">Jubilee Hills, Hyderabad</p>
                                <div class="w-full bg-gray-800 rounded-full h-1.5 mb-1"><div class="bg-brand-gold h-1.5 rounded-full" style="width: 75%"></div></div>
                                <button onclick="window.showToast('Routing initiated')" class="mt-2 w-full py-1.5 border border-gray-700 rounded hover:border-brand-gold text-xs font-bold text-gray-300 hover:text-brand-gold transition-colors">Track Details</button>
                            </div>
                            <div class="bg-[#111] border border-gray-800 rounded-xl p-4 hover:border-gray-600 transition-colors">
                                <div class="flex justify-between items-center mb-2">
                                    <span class="text-xs font-bold text-white">#PCK-3341</span>
                                    <span class="text-[10px] bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded border border-blue-500/30">Pickup</span>
                                </div>
                                <h4 class="text-sm font-bold text-gray-200 truncate">Artisan Hub B</h4>
                                <p class="text-xs text-gray-500 mb-3">Sector 4, Weaver Cooperative</p>
                                <button onclick="window.showToast('Pickup Confirmed')" class="w-full py-1.5 bg-[#1a1a1a] border border-gray-700 rounded hover:border-blue-500 text-xs font-bold text-gray-300 hover:text-blue-400 transition-colors">Confirm Pickup</button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="glass-panel p-5 rounded-2xl border border-gray-800"><h3 class="text-sm font-bold text-gray-300 mb-4">Monthly Deliveries</h3><div class="h-40"><canvas id="monthlyChart"></canvas></div></div>
                    <div class="glass-panel p-5 rounded-2xl border border-gray-800"><h3 class="text-sm font-bold text-gray-300 mb-4">Success Rate</h3><div class="h-40 flex items-center justify-center relative"><canvas id="successChart"></canvas><div class="absolute inset-0 flex items-center justify-center pointer-events-none mt-4"><span class="text-xl font-bold text-white">99%</span></div></div></div>
                    <div class="glass-panel p-5 rounded-2xl border border-gray-800"><h3 class="text-sm font-bold text-gray-300 mb-4">Earnings Growth</h3><div class="h-40"><canvas id="earningsGrowthChart"></canvas></div></div>
                </div>
            </div>

            <!-- 2. LIVE TRACKING & ROUTES -->
            <div id="tab-tracking" class="tab-content space-y-6">
                <div class="flex justify-between items-end mb-4">
                    <div>
                        <h2 class="text-3xl font-serif text-brand-lightgold mb-1">Logistics Mapping</h2>
                        <p class="text-sm text-gray-400">Detailed route planning and execution.</p>
                    </div>
                </div>
                
                <div class="grid grid-cols-1 xl:grid-cols-4 gap-6 h-[700px]">
                    <!-- Left sidebar with active route cards -->
                    <div class="xl:col-span-1 glass-panel rounded-2xl border border-gray-800 flex flex-col">
                        <div class="p-4 border-b border-gray-800 font-bold text-white flex justify-between items-center">
                            <span>Active Route List</span>
                            <span class="bg-brand-gold text-black px-2 py-0.5 rounded text-xs">4</span>
                        </div>
                        <div class="flex-1 overflow-y-auto p-4 space-y-4">
                            <!-- Route Card 1 -->
                            <div class="p-4 bg-[#111] border border-brand-gold/50 rounded-xl">
                                <div class="flex justify-between text-xs mb-2 text-gray-400"><span>#ORD-8921</span><span class="text-brand-gold">In Transit</span></div>
                                <h4 class="text-sm font-bold text-white mb-2">Artisan HQ to Jubilee Hills</h4>
                                <div class="flex items-center space-x-2 text-xs mb-3 text-gray-300">
                                    <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                    <span>ETA: 45 min</span>
                                    <span class="mx-1">•</span>
                                    <span>Dist: 14km</span>
                                </div>
                                <div class="flex space-x-1 mb-2">
                                    <span class="w-2 h-2 rounded-full bg-green-500"></span><span class="w-2 h-2 rounded-full bg-green-500"></span><span class="w-2 h-2 rounded-full bg-green-500"></span><span class="w-2 h-2 rounded-full bg-yellow-500 animate-pulse"></span><span class="w-2 h-2 rounded-full bg-gray-700"></span>
                                </div>
                            </div>
                            <!-- Route Card 2 -->
                            <div class="p-4 bg-[#111] border border-gray-800 rounded-xl hover:border-gray-600 transition-colors cursor-pointer">
                                <div class="flex justify-between text-xs mb-2 text-gray-400"><span>#PCK-3341</span><span class="text-blue-400">Pickup</span></div>
                                <h4 class="text-sm font-bold text-white mb-2">Sector 4 to Warehouse</h4>
                                <div class="flex items-center space-x-2 text-xs mb-2 text-gray-500">
                                    <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                    <span>ETA: 1h 15m</span>
                                </div>
                            </div>
                            <!-- Route Card 3 -->
                            <div class="p-4 bg-[#111] border border-gray-800 rounded-xl hover:border-gray-600 transition-colors cursor-pointer">
                                <div class="flex justify-between text-xs mb-2 text-gray-400"><span>#ORD-8930</span><span class="text-yellow-500">Pending</span></div>
                                <h4 class="text-sm font-bold text-white mb-2">Warehouse to Gachibowli</h4>
                                <div class="flex items-center space-x-2 text-xs mb-2 text-gray-500">
                                    <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                    <span>Scheduled: 16:00</span>
                                </div>
                            </div>
                            <!-- Route Card 4 -->
                            <div class="p-4 bg-[#111] border border-gray-800 rounded-xl hover:border-gray-600 transition-colors cursor-pointer">
                                <div class="flex justify-between text-xs mb-2 text-gray-400"><span>#ORD-8942</span><span class="text-yellow-500">Pending</span></div>
                                <h4 class="text-sm font-bold text-white mb-2">Warehouse to HITEC City</h4>
                                <div class="flex items-center space-x-2 text-xs mb-2 text-gray-500">
                                    <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                    <span>Scheduled: 18:00</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Massive Animated Map -->
                    <div class="xl:col-span-3 glass-panel rounded-2xl border border-gray-800 relative overflow-hidden flex flex-col">
                        <div class="p-4 border-b border-gray-800 flex justify-between items-center z-10 bg-[#0a0a0a]/80 backdrop-blur">
                            <div class="flex items-center space-x-4">
                                <h3 class="text-lg font-serif text-white">Full Area Map</h3>
                                <div class="px-2 py-1 bg-red-500/20 border border-red-500/30 text-red-400 text-xs rounded font-bold animate-pulse">Traffic Alert: Route 4</div>
                            </div>
                            <div class="flex space-x-3 text-xs">
                                <span class="flex items-center"><span class="w-3 h-3 bg-gray-600 rounded-full border border-white mr-1"></span> Supplier</span>
                                <span class="flex items-center"><span class="w-3 h-3 bg-blue-500 rounded-full border border-white mr-1"></span> Warehouse</span>
                                <span class="flex items-center"><span class="w-3 h-3 bg-brand-gold rounded-full border border-white mr-1"></span> Customer</span>
                                <span class="flex items-center"><span class="w-3 h-3 bg-purple-500 rounded-full border border-white mr-1"></span> Artisan</span>
                            </div>
                        </div>
                        <div class="flex-1 relative bg-[#080808]">
                            <!-- Grid background -->
                            <div class="absolute inset-0 opacity-10 pointer-events-none" style="background-image: linear-gradient(rgba(255,255,255,1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,1) 1px, transparent 1px); background-size: 80px 80px;"></div>
                            
                            <svg class="absolute inset-0 w-full h-full" xmlns="http://www.w3.org/2000/svg">
                                <defs><linearGradient id="largeDash" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#4B5563"/><stop offset="100%" stop-color="#D4AF37"/></linearGradient></defs>
                                <path d="M 150 150 C 300 150, 400 400, 600 350 S 800 500, 950 250" fill="none" stroke="url(#largeDash)" stroke-width="4" stroke-linecap="round" class="map-path"/>
                                <!-- Secondary route -->
                                <path d="M 600 350 C 650 200, 750 150, 850 100" fill="none" stroke="#4B5563" stroke-dasharray="5 5" stroke-width="2"/>
                                
                                <g><circle r="8" fill="#ffffff" filter="drop-shadow(0 0 10px rgba(255,255,255,1))"/><circle r="3" fill="#000"/><animateMotion dur="20s" repeatCount="indefinite" path="M 150 150 C 300 150, 400 400, 600 350 S 800 500, 950 250" /></g>
                            </svg>

                            <!-- Nodes -->
                            <div class="absolute top-[130px] left-[130px] flex flex-col items-center"><div class="w-6 h-6 bg-purple-500 rounded-full border-2 border-white shadow-[0_0_15px_rgba(168,85,247,0.5)]"></div><span class="mt-2 text-xs font-bold text-purple-400 bg-black/80 px-2 py-1 rounded">Artisan HQ</span></div>
                            <div class="absolute top-[330px] left-[580px] flex flex-col items-center"><div class="relative map-marker w-7 h-7 bg-blue-500 rounded-full border-2 border-white z-10 shadow-[0_0_15px_rgba(59,130,246,0.5)]"></div><span class="mt-2 text-xs font-bold text-blue-400 bg-black/80 px-2 py-1 rounded">Central Warehouse</span></div>
                            <div class="absolute top-[80px] left-[830px] flex flex-col items-center"><div class="w-5 h-5 bg-gray-600 rounded-full border-2 border-white"></div><span class="mt-2 text-[10px] text-gray-400 bg-black/80 px-2 py-1 rounded">Supplier Node</span></div>
                            <div class="absolute top-[230px] left-[930px] flex flex-col items-center"><div class="relative w-8 h-8 bg-brand-gold rounded-full border-[3px] border-white z-10 shadow-[0_0_20px_#D4AF37] flex items-center justify-center"><div class="w-3 h-3 bg-white rounded-full animate-pulse"></div></div><span class="mt-2 text-xs font-bold text-brand-lightgold bg-black/80 px-2 py-1 rounded">Customer (ETA: 45m)</span></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 3. DELIVERY VERIFICATION -->
            <div id="tab-verification" class="tab-content space-y-6">
                <div class="flex justify-between items-end mb-4">
                    <div>
                        <h2 class="text-3xl font-serif text-brand-lightgold mb-1">Proof of Delivery</h2>
                        <p class="text-sm text-gray-400">Verify packages securely at the drop-off point.</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <!-- Queue -->
                    <div class="lg:col-span-1 glass-panel rounded-2xl border border-gray-800 p-5">
                        <h3 class="font-bold text-white mb-4">Drop-off Queue</h3>
                        <div class="space-y-3">
                            <div class="bg-brand-gold/10 border border-brand-gold/50 p-4 rounded-xl cursor-pointer">
                                <div class="flex justify-between mb-1"><span class="font-bold text-brand-lightgold text-sm">#ORD-8921</span><span class="text-xs text-green-500 font-bold">At Location</span></div>
                                <p class="text-xs text-gray-300">Anjali Sharma • 123 Heritage Lane</p>
                            </div>
                            <div class="bg-[#111] border border-gray-800 p-4 rounded-xl opacity-50 cursor-not-allowed">
                                <div class="flex justify-between mb-1"><span class="font-bold text-white text-sm">#ORD-8930</span><span class="text-xs text-yellow-500">En Route</span></div>
                                <p class="text-xs text-gray-500">Vikram Singh • Block 4, Gachibowli</p>
                            </div>
                            <div class="bg-[#111] border border-gray-800 p-4 rounded-xl opacity-50 cursor-not-allowed">
                                <div class="flex justify-between mb-1"><span class="font-bold text-white text-sm">#ORD-8942</span><span class="text-xs text-gray-500">Pending</span></div>
                                <p class="text-xs text-gray-500">Priya Patel • HITEC City</p>
                            </div>
                        </div>
                    </div>

                    <!-- Verification Panel -->
                    <div class="lg:col-span-2 glass-panel rounded-2xl border border-gray-800 p-8">
                        <div class="flex justify-between border-b border-gray-800 pb-4 mb-6">
                            <div>
                                <h3 class="text-xl font-serif text-white">Order #ORD-8921</h3>
                                <p class="text-sm text-gray-400 mt-1">Pure Kanchipuram Silk Saree (1 Item)</p>
                            </div>
                            <div class="text-right">
                                <h3 class="text-lg font-bold text-white">Anjali Sharma</h3>
                                <p class="text-sm text-gray-400">+91 98765 43210</p>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                            <!-- OTP/QR -->
                            <div>
                                <label class="block text-sm font-bold text-gray-300 mb-3">Customer Verification PIN</label>
                                <div class="flex space-x-3 mb-4">
                                    <input type="text" maxlength="1" class="w-12 h-14 text-center text-2xl font-bold bg-[#111] border border-gray-700 focus:border-brand-gold rounded-xl text-white outline-none">
                                    <input type="text" maxlength="1" class="w-12 h-14 text-center text-2xl font-bold bg-[#111] border border-gray-700 focus:border-brand-gold rounded-xl text-white outline-none">
                                    <input type="text" maxlength="1" class="w-12 h-14 text-center text-2xl font-bold bg-[#111] border border-gray-700 focus:border-brand-gold rounded-xl text-white outline-none">
                                    <input type="text" maxlength="1" class="w-12 h-14 text-center text-2xl font-bold bg-[#111] border border-gray-700 focus:border-brand-gold rounded-xl text-white outline-none">
                                </div>
                                <button onclick="window.showToast('Scanner opened')" class="px-4 py-2 bg-[#1a1a1a] border border-gray-700 hover:border-brand-gold text-brand-gold rounded-xl text-sm font-bold transition-colors flex items-center">
                                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"></path></svg>
                                    Scan Delivery QR instead
                                </button>
                            </div>

                            <!-- Photo -->
                            <div>
                                <label class="block text-sm font-bold text-gray-300 mb-3">Package Photo Proof</label>
                                <div onclick="window.showToast('Camera triggered for photo')" class="border-2 border-dashed border-gray-700 hover:border-brand-gold bg-[#111] rounded-xl p-6 text-center cursor-pointer transition-colors group">
                                    <div class="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-2 group-hover:bg-brand-gold/20 group-hover:text-brand-gold text-gray-400 transition-colors">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                                    </div>
                                    <p class="text-xs text-gray-400">Tap to capture package at doorstep</p>
                                </div>
                            </div>
                        </div>

                        <!-- Signature -->
                        <div class="mb-6">
                            <label class="block text-sm font-bold text-gray-300 mb-2">Customer Signature (Required for high value items)</label>
                            <div class="h-24 bg-[#111] border border-gray-700 rounded-xl w-full relative">
                                <span class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-gray-600 text-sm pointer-events-none">Sign Here</span>
                            </div>
                        </div>
                        
                        <div class="mb-6">
                            <label class="block text-sm font-bold text-gray-300 mb-2">Delivery Notes (Optional)</label>
                            <textarea class="w-full bg-[#111] border border-gray-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-brand-gold" rows="2" placeholder="E.g., Handed to security guard..."></textarea>
                        </div>

                        <div class="flex space-x-4">
                            <button onclick="window.showToast('Delivery Verified! Order marked as complete.'); document.getElementById('successBadge').classList.remove('hidden');" class="flex-1 py-4 bg-brand-gold text-black rounded-xl font-bold text-lg hover:bg-yellow-500 transition-colors shadow-[0_0_20px_rgba(212,175,55,0.3)]">
                                Verify & Complete Delivery
                            </button>
                            <button class="px-6 py-4 bg-red-500/10 text-red-500 border border-red-500/30 rounded-xl font-bold text-sm hover:bg-red-500/20 transition-colors">
                                Report Issue
                            </button>
                        </div>
                        
                        <div id="successBadge" class="hidden mt-6 p-4 bg-green-500/20 border border-green-500/50 rounded-xl flex items-center justify-center">
                            <svg class="w-6 h-6 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            <span class="text-green-500 font-bold">Successfully Delivered</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 4. DELIVERY HISTORY -->
            <div id="tab-history" class="tab-content space-y-6">
                <div class="flex justify-between items-end mb-4">
                    <div>
                        <h2 class="text-3xl font-serif text-brand-lightgold mb-1">Delivery Log</h2>
                        <p class="text-sm text-gray-400">History of all your completed tasks.</p>
                    </div>
                    <div class="flex space-x-3">
                        <button class="px-4 py-2 bg-[#111] border border-gray-700 text-gray-300 rounded hover:border-brand-gold transition-colors text-sm flex items-center">
                            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg> Filter
                        </button>
                        <button onclick="window.showToast('Exporting PDF Report...')" class="px-4 py-2 bg-[#1a1a1a] border border-brand-gold text-brand-gold rounded hover:bg-brand-gold/10 transition-colors text-sm font-bold flex items-center">
                            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg> Export PDF
                        </button>
                    </div>
                </div>

                <div class="grid grid-cols-4 gap-4 mb-6">
                    <div class="glass-panel p-4 rounded-xl border border-gray-800"><p class="text-xs text-gray-400 uppercase font-bold">Total Deliveries</p><h3 class="text-2xl font-serif text-white mt-1">420</h3></div>
                    <div class="glass-panel p-4 rounded-xl border border-gray-800"><p class="text-xs text-green-500 uppercase font-bold">Successful</p><h3 class="text-2xl font-serif text-white mt-1">415</h3></div>
                    <div class="glass-panel p-4 rounded-xl border border-gray-800"><p class="text-xs text-red-500 uppercase font-bold">Failed / Returned</p><h3 class="text-2xl font-serif text-white mt-1">5</h3></div>
                    <div class="glass-panel p-4 rounded-xl border border-gray-800"><p class="text-xs text-brand-gold uppercase font-bold">Avg. Time</p><h3 class="text-2xl font-serif text-white mt-1">42 min</h3></div>
                </div>

                <div class="glass-panel rounded-2xl border border-gray-800 overflow-hidden">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-gray-800 bg-[#111]">
                                <th class="p-4 text-xs uppercase tracking-widest text-gray-500 font-bold">Order ID</th>
                                <th class="p-4 text-xs uppercase tracking-widest text-gray-500 font-bold">Date & Time</th>
                                <th class="p-4 text-xs uppercase tracking-widest text-gray-500 font-bold">Customer</th>
                                <th class="p-4 text-xs uppercase tracking-widest text-gray-500 font-bold">Product</th>
                                <th class="p-4 text-xs uppercase tracking-widest text-gray-500 font-bold">Dist.</th>
                                <th class="p-4 text-xs uppercase tracking-widest text-gray-500 font-bold">Status</th>
                            </tr>
                        </thead>
                        <tbody class="text-sm text-gray-300">
                            <!-- 20 Sample Rows Generated dynamically for brevity in python script output -->
                            """ + "".join([f"""
                            <tr class="border-b border-gray-800/50 hover:bg-[#1a1a1a] transition-colors">
                                <td class="p-4 font-bold text-white">#ORD-{8890-i}</td>
                                <td class="p-4 text-gray-400">May {28-(i//5)}, 2026 {10+(i%8)}:{15+(i*3)%60} AM</td>
                                <td class="p-4">Customer {i+1}</td>
                                <td class="p-4 truncate max-w-[150px]">Handloom Silk {i}</td>
                                <td class="p-4">{5+(i%10)} km</td>
                                <td class="p-4"><span class="px-2 py-1 bg-green-500/20 text-green-500 rounded text-xs font-bold border border-green-500/30">Delivered</span></td>
                            </tr>""" for i in range(20)]) + """
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 5. EARNINGS TAB -->
            <div id="tab-earnings" class="tab-content space-y-6">
                <div class="flex justify-between items-end mb-4">
                    <div>
                        <h2 class="text-3xl font-serif text-brand-lightgold mb-1">Financial Dashboard</h2>
                        <p class="text-sm text-gray-400">Track payouts, incentives, and growth.</p>
                    </div>
                    <select class="bg-[#111] border border-gray-700 text-white rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-brand-gold">
                        <option>May 2026</option>
                        <option>April 2026</option>
                        <option>March 2026</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                    <div class="glass-panel p-6 rounded-xl border border-brand-gold/30 relative overflow-hidden">
                        <div class="absolute top-0 right-0 w-16 h-16 bg-brand-gold/10 rounded-bl-full"></div>
                        <p class="text-gray-400 text-xs uppercase font-bold mb-1">Today's Earnings</p>
                        <h3 class="text-3xl font-serif font-bold text-brand-lightgold">₹1,250</h3>
                        <p class="text-xs text-green-500 mt-2 font-bold">+₹150 Incentive</p>
                    </div>
                    <div class="glass-panel p-6 rounded-xl border border-gray-800">
                        <p class="text-gray-400 text-xs uppercase font-bold mb-1">Weekly Earnings</p>
                        <h3 class="text-3xl font-serif font-bold text-white">₹8,400</h3>
                        <p class="text-xs text-gray-500 mt-2">Mon - Sun</p>
                    </div>
                    <div class="glass-panel p-6 rounded-xl border border-gray-800">
                        <p class="text-gray-400 text-xs uppercase font-bold mb-1">Monthly Earnings</p>
                        <h3 class="text-3xl font-serif font-bold text-white">₹41,200</h3>
                        <p class="text-xs text-green-500 mt-2">Target reached!</p>
                    </div>
                    <div class="glass-panel p-6 rounded-xl border border-gray-800 bg-brand-gold/5">
                        <p class="text-brand-gold text-xs uppercase font-bold mb-1">Total Bonus</p>
                        <h3 class="text-3xl font-serif font-bold text-brand-lightgold">₹4,200</h3>
                        <p class="text-xs text-gray-400 mt-2">From perfect deliveries</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="glass-panel p-5 rounded-2xl border border-gray-800"><h3 class="text-sm font-bold text-white mb-4">Earnings vs Deliveries (Monthly)</h3><div class="h-64"><canvas id="earningsComboChart"></canvas></div></div>
                    <div class="glass-panel p-5 rounded-2xl border border-gray-800">
                        <h3 class="text-sm font-bold text-white mb-4">Incentive Breakdown</h3>
                        <div class="space-y-4">
                            <div class="flex justify-between items-center"><div class="flex items-center"><span class="w-3 h-3 bg-green-500 rounded-full mr-3"></span><span class="text-sm text-gray-300">On-Time Bonus</span></div><span class="text-sm font-bold text-white">₹2,000</span></div>
                            <div class="w-full bg-gray-800 rounded-full h-1.5 mb-2"><div class="bg-green-500 h-1.5 rounded-full" style="width: 45%"></div></div>
                            
                            <div class="flex justify-between items-center"><div class="flex items-center"><span class="w-3 h-3 bg-brand-gold rounded-full mr-3"></span><span class="text-sm text-gray-300">Zero Damage Rating</span></div><span class="text-sm font-bold text-white">₹1,500</span></div>
                            <div class="w-full bg-gray-800 rounded-full h-1.5 mb-2"><div class="bg-brand-gold h-1.5 rounded-full" style="width: 35%"></div></div>
                            
                            <div class="flex justify-between items-center"><div class="flex items-center"><span class="w-3 h-3 bg-blue-500 rounded-full mr-3"></span><span class="text-sm text-gray-300">Fuel Surcharge Adj.</span></div><span class="text-sm font-bold text-white">₹700</span></div>
                            <div class="w-full bg-gray-800 rounded-full h-1.5 mb-2"><div class="bg-blue-500 h-1.5 rounded-full" style="width: 20%"></div></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 6. MESSAGES TAB -->
            <div id="tab-messages" class="tab-content h-[700px]">
                <div class="glass-panel rounded-2xl border border-gray-800 flex h-full overflow-hidden">
                    <div class="w-1/3 border-r border-gray-800 flex flex-col">
                        <div class="p-4 border-b border-gray-800">
                            <input type="text" placeholder="Search chats..." class="w-full bg-[#111] border border-gray-700 rounded-full py-2 px-4 text-sm text-white focus:outline-none focus:border-brand-gold transition-colors">
                        </div>
                        <div class="flex border-b border-gray-800 text-xs font-bold text-gray-500">
                            <button class="flex-1 py-3 border-b-2 border-brand-gold text-brand-gold">All</button>
                            <button class="flex-1 py-3 border-b-2 border-transparent hover:text-white">Admin</button>
                            <button class="flex-1 py-3 border-b-2 border-transparent hover:text-white">Artisans</button>
                            <button class="flex-1 py-3 border-b-2 border-transparent hover:text-white">Customers</button>
                        </div>
                        <div class="flex-1 overflow-y-auto">
                            <div class="p-4 border-b border-gray-800 bg-[#1a1a1a] cursor-pointer">
                                <div class="flex justify-between items-center mb-1">
                                    <h4 class="text-white font-bold text-sm">HQ Logistics Support</h4>
                                    <span class="text-xs text-brand-gold">10:45 AM</span>
                                </div>
                                <p class="text-xs text-gray-400 truncate">Are you facing traffic on route 4?</p>
                            </div>
                            <div class="p-4 border-b border-gray-800 hover:bg-[#1a1a1a] cursor-pointer">
                                <div class="flex justify-between items-center mb-1">
                                    <h4 class="text-gray-300 font-bold text-sm">Anjali Sharma (Customer)</h4>
                                    <span class="text-xs text-gray-500">Yesterday</span>
                                </div>
                                <p class="text-xs text-gray-500 truncate">Please leave it with the security guard.</p>
                            </div>
                            <div class="p-4 border-b border-gray-800 hover:bg-[#1a1a1a] cursor-pointer">
                                <div class="flex justify-between items-center mb-1">
                                    <h4 class="text-gray-300 font-bold text-sm">Weaver Cooperative</h4>
                                    <span class="text-xs text-gray-500">May 25</span>
                                </div>
                                <p class="text-xs text-gray-500 truncate">Package is ready for pickup at Gate B.</p>
                            </div>
                        </div>
                    </div>
                    <div class="flex-1 flex flex-col bg-[#0a0a0a]">
                        <div class="p-4 border-b border-gray-800 flex justify-between items-center">
                            <h4 class="text-white font-bold">HQ Logistics Support</h4>
                            <span class="text-xs text-green-500 flex items-center"><span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>Online</span>
                        </div>
                        <div class="flex-1 p-6 space-y-4 overflow-y-auto">
                            <div class="flex justify-center mb-4"><span class="text-xs text-gray-600 bg-[#111] px-2 py-1 rounded">Today</span></div>
                            <div class="flex justify-start">
                                <div class="bg-[#1a1a1a] border border-gray-800 text-gray-300 rounded-2xl px-4 py-2 max-w-[70%] text-sm">
                                    Hello Rahul, we noticed a delay on your route to Jubilee Hills. Are you facing traffic on route 4?
                                </div>
                            </div>
                            <div class="flex justify-end">
                                <div class="bg-brand-gold text-black rounded-2xl px-4 py-2 max-w-[70%] text-sm">
                                    Yes, there's a roadblock near the main intersection. I am taking the alternate route via the bypass. ETA updated to +10 mins.
                                </div>
                            </div>
                            <div class="flex justify-start">
                                <div class="bg-[#1a1a1a] border border-gray-800 text-gray-300 rounded-2xl px-4 py-2 max-w-[70%] text-sm">
                                    Copy that. Drive safe!
                                </div>
                            </div>
                        </div>
                        <div class="p-4 border-t border-gray-800 bg-[#111] flex space-x-2">
                            <button class="text-gray-500 hover:text-brand-gold"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"></path></svg></button>
                            <input type="text" placeholder="Type a message..." class="flex-1 bg-black border border-gray-700 rounded py-2 px-3 text-sm text-white focus:outline-none focus:border-brand-gold">
                            <button onclick="window.showToast('Message Sent')" class="bg-brand-gold text-black px-4 rounded font-bold hover:bg-yellow-500 text-sm">Send</button>
                        </div>
                    </div>
                </div>
            </div>
            
        </div>
        
    </main>

    <script>
        window.switchTab = function(tabId, element) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            
            if(element) {
                document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active', 'border-brand-gold', 'bg-brand-gold/10'));
                document.querySelectorAll('.nav-link').forEach(el => el.classList.add('border-transparent'));
                element.classList.remove('border-transparent');
                element.classList.add('active', 'border-brand-gold', 'bg-brand-gold/10');
            }
            
            // Scroll to top
            document.getElementById('main-scroll').scrollTop = 0;
        };

        window.showToast = function(message) {
            const toast = document.createElement('div');
            toast.className = 'bg-black/90 border border-brand-gold/50 shadow-lg text-white px-5 py-3 rounded-lg text-sm transition-opacity duration-300 opacity-0';
            toast.innerHTML = `<span class="flex items-center"><svg class="w-5 h-5 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>${message}</span>`;
            const container = document.getElementById('toast-container');
            if(container) {
                container.appendChild(toast);
                setTimeout(() => toast.style.opacity = '1', 10);
                setTimeout(() => {
                    toast.style.opacity = '0';
                    setTimeout(() => toast.remove(), 400);
                }, 3000);
            }
        };

        // Initialize Charts
        document.addEventListener("DOMContentLoaded", () => {
            // Dashboard Combo Chart
            const ctx1 = document.getElementById('monthlyChart').getContext('2d');
            new Chart(ctx1, { type: 'bar', data: { labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'], datasets: [{ label: 'Deliveries', data: [120, 150, 140, 180, 210], backgroundColor: '#D4AF37', borderRadius: 4 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { display: false }, x: { grid: { display: false, drawBorder: false }, ticks: { color: '#666', font: {size: 10} } } } } });

            const ctx2 = document.getElementById('successChart').getContext('2d');
            new Chart(ctx2, { type: 'doughnut', data: { labels: ['Success', 'Failed'], datasets: [{ data: [99, 1], backgroundColor: ['#10B981', '#374151'], borderWidth: 0, cutout: '75%' }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } } });

            const ctx3 = document.getElementById('earningsGrowthChart').getContext('2d');
            let grad3 = ctx3.createLinearGradient(0, 0, 0, 200); grad3.addColorStop(0, 'rgba(168, 85, 247, 0.5)'); grad3.addColorStop(1, 'rgba(168, 85, 247, 0.0)');
            new Chart(ctx3, { type: 'line', data: { labels: ['W1', 'W2', 'W3', 'W4'], datasets: [{ data: [4000, 5200, 4800, 6100], borderColor: '#A855F7', backgroundColor: grad3, borderWidth: 2, fill: true, pointRadius: 0, tension: 0.4 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { display: false }, x: { grid: { display: false, drawBorder: false }, ticks: { color: '#666', font: {size: 10} } } } } });

            // Earnings Tab Combo Chart
            const ctx4 = document.getElementById('earningsComboChart').getContext('2d');
            new Chart(ctx4, {
                type: 'bar',
                data: {
                    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                    datasets: [
                        {
                            type: 'line',
                            label: 'Earnings (₹)',
                            data: [8000, 9500, 11000, 12700],
                            borderColor: '#D4AF37',
                            borderWidth: 2,
                            tension: 0.4,
                            yAxisID: 'y1'
                        },
                        {
                            type: 'bar',
                            label: 'Deliveries',
                            data: [100, 115, 130, 150],
                            backgroundColor: 'rgba(255, 255, 255, 0.1)',
                            borderRadius: 4,
                            yAxisID: 'y'
                        }
                    ]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: '#888' } } },
                    scales: {
                        x: { grid: { color: '#333' }, ticks: { color: '#888' } },
                        y: { position: 'left', grid: { color: '#333' }, ticks: { color: '#888' } },
                        y1: { position: 'right', grid: { drawOnChartArea: false }, ticks: { color: '#D4AF37' } }
                    }
                }
            });
        });
    </script>
</body>
</html>
"""

with open('d:/dbmss/templates/delivery_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Full Dashboard Generated Successfully")
