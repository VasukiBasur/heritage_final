import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def fix_payouts():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "heritage_handloom")
    )
    cursor = conn.cursor()

    try:
        # Update existing zero or null payouts
        print("Fixing zero payouts...")
        cursor.execute("""
            UPDATE production_logs 
            SET payout_amount = (quantity * 850) 
            WHERE payout_amount = 0 OR payout_amount IS NULL
        """)
        conn.commit()
        print("Payouts fixed successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    fix_payouts()
