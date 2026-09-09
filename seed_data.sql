CREATE DATABASE IF NOT EXISTS heritage_handloom;
USE heritage_handloom;

CREATE TABLE IF NOT EXISTS artisans (
    artisan_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    contact_number VARCHAR(20),
    skill_level VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS traditional_designs (
    design_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    region_origin VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS production_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    artisan_id INT,
    design_id INT,
    status ENUM('Active', 'Completed', 'Pending') DEFAULT 'Pending',
    start_date DATE,
    end_date DATE,
    quantity INT,
    FOREIGN KEY (artisan_id) REFERENCES artisans(artisan_id),
    FOREIGN KEY (design_id) REFERENCES traditional_designs(design_id)
);

-- Seed Data
INSERT INTO artisans (name, location, contact_number, skill_level) VALUES
('Ramesh Kumar', 'Shivamogga', '9876543210', 'Master Weaver'),
('Lakshmi Devi', 'Mysore', '9876543211', 'Senior Artisan'),
('Basavaraj', 'Ilkal', '9876543212', 'Master Weaver'),
('Kavitha', 'Udupi', '9876543213', 'Apprentice'),
('Nanjundaswamy', 'Chamarajanagar', '9876543214', 'Intermediate Weaver');

INSERT INTO traditional_designs (name, description, region_origin) VALUES
('Mysore Silk Zari', 'Rich silk saree with pure gold zari work', 'Mysore'),
('Ilkal Checkered', 'Traditional cotton-silk blend with red border and checks', 'Ilkal'),
('Udupi Cotton', 'Fine 80s count cotton sarees with distinct borders', 'Udupi'),
('Kasuti Embroidery', 'Intricate folk embroidery patterns', 'Dharwad');

INSERT INTO production_logs (artisan_id, design_id, status, start_date, end_date, quantity) VALUES
(1, 1, 'Completed', '2026-04-01', '2026-04-15', 5),
(2, 1, 'Active', '2026-05-10', NULL, 3),
(3, 2, 'Completed', '2026-03-15', '2026-03-30', 10),
(3, 2, 'Active', '2026-05-15', NULL, 5),
(4, 3, 'Completed', '2026-04-20', '2026-05-05', 8),
(5, 4, 'Active', '2026-05-01', NULL, 2);
