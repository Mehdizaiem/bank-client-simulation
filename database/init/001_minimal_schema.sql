-- Minimal Bank Simulation Schema - Optimized for development
-- Focus on core tables only

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Tunisian governorates reference (essential)
CREATE TABLE ref_governorates (
    id SERIAL PRIMARY KEY,
    code VARCHAR(3) UNIQUE NOT NULL,
    name_en VARCHAR(50) NOT NULL,
    region VARCHAR(20),
    population INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert essential governorates
INSERT INTO ref_governorates (code, name_en, region, population) VALUES
('TUN', 'Tunis', 'North', 1056247),
('SFA', 'Sfax', 'Center', 955421),
('SOU', 'Sousse', 'Center', 674971),
('ARI', 'Ariana', 'North', 576088),
('NAB', 'Nabeul', 'North', 787920),
('MON', 'Monastir', 'Center', 548828),
('BEN', 'Ben Arous', 'North', 631842),
('MAN', 'Manouba', 'North', 379518)
ON CONFLICT (code) DO NOTHING;

-- Retail clients (core table)
CREATE TABLE retail_clients (
    client_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    age INTEGER CHECK (age BETWEEN 18 AND 80),
    gender CHAR(1) CHECK (gender IN ('M', 'F')),
    governorate_id INTEGER REFERENCES ref_governorates(id),
    monthly_income DECIMAL(10,2),
    education_level VARCHAR(20),
    employment_sector VARCHAR(20),
    preferred_channel VARCHAR(20),
    risk_tolerance DECIMAL(3,2) CHECK (risk_tolerance BETWEEN 0 AND 1),
    satisfaction_score DECIMAL(3,2) CHECK (satisfaction_score BETWEEN 0 AND 1),
    digital_engagement_score DECIMAL(3,2) CHECK (digital_engagement_score BETWEEN 0 AND 1),
    data_source VARCHAR(20) DEFAULT 'synthetic',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Corporate clients (core table)
CREATE TABLE corporate_clients (
    client_id VARCHAR(20) PRIMARY KEY,
    company_name VARCHAR(200) NOT NULL,
    business_sector VARCHAR(30),
    company_size VARCHAR(20),
    employee_count INTEGER,
    annual_revenue DECIMAL(15,2),
    headquarters_governorate_id INTEGER REFERENCES ref_governorates(id),
    credit_rating VARCHAR(5),
    digital_maturity_score DECIMAL(3,2) CHECK (digital_maturity_score BETWEEN 0 AND 1),
    data_source VARCHAR(20) DEFAULT 'synthetic',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Simulation runs (for tracking your pipeline executions)
CREATE TABLE pipeline_runs (
    run_id VARCHAR(50) PRIMARY KEY,
    run_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'running',
    retail_count INTEGER DEFAULT 0,
    corporate_count INTEGER DEFAULT 0,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    config_json JSONB
);

-- Indexes for performance
CREATE INDEX idx_retail_governorate ON retail_clients(governorate_id);
CREATE INDEX idx_retail_income ON retail_clients(monthly_income);
CREATE INDEX idx_corporate_sector ON corporate_clients(business_sector);
CREATE INDEX idx_corporate_revenue ON corporate_clients(annual_revenue);

-- Create view for quick client summary
CREATE VIEW v_client_summary AS
SELECT 
    'retail' as client_type,
    COUNT(*) as total_clients,
    AVG(monthly_income) as avg_income,
    AVG(satisfaction_score) as avg_satisfaction
FROM retail_clients WHERE is_active = TRUE
UNION ALL
SELECT 
    'corporate' as client_type,
    COUNT(*) as total_clients,
    AVG(annual_revenue) as avg_revenue,
    AVG(digital_maturity_score) as avg_digital_maturity
FROM corporate_clients WHERE is_active = TRUE;

