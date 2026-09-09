import os
import mysql.connector
import json
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

conn = mysql.connector.connect(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME')
)
cursor = conn.cursor(dictionary=True)

test_users = [
    {
        "role_name": "Weaver",
        "email": "artisan@example.com",
        "name": "Test Artisan",
        "profile": {"village": "Ilkal", "skill_type": "Master Weaver", "aadhaar": "123456789012"}
    },
    {
        "role_name": "Supplier",
        "email": "supplier@example.com",
        "name": "Test Supplier",
        "profile": {"company_name": "Silk Threads Ltd", "gst": "29ABCDE1234F1Z5"}
    },
    {
        "role_name": "Customer",
        "email": "customer@example.com",
        "name": "Test Customer",
        "profile": {"address": "123 MG Road, Bangalore"}
    },
    {
        "role_name": "Delivery Partner",
        "email": "delivery@example.com",
        "name": "Test Driver",
        "profile": {"vehicle_type": "Light Truck", "vehicle_reg": "KA-01-AB-1234"}
    }
]

password_hash = generate_password_hash('1234')

for u in test_users:
    cursor.execute("SELECT role_id FROM roles WHERE role_name = %s", (u["role_name"],))
    role = cursor.fetchone()
    if role:
        try:
            cursor.execute(
                "INSERT INTO users (role_id, email, password_hash, name, is_verified) VALUES (%s, %s, %s, %s, True)",
                (role['role_id'], u["email"], password_hash, u["name"])
            )
            user_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO user_profiles (user_id, profile_data) VALUES (%s, %s)",
                (user_id, json.dumps(u["profile"]))
            )
            print(f"Created {u['role_name']}: {u['email']}")
        except Exception as e:
            print(f"Skipping {u['email']} (likely already exists)")

conn.commit()
cursor.close()
conn.close()
print("Seeding complete.")
