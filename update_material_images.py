import mysql.connector
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

def update_images():
    source_dir = os.path.join("static", "images")
    dest_dir = os.path.join("static", "uploads")
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Dictionary mapping material names to image filenames
    image_mapping = {
        "Muga Silk Yarn": "Muga_silk_yarn.png.jpeg",
        "Tussar Silk Yarn": "Tussar_silk_yarn.png.jpeg",
        "Eri Silk": "eri_silk.png.jpeg",
        "Eri Silk Yarn": "eri_silk.png.jpeg",
        "Cotton Yarn": "cotton_yarn.png.jpeg",
        "Organic Cotton": "organic_cotton.png.jpeg",
        "Organic Cotton Yarn": "organic_cotton_yarn.png.jpeg",
        "Pure cotton": "pure_cotton_yarn.png.jpeg",
        "Natural Indigo Dye": "natural_indigo_dye.png.jpeg",
        "Indigo Natural Dye": "natural_indigo_dye.png.jpeg",
        "Silk Yarn": "silk_yarn.png.jpeg",
        "Mulberry Silk": "mulberry_silk.png.jpeg",
        "Premium Zari Thread": "premium_zari_thread.png.jpeg",
        "Pure Gold Zari": "pure_gold_zari.png.jpeg",
        "Silver Zari Thread": "premium_zari_thread.png.jpeg", # fallback
        "Kora Silk Thread": "kora_silk_thread.png.jpeg",
        "Linen Blended Yarn": "linen_blended_yarn.png.jpeg",
        "Madder Root Dye": "madder_root_dye.png.jpeg",
        "Viscose Blended Yarn": "viscose_blended_yarn.png.jpeg",
    }

    # First, copy the images
    for material, filename in image_mapping.items():
        src_path = os.path.join(source_dir, filename)
        dst_path = os.path.join(dest_dir, filename)
        if os.path.exists(src_path) and not os.path.exists(dst_path):
            shutil.copy(src_path, dst_path)

    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "heritage_handloom")
    )
    cursor = conn.cursor()

    try:
        # Fetch all materials
        cursor.execute("SELECT material_id, material_name FROM raw_materials")
        materials = cursor.fetchall()

        updated_count = 0
        for mat in materials:
            mat_id = mat[0]
            mat_name = mat[1]
            
            # Find the best matching image
            best_image = None
            if mat_name in image_mapping:
                best_image = image_mapping[mat_name]
            
            if best_image:
                # Also ensure the file exists in static/uploads
                if os.path.exists(os.path.join(dest_dir, best_image)):
                    cursor.execute("UPDATE raw_materials SET image_file = %s WHERE material_id = %s", (best_image, mat_id))
                    updated_count += 1
                else:
                    print(f"Warning: Image file {best_image} not found in {dest_dir} for {mat_name}")

        conn.commit()
        print(f"Successfully updated images for {updated_count} materials!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    update_images()
