import re

file_path = r'd:\dbmss\templates\buyer_marketplace.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_nav = """            <nav class="hidden md:flex space-x-6">
                <a href="{{ url_for('shop_home') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Shop Home</a>
                <a href="{{ url_for('shop_products') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Collections</a>
                <a href="{{ url_for('shop_cart') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">My Cart</a>
                <a href="{{ url_for('shop_checkout') }}" class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors">Checkout</a>
                
                <div class="relative group">
                    <button class="text-brand-lightgold hover:text-brand-gold font-medium transition-colors flex items-center">
                        My Account <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </button>
                    <div class="absolute left-0 mt-2 w-48 bg-brand-dark border border-brand-gold/30 rounded-sm shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50 grid grid-cols-1 divide-y divide-brand-gold/10">
                        <a href="{{ url_for('shop_orders') }}" class="block px-4 py-2 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">Previous Orders</a>
                        <a href="{{ url_for('shop_tracking') }}" class="block px-4 py-2 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">Order Tracking</a>
                        <a href="{{ url_for('shop_wishlist') }}" class="block px-4 py-2 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">Wishlist</a>
                        <a href="{{ url_for('shop_reviews') }}" class="block px-4 py-2 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">My Reviews</a>
                        <a href="{{ url_for('shop_profile') }}" class="block px-4 py-2 text-xs text-brand-lightgold hover:bg-brand-gold hover:text-brand-black transition-colors">Profile Settings</a>
                    </div>
                </div>
            </nav>"""

nav_start = content.find('<nav class="hidden md:flex space-x-6">')
nav_end = content.find('</nav>', nav_start) + 6

if nav_start != -1 and nav_end != -1:
    content = content[:nav_start] + new_nav + content[nav_end:]
    
    # Let's also fix the logo link to shop_home
    content = content.replace('<a href="{{ url_for(\'dashboard\') }}">Heritage Handloom</a>', '<a href="{{ url_for(\'shop_home\') }}">Heritage Handloom</a>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Customer E-Commerce Nav injected successfully.")
else:
    print("Failed to find nav tag.")
