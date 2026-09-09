import shutil
import re

# 1. Copy template so that Tracking has its own dedicated page
shutil.copyfile('templates/supplier_active.html', 'templates/supplier_tracking.html')

# 2. Edit app.py so the route /supplier/tracking explicitly points to the new template
with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('def supplier_tracking():')
if start_idx != -1:
    end_idx = text.find("url_for('supplier_active'))", start_idx)
    if end_idx != -1:
        # Construct the new function
        replacement = '''def supplier_tracking():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    return render_template('supplier_tracking.html')'''
        
        text = text[:start_idx] + replacement + text[end_idx + len("url_for('supplier_active'))"):]

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

# 3. Edit supplier_tracking.html title
with open('templates/supplier_tracking.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('Active Transits - Live Map', 'Live Delivery Tracking Map')
html = html.replace('{% block title %}Supplier Active{% endblock %}', '{% block title %}Tracking Map{% endblock %}')
html = html.replace('{% block header_title %}Active Transits{% endblock %}', '{% block header_title %}Live Fleet Tracking{% endblock %}')

with open('templates/supplier_tracking.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Successfully created supplier_tracking.html and updated app.py')
