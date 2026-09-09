import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "heritage_handloom")
    )
    cursor = conn.cursor()
    
    queries = [
        "ALTER TABLE artisans ADD COLUMN image_file VARCHAR(255) DEFAULT 'default_artisan.jpg';",
        "ALTER TABLE traditional_designs ADD COLUMN image_file VARCHAR(255) DEFAULT 'default_design.jpg';",
        "ALTER TABLE raw_materials ADD COLUMN image_file VARCHAR(255) DEFAULT 'default_material.jpg';"
    ]
    
    for q in queries:
        try:
            cursor.execute(q)
            print(f"Executed: {q}")
        except mysql.connector.Error as err:
            print(f"Error on query {q}: {err}")
            
    conn.commit()
    cursor.close()
    conn.close()
    print("Database migration completed.")
except Exception as e:
    print(f"Connection error: {e}")
