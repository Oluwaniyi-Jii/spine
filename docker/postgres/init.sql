-- Initialize database schemas for Shelf Data Warehouse
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS intermediate;
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE SCHEMA IF NOT EXISTS marts;
CREATE SCHEMA IF NOT EXISTS meta;

-- Set default search path
ALTER DATABASE shelf_db SET search_path TO warehouse, marts, staging, raw, meta, public;
