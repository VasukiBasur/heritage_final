import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def add_old_materials():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "heritage_handloom")
    )
    cursor = conn.cursor()

    # The previous materials the user wants back
    old_materials = [
        ("Eri Silk", 100),
        ("Cotton Yarn", 200),
        ("Pure cotton", 150),
        ("Organic Cotton", 300),
        ("Natural Indigo Dye", 100),
        ("Silk Yarn", 250)
    ]

    try:
        print("Restoring previous materials...")
        cursor.executemany(
            "INSERT INTO raw_materials (material_name, quantity_available) VALUES (%s, %s)",
            old_materials
        )
        conn.commit()
        print(f"Successfully restored {cursor.rowcount} previous materials!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    add_old_materials()
