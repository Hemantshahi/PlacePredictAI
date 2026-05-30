-- ================================================================
--  PlacePredict AI — MCE Training & Placement Cell
--  MySQL Database Setup Script
--  Run: mysql -u root -p < database_setup.sql
-- ================================================================

CREATE DATABASE IF NOT EXISTS mce_placement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE mce_placement_db;

-- Create dedicated user (optional but recommended)
-- CREATE USER 'mce_user'@'localhost' IDENTIFIED BY 'MCE@PlacePredict2024';
-- GRANT ALL PRIVILEGES ON mce_placement_db.* TO 'mce_user'@'localhost';
-- FLUSH PRIVILEGES;

-- Tables are auto-created by SQLAlchemy when app starts (db.create_all())
-- This script just ensures the database exists.

SELECT 'MCE Placement DB created successfully!' AS status;
