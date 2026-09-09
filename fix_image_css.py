import os
import glob
import re

template_dir = r"d:\dbmss\templates"
files_to_update = ['dashboard.html', 'artisans.html', 'designs.html', 'materials.html', 'buyer_marketplace.html']

for fname in files_to_update:
    filepath = os.path.join(template_dir, fname)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all img tags
    # We will use regex to find <img ... class="...">
    # We want to replace the class attribute with the new one, but SKIP qr codes and table icons (w-10, w-12)
    def replacer(match):
        full_tag = match.group(0)
        class_attr = match.group(1)
        
        # Don't touch small images
        if 'w-10' in class_attr or 'w-12' in class_attr:
            return full_tag
            
        # Replace the class string
        new_class = "w-full h-56 object-cover rounded-t-lg opacity-80 hover:opacity-100 transition-opacity"
        return full_tag.replace(class_attr, new_class)
        
    # Regex to find class attribute in img tag
    # <img ... class="something" ...>
    # Note: this simple regex assumes class="something" is present
    new_content = re.sub(r'<img[^>]+class="([^"]+)"[^>]*>', replacer, content)
    
    # Also we need to remove the wrapper div's fixed height if it has one (like h-40 or h-64) so it doesn't clip the h-56 image.
    new_content = new_content.replace('class="h-40 w-full bg-brand-black"', 'class="w-full bg-brand-black rounded-t-lg"')
    new_content = new_content.replace('class="relative h-64 rounded-sm overflow-hidden group shadow-lg border border-brand-gold/20"', 'class="relative rounded-sm overflow-hidden group shadow-lg border border-brand-gold/20"')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
print("Updated image CSS.")
