-- Bank Client Simulation Database Schema
-- PostgreSQL 14+ with TimescaleDB for time-series data

-- =====================================================
-- 1. REFERENCE DATA TABLES
-- =====================================================

-- Tunisian geographic reference data
CREATE TABLE ref_governorates (
    id SERIAL PRIMARY KEY,
    code VARCHAR(3) UNIQUE NOT NULL,
    name_en VARCHAR(50) NOT NULL,
    name_ar VARCHAR(50),
    name_fr VARCHAR(50),
    region VARCHAR(20), -- North, Center, South
    population INTEGER,
    economic_index DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ref_delegations (
    id SERIAL PRIMARY KEY,
    governorate_id INTEGER REFERENCES ref_governorates(id),
    code VARCHAR(6) UNIQUE NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    name_ar VARCHAR(100),
    postal_code_prefix VARCHAR(4),
    urban_rural VARCHAR(10), -- urban, semi_urban, rural
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Banking product reference
CREATE TABLE ref_banking_products (
    id SERIAL PRIMARY KEY,
    product_code VARCHAR(20) UNIQUE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    product_category VARCHAR(30), -- checking, savings, credit, investment
    target_segment VARCHAR(20), -- retail, corporate, both
    min_income_requirement DECIMAL(10,2),
    risk_level INTEGER CHECK (risk_level BETWEEN 1 AND 5),
    digital_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 2. CLIENT DATA TABLES
-- =====================================================

-- Retail clients (individual customers)
CREATE TABLE retail_clients (
    client_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F')),
    
    -- Geographic
    governorate_id INTEGER REFERENCES ref_governorates(id),
    delegation_id INTEGER REFERENCES ref_delegations(id),
    postal_code VARCHAR(10),
    address_type VARCHAR(20), -- urban, suburban, rural
    
    -- Socio-economic
    monthly_income DECIMAL(10,2),
    education_level VARCHAR(20) CHECK (education_level IN ('primary', 'secondary', 'university', 'postgraduate')),
    employment_sector VARCHAR(20) CHECK (employment_sector IN ('public', 'private', 'self_employed', 'unemployed', 'retired')),
    occupation VARCHAR(100),
    household_size INTEGER CHECK (household_size BETWEEN 1 AND 15),
    
    -- Banking behavior
    client_since DATE NOT NULL,
    relationship_manager_id VARCHAR(20),
    primary_branch_code VARCHAR(10),
    preferred_channel VARCHAR(20) CHECK (preferred_channel IN ('branch', 'mobile', 'web', 'whatsapp', 'phone')),
    
    -- Risk and preferences
    risk_tolerance DECIMAL(3,2) CHECK (risk_tolerance BETWEEN 0 AND 1),
    investment_experience VARCHAR(20),
    communication_language VARCHAR(5) DEFAULT 'ar', -- ar, fr, en
    
    -- Behavioral scores (updated by ML models)
    satisfaction_score DECIMAL(3,2) CHECK (satisfaction_score BETWEEN 0 AND 1),
    churn_probability DECIMAL(3,2) CHECK (churn_probability BETWEEN 0 AND 1),
    digital_engagement_score DECIMAL(3,2) CHECK (digital_engagement_score BETWEEN 0 AND 1),
    loyalty_score DECIMAL(3,2) CHECK (loyalty_score BETWEEN 0 AND 1),
    
    -- Metadata
    data_source VARCHAR(20) DEFAULT 'synthetic', -- real, synthetic, hybrid
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Corporate clients (business customers)
CREATE TABLE corporate_clients (
    client_id VARCHAR(20) PRIMARY KEY,
    company_name VARCHAR(200) NOT NULL,
    legal_form VARCHAR(50), -- SARL, SA, SUARL, etc.
    tax_id VARCHAR(20) UNIQUE,
    
    -- Business profile
    business_sector VARCHAR(30) CHECK (business_sector IN ('agriculture', 'manufacturing', 'services', 'retail', 'construction', 'technology', 'tourism', 'finance')),
    company_size VARCHAR(20) CHECK (company_size IN ('micro', 'small', 'medium', 'large')),
    employee_count INTEGER,
    annual_revenue DECIMAL(15,2),
    establishment_date DATE,
    
    -- Geographic presence
    headquarters_governorate_id INTEGER REFERENCES ref_governorates(id),
    headquarters_delegation_id INTEGER REFERENCES ref_delegations(id),
    regional_presence TEXT[], -- Array of governorate codes
    export_activity BOOLEAN DEFAULT FALSE,
    
    -- Banking relationship
    client_since DATE NOT NULL,
    relationship_manager_id VARCHAR(20) NOT NULL,
    primary_branch_code VARCHAR(10),
    credit_rating VARCHAR(5) CHECK (credit_rating IN ('AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC', 'CC', 'C', 'D')),
    
    -- Digital and operational
    digital_maturity_score DECIMAL(3,2) CHECK (digital_maturity_score BETWEEN 0 AND 1),
    uses_digital_banking BOOLEAN DEFAULT FALSE,
    preferred_communication VARCHAR(20) CHECK (preferred_communication IN ('email', 'phone', 'in_person', 'portal')),
    
    -- Financial behavior
    cash_flow_predictability DECIMAL(3,2) CHECK (cash_flow_predictability BETWEEN 0 AND 1),
    seasonal_variation DECIMAL(3,2) CHECK (seasonal_variation BETWEEN 0 AND 1),
    payment_behavior_score DECIMAL(3,2) CHECK (payment_behavior_score BETWEEN 0 AND 1),
    
    -- Metadata
    data_source VARCHAR(20) DEFAULT 'synthetic',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
