import urllib.request
import re

try:
    with urllib.request.urlopen('http://localhost:5000/shop/products') as response:
        html = response.read().decode('utf-8')
        if 'DOMContentLoaded' in html:
            print('Successfully loaded HTML via localhost')
            # Look for the product grid content
            match = re.search(r'<div id="product-grid"[^>]*>(.*?)</div>', html, re.DOTALL)
            if match:
                print('Grid content snippet:', match.group(1)[:100])
        else:
            print("DOMContentLoaded NOT FOUND in html!")
except Exception as e:
    print('Failed:', e)
