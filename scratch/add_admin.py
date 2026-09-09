import os
import mysql.connector
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

conn = mysql.connector.connect(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME')
)
cursor = conn.cursor()

try:
    cursor.execute(
        "INSERT INTO users (role_id, email, password_hash, name, is_verified) VALUES (1, 'admin@example.com', %s, 'Super Admin', True)",
        (generate_password_hash('1234'),)
    )
    conn.commit()
    print("Admin user created")
except Exception as e:
    print("Admin user likely already exists or error:", e)

cursor.close()
conn.close()
