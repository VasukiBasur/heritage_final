import re
import urllib.parse

# 1. Update dashboard.html
dashboard_path = r'd:\dbmss\templates\dashboard.html'
with open(dashboard_path, 'r', encoding='utf-8') as f:
    dash_content = f.read()

# Fix QR Codes by parsing the HTML and carefully replacing them with api.qrserver.com
# We will extract the row ID and generate the correct URL for each.
def fix_static_qr(match):
    full_html = match.group(0)
    # The row ID is in the preceding td like: <td class="p-3 font-bold text-brand-gold">#15</td>
    # But since we're just matching the img tag, we can't easily look back with regex.
    # We can just match the tr blocks.
    return full_html

# Let's split by <tr> and replace inside
tr_blocks = dash_content.split('<tr ')
new_dash_content = tr_blocks[0]

for block in tr_blocks[1:]:
    if 'alt="QR"' in block:
        # Find the ID in this row
        id_match = re.search(r'#(\d+)', block)
        row_id = id_match.group(1) if id_match else '15'
        
        # Build the exact, safe qrserver URL
        payload = f"http://127.0.0.1:5000/scan/{row_id}"
        encoded = urllib.parse.quote(payload, safe='')
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={encoded}&color=000000&bgcolor=FFFFFF"
        
        # Replace the img src
        # It could be chart.googleapis.com or api.qrserver.com
        block = re.sub(r'src=\"[^\"]*(qrserver|googleapis)[^\"]*\"', f'src="{qr_url}"', block)
    
    new_dash_content += '<tr ' + block

dash_content = new_dash_content

# Also fix the dynamic JS QR code back to qrserver
dash_content = re.sub(
    r'src=\"https://chart\.googleapis\.com[^\"]*\"',
    r'src="https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=${encodedPayload}&color=000000&bgcolor=FFFFFF"',
    dash_content
)

# 2. Add "Purpose" to the Search Dropdown
# We will modify the onclick of the dropdown items to call addMockLog with the specific item name!
search_js_old = r"onclick=\"document\.getElementById\('searchResults'\)\.classList\.add\('hidden'\); alert\('Navigating to ' \+ '\$\{item\.name\}...'\);\""
search_js_new = r"onclick=\"document.getElementById('searchResults').classList.add('hidden'); window.addMockLog('${item.name}'); document.querySelector('table').scrollIntoView({behavior: 'smooth'});\""
dash_content = re.sub(search_js_old, search_js_new, dash_content)

# And we need to modify addMockLog to accept a custom name optionally
add_log_old = r"window\.addMockLog = function\(\) \{"
add_log_new = r"window.addMockLog = function(customName) {"
dash_content = dash_content.replace(add_log_old, add_log_new)

# Modify the design selection to use customName if provided
design_logic_old = "const design = designs[Math.floor(Math.random() * designs.length)];"
design_logic_new = """let design = designs[Math.floor(Math.random() * designs.length)];
        if (customName) {
            design = { ...design, name: customName }; // Override name with searched item
        }"""
dash_content = dash_content.replace(design_logic_old, design_logic_new)

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(dash_content)

print("Dashboard QR codes restored and search purpose added.")
