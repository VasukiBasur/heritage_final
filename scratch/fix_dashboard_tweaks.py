import re

path = r'd:\dbmss\templates\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Map to White & Disable Scroll Zoom
content = content.replace("zoomControl: false", "zoomControl: false, scrollWheelZoom: false")
content = content.replace("cartocdn.com/dark_all/", "cartocdn.com/light_all/")

# 2. Make Search Input Work
search_input = '<input type="text" placeholder="Search orders, products, or artisans..."'
content = content.replace(search_input, '<input type="text" id="dashboardSearch" onkeyup="filterTable()" placeholder="Search orders, products, or artisans..."')

filter_js_safe = """
    // Table Search Filter
    window.filterTable = function() {
        const input = document.getElementById("dashboardSearch");
        const filter = input.value.toLowerCase();
        
        // Find all rows in the tracking table (the only table with a tbody on this page)
        const trs = document.querySelectorAll('table tbody tr');
        trs.forEach(tr => {
            const text = tr.innerText.toLowerCase();
            tr.style.display = text.includes(filter) ? "" : "none";
        });
    };
"""
content = content.replace("// Add Mock Log Function", filter_js_safe + "\n    // Add Mock Log Function")

# 3. Fix QR Code to link to /scan/<log_id>
# For static HTML QRs
def repl_static_qr(match):
    return "data=http%3A%2F%2F127.0.0.1%3A5000%2Fscan%2F15&color"
content = re.sub(r'data=Product%20ID%3A[^&]+&color', repl_static_qr, content)

# For dynamic JS QRs
content = re.sub(
    r'const payloadText = `ID:\$\{design\.id\}\\nItem:\$\{design\.name\}\\nFab:\$\{design\.fabric\}\\nCol:\$\{design\.color\}\\nSize:\$\{design\.size\}\\nPat:\$\{design\.pattern\}\\nRs:\$\{design\.price\}`;',
    r'const payloadText = `http://127.0.0.1:5000/scan/${newId}`;',
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Dashboard tweaks applied successfully.")
