-- Health-Bite Database Schema
-- This file initializes the database structure

-- Create database if not exists (already created via env var, but included for safety)
CREATE DATABASE IF NOT EXISTS health_bite_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE health_bite_db;

-- Note: Django will create tables via migrations
-- This file can be used for any initial data or custom SQL needed
