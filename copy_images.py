import os
import glob
import struct
import shutil

def get_png_size(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = f.read(24)
            if data[:8] == b'\x89PNG\r\n\x1a\n':
                return struct.unpack('>LL', data[16:24])
    except Exception:
        pass
    return (0, 0)

files = glob.glob('C:/Users/user/.gemini/antigravity/brain/70d5ad52-4181-4835-ad41-559a5ffca6d6/.tempmediaStorage/*.png')
files.sort(key=os.path.getmtime, reverse=True)

# The first 3 files are the diagrams we just uploaded:
diagrams = files[:3]
shutil.copy(diagrams[0], 'd:/dbmss/diagram1.png')
shutil.copy(diagrams[1], 'd:/dbmss/diagram2.png')
shutil.copy(diagrams[2], 'd:/dbmss/diagram3.png')

print("Diagrams copied.")

dashboards = []
# Dashboards are 1920x1080 (or similar aspect ratios), very large width compared to height, or just look for the next set of distinct files uploaded earlier.
# Let's just print sizes for all recent files.
for f in files[:20]:
    size = get_png_size(f)
    print(f"{os.path.basename(f)} : {size} : {os.path.getsize(f)} bytes")
