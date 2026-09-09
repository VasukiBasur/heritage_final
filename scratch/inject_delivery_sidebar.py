import re

file_path = r'd:\dbmss\templates\shipment_dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

sidebar_html = """<body class="flex h-screen w-full overflow-hidden bg-[#121212] text-[#e5e5e5]">
    <!-- Logistics Sidebar -->
    <aside class="w-64 bg-brand-dark border-r border-brand-gold/20 flex flex-col h-full shrink-0">
        <div class="h-16 flex items-center justify-center border-b border-brand-gold/20">
            <h1 class="text-xl font-serif font-bold text-brand-gold tracking-wider">Logistics Portal</h1>
        </div>
        <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-1">
            <p class="px-3 text-xs font-bold text-brand-gold/50 uppercase tracking-widest mb-2">Workspace</p>
            <a href="{{ url_for('del_dashboard') }}" class="block px-3 py-2 rounded-sm text-sm font-medium bg-brand-gold text-brand-black transition-colors">Dashboard</a>
            <a href="{{ url_for('delivery_assigned') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Assigned Orders</a>
            <a href="{{ url_for('delivery_status') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Delivery Status</a>
            
            <p class="px-3 text-xs font-bold text-brand-gold/50 uppercase tracking-widest mt-6 mb-2">Operations</p>
            <a href="{{ url_for('delivery_routes') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Route Details</a>
            <a href="{{ url_for('delivery_delivered') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Delivered Orders</a>
            
            <p class="px-3 text-xs font-bold text-brand-gold/50 uppercase tracking-widest mt-6 mb-2">Account</p>
            <a href="{{ url_for('delivery_contact') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Contact Customer</a>
            <a href="{{ url_for('logout') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-red-400 hover:bg-red-400/10 transition-colors mt-4">Logout</a>
        </nav>
    </aside>

    <!-- Main Content Wrapper -->
    <div class="flex flex-col h-full overflow-hidden w-full relative">
        <!-- Top Navbar -->
        <header class="bg-brand-dark/50 border-b border-brand-gold/10 h-16 flex items-center justify-between px-6 shrink-0 z-50">
            <h2 class="text-lg font-serif font-bold text-brand-lightgold">Delivery Overview</h2>
            <div class="flex items-center space-x-4">
                <span class="text-xs text-brand-lightgold">Logged in as <span class="font-bold text-brand-gold">{{ session.get('username', 'Driver') }}</span></span>
            </div>
        </header>
        
        <!-- Main Scrollable Area -->
        <main class="flex-1 overflow-y-auto p-6 lg:p-10">"""

body_start = content.find('<body')
main_end = content.find('>', content.find('<main')) + 1

if body_start != -1 and main_end != -1:
    new_content = content[:body_start] + sidebar_html + content[main_end:]
    new_content = new_content.replace("</body>", "</div>\n</body>")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Delivery Sidebar injected successfully.")
else:
    print("Failed to find body or main tag.")
