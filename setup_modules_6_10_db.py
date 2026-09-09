import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

cursor = db.cursor()

# Module 7: Customers
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    buyer_type ENUM('Retail', 'Wholesale', 'Exporter') DEFAULT 'Retail',
    location VARCHAR(255),
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Module 6: Orders
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    quantity INT,
    total_price DECIMAL(10, 2),
    status ENUM('Placed', 'Processing', 'Shipped', 'Delivered') DEFAULT 'Placed',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE SET NULL
)
''')

# Module 8: Inventory & Warehouse
cursor.execute('''
CREATE TABLE IF NOT EXISTS warehouse_inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    warehouse_location VARCHAR(255),
    stock_in INT DEFAULT 0,
    stock_out INT DEFAULT 0,
    damaged_stock INT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE
)
''')

# Module 9: Payment & Billing
cursor.execute('''
CREATE TABLE IF NOT EXISTS billing_payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    entity_type ENUM('Artisan', 'Supplier', 'Customer'),
    entity_id INT,
    amount DECIMAL(10, 2),
    payment_type ENUM('Wage', 'Invoice', 'Purchase'),
    status ENUM('Pending', 'Completed', 'Failed') DEFAULT 'Pending',
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Module 10: Logistics & Transportation
cursor.execute('''
CREATE TABLE IF NOT EXISTS logistics (
    shipment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    transport_agency VARCHAR(255),
    tracking_number VARCHAR(100),
    status ENUM('Dispatched', 'In Transit', 'Delivered', 'Delayed') DEFAULT 'Dispatched',
    estimated_delivery DATE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
)
''')

# Insert Seed Data for Customers
cursor.execute("SELECT COUNT(*) FROM customers")
if cursor.fetchone()[0] == 0:
    cursor.execute('''
    INSERT INTO customers (name, email, phone, buyer_type, location, feedback) VALUES 
    ('FabIndia', 'procurement@fabindia.com', '+91 9876543210', 'Wholesale', 'New Delhi, India', 'Consistent quality, minor delays in last batch.'),
    ('Ritu Kumar Designs', 'sourcing@ritukumar.com', '+91 9876543211', 'Wholesale', 'Mumbai, India', 'Excellent intricate work on the borders.'),
    ('Global Textiles Inc.', 'import@globaltextiles.us', '+1 555 123 4567', 'Exporter', 'New York, USA', 'Highly sought after in western markets.')
    ''')

# Insert Seed Data for Orders (assuming product_catalog has IDs 1, 2)
cursor.execute("SELECT COUNT(*) FROM orders")
if cursor.fetchone()[0] == 0:
    cursor.execute('''
    INSERT INTO orders (customer_id, product_id, quantity, total_price, status, delivery_date) VALUES 
    (1, 1, 50, 425000.00, 'Processing', '2026-06-15'),
    (3, 2, 100, 250000.00, 'Shipped', '2026-06-01')
    ''')

# Insert Seed Data for Warehouse Inventory
cursor.execute("SELECT COUNT(*) FROM warehouse_inventory")
if cursor.fetchone()[0] == 0:
    cursor.execute('''
    INSERT INTO warehouse_inventory (product_id, warehouse_location, stock_in, stock_out, damaged_stock) VALUES 
    (1, 'Central Warehouse - Hubli', 200, 50, 2),
    (2, 'Secondary Facility - Mysore', 500, 150, 5)
    ''')

# Insert Seed Data for Billing
cursor.execute("SELECT COUNT(*) FROM billing_payments")
if cursor.fetchone()[0] == 0:
    cursor.execute('''
    INSERT INTO billing_payments (entity_type, entity_id, amount, payment_type, status) VALUES 
    ('Customer', 1, 425000.00, 'Purchase', 'Pending'),
    ('Artisan', 1, 15000.00, 'Wage', 'Completed'),
    ('Supplier', 1, 45000.00, 'Invoice', 'Completed')
    ''')

# Insert Seed Data for Logistics
cursor.execute("SELECT COUNT(*) FROM logistics")
if cursor.fetchone()[0] == 0:
    cursor.execute('''
    INSERT INTO logistics (order_id, transport_agency, tracking_number, status, estimated_delivery) VALUES 
    (2, 'DHL International', 'DHL-78493021', 'In Transit', '2026-06-01')
    ''')

db.commit()
print("Database tables for Modules 6-10 created and seeded.")
