import os

html_path = r'd:\dbmss\templates\shop_products.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject CSS
css_to_add = """
    /* Wishlist Drawer Styles */
    #wishlist-drawer {
        position: fixed;
        top: 0;
        right: -100%;
        width: 100%;
        max-width: 420px;
        height: 100vh;
        background: rgba(18, 18, 18, 0.98);
        backdrop-filter: blur(10px);
        border-left: 1px solid rgba(220, 38, 38, 0.2); /* red border */
        box-shadow: -5px 0 30px rgba(0, 0, 0, 0.8);
        z-index: 100;
        transition: right 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        display: flex;
        flex-direction: column;
    }
    #wishlist-drawer.open { right: 0; }
"""
content = content.replace("#cart-drawer.open { right: 0; }", "#cart-drawer.open { right: 0; }\n" + css_to_add)

# 2. Inject HTML Drawer
drawer_html = """
<!-- Wishlist Drawer -->
<div id="wishlist-drawer">
    <div class="p-6 border-b border-gray-800 flex justify-between items-center">
        <h3 class="text-xl font-serif text-red-400 flex items-center gap-2">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path></svg>
            My Wishlist
        </h3>
        <button id="close-wishlist-btn" class="text-gray-400 hover:text-white transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
    </div>
    
    <div id="wishlist-items-container" class="flex-1 overflow-y-auto p-6 space-y-4">
        <div class="text-center text-gray-500 mt-10" id="empty-wishlist-msg">
            <svg class="w-12 h-12 mx-auto mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
            <p>Your wishlist is empty.</p>
        </div>
    </div>
</div>
"""
# insert after cart-drawer closing div. Let's find: `        </div>\n    </div>\n</div>`
content = content.replace("    </div>\n</div>\n\n<script>", "    </div>\n</div>\n" + drawer_html + "\n<script>")

# 3. Add class to heart button
button_target = '<button class="absolute top-3 right-3 z-20 p-2 bg-black/50 backdrop-blur rounded-full text-gray-300 hover:text-red-500 transition-colors">'
button_replacement = '<button class="wishlist-btn absolute top-3 right-3 z-20 p-2 bg-black/50 backdrop-blur rounded-full text-gray-300 hover:text-red-500 transition-colors">'
content = content.replace(button_target, button_replacement)

