import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def consolidate():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "heritage_handloom")
    )
    cursor = conn.cursor(dictionary=True)

    # Dictionary of redundant material names mapping to their target canonical name
    merges = {
        'Eri Silk': 'Eri Silk Yarn',
        'Cotton Yarn': 'Organic Cotton Yarn',
        'Pure cotton': 'Organic Cotton Yarn',
        'Organic Cotton': 'Organic Cotton Yarn',
        'Natural Indigo Dye': 'Indigo Natural Dye',
        'Silk Yarn': 'Mulberry Silk'
    }

    try:
        for old_name, new_name in merges.items():
            # Find the ID of the new (canonical) material
            cursor.execute("SELECT material_id, quantity_available FROM raw_materials WHERE material_name = %s LIMIT 1", (new_name,))
            target = cursor.fetchone()
            
            # Find the ID of the old (redundant) material
            cursor.execute("SELECT material_id, quantity_available FROM raw_materials WHERE material_name = %s LIMIT 1", (old_name,))
            source = cursor.fetchone()
            
            if target and source:
                target_id = target['material_id']
                source_id = source['material_id']
                source_qty = source['quantity_available']
                
                # Combine quantities
                cursor.execute(
                    "UPDATE raw_materials SET quantity_available = quantity_available + %s WHERE material_id = %s",
                    (source_qty, target_id)
                )
                
                # Update any foreign keys in design_materials (if exists, wait, we don't have design_materials table, but maybe product_catalog has material_id)
                cursor.execute("""
                    SELECT count(*) as cnt FROM information_schema.columns 
                    WHERE table_schema = %s AND table_name = 'product_catalog' AND column_name = 'material_id'
                """, (os.getenv("DB_NAME", "heritage_handloom"),))
                if cursor.fetchone()['cnt'] > 0:
                    cursor.execute("UPDATE product_catalog SET material_id = %s WHERE material_id = %s", (target_id, source_id))
                
                # Delete the redundant material
                cursor.execute("DELETE FROM raw_materials WHERE material_id = %s", (source_id,))
                print(f"Merged '{old_name}' into '{new_name}' (added {source_qty} units).")

        conn.commit()
        print("Consolidation complete.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    consolidate()
