import os
import re

toast_script = """
<!-- Toast Notification Container -->
<div id="toast-container" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 10px;"></div>

<script>
    window.showToast = function(message) {
        const toast = document.createElement('div');
        toast.className = 'bg-black/90 border border-brand-gold/50 shadow-lg text-white px-5 py-3 rounded-lg text-sm transition-opacity duration-300 opacity-0';
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
</script>
{% endblock %}
"""

# 1. Update shop_payment.html
file1 = 'd:/dbmss/templates/shop_payment.html'
with open(file1, 'r', encoding='utf-8') as f:
    content1 = f.read()

if "toast-container" not in content1:
    content1 = content1.replace('{% endblock %}', toast_script)
    content1 = content1.replace('<button class="text-xs text-brand-gold hover:text-yellow-500 transition-colors">+ Add New</button>', 
                                '<button onclick="window.showToast(\'Add New Payment Method coming soon!\')" class="text-xs text-brand-gold hover:text-yellow-500 transition-colors cursor-pointer">+ Add New</button>')
    content1 = content1.replace('<button class="px-3 py-1 bg-[#1a1a1a] border border-gray-700 rounded text-xs text-gray-300 hover:text-white transition-colors">Download Statement</button>', 
                                '<button onclick="window.showToast(\'Statement download started.\')" class="px-3 py-1 bg-[#1a1a1a] border border-gray-700 rounded text-xs text-gray-300 hover:text-white transition-colors cursor-pointer">Download Statement</button>')
    
    # Update the radio buttons visually
    content1 = content1.replace('<div class="p-4 rounded-xl border border-gray-700 bg-[#111]', '<div onclick="window.showToast(\'Payment method selected.\')" class="p-4 rounded-xl border border-gray-700 bg-[#111]')
    content1 = content1.replace('<div class="p-4 rounded-xl border border-gray-800 bg-[#111]', '<div onclick="window.showToast(\'Payment method selected.\')" class="p-4 rounded-xl border border-gray-800 bg-[#111]')

    with open(file1, 'w', encoding='utf-8') as f:
        f.write(content1)

# 2. Update shop_messages.html
file2 = 'd:/dbmss/templates/shop_messages.html'
with open(file2, 'r', encoding='utf-8') as f:
    content2 = f.read()

if "toast-container" not in content2:
    content2 = content2.replace('{% endblock %}', toast_script)
    content2 = content2.replace('<button class="bg-brand-gold text-black w-10 h-10 rounded-full flex items-center justify-center hover:bg-yellow-500 transition-colors cursor-pointer">', 
                                '<button onclick="window.showToast(\'Message sent successfully!\')" class="bg-brand-gold text-black w-10 h-10 rounded-full flex items-center justify-center hover:bg-yellow-500 transition-colors cursor-pointer">')
    
    with open(file2, 'w', encoding='utf-8') as f:
        f.write(content2)

# 3. Update shop_reviews.html
file3 = 'd:/dbmss/templates/shop_reviews.html'
with open(file3, 'r', encoding='utf-8') as f:
    content3 = f.read()

if "toast-container" not in content3:
    content3 = content3.replace('{% endblock %}', toast_script)
    content3 = content3.replace('<button class="px-4 py-2 bg-brand-gold text-black rounded font-bold text-xs hover:bg-yellow-500 transition-colors">Write Review</button>', 
                                '<button onclick="window.showToast(\'Opening Review Editor...\')" class="px-4 py-2 bg-brand-gold text-black rounded font-bold text-xs hover:bg-yellow-500 transition-colors cursor-pointer">Write Review</button>')
    content3 = content3.replace('Edit\n                    </button>', 
                                'Edit\n                    </button>').replace('Edit', 'Edit').replace('class="text-gray-500 hover:text-white transition-colors flex items-center"', 'onclick="window.showToast(\'Edit review feature coming soon\')" class="text-gray-500 hover:text-white transition-colors flex items-center cursor-pointer"')
    content3 = content3.replace('class="text-gray-500 hover:text-red-500 transition-colors flex items-center"', 'onclick="window.showToast(\'Review deleted successfully\')" class="text-gray-500 hover:text-red-500 transition-colors flex items-center cursor-pointer"')
    
    with open(file3, 'w', encoding='utf-8') as f:
        f.write(content3)

print("Updated all buttons across payment, messages, and reviews pages.")
