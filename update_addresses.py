import os

file_path = 'd:/dbmss/templates/shop_profile.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Add New Address button
old_add_btn = '<button class="px-4 py-2 bg-[#1a1a1a] border border-gray-700 text-brand-gold rounded hover:text-yellow-500 transition-colors text-sm font-bold">+ Add New Address</button>'
new_add_btn = '<button onclick="addAddress()" class="px-4 py-2 bg-[#1a1a1a] border border-gray-700 text-brand-gold rounded hover:text-yellow-500 transition-colors text-sm font-bold cursor-pointer">+ Add New Address</button>'
content = content.replace(old_add_btn, new_add_btn)

# Replace the static address block with a container
static_address_block = """<div class="space-y-4">
                    <div class="p-6 rounded-xl border border-brand-gold/30 bg-[#111] relative">
                        <div class="absolute top-6 right-6">
                            <span class="px-3 py-1 bg-brand-gold/20 text-brand-gold text-xs font-bold rounded-full">Default</span>
                        </div>
                        <h4 class="text-white font-bold mb-2">Home</h4>
                        <p class="text-sm text-gray-300 leading-relaxed mb-4">
                            123 Heritage Lane, Apt 4B<br>
                            Banjara Hills<br>
                            Hyderabad, Telangana 500034<br>
                            India
                        </p>
                        <div class="flex space-x-4 text-sm font-bold">
                            <button class="text-gray-400 hover:text-white transition-colors">Edit</button>
                            <button class="text-gray-400 hover:text-red-500 transition-colors">Remove</button>
                        </div>
                    </div>
                </div>"""

dynamic_container = """<div id="addresses-container" class="space-y-4">
                    <!-- JS renders addresses here -->
                </div>"""
content = content.replace(static_address_block, dynamic_container)


js_addition = """
    // Addresses Management Logic
    const defaultAddresses = [
        { 
            id: 1, 
            label: 'Home', 
            lines: '123 Heritage Lane, Apt 4B<br>Banjara Hills<br>Hyderabad, Telangana 500034<br>India', 
            isDefault: true 
        }
    ];

    function renderAddresses() {
        let addresses = JSON.parse(localStorage.getItem('userAddresses'));
        if (!addresses || addresses.length === 0) {
            addresses = defaultAddresses;
            localStorage.setItem('userAddresses', JSON.stringify(addresses));
        }

        const container = document.getElementById('addresses-container');
        if(!container) return;
        
        container.innerHTML = '';
        
        addresses.forEach(addr => {
            const borderClass = addr.isDefault ? 'border-brand-gold/30' : 'border-gray-800';
            const defaultBadge = addr.isDefault ? '<div class="absolute top-6 right-6"><span class="px-3 py-1 bg-brand-gold/20 text-brand-gold text-xs font-bold rounded-full">Default</span></div>' : `<div class="absolute top-6 right-6"><button onclick="setDefaultAddress(${addr.id})" class="text-xs text-gray-500 hover:text-brand-gold transition-colors">Set as Default</button></div>`;
            
            container.innerHTML += `
                <div class="p-6 rounded-xl border ${borderClass} bg-[#111] relative group transition-colors hover:border-gray-600">
                    ${defaultBadge}
                    <h4 class="text-white font-bold mb-2">${addr.label}</h4>
                    <p class="text-sm text-gray-300 leading-relaxed mb-4">
                        ${addr.lines}
                    </p>
                    <div class="flex space-x-4 text-sm font-bold">
                        <button onclick="editAddress(${addr.id})" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Edit</button>
                        <button onclick="removeAddress(${addr.id})" class="text-gray-400 hover:text-red-500 transition-colors cursor-pointer">Remove</button>
                    </div>
                </div>
            `;
        });
    }

    window.addAddress = function() {
        const label = prompt("Address Label (e.g., Home, Office):", "Work");
        if(!label) return;
        const line1 = prompt("Address Line 1:");
        const city = prompt("City & State:");
        const pin = prompt("Pincode/ZIP:");
        
        if (label && line1 && city && pin) {
            let addresses = JSON.parse(localStorage.getItem('userAddresses')) || defaultAddresses;
            const formattedLines = `${line1}<br>${city}<br>${pin}<br>India`;
            addresses.push({
                id: Date.now(),
                label: label,
                lines: formattedLines,
                isDefault: addresses.length === 0
            });
            localStorage.setItem('userAddresses', JSON.stringify(addresses));
            window.showToast("Address added successfully");
            renderAddresses();
        } else {
            window.showToast("Address addition cancelled");
        }
    };

    window.editAddress = function(id) {
        let addresses = JSON.parse(localStorage.getItem('userAddresses'));
        const addr = addresses.find(a => a.id === id);
        if(!addr) return;
        
        const newLabel = prompt("Edit Label:", addr.label);
        if(newLabel) {
            addr.label = newLabel;
            // Simplification: only editing the label for the mock
            localStorage.setItem('userAddresses', JSON.stringify(addresses));
            window.showToast("Address updated");
            renderAddresses();
        }
    };

    window.removeAddress = function(id) {
        if(confirm("Are you sure you want to delete this address?")) {
            let addresses = JSON.parse(localStorage.getItem('userAddresses'));
            const idx = addresses.findIndex(a => a.id === id);
            const wasDefault = addresses[idx].isDefault;
            addresses.splice(idx, 1);
            
            if(wasDefault && addresses.length > 0) {
                addresses[0].isDefault = true;
            }
            
            localStorage.setItem('userAddresses', JSON.stringify(addresses));
            window.showToast("Address removed");
            renderAddresses();
        }
    };

    window.setDefaultAddress = function(id) {
        let addresses = JSON.parse(localStorage.getItem('userAddresses'));
        addresses.forEach(a => a.isDefault = (a.id === id));
        localStorage.setItem('userAddresses', JSON.stringify(addresses));
        window.showToast("Default address updated");
        renderAddresses();
    };
"""

content = content.replace('document.addEventListener("DOMContentLoaded", loadProfile);', js_addition + '\n    document.addEventListener("DOMContentLoaded", () => { loadProfile(); renderAddresses(); });')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Addresses tab logic updated.")
