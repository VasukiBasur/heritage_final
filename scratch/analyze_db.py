import re
import os

tables_and_columns = {}

for fname in ['app.py', 'api_routes.py', 'artisan_api_routes.py']:
    if not os.path.exists(fname): continue
    content = open(fname, encoding='utf-8').read()
    
    # Find all cursor.execute statements
    pattern = r'cursor\.execute\s*\(\s*("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')'
    for match in re.finditer(pattern, content):
        q = match.group(1).strip('"\' \n\t')
        clean_q = " ".join(q.split())
        print(f"[{fname}] {clean_q}")
