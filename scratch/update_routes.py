import re

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_messages = '''@app.route('/supplier/messages')
@login_required
def supplier_messages():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    return render_template('supplier_messages.html')'''
text = re.sub(r'def supplier_messages\(\): return render_placeholder\("Messages"\)', new_messages, text)

new_tracking = '''@app.route('/supplier/tracking')
@login_required
def supplier_tracking():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    return redirect(url_for('supplier_active'))'''
text = re.sub(r'@app\.route\(\'/supplier/tracking\'\)\ndef supplier_tracking\(\): return render_placeholder\("Tracking"\)', new_tracking, text)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated app.py routes successfully.')
