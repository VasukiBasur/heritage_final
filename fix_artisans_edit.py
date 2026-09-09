import os
import re

app_file = r"d:\dbmss\templates\artisans.html"

with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace session['role'] == 'Admin' with session.get('role', '').lower() == 'admin'
content = content.replace("session['role'] == 'Admin'", "session.get('role', '').lower() == 'admin'")

# Just in case, replace session.get('role') == 'Admin'
content = content.replace("session.get('role') == 'Admin'", "session.get('role', '').lower() == 'admin'")

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed edit button visibility in artisans.html")
