import re

dashboard_path = r'd:\dbmss\templates\dashboard.html'
with open(dashboard_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Modals HTML to the bottom of the body
modals_html = """
<!-- Universal Profile Modal -->
<div id="profileModal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-[200] flex items-center justify-center p-4">
    <div class="bg-[#1a1a1a] border border-brand-gold/30 rounded-lg shadow-2xl w-full max-w-md overflow-hidden transform transition-all">
        <div class="bg-[#121212] p-4 border-b border-brand-gold/20 flex justify-between items-center">
            <h3 id="profileModalTitle" class="text-brand-gold font-bold text-lg font-serif">Profile Details</h3>
            <button onclick="document.getElementById('profileModal').classList.add('hidden')" class="text-gray-400 hover:text-white">&times;</button>
        </div>
        <div class="p-6">
            <div class="flex items-center gap-4 mb-6">
                <div id="profileModalIcon" class="w-16 h-16 rounded-full bg-[#121212] border-2 border-brand-gold/50 flex items-center justify-center text-3xl">🧶</div>
                <div>
                    <h4 id="profileModalName" class="text-white font-bold text-xl">Name</h4>
                    <p id="profileModalType" class="text-brand-gold text-sm uppercase tracking-wider">Type</p>
                </div>
            </div>
            <div class="space-y-3">
                <div class="bg-[#121212] p-3 rounded border border-white/5">
                    <p class="text-xs text-gray-500 uppercase">Description</p>
                    <p id="profileModalDesc" class="text-gray-300 text-sm mt-1">Details...</p>
                </div>
                <div class="bg-[#121212] p-3 rounded border border-white/5">
                    <p class="text-xs text-gray-500 uppercase">Status</p>
                    <p class="text-green-400 text-sm mt-1 font-bold">Active / Verified</p>
                </div>
            </div>
            <button onclick="document.getElementById('profileModal').classList.add('hidden')" class="mt-6 w-full bg-brand-gold text-black font-bold py-2 rounded hover:bg-yellow-500 transition-colors">Close Profile</button>
        </div>
    </div>
</div>

<!-- Universal Action Modal -->
<div id="actionModal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-[200] flex items-center justify-center p-4">
    <div class="bg-[#1a1a1a] border border-brand-gold/30 rounded-lg shadow-2xl w-full max-w-md overflow-hidden">
        <div class="bg-[#121212] p-4 border-b border-brand-gold/20 flex justify-between items-center">
            <h3 id="actionModalTitle" class="text-brand-gold font-bold text-lg font-serif">Action</h3>
            <button onclick="document.getElementById('actionModal').classList.add('hidden')" class="text-gray-400 hover:text-white">&times;</button>
        </div>
        <div class="p-6">
            <form id="actionForm" onsubmit="handleActionSubmit(event)" class="space-y-4">
                <div>
                    <label class="block text-xs text-gray-400 uppercase tracking-wider mb-1">Name / Identifier</label>
                    <input type="text" required class="w-full bg-[#121212] border border-brand-gold/30 text-white rounded p-2 focus:outline-none focus:border-brand-gold">
                </div>
                <div>
                    <label class="block text-xs text-gray-400 uppercase tracking-wider mb-1">Details</label>
                    <textarea rows="3" class="w-full bg-[#121212] border border-brand-gold/30 text-white rounded p-2 focus:outline-none focus:border-brand-gold"></textarea>
                </div>
                <button type="submit" class="w-full bg-brand-gold text-black font-bold py-2 rounded hover:bg-yellow-500 transition-colors mt-4">Save Entry</button>
            </form>
        </div>
    </div>
</div>
"""
if "id=\"profileModal\"" not in content:
    content = content.replace("</body>", modals_html + "\n</body>")


# 2. Add onclick handlers to the Quick Action buttons
# We'll use a regex to replace those specific buttons.
def add_action_onclick(match):
    full_btn = match.group(0)
    inner_text = match.group(1)
    if 'onclick' not in full_btn:
        return full_btn.replace('class="', f'onclick="openActionModal(\'{inner_text}\')" class="')
    return full_btn

content = re.sub(r'<button class="bg-\[#121212\].*?>(.*?)</button>', add_action_onclick, content)


# 3. Update the handleSearch onclick behavior to open the Profile Modal
search_js_old = r"onclick=\"document.getElementById\('searchResults'\)\.classList\.add\('hidden'\); window\.addMockLog\('\$\{item\.name\}'\); document\.querySelector\('table'\)\.scrollIntoView\(\{behavior: 'smooth'\}\);\""
search_js_new = r"onclick=\"openProfileModal('${item.name}', '${item.type}', '${item.desc}', '${item.icon}')\""
content = re.sub(search_js_old, search_js_new, content)


# 4. Inject the new JS functions at the end of the script tag
new_js_logic = """
    // UI Modal Logic
    window.openProfileModal = function(name, type, desc, icon) {
        document.getElementById('searchResults').classList.add('hidden');
        document.getElementById('profileModalName').innerText = name;
        document.getElementById('profileModalType').innerText = type;
        document.getElementById('profileModalDesc').innerText = desc;
        document.getElementById('profileModalIcon').innerText = icon;
        document.getElementById('profileModal').classList.remove('hidden');
    };

    window.openActionModal = function(actionName) {
        document.getElementById('actionModalTitle').innerText = actionName;
        document.getElementById('actionModal').classList.remove('hidden');
    };

    window.handleActionSubmit = function(e) {
        e.preventDefault();
        const actionName = document.getElementById('actionModalTitle').innerText;
        alert(actionName + " executed successfully!");
        document.getElementById('actionModal').classList.add('hidden');
        e.target.reset();
    };

    // Global QR Code Click Listener (Click QR to open product details directly)
    document.addEventListener('click', function(e) {
        if (e.target.tagName === 'IMG' && e.target.alt === 'QR') {
            const src = e.target.src;
            const scanMatch = src.match(/scan%2F(\\d+)/);
            if (scanMatch) {
                window.open('/scan/' + scanMatch[1], '_blank');
            } else {
                const unencodedMatch = src.match(/scan\\/(\\d+)/);
                if (unencodedMatch) {
                    window.open('/scan/' + unencodedMatch[1], '_blank');
                }
            }
        }
    });
"""
if "window.openProfileModal =" not in content:
    content = content.replace("</script>\n</body>", new_js_logic + "\n</script>\n</body>")

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Dashboard interactions upgraded with Modals and QR clicking.")
