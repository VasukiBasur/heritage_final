import re

with open('templates/shop_products.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the entire Product Grid and Pagination section with empty containers
new_html = """<div id="product-grid" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
                <!-- Products dynamically rendered here by JS -->
            </div>
            
            <!-- Pagination Controls -->
            <div class="mt-10 flex justify-center space-x-2" id="pagination-controls">
                <!-- Controls dynamically rendered here by JS -->
            </div>"""

# This regex matches from <div id="product-grid" down to the end of the pagination controls div
pattern = re.compile(r'<div id="product-grid".*?id="btn-next".*?</button>\s*</div>', re.DOTALL)
content = pattern.sub(new_html, content)

# 2. Prepare the 42 products JS Array
js_products = """
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
            const grid = document.getElementById('product-grid');
            grid.innerHTML = '';
            
            const start = (currentPage - 1) * productsPerPage;
            const end = start + productsPerPage;
            const pageProducts = filteredProducts.slice(start, end);

            if (pageProducts.length === 0) {
                grid.innerHTML = '<div class="col-span-full text-center text-gray-500 py-10">No products found matching your filters.</div>';
                return;
            }

            pageProducts.forEach(product => {
                // Ensure region string matches uppercase
                const regionMap = {
                    'varanasi': 'Varanasi, UP',
                    'mysuru': 'Mysuru, KA',
                    'kanchipuram': 'Kanchipuram, TN',
                    'chanderi': 'Chanderi, MP',
                    'maharashtra': 'Paithan, MH',
                    'telangana': 'Pochampally, TS',
                    'gujarat': 'Patan, GJ'
                };
                
                let regionLabel = regionMap[product.region] || product.region;

                const cardHtml = `
                <div class="product-card glass-panel rounded-2xl overflow-hidden border border-gray-800 transition-all glow-hover group relative flex flex-col" data-category="${product.category}" data-region="${product.region}">
                    <button class="absolute top-3 right-3 z-20 p-2 bg-black/50 backdrop-blur rounded-full text-gray-300 hover:text-red-500 transition-colors">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
                    </button>
                    <div class="h-56 overflow-hidden relative">
                        <img src="{{ url_for('static', filename='') }}${product.img}" class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700" alt="Product">
                    </div>
                    <div class="p-5 flex-1 flex flex-col">
                        <span class="text-xs text-brand-gold font-bold uppercase tracking-wider mb-1">${regionLabel}</span>
                        <h3 class="text-lg font-serif text-white mb-2 line-clamp-1 product-title">${product.title}</h3>
                        <div class="mt-auto flex items-center justify-between">
                            <span class="text-lg font-bold text-brand-lightgold">₹${product.price.toLocaleString('en-IN')} ${product.category === 'raw' ? '<span class="text-xs text-gray-500 font-normal">/ meter</span>' : ''}</span>
                            <button class="add-to-cart-btn px-3 py-1.5 bg-brand-gold text-black rounded text-xs font-bold hover:bg-yellow-500 transition-colors">Add to Cart</button>
                        </div>
                    </div>
                </div>`;
                grid.innerHTML += cardHtml;
            });
            
            // Re-attach listeners to new buttons
            document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const card = e.target.closest('.product-card');
                    const title = card.querySelector('.product-title').innerText;
                    const priceText = card.querySelector('.text-brand-lightgold').innerText.split('/')[0].replace('₹', '').replace(/,/g, '').trim();
                    const price = parseFloat(priceText);
                    const img = card.querySelector('img').src;
                    
                    cart.push({
                        id: 'PROD-' + Math.floor(Math.random() * 10000),
                        title: title,
                        price: price,
                        img: img,
                        quantity: 1
                    });
                    
                    updateCartUI();
                    
                    const drawer = document.getElementById('cart-drawer');
                    const overlay = document.getElementById('cart-overlay');
                    drawer.classList.add('open');
                    overlay.classList.add('open');
                });
            });
        }

        function renderPagination() {
            const paginationContainer = document.getElementById('pagination-controls');
            const totalPages = Math.ceil(filteredProducts.length / productsPerPage);
            
            if (totalPages <= 1) {
                paginationContainer.innerHTML = '';
                return;
            }

            let html = `<button id="btn-prev" class="w-8 h-8 rounded border border-gray-700 flex items-center justify-center text-gray-400 hover:border-brand-gold hover:text-brand-gold transition-colors ${currentPage === 1 ? 'opacity-50 cursor-not-allowed' : ''}"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg></button>`;
            
            for (let i = 1; i <= totalPages; i++) {
                html += `<button class="pagination-btn ${currentPage === i ? 'active bg-brand-gold/10 text-brand-gold border-brand-gold' : 'text-gray-400 hover:border-brand-gold hover:text-brand-gold'} w-8 h-8 rounded border border-gray-700 flex items-center justify-center transition-colors font-medium" data-page="${i}">${i}</button>`;
            }
            
            html += `<button id="btn-next" class="w-8 h-8 rounded border border-gray-700 flex items-center justify-center text-gray-400 hover:border-brand-gold hover:text-brand-gold transition-colors ${currentPage === totalPages ? 'opacity-50 cursor-not-allowed' : ''}"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg></button>`;
            
            paginationContainer.innerHTML = html;

            // Attach pagination events
            document.querySelectorAll('.pagination-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    currentPage = parseInt(e.target.dataset.page);
                    renderProducts();
                    renderPagination();
                    window.scrollTo({ top: document.getElementById('product-grid').offsetTop - 100, behavior: 'smooth' });
                });
            });

            const prevBtn = document.getElementById('btn-prev');
            if (prevBtn) {
                prevBtn.addEventListener('click', () => {
                    if (currentPage > 1) {
                        currentPage--;
                        renderProducts();
                        renderPagination();
                        window.scrollTo({ top: document.getElementById('product-grid').offsetTop - 100, behavior: 'smooth' });
                    }
                });
            }

            const nextBtn = document.getElementById('btn-next');
            if (nextBtn) {
                nextBtn.addEventListener('click', () => {
                    if (currentPage < totalPages) {
                        currentPage++;
                        renderProducts();
                        renderPagination();
                        window.scrollTo({ top: document.getElementById('product-grid').offsetTop - 100, behavior: 'smooth' });
                    }
                });
            }
        }
"""

# 3. Inject JS logic into the <script> block
# Let's replace the existing filtering and add to cart logic inside document.addEventListener("DOMContentLoaded")

script_replacement = """
    // -----------------------------------------
    // NEW DYNAMIC RENDER LOGIC
    // -----------------------------------------
""" + js_products + """

        // Initialize first render
        renderProducts();
        renderPagination();

        // -----------------------------------------
        // FILTER LOGIC UPDATE
        // -----------------------------------------
        const categoryCheckboxes = document.querySelectorAll('#category-filters .filter-checkbox');
        const regionCheckboxes = document.querySelectorAll('#region-filters .filter-checkbox');

        function applyFilters() {
            const activeCategories = Array.from(categoryCheckboxes).filter(cb => cb.checked).map(cb => cb.value);
            const activeRegions = Array.from(regionCheckboxes).filter(cb => cb.checked).map(cb => cb.value);

            filteredProducts = allProducts.filter(product => {
                const categoryMatch = activeCategories.length === 0 || activeCategories.includes(product.category);
                const regionMatch = activeRegions.length === 0 || activeRegions.includes(product.region);
                return categoryMatch && regionMatch;
            });

            currentPage = 1;
            renderProducts();
            renderPagination();
        }

        categoryCheckboxes.forEach(cb => cb.addEventListener('change', applyFilters));
        regionCheckboxes.forEach(cb => cb.addEventListener('change', applyFilters));

"""

# We'll regex replace the old JS filtering logic
js_pattern = re.compile(r'// Filtering Logic.*?(?=\s*// Cart Logic)', re.DOTALL)
content = js_pattern.sub(script_replacement, content)

# Remove the old hardcoded Add to Cart logic since we added it to renderProducts()
# Wait, the old Add to Cart logic starts around line 683: "const addToCartBtns = document.querySelectorAll..."
# We should remove it.
old_add_cart_pattern = re.compile(r'const addToCartBtns = document\.querySelectorAll\(.*?\}\);', re.DOTALL)
content = old_add_cart_pattern.sub('', content)

with open('templates/shop_products.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Finished rewriting shop_products.html")
