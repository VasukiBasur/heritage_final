with open('d:\\dbmss\\templates\\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Reverse the Powershell expansion damage
content = content.replace('{{ lan_ip }}:5000', '')

# 2. Properly replace the JS variable without Powershell breaking it
# The original JS had: const payloadText = `http://${window.location.host}/scan/${newId}`;
# We want it to be: const payloadText = `http://{{ lan_ip }}:5000/scan/${newId}`;
content = content.replace('const payloadText = `http://${window.location.host}/scan/${newId}`;', 'const payloadText = `http://{{ lan_ip }}:5000/scan/${newId}`;')

with open('d:\\dbmss\\templates\\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Dashboard restored and JS payload properly updated.")
