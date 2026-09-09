import re

dashboard_path = r'd:\dbmss\templates\dashboard.html'
with open(dashboard_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update all <select> elements to have the full set of options
full_select_options = """<select class="bg-[#121212] border border-brand-gold/30 text-gray-300 text-xs rounded px-2 py-1 outline-none font-bold">
                        <option>Order Placed</option>
                        <option>Raw Material Supply</option>
                        <option>Weaving</option>
                        <option>Quality Check</option>
                        <option>Shipped</option>
                        <option>Delivered</option>
                    </select>"""

# We can replace all select elements inside the table
# The original selects might look like:
# <select class="bg-[#121212] border border-brand-gold/30 text-gray-300 text-xs rounded px-2 py-1 outline-none font-bold">\n<option>Raw Material Supply</option>\n<option>Weaving</option>\n</select>
content = re.sub(
    r'<select class="bg-\[#121212\] border border-brand-gold/30 text-gray-300 text-xs rounded px-2 py-1 outline-none font-bold">.*?</select>',
    full_select_options,
    content,
    flags=re.DOTALL
)


# 2. Update all hardcoded 127.0.0.1 IPs in the QR urls to use {{ request.host }} dynamically!
# In the HTML tags:
# src="https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=http%3A%2F%2F127.0.0.1%3A5000%2Fscan%2F15&color=000000&bgcolor=FFFFFF"
content = re.sub(
    r'data=http%3A%2F%2F127\.0\.0\.1%3A5000%2Fscan%2F(\d+)',
    r'data=http%3A%2F%2F{{ request.host | urlencode }}%2Fscan%2F\1',
    content
)

# 3. Update the JavaScript hardcoded IP to use window.location.host
# const payloadText = `http://127.0.0.1:5000/scan/${newId}`;
content = content.replace(
    'const payloadText = `http://127.0.0.1:5000/scan/${newId}`;',
    'const payloadText = `http://${window.location.host}/scan/${newId}`;'
)

# 4. Make sure app.py runs on 0.0.0.0
app_path = r'd:\dbmss\app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

app_content = app_content.replace('app.run(debug=True)', "app.run(debug=True, host='0.0.0.0')")

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(content)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_content)

print("Dashboard QR IPs are now fully dynamic. All select options are restored. Flask listens on all interfaces.")
