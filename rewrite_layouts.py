import os
import glob

template_dir = r"d:\dbmss\templates"

sidebar_html = """<body class="flex h-screen overflow-hidden bg-[#121212] text-[#e5e5e5]">
    <!-- Sidebar -->
    <aside class="w-64 bg-brand-dark border-r border-brand-gold/30 flex-col hidden md:flex h-full">
        <div class="h-16 flex items-center px-6 border-b border-brand-gold/30">
            <h1 class="text-xl font-serif font-bold text-brand-gold tracking-wide"><a href="{{ url_for('dashboard') }}">Heritage Handloom</a></h1>
        </div>
        <nav class="flex-1 overflow-y-auto py-6">
            <ul class="space-y-2 px-4">
                <li><a href="{{ url_for('dashboard') }}" class="block px-4 py-2 rounded text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors font-medium">Dashboard</a></li>
                <li><a href="{{ url_for('artisans') }}" class="block px-4 py-2 rounded text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors font-medium">Artisans</a></li>
                <li><a href="{{ url_for('designs') }}" class="block px-4 py-2 rounded text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors font-medium">Designs</a></li>
                <li><a href="{{ url_for('materials') }}" class="block px-4 py-2 rounded text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors font-medium">Materials</a></li>
                {% if session.get('role') == 'Artisan' %}
                <li><a href="{{ url_for('artisan_dashboard') }}" class="block px-4 py-2 rounded text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors font-medium">My Workspace</a></li>
                {% endif %}
                {% if session.get('role') == 'Buyer' %}
                <li><a href="{{ url_for('buyer_marketplace') }}" class="block px-4 py-2 rounded text-brand-lightgold hover:bg-brand-gold/10 hover:text-brand-gold transition-colors font-medium">Marketplace</a></li>
                {% endif %}
            </ul>
        </nav>
        <div class="p-4 border-t border-brand-gold/30">
            <div class="text-xs text-brand-lightgold/50 mb-2 uppercase tracking-widest">Logged in as</div>
            <div class="font-medium text-brand-gold mb-4">{{ session.get('username', 'Guest') }} ({{ session.get('role', 'User') }})</div>
            <a href="{{ url_for('logout') }}" class="block w-full text-center bg-brand-gold text-brand-black hover:bg-yellow-500 px-4 py-2 rounded-sm transition-colors font-semibold text-sm">Logout</a>
        </div>
    </aside>

    <!-- Main Content Wrapper -->
    <div class="flex-1 flex flex-col h-full overflow-hidden">
        <!-- Top Navbar (Mobile only) -->
        <header class="md:hidden bg-brand-dark border-b border-brand-gold/30 h-16 flex items-center justify-between px-4">
            <h1 class="text-xl font-serif font-bold text-brand-gold"><a href="{{ url_for('dashboard') }}">Heritage</a></h1>
            <a href="{{ url_for('logout') }}" class="text-xs bg-brand-gold text-brand-black px-3 py-1 rounded-sm font-semibold">Logout</a>
        </header>

        <!-- Main Scrollable Area -->
        <main class="flex-1 overflow-y-auto p-6 lg:p-10 w-full relative">
"""

footer_html = """
        </main>
    </div>
"""

for filepath in glob.glob(os.path.join(template_dir, "*.html")):
    if 'login.html' in filepath or 'track.html' in filepath:
        continue # Don't touch login page layout
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace the top part
    if '<body class="flex flex-col min-h-screen">' in content:
        # Split the string at <main
        parts = content.split('<main', 1)
        if len(parts) == 2:
            top_part = parts[0]
            bottom_part = '<main' + parts[1]
            
            # Find the end of <main> tag to keep its classes if needed, but we're replacing the whole main opening tag anyway
            main_end = bottom_part.find('>')
            if main_end != -1:
                inner_content = bottom_part[main_end+1:]
                
                # We need to replace the old header and main tag with our sidebar
                # We keep the head part up to <body>
                head_part = top_part.split('<body')[0]
                
                # Now we need to handle the closing tags
                # Split at </main>
                inner_parts = inner_content.split('</main>')
                if len(inner_parts) == 2:
                    content_inside_main = inner_parts[0]
                    after_main = inner_parts[1]
                    
                    # Ensure chat widget is inside the body wrapper but not restricted to main
                    # It's currently in after_main
                    
                    new_content = head_part + sidebar_html + content_inside_main + footer_html + after_main
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated layout for {filepath}")
