import os

html_content = r"""<!DOCTYPE html>
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

        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #0a0a0a; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #D4AF37; }

        /* Map Animations */
        @keyframes pulse-ring {
            0% { transform: scale(0.8); opacity: 0.5; }
            100% { transform: scale(2.5); opacity: 0; }
        }
        
        .map-marker::before {
            content: '';
            position: absolute;
            left: -100%; top: -100%; right: -100%; bottom: -100%;
            border-radius: 50%;
            animation: pulse-ring 2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
            border: 2px solid #D4AF37;
        }

        .map-path {
            stroke-dasharray: 10;
            animation: dash 20s linear infinite;
        }
        
        @keyframes dash {
            to { stroke-dashoffset: -100; }
        }

        .tab-content { display: none; }
        .tab-content.active { display: block; animation: fadeIn 0.4s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        /* Chat bubble styles */
        .chat-bubble-me {
            background-color: #D4AF37;
            color: #000;
            border-radius: 16px 16px 4px 16px;
        }
        .chat-bubble-other {
            background-color: #1a1a1a;
            border: 1px solid #333;
            color: #fff;
            border-radius: 16px 16px 16px 4px;
        }
    </style>
</head>
<body class="flex h-screen overflow-hidden">

    <!-- Toast Notification Container -->
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
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
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
        
        <!-- TOP NAVBAR -->
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
                    <span class="absolute -top-1 -right-1 w-3 h-3 bg-red-500 border-2 border-[#0a0a0a] rounded-full"></span>
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

        <!-- SCROLLABLE CONTENT AREA -->
        <div class="flex-1 overflow-y-auto p-6 relative" id="main-scroll">
            
            <!-- 1. DASHBOARD OVERVIEW TAB -->
            <div id="tab-dashboard" class="tab-content active space-y-6">
                <div class="flex justify-between items-end">
                    <div>
                        <h2 class="text-3xl font-serif text-brand-lightgold mb-1">Welcome back, Rahul</h2>
                        <p class="text-sm text-gray-400">Here is your high-level logistics overview.</p>
                    </div>
                    <button onclick="switchTab('verification', document.querySelector('nav a:nth-child(3)'))" class="bg-brand-gold text-black px-6 py-2 rounded-lg font-bold text-sm hover:bg-yellow-500 transition-colors shadow-[0_0_15px_rgba(212,175,55,0.3)]">Scan QR Code</button>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
                    <div class="glass-panel p-4 rounded-xl border border-gray-800 hover:border-brand-gold/30 transition-colors group">
                        <p class="text-xs text-gray-400 mb-1 uppercase tracking-wider font-bold">Assigned Orders</p>
                        <h3 class="text-2xl font-serif font-bold text-white">12</h3>
                    </div>
                    <div class="glass-panel p-4 rounded-xl border border-brand-gold/40 shadow-[0_0_15px_rgba(212,175,55,0.1)] group">
                        <p class="text-xs text-brand-gold mb-1 uppercase tracking-wider font-bold">In Progress</p>
                        <h3 class="text-2xl font-serif font-bold text-white">3</h3>
                    </div>
                    <div class="glass-panel p-4 rounded-xl border border-gray-800 hover:border-blue-500/30 transition-colors group">
                        <p class="text-xs text-blue-400 mb-1 uppercase tracking-wider font-bold">Pending Pickups</p>
                        <h3 class="text-2xl font-serif font-bold text-white">4</h3>
                    </div>
                    <div class="glass-panel p-4 rounded-xl border border-gray-800 hover:border-green-500/30 transition-colors group">
                        <p class="text-xs text-green-500 mb-1 uppercase tracking-wider font-bold">Delivered Today</p>
                        <h3 class="text-2xl font-serif font-bold text-white">8</h3>
                    </div>
                    <div class="glass-panel p-4 rounded-xl border border-gray-800 hover:border-purple-500/30 transition-colors group">
                        <p class="text-xs text-purple-400 mb-1 uppercase tracking-wider font-bold">On-Time Rate</p>
                        <h3 class="text-2xl font-serif font-bold text-white">98.5%</h3>
                    </div>
                    <div class="glass-panel p-4 rounded-xl border border-gray-800 hover:border-brand-gold/30 transition-colors group">
                        <p class="text-xs text-gray-400 mb-1 uppercase tracking-wider font-bold">Monthly Earnings</p>
                        <h3 class="text-2xl font-serif font-bold text-brand-lightgold">₹34.5k</h3>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="glass-panel p-5 rounded-2xl border border-gray-800">
                        <h3 class="text-sm font-bold text-gray-300 mb-4">Monthly Deliveries</h3>
                        <div class="h-40"><canvas id="monthlyChart"></canvas></div>
                    </div>
                    <div class="glass-panel p-5 rounded-2xl border border-gray-800">
                        <h3 class="text-sm font-bold text-gray-300 mb-4">Success Rate</h3>
                        <div class="h-40 flex items-center justify-center relative">
                            <canvas id="successChart"></canvas>
                            <div class="absolute inset-0 flex items-center justify-center pointer-events-none mt-4">
                                <span class="text-xl font-bold text-white">98%</span>
                            </div>
                        </div>
                    </div>
                    <div class="glass-panel p-5 rounded-2xl border border-gray-800">
                        <h3 class="text-sm font-bold text-gray-300 mb-4">Earnings Growth</h3>
                        <div class="h-40"><canvas id="earningsGrowthChart"></canvas></div>
                    </div>
                </div>
            </div>

            <!-- 2. LIVE TRACKING & ROUTES TAB -->
            <div id="tab-tracking" class="tab-content space-y-6">
                <div class="flex justify-between items-end mb-4">
                    <div>
                        <h2 class="text-3xl font-serif text-brand-lightgold mb-1">Live Tracking & Routes</h2>
                        <p class="text-sm text-gray-400">Real-time logistics monitoring and active route efficiency.</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 xl:grid-cols-4 gap-6 h-[600px]">
                    <div class="xl:col-span-3 glass-panel rounded-2xl border border-gray-800 flex flex-col relative overflow-hidden">
                        <div class="p-4 border-b border-gray-800 flex justify-between items-center z-10 bg-[#0a0a0a]/90 backdrop-blur">
                            <h3 class="text-lg font-serif text-white">Active Route: #ORD-8921</h3>
                            <div class="flex space-x-3 text-xs font-bold text-gray-300">
                                <span class="bg-[#111] border border-gray-700 px-3 py-1 rounded">Dist: 14.5 km</span>
                                <span class="bg-[#111] border border-gray-700 px-3 py-1 rounded">Stops: 3</span>
                                <span class="bg-[#111] border border-brand-gold/30 text-brand-gold px-3 py-1 rounded">ETA: 45 min</span>
                                <span class="bg-green-500/10 border border-green-500/30 text-green-400 px-3 py-1 rounded">Traffic: Light</span>
                            </div>
                        </div>
                        
                        <div class="flex-1 relative bg-[#080808]">
                            <div class="absolute inset-0 opacity-20 pointer-events-none" style="background-image: linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px); background-size: 50px 50px;"></div>
                            
                            <!-- Tracking Map SVG -->
                            <svg class="absolute inset-0 w-full h-full" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
                                <defs>
                                    <linearGradient id="routeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                        <stop offset="0%" stop-color="#4B5563" />
                                        <stop offset="50%" stop-color="#D4AF37" />
                                        <stop offset="100%" stop-color="#10B981" />
                                    </linearGradient>
                                    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                                        <feGaussianBlur stdDeviation="5" result="blur" />
                                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                                    </filter>
                                </defs>
                                <path id="delivery-route" d="M 100 100 C 250 150, 300 350, 500 400 S 750 250, 900 300" fill="none" stroke="url(#routeGradient)" stroke-width="4" stroke-linecap="round" class="map-path" filter="url(#glow)"/>
                                <g>
                                    <circle r="8" fill="#ffffff" filter="drop-shadow(0 0 10px rgba(255,255,255,1))"/>
                                    <animateMotion dur="15s" repeatCount="indefinite" path="M 100 100 C 250 150, 300 350, 500 400 S 750 250, 900 300" />
                                </g>
                            </svg>

                            <div class="absolute top-[80px] left-[80px] flex flex-col items-center">
                                <div class="w-5 h-5 bg-gray-600 rounded-full border-2 border-white z-10 shadow-lg"></div>
                                <div class="mt-2 px-2 py-1 bg-black border border-gray-700 rounded text-xs text-gray-300">Supplier Hub A</div>
                            </div>

                            <div class="absolute top-[380px] left-[480px] flex flex-col items-center">
                                <div class="relative map-marker w-6 h-6 bg-blue-500 rounded-full border-2 border-white z-10 shadow-lg"></div>
                                <div class="mt-2 px-2 py-1 bg-black border border-blue-500/50 rounded text-xs text-blue-400 font-bold">Warehouse B</div>
                            </div>

                            <div class="absolute top-[280px] left-[880px] flex flex-col items-center">
                                <div class="relative map-marker w-7 h-7 bg-brand-gold rounded-full border-2 border-white z-10 shadow-[0_0_20px_#D4AF37]">
                                    <span class="absolute inset-0 m-auto w-3 h-3 bg-white rounded-full animate-pulse"></span>
                                </div>
                                <div class="mt-2 px-3 py-1 bg-black border border-brand-gold rounded text-xs text-brand-lightgold font-bold">Customer Drop-off</div>
                            </div>
                        </div>
                    </div>

                    <div class="glass-panel p-5 rounded-2xl border border-gray-800 flex flex-col">
                        <h3 class="text-lg font-serif text-white mb-4">Active Deliveries</h3>
                        <div class="flex-1 overflow-y-auto space-y-4 pr-2">
                            <div class="bg-brand-gold/10 border border-brand-gold rounded-xl p-4 cursor-pointer">
                                <div class="flex justify-between items-center mb-2">
                                    <span class="text-sm font-bold text-brand-lightgold">#ORD-8921</span>
                                    <span class="text-[10px] bg-brand-gold text-black px-2 py-0.5 rounded font-bold">In Transit</span>
                                </div>
                                <h4 class="text-sm font-bold text-white mb-1">Premium Silk Saree</h4>
                                <p class="text-xs text-gray-400 mb-3">To: Jubilee Hills, Hyderabad</p>
                                <div class="w-full bg-gray-800 rounded-full h-1.5 mb-1"><div class="bg-brand-gold h-1.5 rounded-full" style="width: 65%"></div></div>
                                <div class="flex justify-between text-[10px] text-gray-400"><span>Progress: 65%</span><span>ETA: 14:30</span></div>
                            </div>

                            <div class="bg-[#111] border border-gray-800 rounded-xl p-4 hover:border-gray-600 transition-colors cursor-pointer">
                                <div class="flex justify-between items-center mb-2">
                                    <span class="text-sm font-bold text-gray-300">#PCK-3341</span>
                                    <span class="text-[10px] bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded border border-blue-500/30">Pending Pickup</span>
                                </div>
                                <h4 class="text-sm font-bold text-white mb-1">Artisan Batch B</h4>
                                <p class="text-xs text-gray-400 mb-3">From: Sector 4, Weaver Coop</p>
                                <div class="w-full bg-gray-800 rounded-full h-1.5 mb-1"><div class="bg-blue-500 h-1.5 rounded-full" style="width: 10%"></div></div>
                                <div class="flex justify-between text-[10px] text-gray-400"><span>Progress: 10%</span><span>ETA: 15:45</span></div>
                            </div>
                            
                            <div class="bg-[#111] border border-gray-800 rounded-xl p-4 hover:border-gray-600 transition-colors cursor-pointer">
                                <div class="flex justify-between items-center mb-2">
                                    <span class="text-sm font-bold text-gray-300">#ORD-8850</span>
                                    <span class="text-[10px] bg-gray-700 text-gray-300 px-2 py-0.5 rounded">Scheduled</span>
                                </div>
                                <h4 class="text-sm font-bold text-white mb-1">Cotton Dhotis (x5)</h4>
                                <p class="text-xs text-gray-400 mb-3">To: Banjara Hills, Hyderabad</p>
                                <div class="w-full bg-gray-800 rounded-full h-1.5 mb-1"><div class="bg-gray-500 h-1.5 rounded-full" style="width: 0%"></div></div>
                                <div class="flex justify-between text-[10px] text-gray-400"><span>Progress: 0%</span><span>ETA: 18:00</span></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 3. VERIFICATION TAB -->
            <div id="tab-verification" class="tab-content space-y-6">
                <div class="flex justify-between items-end mb-6">
                    <div>
                        <h2 class="text-3xl font-serif text-brand-lightgold mb-1">Delivery Verification</h2>
                        <p class="text-sm text-gray-400">Capture proof of delivery and obtain customer authorization.</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
                    <!-- Left: Verification Queue -->
                    <div class="glass-panel p-6 rounded-2xl border border-gray-800">
                        <h3 class="text-lg font-serif text-white mb-4">Pending Verifications</h3>
                        <div class="space-y-4">
                            <div class="bg-brand-gold/10 border border-brand-gold rounded-xl p-4">
                                <div class="flex justify-between items-start mb-2">
                                    <div>
                                        <span class="text-sm font-bold text-brand-lightgold block">#ORD-8921</span>
                                        <span class="text-xs text-gray-400">Kanchipuram Silk Saree</span>
                                    </div>
                                    <span class="text-[10px] bg-brand-gold text-black px-2 py-0.5 rounded font-bold uppercase tracking-wider">Arrived</span>
                                </div>
                                <div class="mt-3 text-sm text-gray-300 border-t border-brand-gold/30 pt-3">
                                    <p><span class="text-gray-500">Customer:</span> Anjali Sharma</p>
                                    <p><span class="text-gray-500">Address:</span> 14B, Jubilee Hills, Road No 36</p>
                                    <p><span class="text-gray-500">Amount to Collect:</span> ₹0 (Prepaid)</p>
                                </div>
                            </div>
                            
                            <div class="bg-[#111] border border-gray-800 rounded-xl p-4 opacity-50">
                                <div class="flex justify-between items-start mb-2">
                                    <div>
                                        <span class="text-sm font-bold text-gray-300 block">#ORD-8850</span>
                                        <span class="text-xs text-gray-500">Cotton Dhotis (x5)</span>
                                    </div>
                                    <span class="text-[10px] bg-gray-800 text-gray-400 px-2 py-0.5 rounded">In Transit</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Right: Proof of Delivery Form -->
                    <div class="glass-panel p-6 rounded-2xl border border-gray-800">
                        <h3 class="text-lg font-serif text-white mb-6">Complete Delivery: <span class="text-brand-gold">#ORD-8921</span></h3>
                        
                        <div class="space-y-6">
                            <!-- QR Code -->
                            <div>
                                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">1. Scan Package QR Code</label>
                                <div class="h-32 border-2 border-dashed border-brand-gold/50 rounded-xl flex flex-col items-center justify-center bg-brand-gold/5 cursor-pointer hover:bg-brand-gold/10 transition-colors">
                                    <svg class="w-8 h-8 text-brand-gold mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"></path></svg>
                                    <span class="text-sm font-bold text-brand-lightgold">Tap to Scan QR</span>
                                </div>
                            </div>
                            
                            <!-- OTP -->
                            <div>
                                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">2. Enter Customer OTP</label>
                                <div class="flex space-x-3">
                                    <input type="text" maxlength="1" class="w-12 h-14 bg-[#111] border border-gray-700 rounded-lg text-center text-xl text-white focus:border-brand-gold focus:outline-none" placeholder="-">
                                    <input type="text" maxlength="1" class="w-12 h-14 bg-[#111] border border-gray-700 rounded-lg text-center text-xl text-white focus:border-brand-gold focus:outline-none" placeholder="-">
                                    <input type="text" maxlength="1" class="w-12 h-14 bg-[#111] border border-gray-700 rounded-lg text-center text-xl text-white focus:border-brand-gold focus:outline-none" placeholder="-">
                                    <input type="text" maxlength="1" class="w-12 h-14 bg-[#111] border border-gray-700 rounded-lg text-center text-xl text-white focus:border-brand-gold focus:outline-none" placeholder="-">
                                </div>
                            </div>
                            
                            <!-- Signature -->
                            <div>
                                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">3. Customer Signature</label>
                                <div class="h-24 bg-[#111] border border-gray-700 rounded-xl w-full"></div>
                            </div>
                            
                            <!-- Buttons -->
                            <div class="flex space-x-4 pt-4 border-t border-gray-800">
                                <button onclick="window.showToast('Delivery Successfully Verified!');" class="flex-1 bg-brand-gold text-black py-3 rounded-xl font-bold hover:bg-yellow-500 transition-colors shadow-[0_0_15px_rgba(212,175,55,0.3)]">Verify Delivery</button>
                                <button onclick="window.showToast('Issue Reported')" class="px-6 bg-[#1a1a1a] text-red-400 border border-red-900/50 py-3 rounded-xl font-bold hover:bg-red-900/20 transition-colors">Report Issue</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 4. DELIVERY HISTORY TAB -->
            <div id="tab-history" class="tab-content space-y-6">
                <div class="flex justify-between items-end mb-6">
                    <div>
                        <h2 class="text-3xl font-serif text-brand-lightgold mb-1">Delivery History</h2>
                        <p class="text-sm text-gray-400">Complete log of all past deliveries and performance metrics.</p>
                    </div>
                    <button class="bg-[#1a1a1a] border border-gray-700 text-white px-4 py-2 rounded-lg text-sm hover:border-brand-gold transition-colors flex items-center">
                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                        Export Report
                    </button>
                </div>

                <div class="grid grid-cols-4 gap-4 mb-6">
                    <div class="bg-[#111] border border-gray-800 p-4 rounded-xl text-center"><p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Total Deliveries</p><p class="text-2xl font-serif text-white">412</p></div>
                    <div class="bg-[#111] border border-gray-800 p-4 rounded-xl text-center"><p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Successful</p><p class="text-2xl font-serif text-green-500">407</p></div>
                    <div class="bg-[#111] border border-gray-800 p-4 rounded-xl text-center"><p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Failed/Returned</p><p class="text-2xl font-serif text-red-500">5</p></div>
                    <div class="bg-[#111] border border-gray-800 p-4 rounded-xl text-center"><p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Avg Delivery Time</p><p class="text-2xl font-serif text-brand-gold">42m</p></div>
                </div>

                <div class="glass-panel border border-gray-800 rounded-2xl overflow-hidden">
                    <div class="p-4 border-b border-gray-800 flex justify-between items-center bg-[#0a0a0a]">
                        <input type="text" placeholder="Search Order ID or Customer..." class="bg-[#111] border border-gray-700 rounded-lg px-4 py-1.5 text-sm w-64 text-white focus:outline-none focus:border-brand-gold">
                        <select class="bg-[#111] border border-gray-700 rounded-lg px-4 py-1.5 text-sm text-gray-300 focus:outline-none">
                            <option>All Statuses</option>
                            <option>Delivered</option>
                            <option>Returned</option>
                        </select>
                    </div>
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-[#0f0f0f] text-xs uppercase tracking-wider text-gray-500 border-b border-gray-800">
                                <th class="p-4 font-bold">Order ID</th>
                                <th class="p-4 font-bold">Date & Time</th>
                                <th class="p-4 font-bold">Product</th>
                                <th class="p-4 font-bold">Customer</th>
                                <th class="p-4 font-bold">Distance</th>
                                <th class="p-4 font-bold">Status</th>
                            </tr>
                        </thead>
                        <tbody class="text-sm divide-y divide-gray-800/50">
                            <!-- Generate 10 realistic rows -->
                            <tr class="hover:bg-brand-gold/5 transition-colors">
                                <td class="p-4 font-bold text-gray-300">#ORD-8920</td>
                                <td class="p-4 text-gray-400">May 29, 11:30 AM</td>
                                <td class="p-4 text-brand-lightgold">Banarasi Brocade</td>
                                <td class="p-4 text-gray-300">Rajesh Kumar</td>
                                <td class="p-4 text-gray-400">8.2 km</td>
                                <td class="p-4"><span class="px-2 py-1 bg-green-500/10 text-green-400 text-[10px] uppercase font-bold rounded">Delivered</span></td>
                            </tr>
                            <tr class="hover:bg-brand-gold/5 transition-colors">
                                <td class="p-4 font-bold text-gray-300">#ORD-8919</td>
                                <td class="p-4 text-gray-400">May 29, 09:15 AM</td>
                                <td class="p-4 text-brand-lightgold">Cotton Suit Piece</td>
                                <td class="p-4 text-gray-300">Sneha Reddy</td>
                                <td class="p-4 text-gray-400">12.5 km</td>
                                <td class="p-4"><span class="px-2 py-1 bg-green-500/10 text-green-400 text-[10px] uppercase font-bold rounded">Delivered</span></td>
                            </tr>
                            <tr class="hover:bg-brand-gold/5 transition-colors">
                                <td class="p-4 font-bold text-gray-300">#ORD-8915</td>
                                <td class="p-4 text-gray-400">May 28, 16:45 PM</td>
                                <td class="p-4 text-brand-lightgold">Pashmina Shawl</td>
                                <td class="p-4 text-gray-300">Vikram Singh</td>
                                <td class="p-4 text-gray-400">5.0 km</td>
                                <td class="p-4"><span class="px-2 py-1 bg-green-500/10 text-green-400 text-[10px] uppercase font-bold rounded">Delivered</span></td>
                            </tr>
                            <tr class="hover:bg-brand-gold/5 transition-colors">
                                <td class="p-4 font-bold text-gray-300">#ORD-8912</td>
                                <td class="p-4 text-gray-400">May 28, 14:20 PM</td>
                                <td class="p-4 text-brand-lightgold">Chanderi Saree</td>
                                <td class="p-4 text-gray-300">Pooja Patel</td>
                                <td class="p-4 text-gray-400">18.1 km</td>
                                <td class="p-4"><span class="px-2 py-1 bg-red-500/10 text-red-400 text-[10px] uppercase font-bold rounded">Customer Unavailable</span></td>
                            </tr>
                            <tr class="hover:bg-brand-gold/5 transition-colors">
                                <td class="p-4 font-bold text-gray-300">#ORD-8910</td>
                                <td class="p-4 text-gray-400">May 28, 12:10 PM</td>
                                <td class="p-4 text-brand-lightgold">Linen Kurta</td>
                                <td class="p-4 text-gray-300">Amit Desai</td>
                                <td class="p-4 text-gray-400">3.4 km</td>
                                <td class="p-4"><span class="px-2 py-1 bg-green-500/10 text-green-400 text-[10px] uppercase font-bold rounded">Delivered</span></td>
                            </tr>
                            <tr class="hover:bg-brand-gold/5 transition-colors">
                                <td class="p-4 font-bold text-gray-300">#ORD-8908</td>
                                <td class="p-4 text-gray-400">May 28, 10:05 AM</td>
                                <td class="p-4 text-brand-lightgold">Silk Dupatta</td>
                                <td class="p-4 text-gray-300">Neha Gupta</td>
                                <td class="p-4 text-gray-400">7.8 km</td>
                                <td class="p-4"><span class="px-2 py-1 bg-green-500/10 text-green-400 text-[10px] uppercase font-bold rounded">Delivered</span></td>
                            </tr>
                            <tr class="hover:bg-brand-gold/5 transition-colors">
                                <td class="p-4 font-bold text-gray-300">#ORD-8902</td>
                                <td class="p-4 text-gray-400">May 27, 17:30 PM</td>
                                <td class="p-4 text-brand-lightgold">Handwoven Dhoti</td>
                                <td class="p-4 text-gray-300">Ravi Shankar</td>
                                <td class="p-4 text-gray-400">2.1 km</td>
                                <td class="p-4"><span class="px-2 py-1 bg-green-500/10 text-green-400 text-[10px] uppercase font-bold rounded">Delivered</span></td>
                            </tr>
                            <tr class="hover:bg-brand-gold/5 transition-colors">
                                <td class="p-4 font-bold text-gray-300">#ORD-8899</td>
                                <td class="p-4 text-gray-400">May 27, 15:15 PM</td>
                                <td class="p-4 text-brand-lightgold">Kanchipuram Silk</td>
                                <td class="p-4 text-gray-300">Kavita Iyer</td>
                                <td class="p-4 text-gray-400">9.3 km</td>
                                <td class="p-4"><span class="px-2 py-1 bg-green-500/10 text-green-400 text-[10px] uppercase font-bold rounded">Delivered</span></td>
                            </tr>
                            <tr class="hover:bg-brand-gold/5 transition-colors">
                                <td class="p-4 font-bold text-gray-300">#ORD-8895</td>
                                <td class="p-4 text-gray-400">May 27, 13:00 PM</td>
                                <td class="p-4 text-brand-lightgold">Tussar Silk Saree</td>
                                <td class="p-4 text-gray-300">Sanjay Verma</td>
                                <td class="p-4 text-gray-400">11.6 km</td>
                                <td class="p-4"><span class="px-2 py-1 bg-green-500/10 text-green-400 text-[10px] uppercase font-bold rounded">Delivered</span></td>
                            </tr>
                            <tr class="hover:bg-brand-gold/5 transition-colors">
                                <td class="p-4 font-bold text-gray-300">#ORD-8890</td>
                                <td class="p-4 text-gray-400">May 27, 11:20 AM</td>
                                <td class="p-4 text-brand-lightgold">Cotton Dupatta</td>
                                <td class="p-4 text-gray-300">Priya Singh</td>
                                <td class="p-4 text-gray-400">4.5 km</td>
                                <td class="p-4"><span class="px-2 py-1 bg-green-500/10 text-green-400 text-[10px] uppercase font-bold rounded">Delivered</span></td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="p-4 border-t border-gray-800 flex justify-between items-center text-xs text-gray-500">
                        <span>Showing 1 to 10 of 412 entries</span>
                        <div class="flex space-x-1">
                            <button class="px-3 py-1 bg-[#111] border border-gray-700 rounded hover:border-brand-gold text-white">Previous</button>
                            <button class="px-3 py-1 bg-brand-gold/20 border border-brand-gold text-brand-gold rounded font-bold">1</button>
                            <button class="px-3 py-1 bg-[#111] border border-gray-700 rounded hover:border-brand-gold text-white">2</button>
                            <button class="px-3 py-1 bg-[#111] border border-gray-700 rounded hover:border-brand-gold text-white">Next</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 5. EARNINGS TAB -->
            <div id="tab-earnings" class="tab-content space-y-6">
                <div class="flex justify-between items-end mb-6">
                    <div>
                        <h2 class="text-3xl font-serif text-brand-lightgold mb-1">Earnings Dashboard</h2>
                        <p class="text-sm text-gray-400">Track your financial performance and incentive bonuses.</p>
                    </div>
                    <div class="bg-green-500/10 border border-green-500/30 text-green-400 px-4 py-2 rounded-lg text-sm font-bold flex items-center">
                        <span class="w-2 h-2 rounded-full bg-green-500 mr-2"></span> Next Payout: June 1st
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div class="glass-panel p-5 rounded-xl border border-brand-gold/30 relative overflow-hidden">
                        <div class="absolute right-0 top-0 w-16 h-16 bg-brand-gold/10 rounded-bl-full"></div>
                        <p class="text-xs text-brand-gold uppercase tracking-wider font-bold mb-1">Today's Earnings</p>
                        <h3 class="text-3xl font-serif font-bold text-white mb-2">₹1,250</h3>
                        <p class="text-[10px] text-green-400 flex items-center"><svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg> +12% vs yesterday</p>
                    </div>
                    <div class="glass-panel p-5 rounded-xl border border-gray-800">
                        <p class="text-xs text-gray-400 uppercase tracking-wider font-bold mb-1">Weekly Earnings</p>
                        <h3 class="text-3xl font-serif font-bold text-white mb-2">₹8,450</h3>
                        <p class="text-[10px] text-gray-500 flex items-center">Week of May 23-29</p>
                    </div>
                    <div class="glass-panel p-5 rounded-xl border border-gray-800">
                        <p class="text-xs text-gray-400 uppercase tracking-wider font-bold mb-1">Monthly Earnings</p>
                        <h3 class="text-3xl font-serif font-bold text-white mb-2">₹34,500</h3>
                        <p class="text-[10px] text-green-400 flex items-center"><svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg> +5% vs last month</p>
                    </div>
                    <div class="glass-panel p-5 rounded-xl border border-blue-500/30 relative overflow-hidden">
                        <div class="absolute right-0 top-0 w-16 h-16 bg-blue-500/10 rounded-bl-full"></div>
                        <p class="text-xs text-blue-400 uppercase tracking-wider font-bold mb-1">Bonus Incentives</p>
                        <h3 class="text-3xl font-serif font-bold text-white mb-2">₹2,100</h3>
                        <p class="text-[10px] text-blue-400">98%+ Success Rate Bonus</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 glass-panel p-6 rounded-2xl border border-gray-800">
                        <h3 class="text-sm font-bold text-gray-300 mb-4">Earnings vs Deliveries (Weekly)</h3>
                        <div class="h-64"><canvas id="earningsComboChart"></canvas></div>
                    </div>
                    
                    <div class="glass-panel rounded-2xl border border-gray-800 flex flex-col">
                        <div class="p-4 border-b border-gray-800"><h3 class="text-sm font-bold text-gray-300">Recent Transactions</h3></div>
                        <div class="flex-1 overflow-y-auto p-4 space-y-3">
                            <div class="flex justify-between items-center p-3 bg-[#111] rounded-lg border border-gray-800">
                                <div><p class="text-sm font-bold text-white">Daily Payout</p><p class="text-[10px] text-gray-500">May 28, 2026</p></div>
                                <span class="text-sm font-bold text-green-400">+₹1,150</span>
                            </div>
                            <div class="flex justify-between items-center p-3 bg-[#111] rounded-lg border border-gray-800">
                                <div><p class="text-sm font-bold text-white">Daily Payout</p><p class="text-[10px] text-gray-500">May 27, 2026</p></div>
                                <span class="text-sm font-bold text-green-400">+₹1,420</span>
                            </div>
                            <div class="flex justify-between items-center p-3 bg-brand-gold/10 rounded-lg border border-brand-gold/30">
                                <div><p class="text-sm font-bold text-brand-lightgold">Performance Bonus</p><p class="text-[10px] text-gray-400">May 26, 2026</p></div>
                                <span class="text-sm font-bold text-brand-gold">+₹500</span>
                            </div>
                            <div class="flex justify-between items-center p-3 bg-[#111] rounded-lg border border-gray-800">
                                <div><p class="text-sm font-bold text-white">Daily Payout</p><p class="text-[10px] text-gray-500">May 26, 2026</p></div>
                                <span class="text-sm font-bold text-green-400">+₹1,080</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 6. MESSAGES TAB -->
            <div id="tab-messages" class="tab-content h-[calc(100vh-160px)]">
                <div class="flex h-full glass-panel border border-gray-800 rounded-2xl overflow-hidden">
                    <!-- Contacts Sidebar -->
                    <div class="w-1/3 border-r border-gray-800 flex flex-col bg-[#0a0a0a]">
                        <div class="p-4 border-b border-gray-800">
                            <input type="text" placeholder="Search contacts..." class="w-full bg-[#111] border border-gray-700 rounded-lg py-2 px-4 text-sm text-white focus:outline-none focus:border-brand-gold">
                        </div>
                        <div class="flex-1 overflow-y-auto">
                            <!-- HQ Contact -->
                            <div id="del-contact-hq" onclick="switchDelContact('hq')" class="p-4 border-b border-gray-800 hover:bg-[#1a1a1a] cursor-pointer bg-[#1a1a1a] transition-colors relative">
                                <div class="flex items-center">
                                    <div class="w-10 h-10 rounded-full bg-brand-gold/20 border border-brand-gold text-brand-gold flex items-center justify-center font-bold mr-3">HQ</div>
                                    <div class="flex-1 min-w-0">
                                        <div class="flex justify-between"><h4 class="text-sm font-bold text-white truncate">HQ Logistics Support</h4><span class="text-[10px] text-gray-500">10:48 AM</span></div>
                                        <p class="text-xs text-gray-400 truncate">Copy that. Drive safe!</p>
                                    </div>
                                </div>
                            </div>
                            <!-- Customer Contact -->
                            <div id="del-contact-anjali" onclick="switchDelContact('anjali')" class="p-4 border-b border-gray-800 hover:bg-[#1a1a1a] cursor-pointer transition-colors relative">
                                <div class="flex items-center">
                                    <div class="w-10 h-10 rounded-full bg-[#222] border border-gray-600 text-gray-300 flex items-center justify-center font-bold mr-3">AS</div>
                                    <div class="flex-1 min-w-0">
                                        <div class="flex justify-between"><h4 class="text-sm font-bold text-white truncate">Anjali Sharma (Cust)</h4><span class="text-[10px] text-gray-500">Yesterday</span></div>
                                        <p class="text-xs text-gray-400 truncate font-bold text-white">Hi, I might not be home...</p>
                                    </div>
                                </div>
                                <span class="absolute top-4 right-4 w-2 h-2 bg-brand-gold rounded-full"></span>
                            </div>
                            <!-- Artisan Contact -->
                            <div id="del-contact-weaver" onclick="switchDelContact('weaver')" class="p-4 border-b border-gray-800 hover:bg-[#1a1a1a] cursor-pointer transition-colors">
                                <div class="flex items-center">
                                    <div class="w-10 h-10 rounded-full bg-blue-900/50 border border-blue-700 text-blue-300 flex items-center justify-center font-bold mr-3">WC</div>
                                    <div class="flex-1 min-w-0">
                                        <div class="flex justify-between"><h4 class="text-sm font-bold text-white truncate">Weaver Cooperative</h4><span class="text-[10px] text-gray-500">May 25</span></div>
                                        <p class="text-xs text-gray-400 truncate">Package is ready for pickup at Gate B.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Chat Area -->
                    <div class="flex-1 flex flex-col bg-[#050505]">
                        <div class="h-16 border-b border-gray-800 flex items-center justify-between px-6 bg-[#0a0a0a]">
                            <div class="flex items-center">
                                <div class="w-10 h-10 rounded-full bg-brand-gold/20 border border-brand-gold text-brand-gold flex items-center justify-center font-bold mr-3">HQ</div>
                                <div>
                                    <h3 id="del-chat-header-name" class="font-bold text-white text-sm">HQ Logistics Support</h3>
                                    <p id="del-chat-header-status" class="text-xs text-green-500 flex items-center"><span class="w-2 h-2 rounded-full bg-green-500 mr-2"></span>Online</p>
                                </div>
                            </div>
                        </div>
                        <div id="del-chat-messages" class="flex-1 overflow-y-auto p-6 space-y-4">
                            <!-- Messages injected via JS -->
                        </div>
                        <div class="p-4 border-t border-gray-800 bg-[#0a0a0a]">
                            <div class="flex items-center bg-[#111] border border-gray-700 rounded-full px-4 py-2">
                                <input type="text" id="del-chat-input" placeholder="Type your message..." class="flex-1 bg-transparent border-none focus:outline-none text-sm text-white px-2">
                                <button onclick="window.sendDelMessage()" class="w-8 h-8 rounded-full bg-brand-gold text-black flex items-center justify-center hover:bg-yellow-500 transition-colors">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
        </div>
        
        <footer class="h-10 border-t border-gray-800 flex items-center justify-center text-xs text-gray-600 tracking-widest uppercase shrink-0 z-10 bg-[#050505]">
            Connecting Heritage Crafts To Every Home.
        </footer>
    </main>

    <script>
        // 1. Core Tab Switching Logic (Ultra-Safe)
        window.switchTab = function(tabId, element) {
            try {
                // Hide all tabs
                document.querySelectorAll('.tab-content').forEach(function(el) {
                    el.classList.remove('active');
                });
                
                // Show requested tab
                var targetTab = document.getElementById('tab-' + tabId);
                if (targetTab) {
                    targetTab.classList.add('active');
                }
                
                // Update nav links styling
                if (element) {
                    document.querySelectorAll('.nav-link').forEach(function(el) {
                        el.classList.remove('active');
                        el.classList.add('border-transparent');
                    });
                    element.classList.remove('border-transparent');
                    element.classList.add('active');
                }
                
                // Scroll main area to top
                var scroller = document.getElementById('main-scroll');
                if(scroller) scroller.scrollTop = 0;
            } catch(e) {
                console.error("Tab Switching Error:", e);
            }
        };

        // 2. Global Toast Notification
        window.showToast = function(message) {
            const toast = document.createElement('div');
            toast.className = 'bg-black/90 border border-brand-gold/50 shadow-lg text-white px-5 py-3 rounded-lg text-sm transition-opacity duration-300 opacity-0 flex items-center';
            toast.innerHTML = `<svg class="w-5 h-5 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>${message}`;
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

        // 3. Messages Module Logic
        let currentDelContact = 'hq';
        
        const defaultDelChats = {
            hq: [
                { sender: 'other', text: 'Hello Rahul, we noticed a delay on your route to Jubilee Hills. Are you facing traffic on route 4?', time: '10:45 AM' },
                { sender: 'me', text: 'Yes, there is a roadblock near the main intersection. I am taking the alternate route via the bypass. ETA updated to +10 mins.', time: '10:47 AM' },
                { sender: 'other', text: 'Copy that. Drive safe!', time: '10:48 AM' }
            ],
            anjali: [
                { sender: 'other', text: 'Hi, I might not be home. Please leave it with the security guard.', time: 'Yesterday' }
            ],
            weaver: [
                { sender: 'other', text: 'Package is ready for pickup at Gate B.', time: 'May 25' }
            ]
        };

        const delContactDetails = {
            hq: { name: 'HQ Logistics Support', status: 'Online', statusColor: 'green-500', initials: 'HQ', bg: 'bg-brand-gold/20', border: 'border-brand-gold', text: 'text-brand-gold' },
            anjali: { name: 'Anjali Sharma (Cust)', status: 'Offline', statusColor: 'gray-500', initials: 'AS', bg: 'bg-[#222]', border: 'border-gray-600', text: 'text-gray-300' },
            weaver: { name: 'Weaver Cooperative', status: 'Offline', statusColor: 'gray-500', initials: 'WC', bg: 'bg-blue-900/50', border: 'border-blue-700', text: 'text-blue-300' }
        };

        window.switchDelContact = function(contactId) {
            try {
                currentDelContact = contactId;
                
                // Highlight active contact in sidebar
                document.getElementById('del-contact-hq').classList.remove('bg-[#1a1a1a]');
                document.getElementById('del-contact-anjali').classList.remove('bg-[#1a1a1a]');
                document.getElementById('del-contact-weaver').classList.remove('bg-[#1a1a1a]');
                document.getElementById('del-contact-' + contactId).classList.add('bg-[#1a1a1a]');
                
                // Update chat header
                const details = delContactDetails[contactId];
                document.getElementById('del-chat-header-name').innerText = details.name;
                document.getElementById('del-chat-header-status').innerHTML = `<span class="w-2 h-2 rounded-full bg-${details.statusColor} mr-2"></span>${details.status}`;
                document.getElementById('del-chat-header-status').className = `text-xs text-${details.statusColor} flex items-center`;
                
                // Update header icon
                const headerIcon = document.querySelector('#tab-messages .h-16 .w-10');
                if (headerIcon) {
                    headerIcon.className = `w-10 h-10 rounded-full flex items-center justify-center font-bold mr-3 ${details.bg} ${details.border} ${details.text}`;
                    headerIcon.innerText = details.initials;
                }
                
                window.renderDelMessages();
            } catch(e) { console.error("Message Switch Error:", e); }
        };

        window.renderDelMessages = function() {
            try {
                let chats = JSON.parse(localStorage.getItem('delChats'));
                if (!chats || Object.keys(chats).length === 0) {
                    chats = defaultDelChats;
                    localStorage.setItem('delChats', JSON.stringify(chats));
                }

                const messages = chats[currentDelContact] || [];
                const container = document.getElementById('del-chat-messages');
                if(!container) return;
                
                container.innerHTML = '<div class="flex justify-center mb-4"><span class="text-xs text-gray-600 bg-[#111] px-2 py-1 rounded">Conversation Started</span></div>';

                messages.forEach(msg => {
                    const div = document.createElement('div');
                    if (msg.sender === 'me') {
                        div.className = 'flex justify-end mb-4';
                        div.innerHTML = `
                            <div class="chat-bubble-me px-4 py-2 max-w-[70%] text-sm shadow-md">
                                <p>${msg.text}</p>
                                <span class="text-[10px] opacity-70 block text-right mt-1">${msg.time}</span>
                            </div>`;
                    } else {
                        div.className = 'flex justify-start mb-4';
                        div.innerHTML = `
                            <div class="chat-bubble-other px-4 py-2 max-w-[70%] text-sm shadow-md">
                                <p>${msg.text}</p>
                                <span class="text-[10px] text-gray-500 block mt-1">${msg.time}</span>
                            </div>`;
                    }
                    container.appendChild(div);
                });
                
                container.scrollTop = container.scrollHeight;
            } catch(e) { console.error("Render Messages Error:", e); }
        };

        window.sendDelMessage = function() {
            try {
                const input = document.getElementById('del-chat-input');
                if(!input) return;
                
                const text = input.value.trim();
                if (!text) return;

                let chats = JSON.parse(localStorage.getItem('delChats')) || defaultDelChats;
                if (!chats[currentDelContact]) chats[currentDelContact] = [];
                
                const now = new Date();
                const timeStr = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                
                chats[currentDelContact].push({ sender: 'me', text: text, time: timeStr });
                localStorage.setItem('delChats', JSON.stringify(chats));
                
                input.value = '';
                window.renderDelMessages();
            } catch(e) { console.error("Send Message Error:", e); }
        };

        // 4. Initialization
        document.addEventListener("DOMContentLoaded", () => {
            // Init Chat Input Listener
            try {
                window.renderDelMessages();
                const chatInput = document.getElementById('del-chat-input');
                if(chatInput) {
                    chatInput.addEventListener('keypress', function (e) {
                        if (e.key === 'Enter') {
                            window.sendDelMessage();
                        }
                    });
                }
            } catch(e) { console.error("Chat Init Error:", e); }

            // Init Charts
            try {
                // Dashboard Combo Chart
                const ctx1 = document.getElementById('monthlyChart').getContext('2d');
                new Chart(ctx1, { type: 'bar', data: { labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'], datasets: [{ label: 'Deliveries', data: [120, 150, 140, 180, 210], backgroundColor: '#D4AF37', borderRadius: 4 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { display: false }, x: { grid: { display: false, drawBorder: false }, ticks: { color: '#666', font: {size: 10} } } } } });

                // Success Rate Doughnut
                const ctx2 = document.getElementById('successChart').getContext('2d');
                new Chart(ctx2, { type: 'doughnut', data: { labels: ['Success', 'Failed'], datasets: [{ data: [98, 2], backgroundColor: ['#10B981', '#374151'], borderWidth: 0, cutout: '75%' }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } } });

                // Earnings Growth Line
                const ctx3 = document.getElementById('earningsGrowthChart').getContext('2d');
                let grad3 = ctx3.createLinearGradient(0, 0, 0, 200); grad3.addColorStop(0, 'rgba(168, 85, 247, 0.5)'); grad3.addColorStop(1, 'rgba(168, 85, 247, 0.0)');
                new Chart(ctx3, { type: 'line', data: { labels: ['W1', 'W2', 'W3', 'W4'], datasets: [{ data: [4000, 5200, 4800, 6100], borderColor: '#A855F7', backgroundColor: grad3, borderWidth: 2, fill: true, pointRadius: 0, tension: 0.4 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { display: false }, x: { grid: { display: false, drawBorder: false }, ticks: { color: '#666', font: {size: 10} } } } } });

                // Earnings Tab Combo Chart
                const ctx4 = document.getElementById('earningsComboChart');
                if(ctx4) {
                    new Chart(ctx4.getContext('2d'), {
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
                }
            } catch(e) { console.error("Charts Init Error:", e); }
        });
    </script>
</body>
</html>
"""

with open('d:/dbmss/templates/delivery_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Full Delivery Dashboard Generated Successfully")
