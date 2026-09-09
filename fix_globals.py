import os

filepath = 'd:/dbmss/templates/shop_products.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject global showToast function
toast_func = """
    window.showToast = function(message) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = `<span class="flex items-center"><svg class="w-5 h-5 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>${message}</span>`;
        const container = document.getElementById('toast-container');
        if(container) {
            container.appendChild(toast);
            setTimeout(() => toast.classList.add('show'), 10);
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 400);
            }, 3000);
        } else {
            console.log("Toast:", message);
        }
    };
"""
# Add it right after the global script tag opening
content = content.replace('<script>\n    window.toggleWishlistProduct =', '<script>\n' + toast_func + '\n    window.toggleWishlistProduct =')

# 2. Export local functions to window
export_block = """
        // Export UI functions to global scope so inline handlers can call them
        window.updateWishlistBadge = updateWishlistBadge;
        window.renderWishlist = renderWishlist;
        window.updateHeartIcons = updateHeartIcons;
"""
# Find a good place to inject this inside DOMContentLoaded. Right before `updateWishlistBadge();` call at the end of setup.
setup_call = """        // Initial setup
        updateWishlistBadge();
        renderWishlist();"""
content = content.replace(setup_call, export_block + '\n' + setup_call)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected global functions successfully.")
