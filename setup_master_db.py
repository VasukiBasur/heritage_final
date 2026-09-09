import os
import json
import mysql.connector
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

load_dotenv()

def setup_master():
    print("=" * 60)
    print("Heritage Handloom - Master Database Setup & Seeding")
    print("=" * 60)

    from db_config import get_db_credentials
    creds = get_db_credentials()
    db_name = creds['database']

    print(f"Connecting to MySQL at {creds['host']}:{creds['port']} as {creds['user']}...")
    conn_kwargs = {
        'host': creds['host'],
        'port': creds['port'],
        'user': creds['user'],
        'password': creds['password']
    }
    ssl_ca = os.getenv("DB_SSL_CA")
    if ssl_ca and os.path.exists(ssl_ca):
        conn_kwargs['ssl_ca'] = ssl_ca
    elif os.getenv("DB_SSL", "").lower() in ("true", "1", "required"):
        conn_kwargs['ssl_disabled'] = False

    try:
        conn = mysql.connector.connect(**conn_kwargs)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cursor.execute(f"USE `{db_name}`;")
    except Exception:
        # If user has no permission to CREATE DATABASE (common on managed cloud DBs), connect directly
        conn_kwargs['database'] = db_name
        conn = mysql.connector.connect(**conn_kwargs)
        cursor = conn.cursor()

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

    # Drop any conflicting legacy tables if needed
    drop_tables = [
        "design_materials", "production_audit", "production_logs",
        "batch_materials", "provenance_ledger", "production_batches", "weavers", "retailers",
        "order_items", "logistics", "billing_payments", "warehouse_inventory", "orders",
        "product_catalog", "suppliers", "supplier_dispatches", "traditional_designs",
        "raw_materials", "artisans", "customers", "password_resets", "user_profiles", "users", "roles"
    ]
    for tbl in drop_tables:
        cursor.execute(f"DROP TABLE IF EXISTS {tbl};")

    cursor.execute("DROP VIEW IF EXISTS vw_Textile_Provenance;")
    cursor.execute("DROP PROCEDURE IF EXISTS Calculate_Artisan_Payout;")
    cursor.execute("DROP PROCEDURE IF EXISTS Generate_Lifecycle_Audit_Report;")
    cursor.execute("DROP TRIGGER IF EXISTS check_raw_materials_before_insert;")
    cursor.execute("DROP TRIGGER IF EXISTS after_production_log_update;")
    cursor.execute("DROP TRIGGER IF EXISTS after_batch_status_update;")

    print("Creating core schema...")

    # 1. Roles
    cursor.execute("""
    CREATE TABLE roles (
        role_id INT AUTO_INCREMENT PRIMARY KEY,
        role_name VARCHAR(50) UNIQUE NOT NULL
    ) ENGINE=InnoDB;
    """)

    # 2. Users
    cursor.execute("""
    CREATE TABLE users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        role_id INT NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        name VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    # 3. User Profiles
    cursor.execute("""
    CREATE TABLE user_profiles (
        profile_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        profile_data JSON,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    # 4. Password Resets
    cursor.execute("""
    CREATE TABLE password_resets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        reset_token VARCHAR(20) NOT NULL,
        expires_at DATETIME NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    # 5. Artisans
    cursor.execute("""
    CREATE TABLE artisans (
        artisan_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        location VARCHAR(100) NOT NULL,
        village VARCHAR(100) DEFAULT 'Harapanahalli',
        contact_number VARCHAR(20),
        skill_level VARCHAR(50) DEFAULT 'Master Weaver',
        skill_multiplier DECIMAL(3,2) DEFAULT 1.00,
        experience_years INT DEFAULT 10,
        wage_details VARCHAR(100) DEFAULT '₹800/day',
        image_file VARCHAR(255) DEFAULT 'sunitha.jpg'
    ) ENGINE=InnoDB;
    """)

    # 6. Traditional Designs
    cursor.execute("""
    CREATE TABLE traditional_designs (
        design_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        region_origin VARCHAR(100),
        complexity_rating INT DEFAULT 5,
        image_file VARCHAR(255) DEFAULT 'mysore_silk_zari.png.jpeg'
    ) ENGINE=InnoDB;
    """)

    # 7. Raw Materials
    cursor.execute("""
    CREATE TABLE raw_materials (
        material_id INT AUTO_INCREMENT PRIMARY KEY,
        material_name VARCHAR(100) UNIQUE NOT NULL,
        quantity_available INT NOT NULL DEFAULT 100,
        image_file VARCHAR(255) DEFAULT 'silk_yarn.png.jpeg'
    ) ENGINE=InnoDB;
    """)

    # 8. Design Materials (BOM)
    cursor.execute("""
    CREATE TABLE design_materials (
        design_id INT NOT NULL,
        material_id INT NOT NULL,
        quantity_required_per_unit INT NOT NULL DEFAULT 1,
        PRIMARY KEY (design_id, material_id),
        FOREIGN KEY (design_id) REFERENCES traditional_designs(design_id) ON DELETE CASCADE,
        FOREIGN KEY (material_id) REFERENCES raw_materials(material_id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    # 9. Production Logs
    cursor.execute("""
    CREATE TABLE production_logs (
        log_id INT AUTO_INCREMENT PRIMARY KEY,
        artisan_id INT NOT NULL,
        design_id INT NOT NULL,
        status VARCHAR(50) DEFAULT 'Active',
        start_date DATE NOT NULL,
        end_date DATE,
        quantity INT NOT NULL DEFAULT 1,
        payout_amount DECIMAL(10,2) DEFAULT 0.00,
        supply_chain_stage VARCHAR(50) DEFAULT 'Ordered',
        trade_type VARCHAR(50) DEFAULT 'Domestic',
        destination VARCHAR(100) DEFAULT 'Local Market',
        FOREIGN KEY (artisan_id) REFERENCES artisans(artisan_id) ON DELETE CASCADE,
        FOREIGN KEY (design_id) REFERENCES traditional_designs(design_id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    # 10. Production Audit
    cursor.execute("""
    CREATE TABLE production_audit (
        audit_id INT AUTO_INCREMENT PRIMARY KEY,
        log_id INT NOT NULL,
        old_status VARCHAR(50),
        new_status VARCHAR(50),
        change_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (log_id) REFERENCES production_logs(log_id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    # 11. Suppliers
    cursor.execute("""
    CREATE TABLE suppliers (
        supplier_id INT AUTO_INCREMENT PRIMARY KEY,
        supplier_name VARCHAR(150) NOT NULL,
        company_name VARCHAR(150),
        contact_person VARCHAR(100),
        phone VARCHAR(20),
        material_supplied VARCHAR(150),
        material_type VARCHAR(100),
        cost DECIMAL(10,2) DEFAULT 1200.00,
        delivery_dates VARCHAR(100) DEFAULT 'Weekly',
        rating DECIMAL(3,2) DEFAULT 4.8,
        status VARCHAR(50) DEFAULT 'Active',
        image_file VARCHAR(255)
    ) ENGINE=InnoDB;
    """)

    # 12. Product Catalog
    cursor.execute("""
    CREATE TABLE product_catalog (
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(200) NOT NULL,
        category VARCHAR(100) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        stock_quantity INT DEFAULT 25,
        artisan_id INT,
        material_id INT,
        image_url VARCHAR(255),
        status VARCHAR(50) DEFAULT 'In Stock',
        qr_code TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (artisan_id) REFERENCES artisans(artisan_id) ON DELETE SET NULL,
        FOREIGN KEY (material_id) REFERENCES raw_materials(material_id) ON DELETE SET NULL
    ) ENGINE=InnoDB;
    """)

    # 13. Customers
    cursor.execute("""
    CREATE TABLE customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(150) NOT NULL,
        email VARCHAR(150),
        phone VARCHAR(50),
        buyer_type VARCHAR(50) DEFAULT 'Retail',
        location VARCHAR(255),
        feedback TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """)

    # 14. Orders
    cursor.execute("""
    CREATE TABLE orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        product_id INT,
        customer_name VARCHAR(150),
        quantity INT DEFAULT 1,
        total_price DECIMAL(10,2),
        total_amount DECIMAL(10,2),
        status VARCHAR(50) DEFAULT 'Placed',
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        delivery_date DATE,
        shipping_address TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE SET NULL,
        FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE SET NULL
    ) ENGINE=InnoDB;
    """)

    # 15. Warehouse Inventory
    cursor.execute("""
    CREATE TABLE warehouse_inventory (
        inventory_id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT NOT NULL,
        warehouse_location VARCHAR(255) DEFAULT 'Bengaluru Central Hub',
        stock_in INT DEFAULT 0,
        stock_out INT DEFAULT 0,
        damaged_stock INT DEFAULT 0,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    # 16. Billing Payments
    cursor.execute("""
    CREATE TABLE billing_payments (
        payment_id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        entity_type VARCHAR(50) DEFAULT 'Artisan',
        entity_id INT,
        amount DECIMAL(10,2) NOT NULL,
        payment_type VARCHAR(50) DEFAULT 'Wage',
        payment_method VARCHAR(50) DEFAULT 'Bank Transfer',
        status VARCHAR(50) DEFAULT 'Completed',
        payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    # 17. Logistics
    cursor.execute("""
    CREATE TABLE logistics (
        shipment_id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        delivery_partner_id INT,
        transport_agency VARCHAR(255) DEFAULT 'Heritage Express Logistics',
        tracking_number VARCHAR(100) UNIQUE,
        current_status VARCHAR(50) DEFAULT 'In Transit',
        status VARCHAR(50) DEFAULT 'In Transit',
        route_gps JSON,
        estimated_delivery DATE,
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
        FOREIGN KEY (delivery_partner_id) REFERENCES users(user_id) ON DELETE SET NULL
    ) ENGINE=InnoDB;
    """)

    # 18. Supplier Dispatches
    cursor.execute("""
    CREATE TABLE supplier_dispatches (
        dispatch_id INT AUTO_INCREMENT PRIMARY KEY,
        hub_name VARCHAR(150) NOT NULL,
        dispatch_date DATE NOT NULL,
        dispatch_time TIME NOT NULL,
        fleet_assigned VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """)

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    print("Schema created successfully!")

    # ----------------------------------------------------
    # Advanced DBMS Features: Triggers, Procedure, View
    # ----------------------------------------------------
    print("Creating Triggers, Stored Procedure & View...")

    # Trigger 1: Deduct raw materials before insert on production_logs
    cursor.execute("""
    CREATE TRIGGER check_raw_materials_before_insert
    BEFORE INSERT ON production_logs
    FOR EACH ROW
    BEGIN
        DECLARE done INT DEFAULT FALSE;
        DECLARE v_mat_id INT;
        DECLARE v_req_per_unit INT;
        DECLARE v_avail INT;
        DECLARE v_mat_name VARCHAR(100);
        DECLARE v_total_needed INT;
        
        DECLARE cur CURSOR FOR
            SELECT dm.material_id, dm.quantity_required_per_unit, rm.quantity_available, rm.material_name
            FROM design_materials dm
            JOIN raw_materials rm ON dm.material_id = rm.material_id
            WHERE dm.design_id = NEW.design_id;
            
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
        
        OPEN cur;
        check_loop: LOOP
            FETCH cur INTO v_mat_id, v_req_per_unit, v_avail, v_mat_name;
            IF done THEN
                LEAVE check_loop;
            END IF;
            
            SET v_total_needed = v_req_per_unit * NEW.quantity;
            IF v_avail < v_total_needed THEN
                SET @err_msg = CONCAT('Insufficient ', v_mat_name, '. Required: ', v_total_needed, ', Available: ', v_avail);
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = @err_msg;
            ELSE
                UPDATE raw_materials
                SET quantity_available = quantity_available - v_total_needed
                WHERE material_id = v_mat_id;
            END IF;
        END LOOP;
        CLOSE cur;
    END;
    """)

    # Trigger 2: After update audit log
    cursor.execute("""
    CREATE TRIGGER after_production_log_update
    AFTER UPDATE ON production_logs
    FOR EACH ROW
    BEGIN
        IF OLD.status != NEW.status THEN
            INSERT INTO production_audit (log_id, old_status, new_status)
            VALUES (NEW.log_id, OLD.status, NEW.status);
        END IF;
    END;
    """)

    # Stored Procedure: Calculate Artisan Payout
    cursor.execute("""
    CREATE PROCEDURE Calculate_Artisan_Payout(IN p_log_id INT)
    BEGIN
        DECLARE v_qty INT;
        DECLARE v_complexity INT;
        DECLARE v_multiplier DECIMAL(3,2);
        DECLARE v_payout DECIMAL(10,2);
        
        SELECT pl.quantity, td.complexity_rating, a.skill_multiplier
        INTO v_qty, v_complexity, v_multiplier
        FROM production_logs pl
        JOIN traditional_designs td ON pl.design_id = td.design_id
        JOIN artisans a ON pl.artisan_id = a.artisan_id
        WHERE pl.log_id = p_log_id;
        
        -- Formula: (quantity * 100) * (complexity_rating / 10.0) * skill_multiplier
        SET v_payout = (v_qty * 100) * (v_complexity / 10.0) * v_multiplier;
        
        UPDATE production_logs
        SET payout_amount = v_payout
        WHERE log_id = p_log_id;
    END;
    """)

    # View: Provenance report
    cursor.execute("""
    CREATE VIEW vw_Textile_Provenance AS
    SELECT 
        pl.log_id,
        a.name AS artisan_name,
        td.name AS design_name,
        td.region_origin,
        pl.status,
        pl.supply_chain_stage,
        GROUP_CONCAT(rm.material_name SEPARATOR ', ') AS materials_used
    FROM production_logs pl
    JOIN artisans a ON pl.artisan_id = a.artisan_id
    JOIN traditional_designs td ON pl.design_id = td.design_id
    LEFT JOIN design_materials dm ON td.design_id = dm.design_id
    LEFT JOIN raw_materials rm ON dm.material_id = rm.material_id
    GROUP BY pl.log_id;
    """)

    print("Pillars and advanced DBMS objects created successfully!")

    # ----------------------------------------------------
    # Seeding Data
    # ----------------------------------------------------
    print("Seeding core roles & user accounts...")

    roles_data = [
        (1, 'Admin'),
        (2, 'Weaver'),
        (3, 'Supplier'),
        (4, 'Customer'),
        (5, 'Delivery Partner')
    ]
    cursor.executemany("INSERT INTO roles (role_id, role_name) VALUES (%s, %s)", roles_data)

    password_hash = generate_password_hash('1234')

    users_data = [
        (1, 1, 'admin@example.com', password_hash, 'Super Admin'),
        (2, 2, 'artisan@example.com', password_hash, 'Sunitha Weaver'),
        (3, 3, 'supplier@example.com', password_hash, 'Karnataka Silk Hub'),
        (4, 4, 'customer@example.com', password_hash, 'Pooja Hegde'),
        (5, 5, 'delivery@example.com', password_hash, 'Raju Express')
    ]
    cursor.executemany(
        "INSERT INTO users (user_id, role_id, email, password_hash, name) VALUES (%s, %s, %s, %s, %s)",
        users_data
    )

    user_profiles_data = [
        (1, json.dumps({"title": "Lead ERP Administrator", "access": "Full"})),
        (2, json.dumps({"village": "Gadag", "skill_type": "Master Weaver", "aadhaar": "987654321012"})),
        (3, json.dumps({"company_name": "Silk Threads Ltd", "gst": "29ABCDE1234F1Z5"})),
        (4, json.dumps({"address": "45 MG Road, Indiranagar, Bengaluru, Karnataka"})),
        (5, json.dumps({"vehicle_type": "Light Commercial Van", "vehicle_reg": "KA-01-MJ-8822"}))
    ]
    cursor.executemany("INSERT INTO user_profiles (user_id, profile_data) VALUES (%s, %s)", user_profiles_data)

    print("Seeding artisans...")
    artisans_data = [
        (1, 'Sunitha Reddy', 'Gadag', 'Gadag', '9876543220', 'Master Weaver', 1.50, 15, '₹1,200/day', 'sunitha.jpg'),
        (2, 'Abdul Kareem', 'Tumkur', 'Tumkur Cluster', '9876543221', 'Senior Artisan', 1.30, 12, '₹1,000/day', 'kareem.jpg'),
        (3, 'Savitri Bai', 'Hubli', 'Navalgund', '9876543222', 'Intermediate Weaver', 1.10, 8, '₹850/day', 'savitri.jpg'),
        (4, 'Mohan Das', 'Mangalore', 'Udupi', '9876543223', 'Master Weaver', 1.50, 18, '₹1,250/day', 'mohan2.jpg'),
        (5, 'Anita Desai', 'Belagavi', 'Ilkal', '9876543224', 'Apprentice', 0.80, 3, '₹650/day', 'anitha.webp'),
        (6, 'Ramesh Kumar', 'Shivamogga', 'Harapanahalli', '9876543210', 'Master Weaver', 1.40, 14, '₹1,100/day', 'nangunda.jpg')
    ]
    cursor.executemany("""
        INSERT INTO artisans (artisan_id, name, location, village, contact_number, skill_level, skill_multiplier, experience_years, wage_details, image_file)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, artisans_data)

    print("Seeding traditional designs...")
    designs_data = [
        (1, 'Mysore Silk Zari', 'Authentic royal Mysore silk saree with pure gold zari borders and pallu.', 'Mysore', 9, 'mysore_silk_zari.png.jpeg'),
        (2, 'Ilkal Checkered', 'Traditional cotton-silk blend saree with red kasuti border and signature topeni pallu.', 'Ilkal', 7, 'ilkal_checkered.png.jpeg'),
        (3, 'Udupi Cotton Saree', 'Fine 80s count handspun combed cotton saree with vibrant temple borders.', 'Udupi', 6, 'dharwad_cotton_saree.png.jpeg'),
        (4, 'Kasuti Folk Embroidery', 'Intricate historical geometric motifs embroidered using the sacred Ilkal style.', 'Dharwad', 8, 'kasturi_embroidery.png.jpeg'),
        (5, 'Kanchipuram Silk Bridal', 'Heavy pure mulberry silk woven with pure twisted gold and silver zari threads.', 'Kanchipuram', 10, 'kanchipuram_silk_saree.png.jpeg'),
        (6, 'Banarasi Royal Brocade', 'Opulent silk brocade embedded with floral jals and antique Mughal jaal motifs.', 'Varanasi', 9, 'banarasi_brocode_saree.png.jpeg')
    ]
    cursor.executemany("""
        INSERT INTO traditional_designs (design_id, name, description, region_origin, complexity_rating, image_file)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, designs_data)

    print("Seeding raw materials...")
    materials_data = [
        (1, 'Pure Gold Zari', 250, 'pure_gold_zari.png.jpeg'),
        (2, 'Mulberry Silk Yarn', 500, 'mulberry_silk.png.jpeg'),
        (3, 'Organic Cotton Yarn', 800, 'organic_cotton_yarn.png.jpeg'),
        (4, 'Natural Indigo Dye', 180, 'natural_indigo_dye.png.jpeg'),
        (5, 'Eri Wild Silk', 350, 'eri_silk.png.jpeg'),
        (6, 'Madder Root Dye', 120, 'madder_root_dye.png.jpeg')
    ]
    cursor.executemany("""
        INSERT INTO raw_materials (material_id, material_name, quantity_available, image_file)
        VALUES (%s, %s, %s, %s)
    """, materials_data)

    print("Seeding design bill of materials...")
    design_materials_data = [
        (1, 1, 1), # Mysore Silk needs 1 Pure Gold Zari
        (1, 2, 2), # Mysore Silk needs 2 Mulberry Silk
        (2, 3, 3), # Ilkal needs 3 Cotton
        (2, 2, 1), # Ilkal needs 1 Silk
        (3, 3, 4), # Udupi Cotton needs 4 Cotton
        (4, 3, 2), # Kasuti needs 2 Cotton
        (4, 4, 1), # Kasuti needs 1 Indigo Dye
        (5, 1, 2), # Kanchipuram needs 2 Gold Zari
        (5, 2, 3), # Kanchipuram needs 3 Silk
        (6, 1, 2), # Banarasi needs 2 Gold Zari
        (6, 2, 3)  # Banarasi needs 3 Silk
    ]
    cursor.executemany("""
        INSERT INTO design_materials (design_id, material_id, quantity_required_per_unit)
        VALUES (%s, %s, %s)
    """, design_materials_data)

    print("Seeding production logs...")
    logs_data = [
        (1, 1, 1, 'Completed', '2026-04-01', '2026-04-18', 5, 6750.00, 'Retail', 'Export', 'United States'),
        (2, 2, 1, 'Active', '2026-05-10', None, 3, 3510.00, 'Manufacturing', 'Domestic', 'Bengaluru'),
        (3, 3, 2, 'Completed', '2026-03-15', '2026-03-28', 8, 6160.00, 'Distribution', 'Export', 'United Kingdom'),
        (4, 4, 3, 'Active', '2026-05-12', None, 6, 5400.00, 'Raw_Material_Supply', 'Domestic', 'Chennai'),
        (5, 5, 4, 'Active', '2026-05-02', None, 4, 2560.00, 'Manufacturing', 'Domestic', 'Mumbai'),
        (6, 6, 5, 'Completed', '2026-04-20', '2026-05-05', 4, 5600.00, 'Sold', 'Domestic', 'Delhi')
    ]
    cursor.executemany("""
        INSERT INTO production_logs (log_id, artisan_id, design_id, status, start_date, end_date, quantity, payout_amount, supply_chain_stage, trade_type, destination)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, logs_data)

    print("Seeding suppliers...")
    suppliers_data = [
        (1, 'Silk Route Textiles', 'Silk Route Textiles Pvt Ltd', 'Anand Kumar', '+91 9845012345', 'Mulberry Silk Yarn', 'Silk', 4500.00, 'Mondays & Thursdays', 4.9, 'Active', 'silk_yarn.png.jpeg'),
        (2, 'Organic Dye Co.', 'Organic Natural Dyes LLP', 'Priya Rao', '+91 9845023456', 'Natural Indigo Dye', 'Natural Dye', 1200.50, 'Every 15th of the month', 4.8, 'Active', 'natural_indigo_dye.png.jpeg'),
        (3, 'Deccan Cottons', 'Deccan Organic Cottons', 'Venkatesh Murthy', '+91 9845034567', 'Organic Cotton Yarn', 'Cotton', 850.00, 'Weekly Wednesdays', 4.7, 'Active', 'organic_cotton_yarn.png.jpeg'),
        (4, 'Surat Zari Mills', 'Surat Gold Thread Co.', 'Rajesh Patel', '+91 9845045678', 'Pure Gold Zari', 'Zari', 8500.00, 'Bi-Weekly', 5.0, 'Active', 'pure_gold_zari.png.jpeg')
    ]
    cursor.executemany("""
        INSERT INTO suppliers (supplier_id, supplier_name, company_name, contact_person, phone, material_supplied, material_type, cost, delivery_dates, rating, status, image_file)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, suppliers_data)

    print("Seeding product catalog...")
    catalog_data = [
        (1, 'Royal Mysore Silk Saree', 'Sarees', 18500.00, 25, 1, 1, 'images/mysore_silk_zari.png.jpeg', 'In Stock', 'AUTH-MYS-1001'),
        (2, 'Ilkal Traditional Saree', 'Sarees', 7800.00, 40, 2, 2, 'images/ilkal_checkered.png.jpeg', 'In Stock', 'AUTH-ILK-1002'),
        (3, 'Udupi Handspun Cotton Saree', 'Sarees', 4200.00, 60, 4, 3, 'images/dharwad_cotton_saree.png.jpeg', 'In Stock', 'AUTH-UDP-1003'),
        (4, 'Banarasi Gold Brocade Saree', 'Sarees', 24500.00, 15, 6, 1, 'images/banarasi_brocode_saree.png.jpeg', 'In Stock', 'AUTH-BAN-1004'),
        (5, 'Pure Silk Wedding Dhoti', 'Dhotis', 3800.00, 50, 1, 2, 'images/dhoti.png', 'In Stock', 'AUTH-DHO-1005'),
        (6, 'Kasuti Folk Embroidered Shawl', 'Shawls', 5500.00, 30, 5, 4, 'images/kasturi_embroidery.png.jpeg', 'In Stock', 'AUTH-KAS-1006')
    ]
    cursor.executemany("""
        INSERT INTO product_catalog (product_id, product_name, category, price, stock_quantity, artisan_id, material_id, image_url, status, qr_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, catalog_data)

    print("Seeding customers...")
    customers_data = [
        (1, 'FabIndia Procurement', 'procurement@fabindia.com', '+91 9876543210', 'Wholesale', 'New Delhi, India', 'Excellent consistency and quality in traditional weaves.'),
        (2, 'Ritu Kumar Sourcing', 'sourcing@ritukumar.com', '+91 9876543211', 'Wholesale', 'Mumbai, India', 'Impeccable zari work on the pallu.'),
        (3, 'Global Textiles Inc.', 'import@globaltextiles.us', '+1 555 123 4567', 'Exporter', 'New York, USA', 'High customer demand for authentic artisan products.'),
        (4, 'Pooja Hegde', 'customer@example.com', '+91 9845099887', 'Retail', 'Bengaluru, India', 'Loved the fast shipping and authentic handloom tag.')
    ]
    cursor.executemany("""
        INSERT INTO customers (customer_id, name, email, phone, buyer_type, location, feedback)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, customers_data)

    print("Seeding orders...")
    orders_data = [
        (1, 1, 1, 'FabIndia Procurement', 10, 185000.00, 185000.00, 'Delivered', '2026-04-10', 'Connaught Place, New Delhi'),
        (2, 2, 2, 'Ritu Kumar Sourcing', 5, 39000.00, 39000.00, 'Shipped', '2026-05-18', 'Lower Parel, Mumbai'),
        (3, 4, 1, 'Pooja Hegde', 1, 18500.00, 18500.00, 'Processing', '2026-05-25', '45 MG Road, Indiranagar, Bengaluru'),
        (4, 3, 4, 'Global Textiles Inc.', 8, 196000.00, 196000.00, 'Placed', '2026-06-02', '5th Avenue Warehouse, New York, USA')
    ]
    cursor.executemany("""
        INSERT INTO orders (order_id, customer_id, product_id, customer_name, quantity, total_price, total_amount, status, delivery_date, shipping_address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, orders_data)

    print("Seeding warehouse inventory...")
    inventory_data = [
        (1, 'Bengaluru Central Hub', 100, 15, 0),
        (2, 'Mysuru Regional Depot', 80, 20, 1),
        (3, 'Hubli Distribution Centre', 120, 45, 2),
        (4, 'Varanasi Weave Center', 60, 10, 0),
        (5, 'Bengaluru Central Hub', 150, 25, 1),
        (6, 'Dharwad Depot', 75, 12, 0)
    ]
    cursor.executemany("""
        INSERT INTO warehouse_inventory (product_id, warehouse_location, stock_in, stock_out, damaged_stock)
        VALUES (%s, %s, %s, %s, %s)
    """, inventory_data)

    print("Seeding billing & payments...")
    payments_data = [
        (1, 'Customer', 1, 185000.00, 'Purchase', 'NEFT Bank Transfer', 'Completed'),
        (2, 'Customer', 2, 39000.00, 'Purchase', 'Razorpay Gateway', 'Completed'),
        (3, 'Customer', 4, 18500.00, 'Purchase', 'UPI / Card', 'Completed'),
        (1, 'Artisan', 1, 6750.00, 'Wage', 'Direct Bank Payout', 'Completed'),
        (3, 'Artisan', 3, 6160.00, 'Wage', 'Direct Bank Payout', 'Completed')
    ]
    cursor.executemany("""
        INSERT INTO billing_payments (order_id, entity_type, entity_id, amount, payment_type, payment_method, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, payments_data)

    print("Seeding logistics & shipments...")
    logistics_data = [
        (1, 5, 'BlueDart Express', 'BD-88992211', 'Delivered', 'Delivered', json.dumps({"origin": "Mysore", "current": "Delhi", "lat": 28.6139, "lng": 77.2090}), '2026-04-10'),
        (2, 5, 'Heritage Logistics Fleet', 'HL-55229910', 'In Transit', 'In Transit', json.dumps({"origin": "Ilkal", "current": "Pune", "lat": 18.5204, "lng": 73.8567}), '2026-05-18'),
        (3, 5, 'Delhivery Air', 'DL-33118800', 'In Transit', 'In Transit', json.dumps({"origin": "Mysore", "current": "Bengaluru Hub", "lat": 12.9716, "lng": 77.5946}), '2026-05-25')
    ]
    cursor.executemany("""
        INSERT INTO logistics (order_id, delivery_partner_id, transport_agency, tracking_number, current_status, status, route_gps, estimated_delivery)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, logistics_data)

    print("Seeding supplier dispatches...")
    dispatches_data = [
        ('Bengaluru Central Hub', '2026-05-20', '08:30:00', 'KA-01-TR-4421'),
        ('Mysuru Weave Cluster', '2026-05-22', '10:00:00', 'KA-09-EX-1199'),
        ('Ilkal Logistics Point', '2026-05-25', '07:45:00', 'KA-29-MH-7733')
    ]
    cursor.executemany("""
        INSERT INTO supplier_dispatches (hub_name, dispatch_date, dispatch_time, fleet_assigned)
        VALUES (%s, %s, %s, %s)
    """, dispatches_data)

    conn.commit()
    cursor.close()
    conn.close()

    print("=" * 60)
    print("SUCCESS: All 18 tables, triggers, procedure, view & seed data populated!")
    print("=" * 60)

if __name__ == '__main__':
    setup_master()
