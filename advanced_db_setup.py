import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def setup_advanced_db():
    print("Connecting to the existing configured database...")
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "heritage_handloom")
        )
        cursor = conn.cursor()
        
        # Disable foreign key checks temporarily to allow clean recreation
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # 1. Core Normalized Schema
        print("Creating Core Normalized Schema...")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Weavers (
                weaver_id VARCHAR(20) PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                geo_location VARCHAR(150) NOT NULL,
                skill_level ENUM('Apprentice', 'Intermediate', 'Senior', 'Master') DEFAULT 'Intermediate',
                contact_number VARCHAR(15),
                joined_date DATE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Raw_Materials (
                material_id VARCHAR(20) PRIMARY KEY,
                material_name VARCHAR(100) NOT NULL,
                origin_region VARCHAR(100) NOT NULL,
                current_stock DECIMAL(10,2) NOT NULL DEFAULT 0.00 CHECK (current_stock >= 0),
                unit_of_measure VARCHAR(10) NOT NULL,
                last_restocked_date DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Retailers (
                retailer_id VARCHAR(20) PRIMARY KEY,
                retailer_name VARCHAR(100) NOT NULL,
                store_location VARCHAR(150) NOT NULL,
                contact_email VARCHAR(100) UNIQUE
            ) ENGINE=InnoDB;
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Production_Batches (
                batch_id VARCHAR(50) PRIMARY KEY,
                weaver_id VARCHAR(20) NOT NULL,
                design_name VARCHAR(100) NOT NULL,
                start_date DATE NOT NULL,
                expected_completion_date DATE,
                status ENUM('Planned', 'In Production', 'Quality Check', 'Shipped', 'Delivered') DEFAULT 'Planned',
                quantity_produced INT NOT NULL CHECK (quantity_produced > 0),
                FOREIGN KEY (weaver_id) REFERENCES Weavers(weaver_id) ON UPDATE CASCADE
            ) ENGINE=InnoDB;
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Batch_Materials (
                batch_id VARCHAR(50) NOT NULL,
                material_id VARCHAR(20) NOT NULL,
                quantity_required DECIMAL(10,2) NOT NULL CHECK (quantity_required > 0),
                PRIMARY KEY (batch_id, material_id),
                FOREIGN KEY (batch_id) REFERENCES Production_Batches(batch_id) ON DELETE CASCADE,
                FOREIGN KEY (material_id) REFERENCES Raw_Materials(material_id) ON UPDATE CASCADE
            ) ENGINE=InnoDB;
        """)
        
        # 2. Provenance & Traceability Ledger
        print("Creating Provenance & Traceability Ledger...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Provenance_Ledger (
                ledger_id INT AUTO_INCREMENT PRIMARY KEY,
                batch_id VARCHAR(50) NOT NULL,
                event_type ENUM(
                    'Materials Sourced', 
                    'Loom Prepared', 
                    'Weaving Started', 
                    'Quality Verified', 
                    'Shipped to Retailer', 
                    'Sold to Consumer'
                ) NOT NULL,
                event_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                location VARCHAR(150) NOT NULL,
                actor_id VARCHAR(20) NOT NULL,
                authenticity_hash VARCHAR(64) UNIQUE,
                remarks TEXT,
                FOREIGN KEY (batch_id) REFERENCES Production_Batches(batch_id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
        """)
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        # 3. Automated Business Logic (Triggers & Procedures)
        print("Setting up Automated Business Logic...")
        
        # Trigger
        print("  -> Creating Trigger: after_batch_status_update")
        cursor.execute("DROP TRIGGER IF EXISTS after_batch_status_update;")
        cursor.execute("""
            CREATE TRIGGER after_batch_status_update
            AFTER UPDATE ON Production_Batches
            FOR EACH ROW
            BEGIN
                IF NEW.status = 'In Production' AND OLD.status != 'In Production' THEN
                    
                    -- Automatically deduct raw material inventory
                    UPDATE Raw_Materials rm
                    INNER JOIN Batch_Materials bm ON rm.material_id = bm.material_id
                    SET rm.current_stock = rm.current_stock - bm.quantity_required
                    WHERE bm.batch_id = NEW.batch_id;
                    
                    -- Log event in Provenance Ledger automatically
                    INSERT INTO Provenance_Ledger (
                        batch_id, event_type, event_timestamp, location, actor_id, remarks
                    )
                    SELECT 
                        NEW.batch_id, 
                        'Weaving Started', 
                        NOW(), 
                        (SELECT geo_location FROM Weavers WHERE weaver_id = NEW.weaver_id), 
                        NEW.weaver_id, 
                        'Automated Entry: Production started, inventory deducted.'
                    ;
                    
                END IF;
            END;
        """)
        
        # Stored Procedure
        print("  -> Creating Stored Procedure: Generate_Lifecycle_Audit_Report")
        cursor.execute("DROP PROCEDURE IF EXISTS Generate_Lifecycle_Audit_Report;")
        cursor.execute("""
            CREATE PROCEDURE Generate_Lifecycle_Audit_Report(IN p_batch_id VARCHAR(50))
            BEGIN
                SELECT 
                    pl.event_timestamp AS 'Date & Time',
                    pl.event_type AS 'Milestone',
                    pl.location AS 'Location',
                    CASE 
                        WHEN pl.event_type IN ('Shipped to Retailer', 'Sold to Consumer') THEN r.retailer_name
                        ELSE w.full_name 
                    END AS 'Handled By',
                    pb.design_name AS 'Design',
                    pl.authenticity_hash AS 'Authenticity Hash',
                    pl.remarks AS 'Audit Remarks'
                FROM Provenance_Ledger pl
                JOIN Production_Batches pb ON pl.batch_id = pb.batch_id
                LEFT JOIN Weavers w ON pb.weaver_id = w.weaver_id AND pl.actor_id = w.weaver_id
                LEFT JOIN Retailers r ON pl.actor_id = r.retailer_id
                WHERE pl.batch_id = p_batch_id
                ORDER BY pl.event_timestamp ASC;
            END;
        """)
        
        conn.commit()
        print("Database setup complete! All 3 pillars successfully configured.")
        
    except mysql.connector.Error as err:
        print(f"Error connecting or executing SQL: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

if __name__ == "__main__":
    setup_advanced_db()
