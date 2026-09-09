import os

app_file = r'd:\dbmss\app.py'
with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

google_auth_code = """
@app.route('/google_login')
def google_login():
    flash("Simulated Google OAuth successful! Please use the standard login for the new multi-role system for now.", "success")
    return redirect(url_for('login'))
"""

idx = content.find("@app.route('/logout')")
if idx != -1:
    content = content[:idx] + google_auth_code + '\n' + content[idx:]
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print('google_login route added back.')
else:
    print('Could not find logout route.')
