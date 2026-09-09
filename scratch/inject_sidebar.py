import re

file_path = r'd:\dbmss\templates\dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The current wrapper is:
# <body class="flex justify-center h-screen w-full overflow-hidden bg-[#121212] text-[#e5e5e5]">
#     <div class="flex flex-col h-full overflow-hidden w-full max-w-[1500px] mx-auto relative shadow-[0_0_50px_rgba(0,0,0,0.8)] border-x border-brand-gold/10">
#         <header ...>...</header>
#         <main ...>...</main>
#     </div>
# </body>

# We will replace the body wrapper with a Sidebar layout.
sidebar_html = """<body class="flex h-screen w-full overflow-hidden bg-[#121212] text-[#e5e5e5]">
    <!-- Admin Sidebar -->
    <aside class="w-64 bg-brand-dark border-r border-brand-gold/20 flex flex-col h-full shrink-0">
        <div class="h-16 flex items-center justify-center border-b border-brand-gold/20">
            <h1 class="text-xl font-serif font-bold text-brand-gold tracking-wider">Heritage</h1>
        </div>
        <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-1">
            <p class="px-3 text-xs font-bold text-brand-gold/50 uppercase tracking-widest mb-2">Main Menu</p>
            <a href="{{ url_for('admin_dashboard') }}" class="block px-3 py-2 rounded-sm text-sm font-medium bg-brand-gold text-brand-black transition-colors">Dashboard</a>
            <a href="{{ url_for('admin_manage_users') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Manage Users</a>
            <a href="{{ url_for('admin_manage_artisans') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Manage Artisans</a>
            <a href="{{ url_for('admin_manage_suppliers') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Manage Suppliers</a>
            <a href="{{ url_for('admin_manage_products') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Manage Products</a>
            
            <p class="px-3 text-xs font-bold text-brand-gold/50 uppercase tracking-widest mt-6 mb-2">Operations</p>
            <a href="{{ url_for('admin_inventory') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Inventory</a>
            <a href="{{ url_for('admin_orders') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Orders</a>
            <a href="{{ url_for('admin_payments') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Payments</a>
            <a href="{{ url_for('admin_shipments') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Shipment Tracking</a>
            
            <p class="px-3 text-xs font-bold text-brand-gold/50 uppercase tracking-widest mt-6 mb-2">System</p>
            <a href="{{ url_for('admin_reports') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Reports & Analytics</a>
            <a href="{{ url_for('admin_settings') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Settings</a>
            <a href="{{ url_for('logout') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-red-400 hover:bg-red-400/10 transition-colors mt-4">Logout</a>
        </nav>
    </aside>

    <!-- Main Content Wrapper -->
    <div class="flex flex-col h-full overflow-hidden w-full relative">
        <!-- Top Navbar -->
        <header class="bg-brand-dark/50 border-b border-brand-gold/10 h-16 flex items-center justify-between px-6 shrink-0 z-50">
            <h2 class="text-lg font-serif font-bold text-brand-lightgold">Admin Overview</h2>
            <div class="flex items-center space-x-4">
                <span class="text-xs text-brand-lightgold">Logged in as <span class="font-bold text-brand-gold">{{ session.get('username', 'Admin') }}</span></span>
            </div>
        </header>"""

# Find the start of the body tag
body_start = content.find('<body')
main_start = content.find('<main')

if body_start != -1 and main_start != -1:
    new_content = content[:body_start] + sidebar_html + "\n" + content[main_start:]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Admin Sidebar injected successfully.")
else:
    print("Failed to find body or main tag.")
