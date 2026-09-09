
    document.addEventListener("DOMContentLoaded", () => {
        const checkboxes = document.querySelectorAll('.filter-checkbox');
        const searchInput = document.getElementById('searchInput');
        const clearBtn = document.getElementById('clearFiltersBtn');
        const products = Array.from(document.querySelectorAll('.product-card'));
        const pageBtns = document.querySelectorAll('.pagination-btn');
        const btnPrev = document.getElementById('btn-prev');
        const btnNext = document.getElementById('btn-next');
        const toastContainer = document.getElementById('toast-container');

        // Add to Cart Logic
        let cartItems = [];
        let cartCount = 0;
        const cartItemsContainer = document.getElementById('cart-items-container');
        const emptyCartMsg = document.getElementById('empty-cart-msg');
        const billingSection = document.getElementById('cart-billing-section');
        const subtotalEl = document.getElementById('cart-subtotal');
        const taxEl = document.getElementById('cart-tax');
        const totalEl = document.getElementById('cart-total');
        const cartDrawer = document.getElementById('cart-drawer');
        const cartOverlay = document.getElementById('cart-overlay');
        const closeCartBtn = document.getElementById('close-cart-btn');
        const checkoutBtn = document.getElementById('checkout-btn');
        const checkoutFormSection = document.getElementById('checkout-form-section');
        const placeOrderBtn = document.getElementById('place-order-btn');
        const backToCartBtn = document.getElementById('back-to-cart-btn');

        function toggleCart() {
            if (cartDrawer) {
                cartDrawer.classList.toggle('open');
                cartOverlay.classList.toggle('open');
            }
        }
        
        if (backToCartBtn) {
            backToCartBtn.addEventListener('click', () => {
                // Transition back to cart
                checkoutFormSection.classList.add('hidden');
                checkoutFormSection.classList.remove('flex');
                cartItemsContainer.classList.remove('hidden');
                billingSection.style.display = 'block';
            });
        }
        
        if (placeOrderBtn) {
            placeOrderBtn.addEventListener('click', () => {
                if (cartItems.length === 0) return;

                // Create Order Object
                let subtotal = 0;
                cartItems.forEach(item => subtotal += item.price);
                const tax = Math.round(subtotal * 0.05);
                const total = subtotal + tax;

                const orderId = '#ORD-' + Math.floor(10000 + Math.random() * 90000);
                const orderDate = new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
                
                // Calculate estimated delivery (5 days from now)
                const deliveryDateObj = new Date();
                deliveryDateObj.setDate(deliveryDateObj.getDate() + 5);
                const estDelivery = deliveryDateObj.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
                
                const newOrder = {
                    id: orderId,
                    date: orderDate,
                    estDelivery: estDelivery,
                    total: total,
                    items: cartItems.length,
                    firstItemTitle: cartItems[0].title,
                    firstItemImg: cartItems[0].imgSrc,
                    status: 'Processing',
                    statusColor: 'text-yellow-500',
                    statusBg: 'bg-yellow-500/10'
                };

                // Save to localStorage
                let userOrders = JSON.parse(localStorage.getItem('userOrders')) || [];
                userOrders.unshift(newOrder); // Add to beginning
                localStorage.setItem('userOrders', JSON.stringify(userOrders));

                // Show success toast
                const toast = document.createElement('div');
                toast.className = 'toast';
                toast.innerHTML = `
                    <svg class="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <div>
                        <h4 class="text-sm font-bold text-white">Order Placed Successfully!</h4>
                        <p class="text-xs text-gray-400">Order ${orderId} has been saved.</p>
                    </div>
                `;
                document.getElementById('toast-container').appendChild(toast);
                setTimeout(() => toast.classList.add('show'), 10);
                setTimeout(() => {
                    toast.classList.remove('show');
                    setTimeout(() => toast.remove(), 400);
                }, 4000);
    
                // Empty cart
                cartItems = [];
                cartCount = 0;
                const badge = document.getElementById('global-cart-badge');
                if (badge) badge.remove();
                
                // Reset View
                checkoutFormSection.classList.add('hidden');
                checkoutFormSection.classList.remove('flex');
                cartItemsContainer.classList.remove('hidden');
                
                // Clear form fields
                document.querySelectorAll('#checkout-form-section input, #checkout-form-section textarea').forEach(el => el.value = '');

                renderCart();
                toggleCart();
            });
        }

        closeCartBtn.addEventListener('click', toggleCart);
        cartOverlay.addEventListener('click', toggleCart);

        // Bind global cart badge to open drawer
        document.body.addEventListener('click', (e) => {
            const badge = e.target.closest('#global-cart-badge');
            if (badge) toggleCart();
        });

        function formatCurrency(num) {
            return '₹' + num.toLocaleString('en-IN');
        }

        function renderCart() {
            if (cartItems.length === 0) {
                emptyCartMsg.style.display = 'block';
                billingSection.style.display = 'none';
                Array.from(cartItemsContainer.children).forEach(child => {
                    if (child !== emptyCartMsg) child.remove();
                });
                return;
            }

            emptyCartMsg.style.display = 'none';
            billingSection.style.display = 'block';
            
            // Clear current items
            Array.from(cartItemsContainer.children).forEach(child => {
                if (child !== emptyCartMsg) child.remove();
            });

            let subtotal = 0;

            cartItems.forEach((item, index) => {
                subtotal += item.price;
                
                const itemEl = document.createElement('div');
                itemEl.className = 'flex gap-4 items-center bg-[#1a1a1a] p-3 rounded-lg border border-gray-800 relative group hover:border-gray-600 transition-colors';
                itemEl.innerHTML = `
                    <img src="${item.imgSrc}" class="cart-item-image">
                    <div class="flex-1">
                        <h4 class="text-white text-sm font-medium line-clamp-1">${item.title}</h4>
                        <div class="text-brand-gold font-mono text-sm mt-1">${formatCurrency(item.price)}</div>
                    </div>
                    <button class="remove-item-btn p-2 text-gray-500 hover:text-red-500 transition-colors" data-index="${index}">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                    </button>
                `;
                cartItemsContainer.appendChild(itemEl);
            });

            // Calculate billing
            const tax = Math.round(subtotal * 0.05); // 5% GST
            const total = subtotal + tax;

            subtotalEl.innerText = formatCurrency(subtotal);
            taxEl.innerText = formatCurrency(tax);
            totalEl.innerText = formatCurrency(total);

            // Re-bind remove buttons
            document.querySelectorAll('.remove-item-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const idx = parseInt(e.currentTarget.dataset.index);
                    cartItems.splice(idx, 1);
                    cartCount--;
                    document.getElementById('cart-count-text').innerText = cartCount;
                    if(cartCount <= 0) {
                        const badge = document.getElementById('global-cart-badge');
                        if(badge) badge.remove();
                    }
                    renderCart();
                });
            });
        }


        // 42 Dynamic Products Database
        const allProducts = [
            { id: 1, title: "Royal Banarasi Silk", price: 18500, category: "silk", region: "varanasi", img: "images/banarasi.png" },
            { id: 2, title: "Classic Mysore Silk", price: 12200, category: "silk", region: "mysuru", img: "images/mysore.png" },
            { id: 3, title: "Kanjeevaram Bridal Silk", price: 24000, category: "silk", region: "kanchipuram", img: "images/kanchipuram.png" },
            { id: 4, title: "Chanderi Ivory Handloom", price: 4800, category: "cotton", region: "chanderi", img: "images/cotton.png" },
            { id: 5, title: "Premium Silk Dhoti", price: 3200, category: "dhoti", region: "kanchipuram", img: "images/dhoti.png" },
            { id: 6, title: "Unspun Raw Silk Material", price: 1500, category: "raw", region: "mysuru", img: "images/rawsilk.png" },
            { id: 7, title: "Royal Paithani Silk", price: 28000, category: "silk", region: "maharashtra", img: "images/paithani.png" },
            { id: 8, title: "Pochampally Ikat Handloom", price: 6500, category: "cotton", region: "telangana", img: "images/ikat.png" },
            { id: 9, title: "Double Ikat Patola Silk", price: 35000, category: "silk", region: "gujarat", img: "images/patola.png" },
            { id: 10, title: "Golden Zari Tissue Saree", price: 21000, category: "silk", region: "varanasi", img: "images/tissuesaree.png" },
            { id: 11, title: "Midnight Black Chanderi", price: 5200, category: "cotton", region: "chanderi", img: "images/blackchanderi.png" },
            { id: 12, title: "Festive Cotton Dhoti", price: 1800, category: "dhoti", region: "mysuru", img: "images/dhoti.png" },
            { id: 13, title: "Kalamkari Printed Saree", price: 7500, category: "cotton", region: "telangana", img: "images/cotton.png" },
            { id: 14, title: "Kosa Silk Dupatta", price: 3500, category: "silk", region: "chanderi", img: "images/tissuesaree.png" },
            { id: 15, title: "Gadwal Silk Cotton", price: 11000, category: "silk", region: "telangana", img: "images/banarasi.png" },
            { id: 16, title: "Men's Kurta Fabric", price: 2200, category: "cotton", region: "varanasi", img: "images/rawsilk.png" },
            { id: 17, title: "Zari Border Dhoti Set", price: 4500, category: "dhoti", region: "kanchipuram", img: "images/dhoti.png" },
            { id: 18, title: "Venkatagiri Fine Cotton", price: 6000, category: "cotton", region: "telangana", img: "images/ikat.png" },
            { id: 19, title: "Bridal Red Kanjeevaram", price: 45000, category: "silk", region: "kanchipuram", img: "images/kanchipuram.png" },
            { id: 20, title: "Handwoven Linen Kurti", price: 3800, category: "cotton", region: "mysuru", img: "images/blackchanderi.png" },
            { id: 21, title: "Tussar Silk Yardage", price: 1800, category: "raw", region: "varanasi", img: "images/rawsilk.png" },
            { id: 22, title: "Navari Saree 9-yard", price: 16500, category: "silk", region: "maharashtra", img: "images/paithani.png" },
            { id: 23, title: "Bandhani Silk Dupatta", price: 4200, category: "silk", region: "gujarat", img: "images/patola.png" },
            { id: 24, title: "Chettinad Cotton Saree", price: 2800, category: "cotton", region: "kanchipuram", img: "images/cotton.png" },
            { id: 25, title: "Pure Gold Zari Dhoti", price: 8500, category: "dhoti", region: "kanchipuram", img: "images/dhoti.png" },
            { id: 26, title: "Mashru Silk Fabric", price: 2400, category: "raw", region: "gujarat", img: "images/rawsilk.png" },
            { id: 27, title: "Ilkal Traditional Saree", price: 7800, category: "cotton", region: "mysuru", img: "images/ikat.png" },
            { id: 28, title: "Handblock Printed Kurta", price: 3100, category: "cotton", region: "chanderi", img: "images/blackchanderi.png" },
            { id: 29, title: "Mysore Crepe Silk", price: 14500, category: "silk", region: "mysuru", img: "images/mysore.png" },
            { id: 30, title: "Bhagalpuri Silk Stole", price: 1500, category: "silk", region: "varanasi", img: "images/tissuesaree.png" },
            { id: 31, title: "Dharmavaram Silk", price: 19500, category: "silk", region: "telangana", img: "images/kanchipuram.png" },
            { id: 32, title: "Handspun Cotton Dhoti", price: 1200, category: "dhoti", region: "mysuru", img: "images/dhoti.png" },
            { id: 33, title: "Silk Blend Shirting", price: 1600, category: "raw", region: "chanderi", img: "images/rawsilk.png" },
            { id: 34, title: "Organza Silk Saree", price: 13000, category: "silk", region: "varanasi", img: "images/tissuesaree.png" },
            { id: 35, title: "Khadi Cotton Shirt", price: 2500, category: "cotton", region: "chanderi", img: "images/cotton.png" },
            { id: 36, title: "Narayanpet Cotton Saree", price: 4200, category: "cotton", region: "telangana", img: "images/ikat.png" },
            { id: 37, title: "Baluchari Silk", price: 26000, category: "silk", region: "varanasi", img: "images/banarasi.png" },
            { id: 38, title: "Eri Silk Men's Shawl", price: 8000, category: "silk", region: "mysuru", img: "images/mysore.png" },
            { id: 39, title: "Premium Vest/Veshti", price: 2100, category: "dhoti", region: "kanchipuram", img: "images/dhoti.png" },
            { id: 40, title: "Jamdani Handloom", price: 15500, category: "cotton", region: "varanasi", img: "images/blackchanderi.png" },
            { id: 41, title: "Ajrakh Print Silk", price: 12500, category: "silk", region: "gujarat", img: "images/patola.png" },
            { id: 42, title: "Raw Cotton Yardage", price: 900, category: "raw", region: "maharashtra", img: "images/rawsilk.png" }
        ];

        let currentPage = 1;
        const productsPerPage = 6;
        let filteredProducts = [...allProducts];

        function renderProducts() {
            const grid = document.getElementById("product-grid");
            if(!grid) return;
            grid.innerHTML = "";
            
            const start = (currentPage - 1) * productsPerPage;
            const end = start + productsPerPage;
            const pageProducts = filteredProducts.slice(start, end);

            if (pageProducts.length === 0) {
                grid.innerHTML = '<div class="col-span-full text-center text-gray-500 py-10">No products found matching your filters.</div>';
                return;
            }

            pageProducts.forEach(product => {
                const regionMap = {
                    "varanasi": "Varanasi, UP",
                    "mysuru": "Mysuru, KA",
                    "kanchipuram": "Kanchipuram, TN",
                    "chanderi": "Chanderi, MP",
                    "maharashtra": "Paithan, MH",
                    "telangana": "Pochampally, TS",
                    "gujarat": "Patan, GJ"
                };
                let regionLabel = regionMap[product.region] || product.region;

                const cardHtml = `
                <div class="product-card glass-panel rounded-2xl overflow-hidden border border-gray-800 transition-all glow-hover group relative flex flex-col" data-category="${product.category}" data-region="${product.region}">
                    <button class="absolute top-3 right-3 z-20 p-2 bg-black/50 backdrop-blur rounded-full text-gray-300 hover:text-red-500 transition-colors">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
                    </button>
                    <div class="h-56 overflow-hidden relative">
                        <!-- We use Jinja-like path replacement dynamically by just prepending /static/ -->
                        <img src="/static/${product.img}" class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700" alt="Product">
                    </div>
                    <div class="p-5 flex-1 flex flex-col">
                        <span class="text-xs text-brand-gold font-bold uppercase tracking-wider mb-1">${regionLabel}</span>
                        <h3 class="text-lg font-serif text-white mb-2 line-clamp-1 product-title">${product.title}</h3>
                        <div class="mt-auto flex items-center justify-between">
                            <span class="text-lg font-bold text-brand-lightgold">₹${product.price.toLocaleString("en-IN")} ${product.category === "raw" ? '<span class="text-xs text-gray-500 font-normal">/ meter</span>' : ""}</span>
                            <button class="add-to-cart-btn px-3 py-1.5 bg-brand-gold text-black rounded text-xs font-bold hover:bg-yellow-500 transition-colors">Add to Cart</button>
                        </div>
                    </div>
                </div>`;
                grid.innerHTML += cardHtml;
            });
            
            // Re-attach listeners to new buttons
            document.querySelectorAll(".add-to-cart-btn").forEach(btn => {
                btn.addEventListener("click", (e) => {
                    const card = e.target.closest(".product-card");
                    const title = card.querySelector(".product-title").innerText;
                    const priceText = card.querySelector(".text-brand-lightgold").innerText.split("/")[0].replace("₹", "").replace(/,/g, "").trim();
                    const price = parseFloat(priceText);
                    const img = card.querySelector("img").src;
                    
                    cartItems.push({ title: title, imgSrc: img, price: price });
                    
                    cartCount++;
                    let badge = document.getElementById("global-cart-badge");
                    if (!badge) {
                        badge = document.createElement("div");
                        badge.id = "global-cart-badge";
                        badge.className = "fixed bottom-24 right-8 bg-brand-gold text-black w-14 h-14 rounded-full flex items-center justify-center shadow-[0_0_20px_rgba(212,175,55,0.5)] z-50 cursor-pointer hover:scale-110 transition-transform";
                        badge.innerHTML = `<svg class="w-6 h-6 absolute" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path></svg><span id="cart-count-text" class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold w-6 h-6 flex items-center justify-center rounded-full border-2 border-[#121212]">1</span>`;
                        document.body.appendChild(badge);
                        badge.addEventListener("click", toggleCart);
                    } else {
                        document.getElementById("cart-count-text").innerText = cartCount;
                    }
                    
                    renderCart();
                    
                    // Button UI feedback
                    const originalText = btn.innerText;
                    btn.innerHTML = `<svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Added`;
                    btn.classList.remove("bg-brand-gold", "text-black", "hover:bg-yellow-500");
                    btn.classList.add("bg-green-500", "text-white");
                    showToast(title);
                    setTimeout(() => {
                        btn.innerText = originalText;
                        btn.classList.add("bg-brand-gold", "text-black", "hover:bg-yellow-500");
                        btn.classList.remove("bg-green-500", "text-white");
                    }, 2000);
                });
            });
        }

        function renderPagination() {
            const paginationContainer = document.getElementById("pagination-controls");
            if(!paginationContainer) return;
            const totalPages = Math.ceil(filteredProducts.length / productsPerPage);
            
            if (totalPages <= 1) {
                paginationContainer.innerHTML = "";
                return;
            }

            let html = `<button id="btn-prev" class="w-8 h-8 rounded border border-gray-700 flex items-center justify-center text-gray-400 hover:border-brand-gold hover:text-brand-gold transition-colors ${currentPage === 1 ? 'opacity-50 cursor-not-allowed' : ''}"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg></button>`;
            
            for (let i = 1; i <= totalPages; i++) {
                html += `<button class="pagination-btn ${currentPage === i ? 'active bg-brand-gold/10 text-brand-gold border-brand-gold' : 'text-gray-400 hover:border-brand-gold hover:text-brand-gold'} w-8 h-8 rounded border border-gray-700 flex items-center justify-center transition-colors font-medium" data-page="${i}">${i}</button>`;
            }
            
            html += `<button id="btn-next" class="w-8 h-8 rounded border border-gray-700 flex items-center justify-center text-gray-400 hover:border-brand-gold hover:text-brand-gold transition-colors ${currentPage === totalPages ? 'opacity-50 cursor-not-allowed' : ''}"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg></button>`;
            
            paginationContainer.innerHTML = html;

            document.querySelectorAll(".pagination-btn").forEach(btn => {
                btn.addEventListener("click", (e) => {
                    currentPage = parseInt(e.target.dataset.page);
                    renderProducts();
                    renderPagination();
                    window.scrollTo({ top: document.getElementById("product-grid").offsetTop - 100, behavior: "smooth" });
                });
            });

            const prevBtn = document.getElementById("btn-prev");
            if (prevBtn) {
                prevBtn.addEventListener("click", () => {
                    if (currentPage > 1) {
                        currentPage--;
                        renderProducts();
                        renderPagination();
                        window.scrollTo({ top: document.getElementById("product-grid").offsetTop - 100, behavior: "smooth" });
                    }
                });
            }

            const nextBtn = document.getElementById("btn-next");
            if (nextBtn) {
                nextBtn.addEventListener("click", () => {
                    if (currentPage < totalPages) {
                        currentPage++;
                        renderProducts();
                        renderPagination();
                        window.scrollTo({ top: document.getElementById("product-grid").offsetTop - 100, behavior: "smooth" });
                    }
                });
            }
        }

        const categoryCheckboxes = document.querySelectorAll("#category-filters .filter-checkbox");
        const regionCheckboxes = document.querySelectorAll("#region-filters .filter-checkbox");
        const searchInputEl = document.getElementById("search-input");
        const clearBtnEl = document.getElementById("clear-filters");

        function applyFilters() {
            const activeCategories = Array.from(categoryCheckboxes).filter(cb => cb.checked).map(cb => cb.value);
            const activeRegions = Array.from(regionCheckboxes).filter(cb => cb.checked).map(cb => cb.value);
            const searchTerm = searchInputEl ? searchInputEl.value.toLowerCase() : "";

            filteredProducts = allProducts.filter(product => {
                const categoryMatch = activeCategories.length === 0 || activeCategories.includes(product.category);
                const regionMatch = activeRegions.length === 0 || activeRegions.includes(product.region);
                let titleMatch = true;
                if(searchTerm) {
                    titleMatch = product.title.toLowerCase().includes(searchTerm);
                }
                return categoryMatch && regionMatch && titleMatch;
            });

            currentPage = 1;
            renderProducts();
            renderPagination();
        }

        categoryCheckboxes.forEach(cb => cb.addEventListener("change", applyFilters));
        regionCheckboxes.forEach(cb => cb.addEventListener("change", applyFilters));
        
        if (searchInputEl) searchInputEl.addEventListener("input", applyFilters);
        if (clearBtnEl) {
            clearBtnEl.addEventListener("click", () => {
                categoryCheckboxes.forEach(cb => cb.checked = false);
                regionCheckboxes.forEach(cb => cb.checked = false);
                if(searchInputEl) searchInputEl.value = "";
                applyFilters();
            });
        }

        // Run Initial Render
        renderProducts();
        renderPagination();

    });
