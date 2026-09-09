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
            background: rgba(20, 20, 20, 0.6);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
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
        @keyframes move-vehicle {
            0% { offset-distance: 0%; }
            100% { offset-distance: 100%; }
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
                <a href="#" onclick="switchTab('dashboard', this)" class="nav-link active flex items-center px-6 py-3 text-sm text-gray-400 hover:text-brand-gold hover:bg-brand-gold/5 transition-all border-l-3 border-transparent">
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
                    Dashboard Overview
                </a>
                <a href="#" onclick="switchTab('tracking', this)" class="nav-link flex items-center px-6 py-3 text-sm text-gray-400 hover:text-brand-gold hover:bg-brand-gold/5 transition-all border-l-3 border-transparent">
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path></svg>
                    Live Tracking & Routes
                </a>
                <a href="#" onclick="switchTab('verification', this)" class="nav-link flex items-center px-6 py-3 text-sm text-gray-400 hover:text-brand-gold hover:bg-brand-gold/5 transition-all border-l-3 border-transparent">
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Delivery Verification
                </a>
                <a href="#" onclick="switchTab('history', this)" class="nav-link flex items-center px-6 py-3 text-sm text-gray-400 hover:text-brand-gold hover:bg-brand-gold/5 transition-all border-l-3 border-transparent">
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Delivery History
                </a>
                <a href="#" onclick="switchTab('earnings', this)" class="nav-link flex items-center px-6 py-3 text-sm text-gray-400 hover:text-brand-gold hover:bg-brand-gold/5 transition-all border-l-3 border-transparent">
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Earnings
                </a>
                <a href="#" onclick="switchTab('messages', this)" class="nav-link flex items-center px-6 py-3 text-sm text-gray-400 hover:text-brand-gold hover:bg-brand-gold/5 transition-all border-l-3 border-transparent">
                    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
                    Messages
                    <span class="ml-auto bg-brand-gold text-black text-xs font-bold px-2 py-0.5 rounded-full">2</span>
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
        <header class="h-16 glass-panel border-b border-brand-border/50 flex items-center justify-between px-8 z-10">
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
        <div class="flex-1 overflow-y-auto p-8 relative">
            
            <!-- 1. DASHBOARD OVERVIEW TAB -->
            <div id="tab-dashboard" class="tab-content active space-y-8">
                <div class="flex justify-between items-end">
                    <div>
                        <h2 class="text-3xl font-serif text-brand-lightgold mb-2">Welcome back, Rahul</h2>
                        <p class="text-gray-400">Here is your logistics overview for today.</p>
                    </div>
                    <button class="bg-brand-gold text-black px-6 py-2 rounded-lg font-bold text-sm hover:bg-yellow-500 transition-colors shadow-[0_0_15px_rgba(212,175,55,0.3)]">Scan QR Code</button>
                </div>

                <!-- Metrics Grid -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                    <div class="glass-panel p-6 rounded-2xl border border-gray-800 hover:border-brand-gold/30 transition-colors group">
                        <div class="flex justify-between items-start mb-4">
                            <div class="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-500 flex items-center justify-center group-hover:scale-110 transition-transform">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>
                            </div>
                            <span class="text-xs font-bold text-gray-500">TODAY</span>
                        </div>
                        <h3 class="text-3xl font-serif font-bold text-white mb-1">12</h3>
                        <p class="text-sm text-gray-400">Assigned Deliveries</p>
                    </div>
                    
                    <div class="glass-panel p-6 rounded-2xl border border-brand-gold/30 shadow-[0_0_20px_rgba(212,175,55,0.1)] group">
                        <div class="flex justify-between items-start mb-4">
                            <div class="w-10 h-10 rounded-xl bg-brand-gold/20 text-brand-gold flex items-center justify-center group-hover:scale-110 transition-transform">
                                <svg class="w-5 h-5 animate-spin-slow" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="animation-duration: 3s;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            </div>
                            <span class="px-2 py-1 bg-brand-gold/10 text-brand-gold text-xs rounded-full border border-brand-gold/20">Active</span>
                        </div>
                        <h3 class="text-3xl font-serif font-bold text-white mb-1">3</h3>
                        <p class="text-sm text-gray-400">In Progress</p>
                    </div>

                    <div class="glass-panel p-6 rounded-2xl border border-gray-800 hover:border-green-500/30 transition-colors group">
                        <div class="flex justify-between items-start mb-4">
                            <div class="w-10 h-10 rounded-xl bg-green-500/10 text-green-500 flex items-center justify-center group-hover:scale-110 transition-transform">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                            </div>
                            <span class="text-xs font-bold text-green-500">+4%</span>
                        </div>
                        <h3 class="text-3xl font-serif font-bold text-white mb-1">8</h3>
                        <p class="text-sm text-gray-400">Completed Today</p>
                    </div>

                    <div class="glass-panel p-6 rounded-2xl border border-gray-800 hover:border-purple-500/30 transition-colors group">
                        <div class="flex justify-between items-start mb-4">
                            <div class="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                            </div>
                            <span class="text-xs font-bold text-gray-500">THIS WEEK</span>
                        </div>
                        <h3 class="text-3xl font-serif font-bold text-white mb-1">420<span class="text-lg text-gray-500">km</span></h3>
                        <p class="text-sm text-gray-400">Distance Covered</p>
                    </div>
                </div>

                <!-- Action Lists -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <!-- Pending Pickups -->
                    <div class="glass-panel p-6 rounded-2xl border border-gray-800">
                        <div class="flex justify-between items-center mb-6">
                            <h3 class="text-lg font-serif text-white">Pending Pickups</h3>
                            <button onclick="switchTab('tracking', document.querySelector('nav a:nth-child(2)'))" class="text-sm text-brand-gold hover:text-white transition-colors">View Map →</button>
                        </div>
                        <div class="space-y-4">
                            <!-- Task 1 -->
                            <div class="p-4 bg-[#111] border border-gray-800 rounded-xl flex justify-between items-center hover:border-brand-gold/30 transition-colors">
                                <div class="flex items-center space-x-4">
                                    <div class="w-10 h-10 rounded-lg bg-gray-800 flex items-center justify-center text-gray-400">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                                    </div>
                                    <div>
                                        <h4 class="text-white font-bold text-sm">Weaver Cooperative</h4>
                                        <p class="text-xs text-gray-400">Pochampally Hub • 3 items</p>
                                    </div>
                                </div>
                                <button onclick="window.showToast('Pickup Confirmed!')" class="px-3 py-1.5 bg-[#1a1a1a] border border-gray-700 hover:border-brand-gold text-brand-gold rounded text-xs font-bold transition-colors">Confirm</button>
                            </div>
                            <!-- Task 2 -->
                            <div class="p-4 bg-[#111] border border-gray-800 rounded-xl flex justify-between items-center hover:border-brand-gold/30 transition-colors">
                                <div class="flex items-center space-x-4">
                                    <div class="w-10 h-10 rounded-lg bg-gray-800 flex items-center justify-center text-gray-400">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"></path></svg>
                                    </div>
                                    <div>
                                        <h4 class="text-white font-bold text-sm">Central Warehouse</h4>
                                        <p class="text-xs text-gray-400">Sector 4 • 12 items</p>
                                    </div>
                                </div>
                                <button onclick="window.showToast('Pickup Confirmed!')" class="px-3 py-1.5 bg-[#1a1a1a] border border-gray-700 hover:border-brand-gold text-brand-gold rounded text-xs font-bold transition-colors">Confirm</button>
                            </div>
                        </div>
                    </div>

                    <!-- Current Deliveries -->
                    <div class="glass-panel p-6 rounded-2xl border border-gray-800">
                        <div class="flex justify-between items-center mb-6">
                            <h3 class="text-lg font-serif text-white">Active Deliveries</h3>
                        </div>
                        <div class="space-y-4">
                            <!-- Delivery 1 -->
                            <div class="p-4 bg-[#111] border border-brand-gold/30 rounded-xl relative overflow-hidden group">
                                <div class="absolute top-0 left-0 w-1 h-full bg-brand-gold"></div>
                                <div class="flex justify-between mb-2 pl-2">
                                    <span class="text-xs font-bold text-brand-gold">#ORD-8921</span>
                                    <span class="text-xs text-gray-400">ETA: 14:30</span>
                                </div>
                                <h4 class="text-white font-bold text-sm pl-2 mb-1">Pure Kanchipuram Silk Saree</h4>
                                <p class="text-xs text-gray-400 pl-2 mb-3">To: Anjali Sharma, Jubilee Hills</p>
                                <div class="pl-2 flex space-x-2">
                                    <button onclick="switchTab('verification', document.querySelector('nav a:nth-child(3)'))" class="px-4 py-1.5 bg-brand-gold text-black rounded text-xs font-bold hover:bg-yellow-500 transition-colors">Verify Delivery</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 2. LIVE TRACKING TAB (CSS Map) -->
            <div id="tab-tracking" class="tab-content h-full flex flex-col">
                <div class="flex justify-between items-end mb-6">
                    <div>
                        <h2 class="text-2xl font-serif text-brand-lightgold mb-1">Live Route Planner</h2>
                        <p class="text-sm text-gray-400">Optimized logistics path for your current load.</p>
                    </div>
                    <div class="flex space-x-3">
                        <span class="px-3 py-1 bg-[#111] border border-gray-700 rounded-lg text-xs font-bold text-gray-300">Route Efficiency: 94%</span>
                        <span class="px-3 py-1 bg-[#111] border border-brand-gold/30 rounded-lg text-xs font-bold text-brand-gold">Est. Time: 2h 15m</span>
                    </div>
                </div>

                <div class="flex-1 glass-panel rounded-2xl border border-gray-800 overflow-hidden relative min-h-[500px]">
                    <!-- CSS Mock Map Background -->
                    <div class="absolute inset-0 opacity-20 pointer-events-none" 
                         style="background-image: 
                            linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
                            linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px); 
                            background-size: 50px 50px;">
                    </div>
                    
                    <!-- Decorative Map Elements -->
                    <svg class="absolute inset-0 w-full h-full" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="pathGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#4B5563" />
                                <stop offset="50%" stop-color="#D4AF37" />
                                <stop offset="100%" stop-color="#10B981" />
                            </linearGradient>
                        </defs>
                        <!-- Route Line -->
                        <path d="M 100 100 C 200 100, 300 300, 500 250 S 700 400, 800 150" fill="none" stroke="url(#pathGradient)" stroke-width="4" stroke-linecap="round" class="map-path"/>
                        
                        <!-- Animated Vehicle -->
                        <g>
                            <circle r="8" fill="#ffffff" filter="drop-shadow(0 0 10px rgba(255,255,255,0.8))"/>
                            <circle r="4" fill="#000"/>
                            <animateMotion dur="15s" repeatCount="indefinite" path="M 100 100 C 200 100, 300 300, 500 250 S 700 400, 800 150" />
                        </g>
                    </svg>

                    <!-- Location Markers -->
                    <!-- Warehouse -->
                    <div class="absolute top-[80px] left-[80px] flex flex-col items-center group">
                        <div class="relative map-marker w-6 h-6 bg-gray-700 rounded-full border-2 border-white flex items-center justify-center z-10">
                            <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                        </div>
                        <div class="mt-2 px-2 py-1 bg-black/80 border border-gray-700 rounded text-[10px] text-white opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">Warehouse A</div>
                    </div>

                    <!-- Pickup -->
                    <div class="absolute top-[230px] left-[480px] flex flex-col items-center group">
                        <div class="relative map-marker w-6 h-6 bg-brand-gold rounded-full border-2 border-white flex items-center justify-center z-10 shadow-[0_0_15px_#D4AF37]">
                            <span class="w-2 h-2 bg-white rounded-full animate-pulse"></span>
                        </div>
                        <div class="mt-2 px-2 py-1 bg-black/80 border border-brand-gold/50 rounded text-[10px] text-brand-lightgold whitespace-nowrap">Next Stop: Customer #8921</div>
                    </div>

                    <!-- Destination -->
                    <div class="absolute top-[130px] left-[780px] flex flex-col items-center group">
                        <div class="relative w-6 h-6 bg-green-500 rounded-full border-2 border-white flex items-center justify-center z-10">
                            <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                        </div>
                        <div class="mt-2 px-2 py-1 bg-black/80 border border-green-500/50 rounded text-[10px] text-green-400 whitespace-nowrap">Final Delivery</div>
                    </div>
                </div>
            </div>

            <!-- 3. VERIFICATION TAB -->
            <div id="tab-verification" class="tab-content max-w-3xl mx-auto space-y-8">
                <div class="text-center">
                    <h2 class="text-3xl font-serif text-brand-lightgold mb-2">Proof of Delivery</h2>
                    <p class="text-gray-400">Complete verification for Order #ORD-8921</p>
                </div>

                <div class="glass-panel p-8 rounded-2xl border border-brand-gold/30 relative overflow-hidden">
                    <div class="absolute top-0 right-0 p-4">
                        <span class="px-3 py-1 bg-brand-gold/20 text-brand-gold border border-brand-gold/30 rounded-full text-xs font-bold">At Location</span>
                    </div>
                    
                    <div class="mb-8 border-b border-gray-800 pb-6">
                        <h3 class="text-lg text-white font-bold">Customer Details</h3>
                        <p class="text-sm text-gray-400 mt-1">Anjali Sharma • +91 98765 43210</p>
                        <p class="text-sm text-gray-400">123 Heritage Lane, Jubilee Hills, Hyderabad</p>
                    </div>

                    <div class="space-y-6">
                        <!-- OTP/QR -->
                        <div>
                            <label class="block text-sm font-bold text-gray-300 mb-2">Enter Customer Delivery PIN</label>
                            <div class="flex space-x-4">
                                <input type="text" maxlength="1" class="w-12 h-14 text-center text-2xl font-bold bg-[#111] border border-gray-700 focus:border-brand-gold rounded-xl text-white outline-none">
                                <input type="text" maxlength="1" class="w-12 h-14 text-center text-2xl font-bold bg-[#111] border border-gray-700 focus:border-brand-gold rounded-xl text-white outline-none">
                                <input type="text" maxlength="1" class="w-12 h-14 text-center text-2xl font-bold bg-[#111] border border-gray-700 focus:border-brand-gold rounded-xl text-white outline-none">
                                <input type="text" maxlength="1" class="w-12 h-14 text-center text-2xl font-bold bg-[#111] border border-gray-700 focus:border-brand-gold rounded-xl text-white outline-none">
                                <span class="ml-4 flex items-center text-sm text-gray-500">or</span>
                                <button onclick="window.showToast('Camera opened for QR scan')" class="ml-4 px-4 py-2 bg-[#1a1a1a] border border-gray-700 hover:border-brand-gold text-brand-gold rounded-xl text-sm font-bold transition-colors flex items-center">
                                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"></path></svg>
                                    Scan QR
                                </button>
                            </div>
                        </div>

                        <!-- Photo Upload -->
                        <div>
                            <label class="block text-sm font-bold text-gray-300 mb-2">Upload Delivery Proof Photo</label>
                            <div onclick="window.showToast('Camera triggered for photo')" class="border-2 border-dashed border-gray-700 hover:border-brand-gold bg-[#111] rounded-xl p-8 text-center cursor-pointer transition-colors group">
                                <div class="w-12 h-12 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-3 group-hover:bg-brand-gold/20 group-hover:text-brand-gold text-gray-400 transition-colors">
                                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                                </div>
                                <p class="text-sm text-gray-400">Tap to capture package at doorstep</p>
                            </div>
                        </div>

                        <!-- Signature -->
                        <div>
                            <label class="block text-sm font-bold text-gray-300 mb-2">Customer Signature (Optional)</label>
                            <div class="h-32 bg-[#111] border border-gray-700 rounded-xl w-full relative">
                                <span class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-gray-600 text-sm pointer-events-none">Sign Here</span>
                            </div>
                        </div>

                        <button onclick="window.showToast('Delivery Successfully Verified and Completed!'); switchTab('dashboard', document.querySelector('nav a:nth-child(1)'))" class="w-full py-4 bg-brand-gold text-black rounded-xl font-bold text-lg hover:bg-yellow-500 transition-colors shadow-[0_0_20px_rgba(212,175,55,0.4)]">
                            Mark as Delivered
                        </button>
                    </div>
                </div>
            </div>

            <!-- 4. EARNINGS TAB -->
            <div id="tab-earnings" class="tab-content space-y-8">
                <div class="flex justify-between items-end">
                    <div>
                        <h2 class="text-3xl font-serif text-brand-lightgold mb-2">Earnings Dashboard</h2>
                        <p class="text-gray-400">Track your performance and payouts.</p>
                    </div>
                    <select class="bg-[#111] border border-gray-700 text-white rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-brand-gold">
                        <option>This Month (May 2026)</option>
                        <option>Last Month</option>
                        <option>Year to Date</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="glass-panel p-8 rounded-2xl border border-brand-gold/30 relative overflow-hidden">
                        <div class="absolute top-0 right-0 w-24 h-24 bg-brand-gold/10 rounded-bl-full -mr-4 -mt-4"></div>
                        <p class="text-gray-400 text-sm mb-1">Total Earnings</p>
                        <h3 class="text-4xl font-serif font-bold text-brand-lightgold">₹34,500</h3>
                        <p class="text-xs text-green-500 mt-2 font-bold">+12% vs last month</p>
                    </div>
                    <div class="glass-panel p-8 rounded-2xl border border-gray-800">
                        <p class="text-gray-400 text-sm mb-1">Incentives Earned</p>
                        <h3 class="text-4xl font-serif font-bold text-white">₹4,200</h3>
                        <p class="text-xs text-gray-500 mt-2">From perfect delivery scores</p>
                    </div>
                    <div class="glass-panel p-8 rounded-2xl border border-gray-800">
                        <p class="text-gray-400 text-sm mb-1">Pending Payout</p>
                        <h3 class="text-4xl font-serif font-bold text-white">₹8,450</h3>
                        <p class="text-xs text-brand-gold mt-2">Scheduled for May 31</p>
                    </div>
                </div>

                <div class="glass-panel p-6 rounded-2xl border border-gray-800">
                    <h3 class="text-lg font-bold text-white mb-6">Earnings Trend</h3>
                    <div class="h-64">
                        <canvas id="earningsChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- 5. DELIVERY HISTORY TAB -->
            <div id="tab-history" class="tab-content space-y-6">
                <div>
                    <h2 class="text-2xl font-serif text-brand-lightgold mb-1">Delivery Log</h2>
                    <p class="text-sm text-gray-400">History of all your completed tasks.</p>
                </div>
                
                <div class="glass-panel rounded-2xl border border-gray-800 overflow-hidden">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-gray-800 bg-[#111]">
                                <th class="p-4 text-xs uppercase tracking-widest text-gray-500 font-bold">Order ID</th>
                                <th class="p-4 text-xs uppercase tracking-widest text-gray-500 font-bold">Date</th>
                                <th class="p-4 text-xs uppercase tracking-widest text-gray-500 font-bold">Customer</th>
                                <th class="p-4 text-xs uppercase tracking-widest text-gray-500 font-bold">Distance</th>
                                <th class="p-4 text-xs uppercase tracking-widest text-gray-500 font-bold">Status</th>
                            </tr>
                        </thead>
                        <tbody class="text-sm text-gray-300">
                            <tr class="border-b border-gray-800/50 hover:bg-[#1a1a1a] transition-colors">
                                <td class="p-4 font-bold text-white">#ORD-8890</td>
                                <td class="p-4 text-gray-400">May 28, 2026</td>
                                <td class="p-4">Vikram Singh</td>
                                <td class="p-4">12 km</td>
                                <td class="p-4"><span class="px-2 py-1 bg-green-500/20 text-green-500 rounded text-xs font-bold border border-green-500/30">Delivered</span></td>
                            </tr>
                            <tr class="border-b border-gray-800/50 hover:bg-[#1a1a1a] transition-colors">
                                <td class="p-4 font-bold text-white">#ORD-8885</td>
                                <td class="p-4 text-gray-400">May 27, 2026</td>
                                <td class="p-4">Priya Patel</td>
                                <td class="p-4">8 km</td>
                                <td class="p-4"><span class="px-2 py-1 bg-green-500/20 text-green-500 rounded text-xs font-bold border border-green-500/30">Delivered</span></td>
                            </tr>
                            <tr class="hover:bg-[#1a1a1a] transition-colors">
                                <td class="p-4 font-bold text-white">#ORD-8872</td>
                                <td class="p-4 text-gray-400">May 25, 2026</td>
                                <td class="p-4">Rahul Desai</td>
                                <td class="p-4">24 km</td>
                                <td class="p-4"><span class="px-2 py-1 bg-green-500/20 text-green-500 rounded text-xs font-bold border border-green-500/30">Delivered</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 6. MESSAGES TAB -->
            <div id="tab-messages" class="tab-content h-full">
                <!-- Using a simplified mock for messages to keep it within the single page architecture -->
                <div class="glass-panel rounded-2xl border border-gray-800 flex h-[600px] overflow-hidden">
                    <div class="w-1/3 border-r border-gray-800 flex flex-col">
                        <div class="p-4 border-b border-gray-800 font-bold text-white">Dispatcher Contacts</div>
                        <div class="p-4 border-b border-gray-800 bg-[#1a1a1a]">
                            <h4 class="text-white text-sm font-bold">HQ Logistics Support</h4>
                            <p class="text-xs text-gray-400 truncate">Are you facing traffic on route 4?</p>
                        </div>
                    </div>
                    <div class="flex-1 flex flex-col bg-[#0a0a0a]">
                        <div class="p-4 border-b border-gray-800"><h4 class="text-brand-gold font-bold">HQ Logistics Support</h4></div>
                        <div class="flex-1 p-6 space-y-4">
                            <div class="flex justify-start">
                                <div class="bg-[#1a1a1a] border border-gray-800 text-gray-300 rounded-2xl px-4 py-2 max-w-[70%] text-sm">Are you facing traffic on route 4?</div>
                            </div>
                        </div>
                        <div class="p-4 border-t border-gray-800 bg-[#111] flex space-x-2">
                            <input type="text" placeholder="Reply..." class="flex-1 bg-black border border-gray-700 rounded py-2 px-3 text-sm text-white focus:outline-none focus:border-brand-gold">
                            <button onclick="window.showToast('Message Sent')" class="bg-brand-gold text-black px-4 rounded font-bold hover:bg-yellow-500 text-sm">Send</button>
                        </div>
                    </div>
                </div>
            </div>

        </div>
        
        <footer class="h-10 border-t border-gray-800 flex items-center justify-center text-xs text-gray-600 tracking-widest uppercase">
            Connecting Heritage Crafts To Every Home.
        </footer>
    </main>

    <script>
        // Tab Switching Logic
        window.switchTab = function(tabId, element) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            
            if(element) {
                document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active', 'border-brand-gold', 'bg-brand-gold/10'));
                document.querySelectorAll('.nav-link').forEach(el => el.classList.add('border-transparent'));
                
                element.classList.remove('border-transparent');
                element.classList.add('active', 'border-brand-gold', 'bg-brand-gold/10');
            }
        };

        // Initialize Chart.js for Earnings
        document.addEventListener("DOMContentLoaded", () => {
            const ctx = document.getElementById('earningsChart').getContext('2d');
            
            // Gradient for chart line
            let gradient = ctx.createLinearGradient(0, 0, 0, 400);
            gradient.addColorStop(0, 'rgba(212, 175, 55, 0.5)');   
            gradient.addColorStop(1, 'rgba(212, 175, 55, 0.0)');

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                    datasets: [{
                        label: 'Earnings (₹)',
                        data: [7500, 8200, 9100, 9700],
                        borderColor: '#D4AF37',
                        backgroundColor: gradient,
                        borderWidth: 3,
                        pointBackgroundColor: '#fff',
                        pointBorderColor: '#D4AF37',
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { 
                            beginAtZero: true, 
                            grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
                            ticks: { color: '#888' }
                        },
                        x: { 
                            grid: { display: false, drawBorder: false },
                            ticks: { color: '#888' }
                        }
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

print("Delivery Partner Dashboard Template Created Successfully.")
