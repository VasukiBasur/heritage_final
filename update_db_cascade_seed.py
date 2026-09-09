import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def apply_db_fixes():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "heritage_handloom")
    )
    cursor = conn.cursor()

    try:
        # 1. Update Foreign Keys to CASCADE
        print("Updating foreign keys to CASCADE...")
        
        # We need to find the constraint names first to drop them
        # Let's just drop them by querying information_schema
        cursor.execute("""
            SELECT CONSTRAINT_NAME, TABLE_NAME 
            FROM information_schema.TABLE_CONSTRAINTS 
            WHERE CONSTRAINT_TYPE = 'FOREIGN KEY' 
            AND TABLE_SCHEMA = 'heritage_handloom'
        """)
        constraints = cursor.fetchall()
        for constraint_name, table_name in constraints:
            cursor.execute(f"ALTER TABLE {table_name} DROP FOREIGN KEY {constraint_name}")
            
        # Re-add production_logs constraints
        cursor.execute("""
            ALTER TABLE production_logs
            ADD CONSTRAINT fk_pl_artisan FOREIGN KEY (artisan_id) REFERENCES artisans(artisan_id) ON DELETE CASCADE,
            ADD CONSTRAINT fk_pl_design FOREIGN KEY (design_id) REFERENCES traditional_designs(design_id) ON DELETE CASCADE
        """)
        
        # Re-add design_materials constraints
        cursor.execute("""
            ALTER TABLE design_materials
            ADD CONSTRAINT fk_dm_design FOREIGN KEY (design_id) REFERENCES traditional_designs(design_id) ON DELETE CASCADE,
            ADD CONSTRAINT fk_dm_material FOREIGN KEY (material_id) REFERENCES raw_materials(material_id) ON DELETE CASCADE
        """)
        
        # Re-add production_audit constraints
        cursor.execute("""
            ALTER TABLE production_audit
            ADD CONSTRAINT fk_pa_log FOREIGN KEY (log_id) REFERENCES production_logs(log_id) ON DELETE CASCADE
        """)

        # 2. Seed Data
        print("Seeding more data...")
        
        # Seed 5 Artisans
        cursor.execute("""
            INSERT INTO artisans (name, location, contact_number, skill_level, skill_multiplier) VALUES
            ('Sunitha Reddy', 'Gadag', '9876543220', 'Master Weaver', 1.5),
            ('Abdul Kareem', 'Tumkur', '9876543221', 'Senior Artisan', 1.2),
            ('Savitri Bai', 'Hubli', '9876543222', 'Intermediate Weaver', 1.0),
            ('Mohan Das', 'Mangalore', '9876543223', 'Master Weaver', 1.5),
            ('Anita Desai', 'Belagavi', '9876543224', 'Apprentice', 0.8)
        """)
        
        # Seed 5 Raw Materials
        cursor.execute("""
            INSERT IGNORE INTO raw_materials (material_name, quantity_available) VALUES
            ('Premium Zari Thread', 100),
            ('Mulberry Silk', 250),
            ('Organic Cotton', 500),
            ('Natural Indigo Dye', 50),
            ('Eri Silk', 120)
        """)

        conn.commit()
        print("Database fixes and seeding completed successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    apply_db_fixes()
