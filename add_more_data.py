import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def add_more_data():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "heritage_handloom")
    )
    cursor = conn.cursor()

    # More Materials
    materials = [
        ("Tussar Silk Yarn", 500),
        ("Muga Silk Yarn", 300),
        ("Silver Zari Thread", 150),
        ("Organic Cotton Yarn", 800),
        ("Indigo Natural Dye", 200),
        ("Madder Root Dye", 180),
        ("Eri Silk Yarn", 400),
        ("Linen Blended Yarn", 600),
        ("Kora Silk Thread", 350),
        ("Viscose Blended Yarn", 900)
    ]

    # More Designs
    designs = [
        ("Banarasi Brocade Saree", "Opulent silk saree featuring intricate gold and silver brocade or zari work, characterized by Mughal-inspired designs.", "Varanasi, UP", 9),
        ("Kanchipuram Silk Saree", "Heavyweight pure silk saree known for its deep colors, wide contrasting borders, and temple borders.", "Kanchipuram, TN", 8),
        ("Patola Silk Saree", "Double ikat woven sari, usually made from silk. Extremely intricate and requires precise mathematical alignment.", "Patan, Gujarat", 10),
        ("Chanderi Cotton Silk", "Lightweight sheer texture and fine luxurious feel. Woven in silk and golden Zari in traditional cotton yarn.", "Chanderi, MP", 6),
        ("Sambalpuri Ikat", "A traditional handwoven ikat sari where the warp and the weft are tie-dyed before weaving.", "Odisha", 8),
        ("Jamdani Muslin", "Feather-light and sheer saree, with traditional motifs woven directly on the loom using the supplementary weft technique.", "Bengal", 9),
        ("Paithani Silk Saree", "Characterized by borders of an oblique square design and a pallu with a peacock design.", "Maharashtra", 7),
        ("Pochampally Ikat", "Traditional geometric patterns in Ikat style of dyeing. The fabric is a blend of fine cotton and silk.", "Telangana", 7)
    ]

    try:
        print("Inserting materials...")
        cursor.executemany(
            "INSERT INTO raw_materials (material_name, quantity_available) VALUES (%s, %s)",
            materials
        )
        
        print("Inserting designs...")
        cursor.executemany(
            "INSERT INTO traditional_designs (name, description, region_origin, complexity_rating) VALUES (%s, %s, %s, %s)",
            designs
        )
        
        conn.commit()
        print(f"Successfully added {len(materials)} materials and {len(designs)} designs!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    add_more_data()
