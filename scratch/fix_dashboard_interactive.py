import re

path = r'd:\dbmss\templates\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix Search functionality
# We will make it scroll to the table when searching so they see the result.
search_js_old = """window.filterTable = function() {
        const input = document.getElementById("dashboardSearch");
        const filter = input.value.toLowerCase();
        
        // Find all rows in the tracking table (the only table with a tbody on this page)
        const trs = document.querySelectorAll('table tbody tr');
        trs.forEach(tr => {
            const text = tr.innerText.toLowerCase();
            tr.style.display = text.includes(filter) ? "" : "none";
        });
    };"""

search_js_new = """window.filterTable = function() {
        const input = document.getElementById("dashboardSearch");
        const filter = input.value.toLowerCase();
        
        // Find all rows in the tracking table
        const table = document.querySelector('table');
        if (!table) return;
        
        const trs = table.querySelectorAll('tbody tr');
        let count = 0;
        trs.forEach(tr => {
            const text = tr.innerText.toLowerCase();
            if (text.includes(filter)) {
                tr.style.display = "";
                count++;
            } else {
                tr.style.display = "none";
            }
        });
        
        // Show a small temporary alert if no results found, to make it obvious
        if (filter.length > 2 && count === 0 && !window.searchAlertShown) {
            window.searchAlertShown = true;
            setTimeout(() => {
                alert("No results found for '" + filter + "' in production logs.");
                window.searchAlertShown = false;
            }, 500);
        }
    };"""
content = content.replace(search_js_old, search_js_new)

# 2. Fix Update Buttons
# Replace <button class="bg-brand-gold ... hover:bg-yellow-500">Update</button>
# with <button onclick="updateStatus(this)" class="...">Update</button>
content = content.replace('hover:bg-yellow-500">Update</button>', 'hover:bg-yellow-500" onclick="updateStatus(this)">Update</button>')

# Add updateStatus JS
update_js = """
    window.updateStatus = function(btn) {
        const row = btn.closest('tr');
        const select = row.querySelector('select');
        const badge = row.querySelector('span[class*="px-3 py-1 bg-"]'); // The status badge
        if (select && badge) {
            const newStatus = select.value;
            badge.innerText = newStatus;
            badge.className = "px-3 py-1 rounded text-xs border bg-green-900/40 text-green-400 border-green-500/50";
            alert("Status updated to: " + newStatus);
        }
    };
"""
content = content.replace("// Add Mock Log Function", update_js + "\n    // Add Mock Log Function")

# 3. Fix QR Code dynamic parameters
# Replace payloadText = `http://127.0.0.1:5000/scan/${newId}`
# with payloadText = `http://127.0.0.1:5000/scan/${newId}?design=${encodeURIComponent(design.name)}&img=${encodeURIComponent(design.img)}`;
content = content.replace("const payloadText = `http://127.0.0.1:5000/scan/${newId}`;", "const payloadText = `http://127.0.0.1:5000/scan/${newId}?design=${encodeURIComponent(design.name)}&img=${encodeURIComponent(design.img)}`;")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Dashboard interactive fixes applied.")
