import re
with open(r'd:\dbmss\templates\shop_products.html', 'r', encoding='utf-8') as f:
    content = f.read()
matches = re.findall(r'title:\s*"([^"]+Veshti[^"]*)"', content)
if matches:
    print('Found:', matches)
else:
    print('Not found Vest/Veshti')
