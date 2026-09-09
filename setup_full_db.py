import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def init_db():
    try:
        conn = mysql.connector.connect(
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'heritage_handloom')
        )
        cursor = conn.cursor()

        queries = [
            """
            CREATE TABLE IF NOT EXISTS suppliers (
                supplier_id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(150) NOT NULL,
                contact_person VARCHAR(100),
                phone VARCHAR(20),
                material_type VARCHAR(100),
                rating DECIMAL(3,2) DEFAULT 4.5,
                status ENUM('Active', 'Inactive') DEFAULT 'Active'
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS product_catalog (
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                product_name VARCHAR(200) NOT NULL,
                category VARCHAR(100) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                stock_quantity INT DEFAULT 0,
                artisan_id INT,
                image_url VARCHAR(255),
                status ENUM('In Stock', 'Low Stock', 'Out of Stock') DEFAULT 'In Stock',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artisan_id) REFERENCES artisans(artisan_id) ON DELETE SET NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name VARCHAR(150),
                total_amount DECIMAL(12,2) NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status ENUM('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled') DEFAULT 'Pending',
                shipping_address TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                price_at_purchase DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS billing_payments (
                payment_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                amount DECIMAL(12,2) NOT NULL,
                payment_method VARCHAR(50),
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                transaction_status ENUM('Pending', 'Completed', 'Failed', 'Refunded') DEFAULT 'Pending',
                FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS logistics (
                shipment_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                delivery_partner_id INT,
                current_status ENUM('In Transit', 'Out for Delivery', 'Delivered', 'Delayed') DEFAULT 'In Transit',
                route_gps JSON,
                estimated_delivery DATE,
                FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
                FOREIGN KEY (delivery_partner_id) REFERENCES users(user_id) ON DELETE SET NULL
            )
            """
        ]

        print("Executing schema creation...")
        for q in queries:
            cursor.execute(q)
            
        conn.commit()

        # Insert some mock data for suppliers and products if empty
        cursor.execute("SELECT COUNT(*) FROM suppliers")
        if cursor.fetchone()[0] == 0:
            print("Seeding suppliers...")
            cursor.execute("""
                INSERT INTO suppliers (company_name, contact_person, phone, material_type) VALUES
                ('Mysore Silk Board', 'Srinivas', '9876543210', 'Pure Silk Yarn'),
                ('Deccan Cottons', 'Karthik', '9876543211', 'Organic Cotton'),
                ('Zari Traders', 'Ramesh', '9876543212', 'Gold Zari')
            """)
            
        cursor.execute("SELECT COUNT(*) FROM product_catalog")
        if cursor.fetchone()[0] == 0:
            print("Seeding products...")
            cursor.execute("""
                INSERT INTO product_catalog (product_name, category, price, stock_quantity, artisan_id, status) VALUES
                ('Royal Mysore Silk Saree', 'Saree', 15000.00, 45, 1, 'In Stock'),
                ('Ilkal Traditional Checkered', 'Saree', 8500.00, 12, 3, 'Low Stock'),
                ('Kasuti Embroidery Shawl', 'Shawl', 4500.00, 0, 5, 'Out of Stock')
            """)
            
        cursor.execute("SELECT COUNT(*) FROM orders")
        if cursor.fetchone()[0] == 0:
            print("Seeding orders...")
            cursor.execute("""
                INSERT INTO orders (customer_name, total_amount, status) VALUES
                ('Arjun Reddy', 15000.00, 'Processing'),
                ('Priya Sharma', 8500.00, 'Shipped'),
                ('Kavya Gowda', 4500.00, 'Delivered')
            """)
            
        conn.commit()
        print("Database expansion complete!")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    init_db()
