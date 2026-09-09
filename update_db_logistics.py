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
        "ALTER TABLE production_logs ADD COLUMN trade_type VARCHAR(50) DEFAULT 'Domestic';",
        "ALTER TABLE production_logs ADD COLUMN destination VARCHAR(100) DEFAULT 'Local Market';",
        "UPDATE production_logs SET trade_type = 'Export', destination = 'United States' WHERE log_id IN (1, 3);"
    ]
    
    for q in queries:
        try:
            cursor.execute(q)
            print(f"Executed: {q}")
        except mysql.connector.Error as err:
            if err.errno == 1060:
                print("Column already exists.")
            else:
                print(f"Error executing query {q}: {err}")
            
    conn.commit()
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Connection error: {e}")
