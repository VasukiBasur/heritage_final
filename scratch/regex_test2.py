import re
html = open('d:/dbmss/templates/delivery_dashboard.html', 'r', encoding='utf-8').read()
ids = re.findall(r'id="([^"]+)"', html)
duplicates = [i for i in set(ids) if ids.count(i) > 1]
print("Duplicates:", duplicates)
