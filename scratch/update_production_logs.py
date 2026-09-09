import re

dashboard_path = r'd:\dbmss\templates\dashboard.html'
with open(dashboard_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the old block to match based on unique identifiers or comments
start_marker = "<!-- Recent Production Logs with QR -->"
end_marker = "<!-- Chatbot Widget -->"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_logs_html = """<!-- Recent Production Logs -->
<div class="glass-card p-6 mt-8 shadow-lg border border-brand-gold/20 bg-[#1a1a1a] overflow-x-auto mb-8">
    <div class="flex justify-between items-center mb-6 border-b border-brand-gold/20 pb-4">
        <h2 class="text-xl font-serif text-brand-gold">Recent Production Logs</h2>
        <button class="bg-brand-gold text-brand-black px-4 py-2 rounded text-sm font-bold hover:bg-yellow-500 transition-colors">Add Log</button>
    </div>
    
    <table class="w-full text-left border-collapse min-w-[1000px]">
        <thead>
            <tr class="border-b border-brand-gold/30 text-[10px] tracking-widest text-brand-lightgold uppercase">
                <th class="p-3 font-bold">Image</th>
                <th class="p-3 font-bold">Log ID</th>
                <th class="p-3 font-bold">Artisan</th>
                <th class="p-3 font-bold">Design</th>
                <th class="p-3 font-bold">Status</th>
                <th class="p-3 font-bold">Stage & QR</th>
                <th class="p-3 font-bold">Quantity</th>
                <th class="p-3 font-bold">Payout</th>
            </tr>
        </thead>
        <tbody class="text-sm">
            <!-- Row 1 -->
            <tr class="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td class="p-3"><img src="https://images.unsplash.com/photo-1605814524854-474c102c4b5e?ixlib=rb-4.0.3&auto=format&fit=crop&w=50&q=80" class="w-10 h-10 object-cover rounded border border-brand-gold/30" alt="Saree"></td>
                <td class="p-3 font-bold text-brand-gold">#15</td>
                <td class="p-3 font-bold text-gray-200">Lakshmi Devi</td>
                <td class="p-3 font-bold text-gray-200">Mysore Silk Zari</td>
                <td class="p-3"><span class="px-3 py-1 bg-orange-900/40 text-orange-400 rounded text-xs border border-orange-500/50">Active</span></td>
                <td class="p-3">
                    <div class="flex items-center space-x-2">
                        <select class="bg-[#121212] border border-brand-gold/30 text-gray-300 text-xs rounded px-2 py-1 outline-none font-bold">
                            <option>Raw Material Supply</option>
                            <option>Weaving</option>
                        </select>
                        <button class="bg-brand-gold text-brand-black px-2 py-1 rounded text-xs font-bold hover:bg-yellow-500">Update</button>
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=30x30&data=15&color=D4AF37&bgcolor=121212" alt="QR" class="border border-brand-gold/50 rounded">
                    </div>
                </td>
                <td class="p-3 text-gray-200 font-bold">1</td>
                <td class="p-3 text-brand-gold font-bold">₹850.00</td>
            </tr>
            <!-- Row 2 -->
            <tr class="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td class="p-3"><img src="https://images.unsplash.com/photo-1605814524854-474c102c4b5e?ixlib=rb-4.0.3&auto=format&fit=crop&w=50&q=80" class="w-10 h-10 object-cover rounded border border-brand-gold/30" alt="Saree"></td>
                <td class="p-3 font-bold text-brand-gold">#7</td>
                <td class="p-3 font-bold text-gray-200">Lakshmi Devi</td>
                <td class="p-3 font-bold text-gray-200">Mysore Silk Zari</td>
                <td class="p-3"><span class="px-3 py-1 bg-orange-900/40 text-orange-400 rounded text-xs border border-orange-500/50">Active</span></td>
                <td class="p-3">
                    <div class="flex items-center space-x-2">
                        <select class="bg-[#121212] border border-brand-gold/30 text-gray-300 text-xs rounded px-2 py-1 outline-none font-bold">
                            <option>Raw Material Supply</option>
                            <option>Weaving</option>
                        </select>
                        <button class="bg-brand-gold text-brand-black px-2 py-1 rounded text-xs font-bold hover:bg-yellow-500">Update</button>
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=30x30&data=7&color=D4AF37&bgcolor=121212" alt="QR" class="border border-brand-gold/50 rounded">
                    </div>
                </td>
                <td class="p-3 text-gray-200 font-bold">2</td>
                <td class="p-3 text-brand-gold font-bold">₹1700.00</td>
            </tr>
            <!-- Row 3 -->
            <tr class="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td class="p-3"><img src="https://images.unsplash.com/photo-1605814524854-474c102c4b5e?ixlib=rb-4.0.3&auto=format&fit=crop&w=50&q=80" class="w-10 h-10 object-cover rounded border border-brand-gold/30" alt="Saree"></td>
                <td class="p-3 font-bold text-brand-gold">#10</td>
                <td class="p-3 font-bold text-gray-200">Sunitha Reddy</td>
                <td class="p-3 font-bold text-gray-200">Mysore Silk Zari</td>
                <td class="p-3"><span class="px-3 py-1 bg-green-900/40 text-green-400 rounded text-xs border border-green-500/50">Completed</span></td>
                <td class="p-3">
                    <div class="flex items-center space-x-2">
                        <select class="bg-[#121212] border border-brand-gold/30 text-gray-300 text-xs rounded px-2 py-1 outline-none font-bold">
                            <option>Ordered</option>
                            <option>Shipped</option>
                        </select>
                        <button class="bg-brand-gold text-brand-black px-2 py-1 rounded text-xs font-bold hover:bg-yellow-500">Update</button>
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=30x30&data=10&color=D4AF37&bgcolor=121212" alt="QR" class="border border-brand-gold/50 rounded">
                    </div>
                </td>
                <td class="p-3 text-gray-200 font-bold">5</td>
                <td class="p-3 text-brand-gold font-bold">₹4500.00</td>
            </tr>
            <!-- Row 4 -->
            <tr class="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td class="p-3"><img src="https://images.unsplash.com/photo-1605814524854-474c102c4b5e?ixlib=rb-4.0.3&auto=format&fit=crop&w=50&q=80" class="w-10 h-10 object-cover rounded border border-brand-gold/30" alt="Saree"></td>
                <td class="p-3 font-bold text-brand-gold">#11</td>
                <td class="p-3 font-bold text-gray-200">Abdul Kareem</td>
                <td class="p-3 font-bold text-gray-200">Mysore Silk Zari</td>
                <td class="p-3"><span class="px-3 py-1 bg-green-900/40 text-green-400 rounded text-xs border border-green-500/50">Completed</span></td>
                <td class="p-3">
                    <div class="flex items-center space-x-2">
                        <select class="bg-[#121212] border border-brand-gold/30 text-gray-300 text-xs rounded px-2 py-1 outline-none font-bold">
                            <option>Ordered</option>
                            <option>Shipped</option>
                        </select>
                        <button class="bg-brand-gold text-brand-black px-2 py-1 rounded text-xs font-bold hover:bg-yellow-500">Update</button>
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=30x30&data=11&color=D4AF37&bgcolor=121212" alt="QR" class="border border-brand-gold/50 rounded">
                    </div>
                </td>
                <td class="p-3 text-gray-200 font-bold">5</td>
                <td class="p-3 text-brand-gold font-bold">₹4500.00</td>
            </tr>
            <!-- Row 5 -->
            <tr class="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td class="p-3"><img src="https://images.unsplash.com/photo-1605814524854-474c102c4b5e?ixlib=rb-4.0.3&auto=format&fit=crop&w=50&q=80" class="w-10 h-10 object-cover rounded border border-brand-gold/30" alt="Saree"></td>
                <td class="p-3 font-bold text-brand-gold">#12</td>
                <td class="p-3 font-bold text-gray-200">Savitri Bai</td>
                <td class="p-3 font-bold text-gray-200">Mysore Silk Zari</td>
                <td class="p-3"><span class="px-3 py-1 bg-green-900/40 text-green-400 rounded text-xs border border-green-500/50">Completed</span></td>
                <td class="p-3">
                    <div class="flex items-center space-x-2">
                        <select class="bg-[#121212] border border-brand-gold/30 text-gray-300 text-xs rounded px-2 py-1 outline-none font-bold">
                            <option>Ordered</option>
                            <option>Shipped</option>
                        </select>
                        <button class="bg-brand-gold text-brand-black px-2 py-1 rounded text-xs font-bold hover:bg-yellow-500">Update</button>
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=30x30&data=12&color=D4AF37&bgcolor=121212" alt="QR" class="border border-brand-gold/50 rounded">
                    </div>
                </td>
                <td class="p-3 text-gray-200 font-bold">5</td>
                <td class="p-3 text-brand-gold font-bold">₹4500.00</td>
            </tr>
        </tbody>
    </table>
</div>

"""
    
    # Replace the old section with the new section
    new_content = content[:start_idx] + new_logs_html + content[end_idx:]
    
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Production Logs successfully updated to match second screenshot.")
else:
    print("Could not find the target blocks to replace.")
