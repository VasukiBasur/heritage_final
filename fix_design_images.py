import os

template_dir = r"d:\dbmss\templates"
hardcoded_src = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Kancheepuram_Silk_Saree_01.jpg/640px-Kancheepuram_Silk_Saree_01.jpg'

for fname in ['designs.html', 'buyer_marketplace.html']:
    filepath = os.path.join(template_dir, fname)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    import re
    # We want to replace `{{ url_for('static', filename='uploads/' ~ design.image_file) }}`
    # and any other src representing the design image.
    content = re.sub(r'src="\{\{ url_for\(\'static\', filename=\'uploads/\' \~ design\.image_file\) \}\}"', f'src="{hardcoded_src}"', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Updated designs.html and buyer_marketplace.html with hardcoded images.")
