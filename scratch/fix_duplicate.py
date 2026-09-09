import os

app_file = r'd:\dbmss\app.py'
with open(app_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if line.startswith("@app.route('/buyer_marketplace')"):
        # Check if this is the generic one (without db calls)
        if i + 5 < len(lines) and "return render_template('buyer_marketplace.html')" in lines[i+5]:
            skip = True
            continue
            
    if skip:
        if "return render_template('buyer_marketplace.html')" in line:
            skip = False
        continue
        
    # Update the original db one
    if "if session.get('role') != 'Buyer':" in line:
        line = "    if session.get('role') not in ['Customer', 'Buyer', 'Admin']:\n"
        
    new_lines.append(line)

with open(app_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Duplicate route fixed.")
