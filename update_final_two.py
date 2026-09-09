import shutil
import re
import os

# Paths to the newly generated images
src_baluchari = r'C:\Users\user\.gemini\antigravity\brain\70d5ad52-4181-4835-ad41-559a5ffca6d6\baluchari_silk_saree_1779961883041.png'
src_eri = r'C:\Users\user\.gemini\antigravity\brain\70d5ad52-4181-4835-ad41-559a5ffca6d6\eri_silk_shawl_1779961834610.png'

dest_baluchari = r'd:\dbmss\static\images\baluchari_red.png'
dest_eri = r'd:\dbmss\static\images\eri_blue_shawl.png'

shutil.copy(src_baluchari, dest_baluchari)
shutil.copy(src_eri, dest_eri)

# Update HTML
html_path = r'd:\dbmss\templates\shop_products.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

def replacer(match):
    full_line = match.group(0)
    title = match.group(1)
    
    if title == 'Baluchari Silk':
        return re.sub(r'img:\s*"[^"]*"', f'img: "images/baluchari_red.png"', full_line)
        
    if title == "Eri Silk Men's Shawl":
        return re.sub(r'img:\s*"[^"]*"', f'img: "images/eri_blue_shawl.png"', full_line)

    return full_line

pattern = re.compile(r'\{[^}]*title:\s*"([^"]+)"[^}]*img:\s*"[^"]*"[^}]*\}')
new_content = pattern.sub(replacer, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Successfully updated Baluchari Silk and Eri Silk Mens Shawl.')
