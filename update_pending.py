import os

file_path = 'd:/dbmss/templates/shop_reviews.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the static pending reviews section with a container
static_pending = """<div class="glass-panel p-6 rounded-2xl border border-gray-800 flex items-center justify-between md:col-span-2">
            <div class="space-y-3 w-full">
                <div class="flex items-center justify-between">
                    <h3 class="text-lg font-serif text-white">Pending Reviews</h3>
                    <span class="px-3 py-1 bg-red-500/20 text-red-500 rounded-full text-xs font-bold border border-red-500/30">1 Awaiting</span>
                </div>
                <div class="p-4 rounded-xl border border-gray-700 bg-[#111] flex items-center justify-between group">
                    <div class="flex items-center space-x-4">
                        <div class="w-12 h-12 bg-gray-800 rounded-lg overflow-hidden">
                            <div class="w-full h-full bg-brand-gold/20"></div>
                        </div>
                        <div>
                            <p class="text-sm font-bold text-white">Banarasi Silk Saree</p>
                            <p class="text-xs text-gray-400">Delivered on May 25, 2026</p>
                        </div>
                    </div>
                    <button onclick="addReview('Banarasi Silk Saree')" class="px-4 py-2 bg-brand-gold text-black rounded font-bold text-xs hover:bg-yellow-500 transition-colors cursor-pointer">Write Review</button>
                </div>
            </div>
        </div>"""

dynamic_pending = """<div class="glass-panel p-6 rounded-2xl border border-gray-800 flex items-center justify-between md:col-span-2" id="pending-reviews-card">
            <div class="space-y-3 w-full" id="pending-reviews-container">
                <!-- JS dynamically renders pending reviews here -->
            </div>
        </div>"""

content = content.replace(static_pending, dynamic_pending)

# Modify the JS to handle pending reviews
js_addition = """
    const defaultPending = [
        { id: 101, title: 'Banarasi Silk Saree', date: 'May 25, 2026' }
    ];

    function renderPending() {
        let pending = JSON.parse(localStorage.getItem('userPendingReviews'));
        if (!pending) {
            pending = defaultPending;
            localStorage.setItem('userPendingReviews', JSON.stringify(pending));
        }

        const container = document.getElementById('pending-reviews-container');
        if(!container) return;
        
        container.innerHTML = `
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-serif text-white">Pending Reviews</h3>
                <span class="px-3 py-1 ${pending.length > 0 ? 'bg-red-500/20 text-red-500 border border-red-500/30' : 'bg-green-500/20 text-green-500 border border-green-500/30'} rounded-full text-xs font-bold">${pending.length} Awaiting</span>
            </div>
        `;

        if (pending.length === 0) {
            container.innerHTML += `<div class="p-4 rounded-xl border border-gray-800 bg-[#111] text-center text-gray-500 text-sm">You have no pending reviews. Great job!</div>`;
            return;
        }

        pending.forEach(p => {
            container.innerHTML += `
                <div class="p-4 rounded-xl border border-gray-700 bg-[#111] flex items-center justify-between group mb-2">
                    <div class="flex items-center space-x-4">
                        <div class="w-12 h-12 bg-gray-800 rounded-lg overflow-hidden border border-gray-700">
                            <div class="w-full h-full bg-brand-gold/10 flex items-center justify-center text-brand-gold font-serif text-lg">H</div>
                        </div>
                        <div>
                            <p class="text-sm font-bold text-white">${p.title}</p>
                            <p class="text-xs text-gray-400">Delivered on ${p.date}</p>
                        </div>
                    </div>
                    <button onclick="writePendingReview(${p.id}, '${p.title.replace(/'/g, "\\\\'")}')" class="px-4 py-2 bg-brand-gold text-black rounded font-bold text-xs hover:bg-yellow-500 transition-colors cursor-pointer shadow-[0_0_10px_rgba(212,175,55,0.2)]">Write Review</button>
                </div>
            `;
        });
    }

    window.writePendingReview = function(pendingId, productTitle) {
        const text = prompt("Write your review for " + productTitle + ":");
        if (text) {
            // Remove from pending
            let pending = JSON.parse(localStorage.getItem('userPendingReviews'));
            pending = pending.filter(p => p.id !== pendingId);
            localStorage.setItem('userPendingReviews', JSON.stringify(pending));

            // Add to completed
            let reviews = JSON.parse(localStorage.getItem('userReviews')) || defaultReviews;
            const now = new Date();
            const dateStr = now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
            reviews.unshift({ id: Date.now(), title: productTitle, text: text, date: dateStr });
            localStorage.setItem('userReviews', JSON.stringify(reviews));
            
            window.showToast("Review submitted successfully");
            renderPending();
            renderReviews();
        }
    };
"""

# Inject the new functions into the JS script block
content = content.replace('window.addReview = function(productTitle) {', js_addition + '\n    window.addReview = function(productTitle) {')

# Ensure renderPending is called on DOMContentLoaded
content = content.replace('document.addEventListener("DOMContentLoaded", renderReviews);', 'document.addEventListener("DOMContentLoaded", () => { renderReviews(); renderPending(); });')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Pending Reviews logic updated.")
