-- CNC Tools & Inserts Inventory Management System - Database Schema
-- Target: PostgreSQL
-- Version: 1.0

-- 1. Users & Authentication
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('student', 'instructor', 'technician', 'admin')) NOT NULL,
    student_id VARCHAR(20), -- Nullable, for students only
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Master Tables (Categories & Lookup)
CREATE TABLE tool_categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL, -- e.g., 'Turning', 'Milling', 'Drilling'
    description TEXT
);

CREATE TABLE material_grades (
    grade_id SERIAL PRIMARY KEY,
    iso_code VARCHAR(10) NOT NULL, -- e.g., 'P', 'M', 'K'
    name VARCHAR(50) NOT NULL, -- e.g., 'Steel', 'Stainless Steel'
    color_code VARCHAR(7) -- Hex code for UI display
);

CREATE TABLE machine_compatibility (
    machine_id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL, -- e.g., 'Haas VF-2'
    spindle_type VARCHAR(20) NOT NULL -- e.g., 'CAT40', 'BT40'
);

-- 3. Tool Holders (The physical tool body)
CREATE TABLE tool_holders (
    holder_id SERIAL PRIMARY KEY,
    category_id INT REFERENCES tool_categories(category_id),
    iso_code VARCHAR(50) NOT NULL, -- e.g., 'DCLNR 2525 M12'
    description VARCHAR(200),
    shank_type VARCHAR(20), -- 'Square', 'Cylindrical', 'CAT40'
    gauge_length_mm DECIMAL(10, 2),
    max_rpm INT,
    image_url VARCHAR(255),
    total_quantity INT DEFAULT 0,
    available_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Inserts (Consumables)
CREATE TABLE inserts (
    insert_id SERIAL PRIMARY KEY,
    iso_code VARCHAR(50) NOT NULL, -- e.g., 'CNMG 12 04 08'
    manufacturer VARCHAR(50),
    grade_id INT REFERENCES material_grades(grade_id),
    coating_type VARCHAR(50), -- e.g., 'TiAlN'
    nose_radius_mm DECIMAL(5, 3),
    min_stock_level INT DEFAULT 10,
    current_stock INT DEFAULT 0,
    price_per_unit DECIMAL(10, 2),
    compatible_holder_id INT REFERENCES tool_holders(holder_id), -- simplified 1:1 for MVP, usually M:N
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Link table for Many-to-Many relationship between Holders and Inserts (Better design)
CREATE TABLE holder_insert_compatibility (
    holder_id INT REFERENCES tool_holders(holder_id),
    insert_id INT REFERENCES inserts(insert_id),
    PRIMARY KEY (holder_id, insert_id)
);

-- 5. Inventory Transactions (Issuance & Returns)
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    approver_id INT REFERENCES users(user_id), -- Instructor who approved
    item_type VARCHAR(10) CHECK (item_type IN ('holder', 'insert')),
    item_id INT NOT NULL, -- holder_id or insert_id
    transaction_type VARCHAR(20) CHECK (transaction_type IN ('checkout', 'return', 'restock', 'scrap')),
    quantity INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

-- 6. Current Loans (Active checkouts)
CREATE TABLE active_loans (
    loan_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    holder_id INT REFERENCES tool_holders(holder_id),
    checked_out_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active' -- 'active', 'overdue'
);

-- 7. Tool Lifecycle / Condition (Specific physical instances of holders)
CREATE TABLE tool_instances (
    instance_id SERIAL PRIMARY KEY,
    holder_id INT REFERENCES tool_holders(holder_id),
    qr_code_data VARCHAR(100) UNIQUE NOT NULL,
    condition VARCHAR(20) CHECK (condition IN ('new', 'good', 'worn', 'damaged')) DEFAULT 'new',
    purchase_date DATE,
    usage_hours DECIMAL(10, 2) DEFAULT 0
);

-- Indexes for performance
CREATE INDEX idx_inserts_iso ON inserts(iso_code);
CREATE INDEX idx_holders_iso ON tool_holders(iso_code);
CREATE INDEX idx_transactions_user ON transactions(user_id);
