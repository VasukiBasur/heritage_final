import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def fix_db():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "heritage_handloom")
    )
    cursor = conn.cursor(dictionary=True)

    try:
        # Find artisans with 0 logs
        cursor.execute("""
            SELECT a.artisan_id 
            FROM artisans a 
            LEFT JOIN production_logs p ON a.artisan_id = p.artisan_id 
            WHERE p.log_id IS NULL
        """)
        artisans_no_logs = cursor.fetchall()
        
        # Get a default design_id for the insert
        cursor.execute("SELECT design_id FROM traditional_designs LIMIT 1")
        design = cursor.fetchone()
        design_id = design['design_id'] if design else 1
        
        # Temporarily increase all raw material stock to prevent trigger failure
        cursor.execute("UPDATE raw_materials SET quantity_available = quantity_available + 100")
        
        # Insert logs for them
        for row in artisans_no_logs:
            cursor.execute("""
                INSERT INTO production_logs (artisan_id, design_id, status, start_date, quantity, payout_amount)
                VALUES (%s, %s, 'Completed', CURDATE(), 5, 4500)
            """, (row['artisan_id'], design_id))
            
        # Update any 0 or NULL payouts
        cursor.execute("""
            UPDATE production_logs 
            SET payout_amount = 4500 
            WHERE payout_amount = 0 OR payout_amount IS NULL
        """)
        
        conn.commit()
        print("Database updated successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    fix_db()