# 4. Inject JS logic
# Find: const toastContainer = document.getElementById('toast-container');
# Add wishlist initializations right after it
js_init_target = "const toastContainer = document.getElementById('toast-container');"
js_init_replacement = js_init_target + """
        
        // Wishlist Logic
        let wishlistItems = JSON.parse(localStorage.getItem('userWishlist')) || [];
        const wishlistItemsContainer = document.getElementById('wishlist-items-container');
        const emptyWishlistMsg = document.getElementById('empty-wishlist-msg');
        const wishlistDrawer = document.getElementById('wishlist-drawer');
        const closeWishlistBtn = document.getElementById('close-wishlist-btn');
        
        function toggleWishlist() {
            if (wishlistDrawer) {
                wishlistDrawer.classList.toggle('open');
                cartOverlay.classList.toggle('open');
            }
        }
        
        if (closeWishlistBtn) closeWishlistBtn.addEventListener('click', toggleWishlist);
        
        function updateWishlistBadge() {
            let badge = document.getElementById("global-wishlist-badge");
            if (wishlistItems.length > 0) {
                if (!badge) {
                    badge = document.createElement("div");
                    badge.id = "global-wishlist-badge";
                    // Position it above the cart badge
                    badge.className = "fixed bottom-40 right-8 bg-red-500 text-white w-14 h-14 rounded-full flex items-center justify-center shadow-[0_0_20px_rgba(220,38,38,0.5)] z-50 cursor-pointer hover:scale-110 transition-transform";
                    badge.innerHTML = `<svg class="w-6 h-6 absolute" fill="currentColor" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path></svg><span id="wishlist-count-text" class="absolute -top-2 -right-2 bg-black text-white text-xs font-bold w-6 h-6 flex items-center justify-center rounded-full border-2 border-red-500">${wishlistItems.length}</span>`;
                    document.body.appendChild(badge);
                } else {
                    document.getElementById("wishlist-count-text").innerText = wishlistItems.length;
                }
            } else if (badge) {
                badge.remove();
            }
        }
        
        function renderWishlist() {
            if (wishlistItems.length === 0) {
                emptyWishlistMsg.style.display = 'block';
                Array.from(wishlistItemsContainer.children).forEach(child => {
                    if (child !== emptyWishlistMsg) child.remove();
                });
                return;
            }

            emptyWishlistMsg.style.display = 'none';
            Array.from(wishlistItemsContainer.children).forEach(child => {
                if (child !== emptyWishlistMsg) child.remove();
            });

            wishlistItems.forEach((item, index) => {
                const itemEl = document.createElement('div');
                itemEl.className = 'flex gap-4 items-center bg-[#1a1a1a] p-3 rounded-lg border border-gray-800 relative group hover:border-red-900/50 transition-colors';
                itemEl.innerHTML = `
                    <img src="${item.imgSrc}" class="cart-item-image">
                    <div class="flex-1">
                        <h4 class="text-white text-sm font-medium line-clamp-1">${item.title}</h4>
                        <div class="text-brand-gold font-mono text-sm mt-1">${formatCurrency(item.price)}</div>
                    </div>
                    <div class="flex flex-col gap-2">
                        <button class="move-to-cart-btn p-1.5 text-brand-gold hover:bg-brand-gold hover:text-black rounded transition-colors" data-index="${index}" title="Move to Cart">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
                        </button>
                        <button class="remove-wishlist-btn p-1.5 text-gray-500 hover:text-red-500 rounded transition-colors" data-index="${index}" title="Remove">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                        </button>
                    </div>
                `;
                wishlistItemsContainer.appendChild(itemEl);
            });
            
            // Bind move to cart
            document.querySelectorAll('.move-to-cart-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const idx = parseInt(e.currentTarget.dataset.index);
                    const item = wishlistItems[idx];
                    
                    // Add to cart
                    cartItems.push(item);
                    cartCount++;
                    let cBadge = document.getElementById("global-cart-badge");
                    if (!cBadge) {
                        cBadge = document.createElement("div");
                        cBadge.id = "global-cart-badge";
                        cBadge.className = "fixed bottom-24 right-8 bg-brand-gold text-black w-14 h-14 rounded-full flex items-center justify-center shadow-[0_0_20px_rgba(212,175,55,0.5)] z-50 cursor-pointer hover:scale-110 transition-transform";
                        cBadge.innerHTML = `<svg class="w-6 h-6 absolute" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path></svg><span id="cart-count-text" class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold w-6 h-6 flex items-center justify-center rounded-full border-2 border-[#121212]">1</span>`;
                        document.body.appendChild(cBadge);
                    } else {
                        document.getElementById("cart-count-text").innerText = cartCount;
                    }
                    renderCart();
                    
                    // Remove from wishlist
                    wishlistItems.splice(idx, 1);
                    localStorage.setItem('userWishlist', JSON.stringify(wishlistItems));
                    updateWishlistBadge();
                    renderWishlist();
                    updateHeartIcons();
                    showToast(item.title + " moved to cart!");
                });
            });

            // Bind remove
            document.querySelectorAll('.remove-wishlist-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const idx = parseInt(e.currentTarget.dataset.index);
                    const title = wishlistItems[idx].title;
                    wishlistItems.splice(idx, 1);
                    localStorage.setItem('userWishlist', JSON.stringify(wishlistItems));
                    updateWishlistBadge();
                    renderWishlist();
                    updateHeartIcons();
                    showToast(title + " removed.");
                });
            });
        }
        
        function updateHeartIcons() {
            document.querySelectorAll('.wishlist-btn').forEach(btn => {
                const card = btn.closest('.product-card');
                const title = card.querySelector('.product-title').innerText;
                const inWishlist = wishlistItems.some(i => i.title === title);
                if (inWishlist) {
                    btn.classList.add('text-red-500');
                    btn.classList.remove('text-gray-300');
                    btn.innerHTML = `<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path></svg>`;
                } else {
                    btn.classList.add('text-gray-300');
                    btn.classList.remove('text-red-500');
                    btn.innerHTML = `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>`;
                }
            });
        }
        
        // Initial setup
        updateWishlistBadge();
        renderWishlist();
"""
content = content.replace(js_init_target, js_init_replacement)

# 5. Bind wishlist button clicks in renderProducts
# Find: btn.classList.add("bg-brand-gold", "text-black", "hover:bg-yellow-500");
# Add binding for wishlist buttons
js_bind_target = "            document.querySelectorAll(\".add-to-cart-btn\").forEach(btn => {"
js_bind_replacement = """
            updateHeartIcons();
            
            document.querySelectorAll(".wishlist-btn").forEach(btn => {
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
            });
            
""" + js_bind_target
content = content.replace(js_bind_target, js_bind_replacement)

# 6. Bind global wishlist badge to open drawer
# Find global cart badge binding
badge_bind_target = """        document.body.addEventListener('click', (e) => {
            const badge = e.target.closest('#global-cart-badge');
            if (badge) toggleCart();
        });"""
badge_bind_replacement = badge_bind_target + """
        document.body.addEventListener('click', (e) => {
            const wBadge = e.target.closest('#global-wishlist-badge');
            if (wBadge) toggleWishlist();
        });
"""
content = content.replace(badge_bind_target, badge_bind_replacement)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Wishlist successfully injected')
