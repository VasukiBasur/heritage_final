import mysql.connector
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

def update():
    source_dir = os.path.join("static", "images")
    dest_dir = os.path.join("static", "uploads")
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "heritage_handloom")
    )
    cursor = conn.cursor()

    try:
        # 1. Remove "Natural Indigo Dye" (and "Indigo Natural Dye" if any)
        print("Removing Natural Indigo Dye...")
        cursor.execute("DELETE FROM raw_materials WHERE material_name LIKE '%Indigo%' OR material_name LIKE '%Madder%'")
        # Removing any dye as requested
        
        # 2. Add silver zari thread photo
        filename = "silver_zari_thread.png.jpeg"
        src_path = os.path.join(source_dir, filename)
        dst_path = os.path.join(dest_dir, filename)
        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)
            cursor.execute("UPDATE raw_materials SET image_file = %s WHERE material_name = 'Silver Zari Thread'", (filename,))
            print("Updated Silver Zari Thread image.")

        # 3. Update Designs images
        design_mapping = {
            "Banarasi Brocade Saree": "banarasi_brocode_saree.png.jpeg",
            "Chanderi Cotton Silk": "chanderi_cotton_silk.png.jpeg",
            "Jamdani Muslin": "jamdani_muslin.png.jpeg",
            "Kanchipuram Silk Saree": "kanchipuram_silk_saree.png.jpeg",
            "Paithani Silk Saree": "paithani_silk_saree.png.jpeg",
            "Patola Silk Saree": "patola_silk_saree.png.jpeg",
            "Pochampally Ikat": "ponchampally_ikat.png.jpeg",
            "Sambalpuri Ikat": "sambalpuri_ikat.png.jpeg",
        }

        updated_designs = 0
        for design_name, fname in design_mapping.items():
            src_path = os.path.join(source_dir, fname)
            dst_path = os.path.join(dest_dir, fname)
            if os.path.exists(src_path):
                shutil.copy(src_path, dst_path)
                cursor.execute("UPDATE traditional_designs SET image_file = %s WHERE name = %s", (fname, design_name))
                if cursor.rowcount > 0:
                    updated_designs += 1

        print(f"Updated images for {updated_designs} designs.")
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    update()
