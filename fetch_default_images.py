import os
import urllib.request

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

IMAGES = {
    'default_design.jpg': 'https://upload.wikimedia.org/wikipedia/commons/c/ca/Kancheepuram_Silk_Saree_01.jpg',
    'default_artisan.jpg': 'https://upload.wikimedia.org/wikipedia/commons/1/1a/Handloom_weaving_at_a_village_in_India.jpg',
    'default_material.jpg': 'https://upload.wikimedia.org/wikipedia/commons/6/6f/Silk_yarn.jpg'
}

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

for filename, url in IMAGES.items():
    filepath = os.path.join(UPLOAD_DIR, filename)
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"Saved {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
