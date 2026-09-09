import os

def inject_script(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'frontend_api.js' not in content:
        # Insert right before </body>
        idx = content.rfind('</body>')
        if idx != -1:
            injection = '<script src="{{ url_for(\'static\', filename=\'frontend_api.js\') }}"></script>\n'
            new_content = content[:idx] + injection + content[idx:]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Injected into {os.path.basename(file_path)}')
        else:
            print(f'Could not find </body> in {os.path.basename(file_path)}')
    else:
        print(f'Already injected in {os.path.basename(file_path)}')

inject_script(r'd:\dbmss\templates\base_layout.html')
inject_script(r'd:\dbmss\templates\dashboard.html')
