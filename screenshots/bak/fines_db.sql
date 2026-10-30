-- =====================================================
-- Fines Management System - Database Setup Script
-- Run this script ONCE before starting the Python app.
-- Example: mysql -u root -p < fines_db.sql
-- =====================================================

-- 1. Create the database (drop it first for a clean re-run, optional)
-- DROP DATABASE IF EXISTS fines_db;
CREATE DATABASE IF NOT EXISTS fines_db;

-- 2. Select the database
USE fines_db;

-- 3. Create the 'fines' table
CREATE TABLE IF NOT EXISTS fines (
    fine_id     INT AUTO_INCREMENT PRIMARY KEY,
    person_name VARCHAR(100) NOT NULL,
    amount      DECIMAL(10, 2) NOT NULL,
    status      VARCHAR(20) NOT NULL DEFAULT 'Unpaid'
);

-- 4. (Optional) Insert sample data for testing
INSERT INTO fines (person_name, amount, status) VALUES
('John Doe', 150.50, 'Unpaid'),
('Jane Smith', 75.00, 'Paid');

-- 5. Verify the table was created
SELECT * FROM fines;
