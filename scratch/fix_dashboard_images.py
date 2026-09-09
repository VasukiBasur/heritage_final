import re

dashboard_path = r'd:\dbmss\templates\dashboard.html'
with open(dashboard_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the generic saree image in table rows with design-specific images
# Find all table rows
table_rows = re.findall(r'<tr class="border-b border-white/5 hover:bg-white/5 transition-colors">.*?</tr>', content, re.DOTALL)

for row in table_rows:
    new_row = row
    if 'Mysore Silk Zari' in row:
        new_row = new_row.replace("images/saree.png", "images/mysore_silk_zari.png.jpeg")
    elif 'Ilkal Checkered' in row:
        new_row = new_row.replace("images/saree.png", "images/ilkal_checkered.png.jpeg")
    elif 'Dharwad Cotton' in row:
        new_row = new_row.replace("images/saree.png", "images/dharwad_cotton_saree.png.jpeg")
    elif 'Udupi Cotton' in row:
        new_row = new_row.replace("images/saree.png", "images/udupi_silk.png.jpeg")
    
    content = content.replace(row, new_row)

# 2. Fix the addMockLog() function
old_js = """    // Add Mock Log Function
    window.addMockLog = function() {
        const tbody = document.querySelector('table tbody');
        const newId = Math.floor(Math.random() * 100) + 30;
        const newRow = document.createElement('tr');
        newRow.className = "border-b border-white/5 hover:bg-white/5 transition-colors bg-brand-gold/10";
        newRow.innerHTML = `
            <td class="p-3"><img src="{{ url_for('static', filename='images/saree.png') }}" class="w-10 h-10 object-cover rounded border border-brand-gold/30" alt="Saree"></td>
            <td class="p-3 font-bold text-brand-gold">#${newId}</td>
            <td class="p-3 font-bold text-gray-200">New Artisan</td>
            <td class="p-3 font-bold text-gray-200">New Design Order</td>
            <td class="p-3"><span class="px-3 py-1 bg-blue-900/40 text-blue-400 rounded text-xs border border-blue-500/50">Pending</span></td>
            <td class="p-3">
                <div class="flex items-center space-x-2">
                    <select class="bg-[#121212] border border-brand-gold/30 text-gray-300 text-xs rounded px-2 py-1 outline-none font-bold">
                        <option>Order Placed</option>
                    </select>
                    <button class="bg-brand-gold text-brand-black px-2 py-1 rounded text-xs font-bold hover:bg-yellow-500">Update</button>
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=30x30&data=${newId}&color=D4AF37&bgcolor=121212" alt="QR" class="border border-brand-gold/50 rounded">
                </div>
            </td>
            <td class="p-3 text-gray-200 font-bold">1</td>
            <td class="p-3 text-brand-gold font-bold">₹0.00</td>
        `;
        tbody.insertBefore(newRow, tbody.firstChild);
        setTimeout(() => newRow.classList.remove('bg-brand-gold/10'), 1000);
    };"""

new_js = """    // Add Mock Log Function
    window.addMockLog = function() {
        const tbody = document.querySelector('table tbody');
        const newId = Math.floor(Math.random() * 100) + 30;
        
        const designs = [
            {name: 'Mysore Silk Zari', img: 'mysore_silk_zari.png.jpeg'},
            {name: 'Ilkal Checkered', img: 'ilkal_checkered.png.jpeg'},
            {name: 'Dharwad Cotton', img: 'dharwad_cotton_saree.png.jpeg'},
            {name: 'Udupi Cotton', img: 'udupi_silk.png.jpeg'},
            {name: 'Banarasi Brocade', img: 'banarasi_brocode_saree.png.jpeg'}
        ];
        
        const artisans = ['Ramesh Kumar', 'Lakshmi Devi', 'Basavaraj', 'Sunitha Reddy', 'Abdul Kareem', 'Savitri Bai', 'Gowramma', 'Manjunath'];
        
        const design = designs[Math.floor(Math.random() * designs.length)];
        const artisan = artisans[Math.floor(Math.random() * artisans.length)];
        const qty = Math.floor(Math.random() * 5) + 1;
        const payout = (qty * 850).toFixed(2);
        
        const newRow = document.createElement('tr');
        newRow.className = "border-b border-white/5 hover:bg-white/5 transition-colors bg-brand-gold/20";
        newRow.innerHTML = `
            <td class="p-3"><img src="/static/images/${design.img}" class="w-10 h-10 object-cover rounded border border-brand-gold/30" alt="${design.name}"></td>
            <td class="p-3 font-bold text-brand-gold">#${newId}</td>
            <td class="p-3 font-bold text-gray-200">${artisan}</td>
            <td class="p-3 font-bold text-gray-200">${design.name}</td>
            <td class="p-3"><span class="px-3 py-1 bg-blue-900/40 text-blue-400 rounded text-xs border border-blue-500/50">Pending</span></td>
            <td class="p-3">
                <div class="flex items-center space-x-2">
                    <select class="bg-[#121212] border border-brand-gold/30 text-gray-300 text-xs rounded px-2 py-1 outline-none font-bold">
                        <option>Order Placed</option>
                        <option>Raw Material Supply</option>
                        <option>Weaving</option>
                        <option>Quality Check</option>
                        <option>Shipped</option>
                        <option>Delivered</option>
                    </select>
                    <button class="bg-brand-gold text-brand-black px-2 py-1 rounded text-xs font-bold hover:bg-yellow-500">Update</button>
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=30x30&data=${newId}&color=D4AF37&bgcolor=121212" alt="QR" class="border border-brand-gold/50 rounded">
                </div>
            </td>
            <td class="p-3 text-gray-200 font-bold">${qty}</td>
            <td class="p-3 text-brand-gold font-bold">₹${payout}</td>
        `;
        tbody.insertBefore(newRow, tbody.firstChild);
        setTimeout(() => {
            newRow.classList.remove('bg-brand-gold/20');
        }, 1000);
    };"""

content = content.replace(old_js, new_js)

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated images and Add Log functionality.")
