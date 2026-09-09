import re

html_path = r'd:\dbmss\templates\shop_products.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

def replacer(match):
    full_line = match.group(0)
    title = match.group(1)
    
    if title == "Premium Vest/Veshti" or title == "Premium Silk Dhoti":
        # I notice the product title in the screenshot is "Premium Vest/Veshti"
        # Wait, the title in the screenshot is literally "Premium Vest/Veshti"
        return re.sub(r'img:\s*"[^"]*"', f'img: "images/Premium VestVeshti.png.png"', full_line)
        
    if title == "Raw Cotton Yardage":
        return re.sub(r'img:\s*"[^"]*"', f'img: "images/pure_cotton_yarn.png.jpeg"', full_line)

    return full_line

pattern = re.compile(r'\{[^}]*title:\s*"([^"]+)"[^}]*img:\s*"[^"]*"[^}]*\}')
new_content = pattern.sub(replacer, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated the two specific images.")
