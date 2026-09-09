import mysql.connector

conn = mysql.connector.connect(user='root', password='root@123', host='localhost', database='heritage_handloom')
cursor = conn.cursor(dictionary=True)

# 1. Update foreign key to ON UPDATE CASCADE
try:
    cursor.execute('ALTER TABLE production_logs DROP FOREIGN KEY fk_pl_artisan')
    cursor.execute('ALTER TABLE production_logs ADD CONSTRAINT fk_pl_artisan FOREIGN KEY (artisan_id) REFERENCES artisans(artisan_id) ON UPDATE CASCADE ON DELETE CASCADE')
    conn.commit()
except Exception as e:
    print("FK alter failed (might already be cascaded):", e)

# 2. Get all artisans ordered by name
cursor.execute("SELECT artisan_id, name FROM artisans ORDER BY name ASC")
artisans = cursor.fetchall()

# 3. Shift all IDs to high numbers to avoid collisions
for a in artisans:
    shifted_id = a['artisan_id'] + 10000
    cursor.execute("UPDATE product_catalog SET artisan_id = %s WHERE artisan_id = %s", (shifted_id, a['artisan_id']))
    cursor.execute("UPDATE artisans SET artisan_id = %s WHERE artisan_id = %s", (shifted_id, a['artisan_id']))
conn.commit()

# 4. Update IDs to 1, 2, 3... in alphabetical order
new_id = 1
for a in artisans:
    shifted_id = a['artisan_id'] + 10000
    cursor.execute("UPDATE product_catalog SET artisan_id = %s WHERE artisan_id = %s", (new_id, shifted_id))
    cursor.execute("UPDATE artisans SET artisan_id = %s WHERE artisan_id = %s", (new_id, shifted_id))
    new_id += 1
conn.commit()

# 5. Reset auto increment
cursor.execute(f"ALTER TABLE artisans AUTO_INCREMENT = {new_id}")
conn.commit()

cursor.close()
conn.close()
print("Artisan IDs reordered successfully.")
