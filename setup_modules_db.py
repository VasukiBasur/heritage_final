import mysql.connector

def setup_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root@123',
        database='heritage_handloom'
    )
    cursor = conn.cursor()

    # 1. Create Suppliers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            supplier_id INT AUTO_INCREMENT PRIMARY KEY,
            supplier_name VARCHAR(100) NOT NULL,
            material_supplied VARCHAR(100) NOT NULL,
            cost DECIMAL(10,2) NOT NULL,
            delivery_dates VARCHAR(100) NOT NULL
        ) ENGINE=InnoDB;
    """)

    # 2. Create Product Catalog Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_catalog (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            stock_quantity INT DEFAULT 0
        ) ENGINE=InnoDB;
    """)

    # Add Dummy Suppliers
    cursor.execute("SELECT COUNT(*) FROM suppliers")
    if cursor.fetchone()[0] == 0:
        suppliers_data = [
            ('Silk Route Textiles', 'Mulberry Silk', 4500.00, 'Mondays & Thursdays'),
            ('Organic Dye Co.', 'Natural Indigo Dye', 1200.50, 'Every 15th of the month'),
            ('Deccan Cottons', 'Cotton Yarn', 850.00, 'Weekly (Wednesdays)')
        ]
        cursor.executemany("""
            INSERT INTO suppliers (supplier_name, material_supplied, cost, delivery_dates) 
            VALUES (%s, %s, %s, %s)
        """, suppliers_data)

    # Add Dummy Product Catalog
    cursor.execute("SELECT COUNT(*) FROM product_catalog")
    if cursor.fetchone()[0] == 0:
        catalog_data = [
            ('Mysore Royal Saree', 'Sarees', 12500.00, 45),
            ('Kashmiri Pashmina Shawl', 'Shawls', 18000.00, 12),
            ('Banarasi Zari Dupatta', 'Dupattas', 4500.00, 80),
            ('Navalgund Geometric Carpet', 'Carpets', 8500.00, 5)
        ]
        cursor.executemany("""
            INSERT INTO product_catalog (product_name, category, price, stock_quantity) 
            VALUES (%s, %s, %s, %s)
        """, catalog_data)

    # Add some production logs to test tracking if none exist
    cursor.execute("SELECT COUNT(*) FROM production_logs")
    if cursor.fetchone()[0] == 0:
        logs_data = [
            (1, 1, 'In Progress', '2026-05-01', 50, 'Dyeing'),
            (2, 2, 'In Progress', '2026-05-10', 20, 'Weaving'),
            (3, 3, 'In Progress', '2026-05-15', 30, 'Finishing')
        ]
        cursor.executemany("""
            INSERT INTO production_logs (artisan_id, design_id, status, start_date, quantity, supply_chain_stage) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, logs_data)
    else:
        # Update existing stages to match new enum requirements for demo
        cursor.execute("UPDATE production_logs SET supply_chain_stage = 'Weaving' WHERE supply_chain_stage = 'Ordered'")

    conn.commit()
    cursor.close()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_db()
