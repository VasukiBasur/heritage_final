import re
html = open('d:/dbmss/templates/delivery_dashboard.html', 'r', encoding='utf-8').read()
matches = re.findall(r'id=\"([^\"]+)\"[^>]*class=\"[^\"]*tab-content[^\"]*\"', html)
print(matches)
