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
    
    query = "ALTER TABLE production_logs ADD COLUMN supply_chain_stage VARCHAR(50) DEFAULT 'Ordered';"
    try:
        cursor.execute(query)
        print("Successfully added supply_chain_stage column.")
    except mysql.connector.Error as err:
        if err.errno == 1060: # Duplicate column name
            print("Column supply_chain_stage already exists.")
        else:
            print(f"Error executing query: {err}")
            
    conn.commit()
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Connection error: {e}")
