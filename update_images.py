import os
import re
import difflib

html_path = r'd:\dbmss\templates\shop_products.html'
images_dir = r'd:\dbmss\static\images'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Get all images
all_images = [f for f in os.listdir(images_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

def normalize(s):
    # Remove non-alphanumeric chars
    return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

# Normalize image names for matching
image_map = {normalize(os.path.splitext(f)[0].replace('.png', '').replace('.jpeg', '')): f for f in all_images}
image_keys = list(image_map.keys())

def replace_img(match):
    full_line = match.group(0)
    title = match.group(1)
    
    # Try to find a match
    norm_title = normalize(title)
    
    # First exact normalized match
    best_img = None
    if norm_title in image_map:
        best_img = image_map[norm_title]
    else:
        # Fuzzy match
        matches = difflib.get_close_matches(norm_title, image_keys, n=1, cutoff=0.6)
        if matches:
            best_img = image_map[matches[0]]
    
    if best_img:
        # replace img: "..." with img: "images/best_img"
        new_line = re.sub(r'img:\s*".*?"', f'img: "images/{best_img}"', full_line)
        return new_line
    return full_line

# Regex to find each product line: { ... title: "...", ... img: "..." }
pattern = re.compile(r'\{[^}]*title:\s*"([^"]+)"[^}]*img:\s*"[^"]*"[^}]*\}')
new_content = pattern.sub(replace_img, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully updated shop_products.html with new images.")
