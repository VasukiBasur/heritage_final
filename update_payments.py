import os

file_path = 'd:/dbmss/templates/shop_payment.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Add New button
content = content.replace('onclick="window.showToast(\'Add New Payment Method coming soon!\')"', 'onclick="addPaymentMethod()"')

# Find the start and end of the static payment methods list
start_div = '<div class="space-y-4">'
end_div = '</div>\n            </div>\n        </div>\n        \n        <!-- Transaction History -->'

# Extract the block to replace
start_idx = content.find(start_div)
end_idx = content.find('<!-- Transaction History -->')
if start_idx != -1 and end_idx != -1:
    block_to_replace = content[start_idx:end_idx]
    
    new_block = """<div id="payment-methods-container" class="space-y-4">
                    <!-- Methods rendered by JS -->
                </div>
            </div>
        </div>
        
        """
    content = content.replace(block_to_replace, new_block)


js_script = """
    // Payment Methods Management Logic
    const defaultPayments = [
        { id: 1, type: 'VISA', last4: '4242', expires: '12/28', isDefault: true, color: 'blue-800' },
        { id: 2, type: 'MC', last4: '5555', expires: '08/25', isDefault: false, color: 'red-600' }
    ];

    function renderPaymentMethods() {
        let payments = JSON.parse(localStorage.getItem('userPayments'));
        if (!payments || payments.length === 0) {
            payments = defaultPayments;
            localStorage.setItem('userPayments', JSON.stringify(payments));
        }

        const container = document.getElementById('payment-methods-container');
        container.innerHTML = '';

        payments.forEach(payment => {
            const isDef = payment.isDefault;
            const borderClass = isDef ? 'border-gray-700' : 'border-gray-800';
            const radioClass = isDef ? 
                '<div class="w-4 h-4 rounded-full border-2 border-brand-gold bg-brand-gold/20 flex items-center justify-center"><div class="w-2 h-2 rounded-full bg-brand-gold"></div></div>' : 
                '<div class="w-4 h-4 rounded-full border-2 border-gray-600 group-hover:border-brand-gold transition-colors"></div>';

            const div = document.createElement('div');
            div.className = `p-4 rounded-xl border ${borderClass} bg-[#111] flex items-center justify-between group cursor-pointer hover:border-brand-gold/50 transition-colors`;
            div.onclick = () => selectPaymentMethod(payment.id);
            div.innerHTML = `
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-6 bg-gray-200 rounded flex items-center justify-center">
                        <span class="text-[10px] font-bold text-${payment.color}">${payment.type}</span>
                    </div>
                    <div>
                        <p class="text-sm font-bold text-white">•••• ${payment.last4}</p>
                        <p class="text-xs text-gray-500">Expires ${payment.expires}</p>
                    </div>
                </div>
                <div class="flex items-center space-x-4">
                    <button onclick="event.stopPropagation(); deletePaymentMethod(${payment.id})" class="text-gray-600 hover:text-red-500 transition-colors" title="Remove Card">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                    </button>
                    ${radioClass}
                </div>
            `;
            container.appendChild(div);
        });

        // Update the Saved Cards count in the stats header
        const cardsCountEl = document.querySelector('h3.text-2xl.font-serif.text-white.font-bold');
        if(cardsCountEl) {
            // Find the one for saved cards (the second one)
            const allH3 = document.querySelectorAll('.glass-panel h3.text-2xl');
            if(allH3.length > 1) {
                allH3[1].innerText = payments.length;
            }
        }
    }

    window.addPaymentMethod = function() {
        const type = prompt("Enter Card Type (e.g., VISA, MC, AMEX):", "VISA");
        if (!type) return;
        const last4 = prompt("Enter Last 4 Digits:", "1234");
        if (!last4 || last4.length !== 4) {
            window.showToast("Invalid card digits");
            return;
        }
        const expires = prompt("Enter Expiry (MM/YY):", "12/29");
        if (!expires) return;

        let payments = JSON.parse(localStorage.getItem('userPayments')) || defaultPayments;
        
        // determine color
        let color = 'gray-800';
        if(type.toUpperCase() === 'VISA') color = 'blue-800';
        else if(type.toUpperCase() === 'MC' || type.toUpperCase() === 'MASTERCARD') color = 'red-600';
        else if(type.toUpperCase() === 'AMEX') color = 'green-600';

        payments.push({
            id: Date.now(),
            type: type.toUpperCase(),
            last4: last4,
            expires: expires,
            isDefault: payments.length === 0,
            color: color
        });

        localStorage.setItem('userPayments', JSON.stringify(payments));
        window.showToast(type + " card ending in " + last4 + " added!");
        renderPaymentMethods();
    };

    window.selectPaymentMethod = function(id) {
        let payments = JSON.parse(localStorage.getItem('userPayments'));
        if(!payments) return;
        
        payments.forEach(p => p.isDefault = (p.id === id));
        localStorage.setItem('userPayments', JSON.stringify(payments));
        
        const selectedCard = payments.find(p => p.id === id);
        window.showToast("Default payment set to " + selectedCard.type + " ending in " + selectedCard.last4);
        renderPaymentMethods();
    };

    window.deletePaymentMethod = function(id) {
        if(confirm("Are you sure you want to remove this card?")) {
            let payments = JSON.parse(localStorage.getItem('userPayments'));
            const idx = payments.findIndex(p => p.id === id);
            const wasDefault = payments[idx].isDefault;
            
            payments.splice(idx, 1);
            
            // If we deleted the default, make the first remaining card default
            if(wasDefault && payments.length > 0) {
                payments[0].isDefault = true;
            }
            
            localStorage.setItem('userPayments', JSON.stringify(payments));
            window.showToast("Card removed successfully");
            renderPaymentMethods();
        }
    };

    document.addEventListener("DOMContentLoaded", () => {
        renderPaymentMethods();
    });
</script>
"""

content = content.replace('</script>', js_script)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Payment methods logic updated.")
