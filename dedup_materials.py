import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def remove_duplicates():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "heritage_handloom")
    )
    cursor = conn.cursor()

    try:
        # We will keep the row with the lowest material_id for each material_name
        # and delete the rest.
        print("Removing duplicate materials...")
        
        # In MySQL, deleting from a table while selecting from the same table in a subquery requires a temporary table.
        cursor.execute("""
            DELETE t1 FROM raw_materials t1
            INNER JOIN raw_materials t2 
            WHERE 
                t1.material_id > t2.material_id AND 
                t1.material_name = t2.material_name;
        """)
        
        deleted_materials = cursor.rowcount
        conn.commit()
        print(f"Removed {deleted_materials} duplicate materials.")
        
        print("Removing duplicate designs...")
        cursor.execute("""
            DELETE t1 FROM traditional_designs t1
            INNER JOIN traditional_designs t2 
            WHERE 
                t1.design_id > t2.design_id AND 
                t1.name = t2.name;
        """)
        
        deleted_designs = cursor.rowcount
        conn.commit()
        print(f"Removed {deleted_designs} duplicate designs.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    remove_duplicates()
