import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def add_qr_code_column():
    try:
        conn = mysql.connector.connect(
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'heritage_handloom')
        )
        cursor = conn.cursor()
        
        # Check if qr_code column exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'product_catalog' 
            AND COLUMN_NAME = 'qr_code'
        """, (os.getenv('DB_NAME', 'heritage_handloom'),))
        
        if cursor.fetchone()[0] == 0:
            print("Adding qr_code column to product_catalog...")
            cursor.execute("ALTER TABLE product_catalog ADD COLUMN qr_code TEXT")
            conn.commit()
            print("Successfully added qr_code column.")
        else:
            print("qr_code column already exists.")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    add_qr_code_column()
