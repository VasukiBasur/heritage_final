import shutil
import re

# Copy image
src = r'C:\Users\user\.gemini\antigravity\brain\70d5ad52-4181-4835-ad41-559a5ffca6d6\raw_cotton_yardage_1779961432471.png'
dest = r'd:\dbmss\static\images\raw_cotton_yardage.png'
shutil.copy(src, dest)

# Update HTML
html_path = r'd:\dbmss\templates\shop_products.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

def replacer(match):
    full_line = match.group(0)
    title = match.group(1)
    if title == 'Raw Cotton Yardage':
        return re.sub(r'img:\s*"[^"]*"', f'img: "images/raw_cotton_yardage.png"', full_line)
    return full_line

pattern = re.compile(r'\{[^}]*title:\s*"([^"]+)"[^}]*img:\s*"[^"]*"[^}]*\}')
new_content = pattern.sub(replacer, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Updated successfully')
