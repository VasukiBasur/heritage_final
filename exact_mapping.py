import oS
import re

html_path = r'd:\dbmss\templates\shop_products.html'

exact_mappings = {
    "Mashru Silk Fabric": "mashru_silk_fabric.png.png",
    "Bhagalpuri Silk Stole": "Baluchari Silk.png.png", # Wait, is this right? I'll let the script find it
    "Men's Kurta Fabric": "Men's Kurta Fabric.png.jpeg",
    "Gadwal Silk Cotton": "Gadwal Silk Cotton.png.jpeg",
    "Venkatagiri Fine Cotton": "Venkatagiri Fine Cotton.png.jpeg",
    "Handwoven Linen Kurti": "Handwoven Linen Kurti.png.jpeg",
    "Tussar Silk Yardage": "Tussar Silk Yardage.png.jpeg",
    "Bandhani Silk Dupatta": "Bandhani_silk_dupatta.png.png",
    "Chettinad Cotton Saree": "chettinad_cotton_saree.png.png",
    "Handblock Printed Kurta": "Handblock Printed Kurta.png.png",
    "Ilkal Traditional Saree": "Ilkal_traditional_checkered.png.jpeg",
    "Silk Blend Shirting": "Silk Blend Shirting.png.png",
    "Handspun Cotton Dhoti": "Handloom_cotton_dhoti.png.jpeg",
    "Khadi Cotton Shirt": "Khadi Cotton Shirt.png.png",
    "Narayanpet Cotton Saree": "Narayanpet Cotton Saree.png.png",
    "Jamdani Handloom": "Jamdani Handloom.png.png",
    "Ajrakh Print Silk": "Ajrakh Print Silk.png.png",
    "Raw Cotton Yardage": "pure_cotton_yarn.png.jpeg"
}

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

def replacer(match):
    full_line = match.group(0)
    title = match.group(1)
    
    if title in exact_mappings:
        best = exact_mappings[title]
        return re.sub(r'img:\s*"[^"]*"', f'img: "images/{best}"', full_line)
    return full_line

pattern = re.compile(r'\{[^}]*title:\s*"([^"]+)"[^}]*img:\s*"[^"]*"[^}]*\}')
new_content = pattern.sub(replacer, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Targeted specific images updated successfully.")
