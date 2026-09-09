file_path = r'd:\dbmss\app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

injection = "\nfrom api_routes import api_bp\napp.register_blueprint(api_bp, url_prefix='/api')\n"
if 'api_routes import api_bp' not in content:
    idx = content.find("os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)")
    if idx != -1:
        idx += len("os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)")
        new_content = content[:idx] + injection + content[idx:]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Blueprint registered successfully.')
    else:
        print('Could not find injection point.')
else:
    print('Blueprint already registered.')
