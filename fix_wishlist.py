import os
import re

shop_path = r'd:\dbmss\templates\shop_products.html'
dashboard_path = r'd:\dbmss\templates\customer_dashboard.html'

# 1. Update shop_products.html
with open(shop_path, 'r', encoding='utf-8') as f:
    shop_content = f.read()

# Add global function before DOMContentLoaded
global_func = """
    window.toggleWishlistProduct = function(btn, title, price, imgSrc) {
        let wishlistItems = JSON.parse(localStorage.getItem('userWishlist')) || [];
        const existingIndex = wishlistItems.findIndex(i => i.title === title);
        if (existingIndex >= 0) {
            wishlistItems.splice(existingIndex, 1);
            showToast(title + " removed from wishlist");
        } else {
            wishlistItems.push({ title: title, imgSrc: imgSrc, price: price });
            showToast(title + " saved to wishlist!");
        }
        localStorage.setItem('userWishlist', JSON.stringify(wishlistItems));
        
        // Trigger update functions if they exist in scope
        if (typeof updateWishlistBadge === 'function') updateWishlistBadge();
        if (typeof renderWishlist === 'function') renderWishlist();
        if (typeof updateHeartIcons === 'function') updateHeartIcons();
    };
"""
shop_content = shop_content.replace('<script>', '<script>\n' + global_func)

# Remove the event listener loop for wishlist-btn
loop_to_remove = """            document.querySelectorAll(".wishlist-btn").forEach(btn => {
                btn.addEventListener("click", (e) => {
                    const card = e.target.closest(".product-card");
                    const title = card.querySelector(".product-title").innerText;
                    
                    const existingIndex = wishlistItems.findIndex(i => i.title === title);
                    if (existingIndex >= 0) {
                        // Remove
                        wishlistItems.splice(existingIndex, 1);
                        showToast(title + " removed from wishlist");
                    } else {
                        // Add
                        const priceText = card.querySelector(".text-brand-lightgold").innerText.split("/")[0].replace("₹", "").replace(/,/g, "").trim();
                        const price = parseFloat(priceText);
                        const img = card.querySelector("img").src;
                        wishlistItems.push({ title: title, imgSrc: img, price: price });
                        showToast(title + " saved to wishlist!");
                    }
                    localStorage.setItem('userWishlist', JSON.stringify(wishlistItems));
                    updateWishlistBadge();
                    renderWishlist();
                    updateHeartIcons();
                });
            });"""
shop_content = shop_content.replace(loop_to_remove, "")

# Update the button HTML in cardHtml
btn_old = '<button class="wishlist-btn absolute top-3 right-3 z-20 p-2 bg-black/50 backdrop-blur rounded-full text-gray-300 hover:text-red-500 transition-colors">'
btn_new = '<button class="wishlist-btn absolute top-3 right-3 z-20 p-2 bg-black/50 backdrop-blur rounded-full text-gray-300 hover:text-red-500 transition-colors cursor-pointer" onclick="event.preventDefault(); event.stopPropagation(); window.toggleWishlistProduct(this, \'` + product.title.replace(/\'/g, \\"\\\\\'\\") + `\', ` + product.price + `, \'/static/\' + product.img);">'
shop_content = shop_content.replace(btn_old, btn_new)

with open(shop_path, 'w', encoding='utf-8') as f:
    f.write(shop_content)

# 2. Update customer_dashboard.html
with open(dashboard_path, 'r', encoding='utf-8') as f:
    dash_content = f.read()

# Add minimal global func and toast to dashboard
dash_script = """
<!-- Wishlist Minimal Logic for Dashboard -->
<div id="toast-container" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 10px;"></div>
<script>
    function showToast(message) {
        const toast = document.createElement('div');
        toast.style.cssText = 'background: rgba(20, 20, 20, 0.95); border: 1px solid rgba(212, 175, 55, 0.5); box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5); color: white; padding: 12px 20px; border-radius: 8px; font-family: sans-serif; font-size: 14px; transition: opacity 0.4s;';
        toast.innerText = message;
        document.getElementById('toast-container').appendChild(toast);
        setTimeout(() => toast.style.opacity = '0', 3000);
        setTimeout(() => toast.remove(), 3500);
    }

    function toggleWishlistProductDash(btn, title, price, imgSrc) {
        let wishlistItems = JSON.parse(localStorage.getItem('userWishlist')) || [];
        const existingIndex = wishlistItems.findIndex(i => i.title === title);
        if (existingIndex >= 0) {
            wishlistItems.splice(existingIndex, 1);
            showToast(title + " removed from wishlist");
            btn.classList.remove('text-red-500');
            btn.classList.add('text-gray-300');
            btn.innerHTML = `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>`;
        } else {
            wishlistItems.push({ title: title, imgSrc: imgSrc, price: price });
            showToast(title + " saved to wishlist!");
            btn.classList.add('text-red-500');
            btn.classList.remove('text-gray-300');
            btn.innerHTML = `<svg class="w-5 h-5 fill-current" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>`;
        }
        localStorage.setItem('userWishlist', JSON.stringify(wishlistItems));
    }
    
    document.addEventListener("DOMContentLoaded", () => {
        let wishlistItems = JSON.parse(localStorage.getItem('userWishlist')) || [];
        document.querySelectorAll('.dash-wishlist-btn').forEach(btn => {
            if (wishlistItems.some(i => i.title === btn.dataset.title)) {
                btn.classList.add('text-red-500');
                btn.classList.remove('text-gray-300');
                btn.innerHTML = `<svg class="w-5 h-5 fill-current" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>`;
            }
        });
    });
</script>
</body>
"""
dash_content = dash_content.replace('</body>', dash_script)

# Replace the specific links with buttons
link_1 = """<a href="/shop/products" class="absolute top-4 right-4 z-20 p-2 bg-black/50 backdrop-blur rounded-full text-gray-300 hover:text-red-500 transition-colors block">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
                    </a>"""
btn_1 = """<button class="dash-wishlist-btn absolute top-4 right-4 z-20 p-2 bg-black/50 backdrop-blur rounded-full text-gray-300 hover:text-red-500 transition-colors block cursor-pointer" data-title="Royal Banarasi Silk" onclick="event.preventDefault(); event.stopPropagation(); toggleWishlistProductDash(this, 'Royal Banarasi Silk', 18500, '{{ url_for('static', filename='images/banarasi.png') }}')">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
                    </button>"""
dash_content = dash_content.replace(link_1, btn_1)

link_2 = """<a href="/shop/products" class="absolute top-4 right-4 z-20 p-2 bg-black/50 backdrop-blur rounded-full text-red-500 hover:text-red-400 transition-colors block">
                        <svg class="w-5 h-5 fill-current" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
                    </a>"""
btn_2 = """<button class="dash-wishlist-btn absolute top-4 right-4 z-20 p-2 bg-black/50 backdrop-blur rounded-full text-gray-300 hover:text-red-500 transition-colors block cursor-pointer" data-title="Classic Mysore Silk" onclick="event.preventDefault(); event.stopPropagation(); toggleWishlistProductDash(this, 'Classic Mysore Silk', 12200, '{{ url_for('static', filename='images/mysore.png') }}')">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
                    </button>"""
dash_content = dash_content.replace(link_2, btn_2)

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(dash_content)

print("Rewritten successfully")
