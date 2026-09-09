-- 1. Tables
CREATE TABLE artisans (
    artisan_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    contact_number VARCHAR(20),
    skill_level VARCHAR(100),
    skill_multiplier DECIMAL(3,2) DEFAULT 1.00
);

CREATE TABLE traditional_designs (
    design_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    region_origin VARCHAR(255),
    complexity_rating INT DEFAULT 5
);

CREATE TABLE raw_materials (
    material_id INT AUTO_INCREMENT PRIMARY KEY,
    material_name VARCHAR(255) NOT NULL,
    quantity_available INT DEFAULT 0
);

CREATE TABLE design_materials (
    design_id INT,
    material_id INT,
    quantity_required INT DEFAULT 1,
    PRIMARY KEY (design_id, material_id),
    CONSTRAINT fk_dm_design FOREIGN KEY (design_id) REFERENCES traditional_designs(design_id) ON DELETE CASCADE,
    CONSTRAINT fk_dm_material FOREIGN KEY (material_id) REFERENCES raw_materials(material_id) ON DELETE CASCADE
);

CREATE TABLE production_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    artisan_id INT,
    design_id INT,
    status VARCHAR(50),
    start_date DATE,
    quantity INT DEFAULT 1,
    payout_amount DECIMAL(10,2),
    CONSTRAINT fk_pl_artisan FOREIGN KEY (artisan_id) REFERENCES artisans(artisan_id) ON DELETE CASCADE,
    CONSTRAINT fk_pl_design FOREIGN KEY (design_id) REFERENCES traditional_designs(design_id) ON DELETE CASCADE
);

CREATE TABLE production_audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    log_id INT,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    change_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pa_log FOREIGN KEY (log_id) REFERENCES production_logs(log_id) ON DELETE CASCADE
);

CREATE TABLE users_buyers (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- 2. Triggers
DELIMITER //

-- BEFORE INSERT Trigger to check and deduct raw materials
CREATE TRIGGER check_raw_materials_before_insert
BEFORE INSERT ON production_logs
FOR EACH ROW
BEGIN
    DECLARE v_material_id INT;
    DECLARE v_required_qty INT;
    DECLARE v_available_qty INT;
    DECLARE v_material_name VARCHAR(255);
    DECLARE done INT DEFAULT FALSE;
    
    DECLARE material_cursor CURSOR FOR
        SELECT m.material_id, dm.quantity_required * NEW.quantity, m.quantity_available, m.material_name
        FROM design_materials dm
        JOIN raw_materials m ON dm.material_id = m.material_id
        WHERE dm.design_id = NEW.design_id;
        
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN material_cursor;
    
    check_loop: LOOP
        FETCH material_cursor INTO v_material_id, v_required_qty, v_available_qty, v_material_name;
        IF done THEN
            LEAVE check_loop;
        END IF;
        
        IF v_available_qty < v_required_qty THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = CONCAT('Insufficient ', v_material_name, '. Required: ', v_required_qty, ', Available: ', v_available_qty);
        ELSE
            UPDATE raw_materials 
            SET quantity_available = quantity_available - v_required_qty 
            WHERE material_id = v_material_id;
        END IF;
    END LOOP;
    
    CLOSE material_cursor;
END //

-- AFTER UPDATE Trigger to log status changes for data accountability
CREATE TRIGGER after_production_log_update
AFTER UPDATE ON production_logs
FOR EACH ROW
BEGIN
    IF OLD.status != NEW.status THEN
        INSERT INTO production_audit (log_id, old_status, new_status)
        VALUES (NEW.log_id, OLD.status, NEW.status);
    END IF;
END //

-- 3. Stored Procedure
-- Automates dynamic wage calculations based on design complexity and artisan skill
CREATE PROCEDURE Calculate_Artisan_Payout(IN p_log_id INT)
BEGIN
    DECLARE v_quantity INT;
    DECLARE v_complexity INT;
    DECLARE v_skill_mult DECIMAL(3,2);
    DECLARE v_payout DECIMAL(10,2);
    
    SELECT pl.quantity, td.complexity_rating, a.skill_multiplier
    INTO v_quantity, v_complexity, v_skill_mult
    FROM production_logs pl
    JOIN traditional_designs td ON pl.design_id = td.design_id
    JOIN artisans a ON pl.artisan_id = a.artisan_id
    WHERE pl.log_id = p_log_id;
    
    -- Formula: (quantity * 100) * (ComplexityRating / 10) * SkillMultiplier
    SET v_payout = (v_quantity * 100) * (v_complexity / 10.0) * v_skill_mult;
    
    UPDATE production_logs
    SET payout_amount = v_payout
    WHERE log_id = p_log_id;
END //

DELIMITER ;

-- 4. View
-- Flattens complex many-to-many relationships to provide a unified provenance report
CREATE VIEW vw_Textile_Provenance AS
SELECT 
    pl.log_id,
    a.name AS artisan_name,
    td.name AS design_name,
    td.region_origin,
    pl.status,
    GROUP_CONCAT(rm.material_name SEPARATOR ', ') AS materials_used
FROM production_logs pl
JOIN artisans a ON pl.artisan_id = a.artisan_id
JOIN traditional_designs td ON pl.design_id = td.design_id
LEFT JOIN design_materials dm ON td.design_id = dm.design_id
LEFT JOIN raw_materials rm ON dm.material_id = rm.material_id
GROUP BY pl.log_id;
