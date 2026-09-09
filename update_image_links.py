import os
import glob

# Mappings of external URLs to local static routes
REPLACEMENTS = {
    # URLs from step 1
    'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Kancheepuram_Silk_Saree_01.jpg/640px-Kancheepuram_Silk_Saree_01.jpg': "{{ url_for('static', filename='images/saree.jpg') }}",
    'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Handloom_weaving_at_a_village_in_India.jpg/640px-Handloom_weaving_at_a_village_in_India.jpg': "{{ url_for('static', filename='images/weaver.jpg') }}",
    'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Silk_yarn.jpg/640px-Silk_yarn.jpg': "{{ url_for('static', filename='images/materials.jpg') }}",
    
    # login.html background
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Sari_silk_and_gold.jpg/800px-Sari_silk_and_gold.jpg": "{{ url_for('static', filename='images/saree.jpg') }}"
}

template_dir = r"d:\dbmss\templates"
for filepath in glob.glob(os.path.join(template_dir, "*.html")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = False
    for old_url, new_url in REPLACEMENTS.items():
        if old_url in content:
            content = content.replace(old_url, new_url)
            modified = True
            
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filepath}")
