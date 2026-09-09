import os
import urllib.request

# Define the local directory
STATIC_IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images')
os.makedirs(STATIC_IMAGES_DIR, exist_ok=True)

# Image URLs using reliable picsum endpoints to avoid rate limits
IMAGES = {
    'saree.jpg': 'https://picsum.photos/seed/saree/800/600',
    'weaver.jpg': 'https://picsum.photos/seed/weaver/800/600',
    'materials.jpg': 'https://picsum.photos/seed/materials/800/600'
}

# Add a user-agent header
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
urllib.request.install_opener(opener)

# Download images
for filename, url in IMAGES.items():
    filepath = os.path.join(STATIC_IMAGES_DIR, filename)
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"Successfully saved {filename} to {filepath}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
