import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

def update_database():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "heritage_handloom")
    )
    cursor = conn.cursor()
    
    # 1. Create Users_Buyers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users_buyers (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('Admin', 'Buyer', 'Artisan') DEFAULT 'Buyer'
        )
    """)
    
    # Insert default admin user if not exists
    cursor.execute("SELECT * FROM users_buyers WHERE username='admin'")
    if not cursor.fetchone():
        hashed_pw = generate_password_hash('password123')
        cursor.execute("INSERT INTO users_buyers (username, password_hash, role) VALUES (%s, %s, %s)",
                       ('admin', hashed_pw, 'Admin'))
    
    # 2. Create Raw_Materials table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_materials (
            material_id INT AUTO_INCREMENT PRIMARY KEY,
            material_name VARCHAR(100) UNIQUE NOT NULL,
            quantity_available INT NOT NULL DEFAULT 0
        )
    """)
    
    # 3. Create design_materials mapping table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS design_materials (
            design_id INT,
            material_id INT,
            quantity_required_per_unit INT NOT NULL,
            PRIMARY KEY (design_id, material_id),
            FOREIGN KEY (design_id) REFERENCES traditional_designs(design_id),
            FOREIGN KEY (material_id) REFERENCES raw_materials(material_id)
        )
    """)
    
    # Insert raw materials and mappings if empty
    cursor.execute("SELECT COUNT(*) FROM raw_materials")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO raw_materials (material_name, quantity_available) VALUES ('Pure Gold Zari', 10), ('Silk Yarn', 50), ('Cotton Yarn', 20)")
        
        # design_id 1 is 'Mysore Silk Zari' - requires Silk Yarn (2) and Pure Gold Zari (1)
        # design_id 2 is 'Ilkal Checkered' - requires Cotton Yarn (3) and Silk Yarn (1)
        # design_id 3 is 'Udupi Cotton' - requires Cotton Yarn (4)
        # design_id 4 is 'Kasuti Embroidery' - requires Cotton Yarn (2)
        cursor.execute("""
            INSERT INTO design_materials (design_id, material_id, quantity_required_per_unit) VALUES 
            (1, 1, 1), -- Mysore Silk Zari needs 1 Pure Gold Zari
            (1, 2, 2), -- Mysore Silk Zari needs 2 Silk Yarn
            (2, 3, 3), -- Ilkal Checkered needs 3 Cotton Yarn
            (2, 2, 1), -- Ilkal Checkered needs 1 Silk Yarn
            (3, 3, 4), -- Udupi Cotton needs 4 Cotton Yarn
            (4, 3, 2)  -- Kasuti Embroidery needs 2 Cotton Yarn
        """)
        
    # 4. Create trigger
    trigger_sql = """
    CREATE TRIGGER check_raw_materials_before_insert
    BEFORE INSERT ON production_logs
    FOR EACH ROW
    BEGIN
        DECLARE done INT DEFAULT FALSE;
        DECLARE mat_id INT;
        DECLARE req_qty INT;
        DECLARE avail_qty INT;
        DECLARE mat_name VARCHAR(100);
        
        DECLARE cur CURSOR FOR 
            SELECT material_id, quantity_required_per_unit 
            FROM design_materials 
            WHERE design_id = NEW.design_id;
            
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
        
        OPEN cur;
        
        read_loop: LOOP
            FETCH cur INTO mat_id, req_qty;
            IF done THEN
                LEAVE read_loop;
            END IF;
            
            -- Calculate total required
            SET @total_req = req_qty * NEW.quantity;
            
            -- Get available quantity
            SELECT quantity_available, material_name INTO avail_qty, mat_name 
            FROM raw_materials 
            WHERE material_id = mat_id;
            
            IF avail_qty < @total_req THEN
                SET @msg = CONCAT('Insufficient ', mat_name, '. Required: ', @total_req, ', Available: ', avail_qty);
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = @msg;
            ELSE
                -- Optionally, deduct the materials (we will just deduct them here)
                UPDATE raw_materials 
                SET quantity_available = quantity_available - @total_req 
                WHERE material_id = mat_id;
            END IF;
        END LOOP;
        
        CLOSE cur;
    END
    """
    
    # Drop trigger if exists
    cursor.execute("DROP TRIGGER IF EXISTS check_raw_materials_before_insert")
    # Create trigger
    cursor.execute(trigger_sql)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Database schema successfully updated!")

if __name__ == "__main__":
    update_database()
