import re
from bs4 import BeautifulSoup
html = open('d:/dbmss/templates/delivery_dashboard.html', 'r', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')
tabs = soup.find_all(class_='tab-content')
for t in tabs:
    print(t.get('id'))
