import re

path = r'd:\dbmss\templates\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the old search input with the new one containing the dropdown structure
old_input = '<input type="text" id="dashboardSearch" onkeyup="filterTable()" placeholder="Search orders, products, or artisans..." class="w-full bg-[#121212] border border-brand-gold/30 text-white text-sm rounded px-4 py-3 pl-10 focus:outline-none focus:border-brand-gold shadow-inner transition-colors">'
new_input = """<input type="text" id="dashboardSearch" onkeyup="handleSearch()" placeholder="Search orders, products, or artisans..." class="w-full bg-[#121212] border border-brand-gold/30 text-white text-sm rounded px-4 py-3 pl-10 focus:outline-none focus:border-brand-gold shadow-inner transition-colors">
        <div id="searchResults" class="hidden absolute top-full left-0 w-full mt-2 bg-[#1a1a1a] border border-brand-gold/30 rounded shadow-[0_10px_30px_rgba(0,0,0,0.8)] z-[100] overflow-hidden">
            <ul id="searchResultsList" class="max-h-64 overflow-y-auto"></ul>
        </div>"""
content = content.replace(old_input, new_input)

# In case it was still the old one without filterTable
old_input_fallback = '<input type="text" placeholder="Search orders, products, or artisans..." class="w-full bg-[#121212] border border-brand-gold/30 text-white text-sm rounded px-4 py-3 pl-10 focus:outline-none focus:border-brand-gold shadow-inner transition-colors">'
if old_input_fallback in content:
    new_input_fallback = """<input type="text" id="dashboardSearch" onkeyup="handleSearch()" placeholder="Search orders, products, or artisans..." class="w-full bg-[#121212] border border-brand-gold/30 text-white text-sm rounded px-4 py-3 pl-10 focus:outline-none focus:border-brand-gold shadow-inner transition-colors">
        <div id="searchResults" class="hidden absolute top-full left-0 w-full mt-2 bg-[#1a1a1a] border border-brand-gold/30 rounded shadow-[0_10px_30px_rgba(0,0,0,0.8)] z-[100] overflow-hidden">
            <ul id="searchResultsList" class="max-h-64 overflow-y-auto"></ul>
        </div>"""
    content = content.replace(old_input_fallback, new_input_fallback)

# Replace the filterTable JS with handleSearch
old_js_start = "window.filterTable = function() {"
old_js_end = "};" # This is dangerous, better to use regex or find exact string

# Let's just find where filterTable is defined and replace it
match = re.search(r'window\.filterTable = function\(\) \{.*?\n    \};', content, re.DOTALL)
if match:
    new_js = """window.handleSearch = function() {
        const input = document.getElementById("dashboardSearch").value.toLowerCase();
        const resultsContainer = document.getElementById("searchResults");
        const resultsList = document.getElementById("searchResultsList");
        
        if (input.length < 2) {
            resultsContainer.classList.add("hidden");
            return;
        }
        
        resultsContainer.classList.remove("hidden");
        
        // Mock database for global search
        const mockData = [
            { name: "Kavitha Weavers", type: "Artisan", desc: "Expert in Kanchipuram Silk", icon: "🧶" },
            { name: "Order #ORD-KAV99", type: "Order", desc: "Pending Shipment to Kavitha R.", icon: "📦" },
            { name: "Kavi Gold Zari", type: "Raw Material", desc: "Supplier: Surat Hub", icon: "✨" },
            { name: "Mysore Silk Zari", type: "Product", desc: "Active Production", icon: "👘" },
            { name: "Abdul Kareem", type: "Artisan", desc: "Master Weaver", icon: "🧶" },
            { name: "Order #ORD-991", type: "Order", desc: "Delivered", icon: "📦" },
            { name: "Surat Textile Hub", type: "Supplier", desc: "Premium Zari Yarns", icon: "🧵" }
        ];
        
        const filtered = mockData.filter(item => item.name.toLowerCase().includes(input) || item.desc.toLowerCase().includes(input));
        
        if (filtered.length === 0) {
            resultsList.innerHTML = `<li class="p-4 text-center text-gray-500 text-sm">No results found for "${input}"</li>`;
            return;
        }
        
        resultsList.innerHTML = filtered.map(item => `
            <li class="p-3 border-b border-white/5 hover:bg-brand-gold/10 cursor-pointer flex items-center gap-3 transition-colors" onclick="document.getElementById('searchResults').classList.add('hidden'); alert('Navigating to ' + '${item.name}...');">
                <div class="w-8 h-8 rounded-full bg-[#121212] border border-brand-gold/20 flex items-center justify-center text-lg">${item.icon}</div>
                <div>
                    <p class="text-brand-gold font-bold text-sm">${item.name}</p>
                    <p class="text-gray-400 text-xs">${item.type} &bull; ${item.desc}</p>
                </div>
            </li>
        `).join("");
    };
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('#dashboardSearch') && !e.target.closest('#searchResults')) {
            const resultsContainer = document.getElementById("searchResults");
            if(resultsContainer) resultsContainer.classList.add("hidden");
        }
    });"""
    content = content[:match.start()] + new_js + content[match.end():]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Search UI overhauled successfully.")
