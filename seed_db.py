import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def execute_sql_file(filename):
    # Connect without specifying database first to create it
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "")
    )
    cursor = conn.cursor()
    
    with open(filename, 'r') as f:
        sql_file = f.read()
        
    # Split the file by statements
    sql_commands = sql_file.split(';')
    
    for command in sql_commands:
        try:
            if command.strip():
                cursor.execute(command)
                print(f"Executed: {command.strip()[:50]}...")
        except mysql.connector.Error as err:
            print(f"Error executing command: {err}")
            print(f"Command was: {command.strip()}")
            
    conn.commit()
    cursor.close()
    conn.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    execute_sql_file('seed_data.sql')
