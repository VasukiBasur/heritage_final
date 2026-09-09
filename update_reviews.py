import os

file_path = 'd:/dbmss/templates/shop_reviews.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Write Review button
content = content.replace('onclick="window.showToast(\'Opening Review Editor...\')"', 'onclick="addReview(\'Banarasi Silk Saree\')"')

# Replace the static reviews container with an ID
content = content.replace('<div class="space-y-6">', '<div id="reviews-container" class="space-y-6">')

# We'll remove the static reviews and generate them via JS
review1 = """<!-- Review 1 -->
            <div class="border-b border-gray-800 pb-6 last:border-0 last:pb-0">
                <div class="flex justify-between items-start mb-3">
                    <div>
                        <h4 class="text-white font-bold mb-1">Kanjeevaram Bridal Silk</h4>
                        <div class="flex space-x-1 text-brand-gold text-sm">
                            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"></path></svg>
                            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"></path></svg>
                            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"></path></svg>
                            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"></path></svg>
                            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"></path></svg>
                        </div>
                    </div>
                    <span class="text-xs text-gray-500">May 10, 2026</span>
                </div>
                <p class="text-sm text-gray-300 leading-relaxed mb-3">
                    Absolutely stunning piece of craftsmanship. The zari work is exquisite and the silk quality is top-notch. It was exactly as described and shipped very securely.
                </p>
                <div class="flex items-center space-x-4 text-xs">
                    <button onclick="window.showToast('Edit review feature coming soon')" class="text-gray-500 hover:text-white transition-colors flex items-center cursor-pointer">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
                        Edit
                    </button>
                    <button onclick="window.showToast('Review deleted successfully')" class="text-gray-500 hover:text-red-500 transition-colors flex items-center cursor-pointer">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                        Delete
                    </button>
                </div>
            </div>"""

review2 = """<!-- Review 2 -->
            <div class="border-b border-gray-800 pb-6 last:border-0 last:pb-0">
                <div class="flex justify-between items-start mb-3">
                    <div>
                        <h4 class="text-white font-bold mb-1">Unspun Raw Silk Material</h4>
                        <div class="flex space-x-1 text-brand-gold text-sm">
                            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"></path></svg>
                            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"></path></svg>
                            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"></path></svg>
                            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"></path></svg>
                            <svg class="w-4 h-4 text-gray-600 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"></path></svg>
                        </div>
                    </div>
                    <span class="text-xs text-gray-500">April 22, 2026</span>
                </div>
                <p class="text-sm text-gray-300 leading-relaxed mb-3">
                    Great texture and natural sheen. Perfect for the custom jacket I was planning. The delivery was slightly delayed by a day, but the packaging was excellent.
                </p>
                <div class="flex items-center space-x-4 text-xs">
                    <button onclick="window.showToast('Edit review feature coming soon')" class="text-gray-500 hover:text-white transition-colors flex items-center cursor-pointer">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
                        Edit
                    </button>
                    <button onclick="window.showToast('Review deleted successfully')" class="text-gray-500 hover:text-red-500 transition-colors flex items-center cursor-pointer">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                        Delete
                    </button>
                </div>
            </div>"""

content = content.replace(review1, "")
content = content.replace(review2, "")

js_script = """
    // Reviews Management Logic
    const defaultReviews = [
        { id: 1, title: 'Kanjeevaram Bridal Silk', text: 'Absolutely stunning piece of craftsmanship. The zari work is exquisite and the silk quality is top-notch. It was exactly as described and shipped very securely.', date: 'May 10, 2026' },
        { id: 2, title: 'Unspun Raw Silk Material', text: 'Great texture and natural sheen. Perfect for the custom jacket I was planning. The delivery was slightly delayed by a day, but the packaging was excellent.', date: 'April 22, 2026' }
    ];

    function getStars(count) {
        let stars = '';
        for(let i=0; i<5; i++) {
            if(i < count) {
                stars += '<svg class="w-4 h-4 fill-current text-brand-gold" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"></path></svg>';
            } else {
                stars += '<svg class="w-4 h-4 text-gray-600 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"></path></svg>';
            }
        }
        return stars;
    }

    function renderReviews() {
        let reviews = JSON.parse(localStorage.getItem('userReviews'));
        if (!reviews || reviews.length === 0) {
            reviews = defaultReviews;
            localStorage.setItem('userReviews', JSON.stringify(reviews));
        }

        const container = document.getElementById('reviews-container');
        container.innerHTML = '';

        reviews.forEach(review => {
            const div = document.createElement('div');
            div.className = 'border-b border-gray-800 pb-6 last:border-0 last:pb-0';
            div.innerHTML = `
                <div class="flex justify-between items-start mb-3">
                    <div>
                        <h4 class="text-white font-bold mb-1">${review.title}</h4>
                        <div class="flex space-x-1 text-sm">${getStars(5)}</div>
                    </div>
                    <span class="text-xs text-gray-500">${review.date}</span>
                </div>
                <p class="text-sm text-gray-300 leading-relaxed mb-3">${review.text}</p>
                <div class="flex items-center space-x-4 text-xs">
                    <button onclick="editReview(${review.id})" class="text-gray-500 hover:text-white transition-colors flex items-center cursor-pointer">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
                        Edit
                    </button>
                    <button onclick="deleteReview(${review.id})" class="text-gray-500 hover:text-red-500 transition-colors flex items-center cursor-pointer">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                        Delete
                    </button>
                </div>`;
            container.appendChild(div);
        });
    }

    window.addReview = function(productTitle) {
        const text = prompt("Write your review for " + productTitle + ":");
        if (text) {
            let reviews = JSON.parse(localStorage.getItem('userReviews')) || defaultReviews;
            const now = new Date();
            const dateStr = now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
            reviews.unshift({ id: Date.now(), title: productTitle, text: text, date: dateStr });
            localStorage.setItem('userReviews', JSON.stringify(reviews));
            window.showToast("Review submitted successfully");
            renderReviews();
        }
    };

    window.editReview = function(id) {
        let reviews = JSON.parse(localStorage.getItem('userReviews'));
        const review = reviews.find(r => r.id === id);
        const newText = prompt("Edit your review:", review.text);
        if (newText && newText !== review.text) {
            review.text = newText;
            localStorage.setItem('userReviews', JSON.stringify(reviews));
            window.showToast("Review updated successfully");
            renderReviews();
        }
    };

    window.deleteReview = function(id) {
        if(confirm("Are you sure you want to delete this review?")) {
            let reviews = JSON.parse(localStorage.getItem('userReviews'));
            reviews = reviews.filter(r => r.id !== id);
            localStorage.setItem('userReviews', JSON.stringify(reviews));
            window.showToast("Review deleted");
            renderReviews();
        }
    };

    document.addEventListener("DOMContentLoaded", renderReviews);
</script>
"""

content = content.replace('</script>', js_script)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Reviews logic updated.")
