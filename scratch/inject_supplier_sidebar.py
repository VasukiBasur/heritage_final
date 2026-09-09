import re

file_path = r'd:\dbmss\templates\supplier_dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

sidebar_html = """<body class="flex h-screen w-full overflow-hidden bg-[#121212] text-[#e5e5e5]">
    <!-- Supplier Sidebar -->
    <aside class="w-64 bg-brand-dark border-r border-brand-gold/20 flex flex-col h-full shrink-0">
        <div class="h-16 flex items-center justify-center border-b border-brand-gold/20">
            <h1 class="text-xl font-serif font-bold text-brand-gold tracking-wider">Supplier Portal</h1>
        </div>
        <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-1">
            <p class="px-3 text-xs font-bold text-brand-gold/50 uppercase tracking-widest mb-2">Workspace</p>
            <a href="{{ url_for('sup_dashboard') }}" class="block px-3 py-2 rounded-sm text-sm font-medium bg-brand-gold text-brand-black transition-colors">Dashboard</a>
            <a href="{{ url_for('supplier_materials') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Raw Materials</a>
            <a href="{{ url_for('supplier_requests') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Material Requests</a>
            
            <p class="px-3 text-xs font-bold text-brand-gold/50 uppercase tracking-widest mt-6 mb-2">Operations</p>
            <a href="{{ url_for('supplier_deliveries') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Deliveries</a>
            <a href="{{ url_for('supplier_inventory') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Inventory Supply</a>
            
            <p class="px-3 text-xs font-bold text-brand-gold/50 uppercase tracking-widest mt-6 mb-2">Account</p>
            <a href="{{ url_for('supplier_profile') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Profile</a>
            <a href="{{ url_for('logout') }}" class="block px-3 py-2 rounded-sm text-sm font-medium text-red-400 hover:bg-red-400/10 transition-colors mt-4">Logout</a>
        </nav>
    </aside>

    <!-- Main Content Wrapper -->
    <div class="flex flex-col h-full overflow-hidden w-full relative">
        <!-- Top Navbar -->
        <header class="bg-brand-dark/50 border-b border-brand-gold/10 h-16 flex items-center justify-between px-6 shrink-0 z-50">
            <h2 class="text-lg font-serif font-bold text-brand-lightgold">Supplier Overview</h2>
            <div class="flex items-center space-x-4">
                <span class="text-xs text-brand-lightgold">Logged in as <span class="font-bold text-brand-gold">{{ session.get('username', 'Supplier') }}</span></span>
            </div>
        </header>
        
        <!-- Main Scrollable Area -->
        <main class="flex-1 overflow-y-auto p-6 lg:p-10">"""

# Replace the original <body...> through <main...>
# Original: <body class="flex flex-col min-h-screen"> ... <header> ... </header> ... <main ...>

body_start = content.find('<body')
main_end = content.find('>', content.find('<main')) + 1

if body_start != -1 and main_end != -1:
    new_content = content[:body_start] + sidebar_html + content[main_end:]
    
    # Also we need to close the <div class="flex flex-col h-full ..."> we opened in sidebar_html at the end before </body>
    new_content = new_content.replace("</body>", "</div>\n</body>")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Supplier Sidebar injected successfully.")
else:
    print("Failed to find body or main tag.")
