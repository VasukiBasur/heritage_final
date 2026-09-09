import os
import re

html_path = r'd:\dbmss\templates\shop_products.html'
images_dir = r'd:\dbmss\static\images'

targets = [
    "Mashru Silk Fabric",
    "Bhagalpuri Silk Stole",
    "Men's Kurta Fabric",
    "Gadwal Silk Cotton",
    "Venkatagiri Fine Cotton",
    "Handwoven Linen Kurti",
    "Tussar Silk Yardage",
    "Bandhani Silk Dupatta",
    "Chettinad Cotton Saree",
    "Handblock Printed Kurta",
    "Ilkal Traditional Saree",
    "Silk Blend Shirting",
    "Handspun Cotton Dhoti",
    "Khadi Cotton Shirt",
    "Narayanpet Cotton Saree",
    "Jamdani Handloom",
    "Ajrakh Print Silk",
    "Raw Cotton Yardage"
]

all_images = os.listdir(images_dir)

def norm(s):
    return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

img_map = {norm(f.replace('.png','').replace('.jpeg','').replace('.jpg','')): f for f in all_images}

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

def replacer(match):
    full_line = match.group(0)
    title = match.group(1)
    
    if title in targets:
        n_title = norm(title)
        if n_title in img_map:
            best = img_map[n_title]
            print(f'Updated {title} -> {best}')
            return re.sub(r'img:\s*"[^"]*"', f'img: "images/{best}"', full_line)
        else:
            print(f'NO EXACT MATCH FOR {title}, looking for substrings')
            for k, v in img_map.items():
                if k in n_title or n_title in k:
                    print(f'  -> Substring matched {title} -> {v}')
                    return re.sub(r'img:\s*"[^"]*"', f'img: "images/{v}"', full_line)
    return full_line

pattern = re.compile(r'\{[^}]*title:\s*"([^"]+)"[^}]*img:\s*"[^"]*"[^}]*\}')
new_content = pattern.sub(replacer, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Targeted images updated successfully.")
