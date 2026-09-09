import re

dashboard_path = r'd:\dbmss\templates\dashboard.html'
with open(dashboard_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace 4 main frame images with local static paths
replacements = [
    (r'<img src="https://images.unsplash.com/photo-1583391733958-d25e07fac662[^"]+" alt="Textiles"', 
     r'<img src="{{ url_for(\'static\', filename=\'images/saree.png\') }}" alt="Textiles"'),
    
    (r'<img src="https://images.unsplash.com/photo-1605814524854-474c102c4b5e[^"]+" alt="Artisans"', 
     r'<img src="{{ url_for(\'static\', filename=\'images/weaver.png\') }}" alt="Artisans"'),
    
    (r'<img src="https://images.unsplash.com/photo-1590736969955-71cc94801759[^"]+" alt="Materials"', 
     r'<img src="{{ url_for(\'static\', filename=\'images/motif.png\') }}" alt="Materials"'),
    
    (r'<img src="https://images.unsplash.com/photo-1528181304800-259b08848526[^"]+" alt="Heritage"', 
     r'<img src="{{ url_for(\'static\', filename=\'images/global_heritage.png.jpeg\') }}" alt="Heritage"')
]

for old, new in replacements:
    content = re.sub(old, new, content)

# 2. Replace Unsplash images in the table rows
content = re.sub(r'<img src="https://images.unsplash.com/photo-1605814524854-474c102c4b5e[^"]+" class="w-10 h-10 object-cover rounded border border-brand-gold/30" alt="Saree">', 
                 r'<img src="{{ url_for(\'static\', filename=\'images/saree.png\') }}" class="w-10 h-10 object-cover rounded border border-brand-gold/30" alt="Saree">', content)

# 3. Add more logs
old_table_end = """        </tbody>
    </table>
</div>"""

new_logs_addition = """            <!-- Row 6 -->
            <tr class="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td class="p-3"><img src="{{ url_for('static', filename='images/saree.png') }}" class="w-10 h-10 object-cover rounded border border-brand-gold/30" alt="Saree"></td>
                <td class="p-3 font-bold text-brand-gold">#22</td>
                <td class="p-3 font-bold text-gray-200">Gowramma</td>
                <td class="p-3 font-bold text-gray-200">Dharwad Cotton</td>
                <td class="p-3"><span class="px-3 py-1 bg-green-900/40 text-green-400 rounded text-xs border border-green-500/50">Completed</span></td>
                <td class="p-3">
                    <div class="flex items-center space-x-2">
                        <select class="bg-[#121212] border border-brand-gold/30 text-gray-300 text-xs rounded px-2 py-1 outline-none font-bold">
                            <option>Delivered</option>
                            <option>Shipped</option>
                        </select>
                        <button class="bg-brand-gold text-brand-black px-2 py-1 rounded text-xs font-bold hover:bg-yellow-500">Update</button>
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=30x30&data=22&color=D4AF37&bgcolor=121212" alt="QR" class="border border-brand-gold/50 rounded">
                    </div>
                </td>
                <td class="p-3 text-gray-200 font-bold">3</td>
                <td class="p-3 text-brand-gold font-bold">₹1200.00</td>
            </tr>
            <!-- Row 7 -->
            <tr class="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td class="p-3"><img src="{{ url_for('static', filename='images/saree.png') }}" class="w-10 h-10 object-cover rounded border border-brand-gold/30" alt="Saree"></td>
                <td class="p-3 font-bold text-brand-gold">#28</td>
                <td class="p-3 font-bold text-gray-200">Manjunath</td>
                <td class="p-3 font-bold text-gray-200">Ilkal Checkered</td>
                <td class="p-3"><span class="px-3 py-1 bg-orange-900/40 text-orange-400 rounded text-xs border border-orange-500/50">Active</span></td>
                <td class="p-3">
                    <div class="flex items-center space-x-2">
                        <select class="bg-[#121212] border border-brand-gold/30 text-gray-300 text-xs rounded px-2 py-1 outline-none font-bold">
                            <option>Weaving</option>
                            <option>Raw Material Supply</option>
                        </select>
                        <button class="bg-brand-gold text-brand-black px-2 py-1 rounded text-xs font-bold hover:bg-yellow-500">Update</button>
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=30x30&data=28&color=D4AF37&bgcolor=121212" alt="QR" class="border border-brand-gold/50 rounded">
                    </div>
                </td>
                <td class="p-3 text-gray-200 font-bold">4</td>
                <td class="p-3 text-brand-gold font-bold">₹3400.00</td>
            </tr>
        </tbody>
    </table>
</div>"""

content = content.replace(old_table_end, new_logs_addition)

# 4. Make Add Log interactive
content = content.replace('<button class="bg-brand-gold text-brand-black px-4 py-2 rounded text-sm font-bold hover:bg-yellow-500 transition-colors">Add Log</button>',
                          '<button onclick="addMockLog()" class="bg-brand-gold text-brand-black px-4 py-2 rounded text-sm font-bold hover:bg-yellow-500 transition-colors">Add Log</button>')

# 5. Add addMockLog JS function
js_to_add = """
    // Add Mock Log Function
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
    };
"""

content = content.replace('// Chatbot Logic', js_to_add + '\n    // Chatbot Logic')

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated dashboard with local images and interactive Add Log button.")
