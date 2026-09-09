import os
import shutil

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
UPLOAD_DIR = os.path.join(STATIC_DIR, 'uploads')

os.makedirs(UPLOAD_DIR, exist_ok=True)

mappings = {
    'saree.jpg': 'default_design.jpg',
    'weaver.jpg': 'default_artisan.jpg',
    'materials.jpg': 'default_material.jpg'
}

for src_name, dest_name in mappings.items():
    src_path = os.path.join(IMAGES_DIR, src_name)
    dest_path = os.path.join(UPLOAD_DIR, dest_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, dest_path)
        print(f"Copied {src_name} to {dest_name}")
    else:
        print(f"Source file {src_path} not found.")
