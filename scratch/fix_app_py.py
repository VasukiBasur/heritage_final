import re

file_path = r'd:\dbmss\app.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find where the placeholder routes start
placeholder_start = content.find('# ==========================================')
if placeholder_start != -1:
    main_start = content.find("if __name__ == '__main__':")
    
    if main_start != -1 and placeholder_start > main_start:
        # The placeholders are after main! Let's swap them.
        placeholders = content[placeholder_start:]
        rest_of_file = content[:main_start]
        main_block = content[main_start:placeholder_start]
        
        new_content = rest_of_file + "\n" + placeholders + "\n" + main_block
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Fixed app.py route ordering.")
    else:
        print("Placeholders are already before main, or main not found.")
else:
    print("Placeholders not found.")
