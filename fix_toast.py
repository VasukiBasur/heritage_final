import os

filepath = 'd:/dbmss/templates/shop_products.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

toast_func = """
    window.showToast = function(message) {
        const toast = document.createElement('div');
        toast.className = 'toast bg-black/90 border border-brand-gold/50 shadow-lg text-white px-5 py-3 rounded-lg text-sm transition-opacity duration-300';
        toast.innerHTML = `<span class="flex items-center"><svg class="w-5 h-5 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>${message}</span>`;
        const container = document.getElementById('toast-container');
        if(container) {
            container.appendChild(toast);
            setTimeout(() => toast.style.opacity = '1', 10);
            setTimeout(() => {
                toast.style.opacity = '0';
                setTimeout(() => toast.remove(), 400);
            }, 3000);
        }
    };
"""

content = content.replace('<script>', '<script>\n' + toast_func)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected showToast successfully.")
