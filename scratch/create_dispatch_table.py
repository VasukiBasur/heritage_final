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
    
    # Create the table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS supplier_dispatches (
        dispatch_id INT AUTO_INCREMENT PRIMARY KEY,
        hub_name VARCHAR(255) NOT NULL,
        dispatch_date DATE NOT NULL,
        dispatch_time VARCHAR(20) NOT NULL,
        fleet_assigned VARCHAR(100) NOT NULL,
        status VARCHAR(50) DEFAULT 'Scheduled',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("Successfully created supplier_dispatches table.")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
