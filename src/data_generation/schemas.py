#!/usr/bin/env python3
"""
Mehdi's Data Generation Schemas - Week 1 Foundation
Formal schema definitions for Tunisian bank client simulation
Based on INS Tunisia and Central Bank of Tunisia data standards
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
import pandas as pd
import numpy as np

class TunisianGovernorate(Enum):
    """Official Tunisian governorates with INS codes"""
    TUNIS = "Tunis"
    ARIANA = "Ariana"
    BEN_AROUS = "Ben Arous"
    MANOUBA = "Manouba"
    NABEUL = "Nabeul"
    SFAX = "Sfax"
    SOUSSE = "Sousse"
    MONASTIR = "Monastir"
    MAHDIA = "Mahdia"
    KAIROUAN = "Kairouan"
    BIZERTE = "Bizerte"
    GAFSA = "Gafsa"

class EducationLevel(Enum):
    """Education levels aligned with INS Tunisia classification"""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    UNIVERSITY = "university"
    POSTGRADUATE = "postgraduate"

class EmploymentSector(Enum):
    """Employment sectors per INS Tunisia labor statistics"""
    PRIVATE = "private"
    PUBLIC = "public"
    SELF_EMPLOYED = "self_employed"
    UNEMPLOYED = "unemployed"
    RETIRED = "retired"

class ChannelPreference(Enum):
    """Banking channel preferences"""
    BRANCH = "branch"
    MOBILE = "mobile"
    WEB = "web"
    WHATSAPP = "whatsapp"

class CompanySize(Enum):
    """Company size classification per Central Bank of Tunisia"""
    MICRO = "micro"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class BusinessSector(Enum):
    """Business sectors aligned with INS Tunisia classification"""
    AGRICULTURE = "agriculture"
    MANUFACTURING = "manufacturing"
    SERVICES = "services"
    RETAIL = "retail"
    TECHNOLOGY = "technology"

@dataclass
class RetailClientSchema:
    """Retail client schema based on Central Bank of Tunisia standards"""
    client_id: str
    first_name: str
    last_name: str
    age: int
    gender: str
    governorate: str
    monthly_income: float
    education_level: str
    employment_sector: str
    preferred_channel: str
    risk_tolerance: float
    satisfaction_score: float
    digital_engagement_score: float
    
    def __post_init__(self):
        """Validate schema constraints"""
        assert 18 <= self.age <= 80, f"Age {self.age} outside valid range 18-80"
        assert 400 <= self.monthly_income <= 15000, f"Income {self.monthly_income} outside valid range"
        assert 0 <= self.risk_tolerance <= 1, "Risk tolerance must be 0-1"
        assert 0 <= self.satisfaction_score <= 1, "Satisfaction score must be 0-1"
        assert self.gender in ['M', 'F'], "Gender must be M or F"

@dataclass
class CorporateClientSchema:
    """Corporate client schema based on Central Bank of Tunisia SME classification"""
    client_id: str
    company_name: str
    business_sector: str
    company_size: str
    employee_count: int
    annual_revenue: float
    headquarters_governorate: str
    credit_rating: str
    digital_maturity_score: float
    cash_flow_predictability: float
    seasonal_variation: float
    
    def __post_init__(self):
        """Validate business logic constraints"""
        size_revenue_ranges = {
            'micro': (10000, 100000),
            'small': (100000, 1000000),
            'medium': (1000000, 10000000),
            'large': (10000000, 100000000)
        }
        
        if self.company_size in size_revenue_ranges:
            min_rev, max_rev = size_revenue_ranges[self.company_size]
            if not (min_rev <= self.annual_revenue <= max_rev * 2):  # Allow some flexibility
                print(f"Warning: Revenue {self.annual_revenue} may be inconsistent with size {self.company_size}")

class DataValidator:
    """Validation utilities for generated data quality"""
    
    @staticmethod
    def validate_retail_data(df: pd.DataFrame) -> Dict[str, Any]:
        """Validate retail client data against Tunisian standards"""
        issues = []
        
        # Check income distribution
        median_income = df['monthly_income'].median()
        if not (800 <= median_income <= 1500):
            issues.append(f"Median income {median_income:.0f} TND outside expected range 800-1500")
            
        # Check age distribution
        mean_age = df['age'].mean()
        if not (35 <= mean_age <= 45):
            issues.append(f"Mean age {mean_age:.1f} outside typical banking population 35-45")
            
        return {
            'total_records': len(df),
            'validation_issues': issues,
            'quality_score': max(0, 1 - len(issues) * 0.2),
            'median_income_tnd': median_income,
            'mean_age': mean_age
        }
    
    @staticmethod
    def validate_corporate_data(df: pd.DataFrame) -> Dict[str, Any]:
        """Validate corporate client data against Central Bank standards"""
        issues = []
        
        # Check size distribution
        micro_pct = (df['company_size'] == 'micro').mean()
        if micro_pct < 0.70:
            issues.append(f"Micro company percentage {micro_pct:.1%} too low (expected >70%)")
            
        return {
            'total_records': len(df),
            'validation_issues': issues,
            'quality_score': max(0, 1 - len(issues) * 0.3),
            'micro_percentage': micro_pct
        }

class TeamExporter:
    """Export data in formats optimized for each team member"""
    
    @staticmethod
    def export_for_hamza(retail_df: pd.DataFrame, corporate_df: pd.DataFrame, output_dir: str):
        """Export agent-ready data for Hamza's Mesa ABM"""
        hamza_retail = retail_df[['client_id', 'age', 'governorate', 'monthly_income',
                                'risk_tolerance', 'satisfaction_score', 'digital_engagement_score',
                                'preferred_channel']].copy()
        
        hamza_corporate = corporate_df[['client_id', 'company_name', 'business_sector', 'company_size',
                                      'annual_revenue', 'digital_maturity_score', 'headquarters_governorate']].copy()
        
        hamza_retail.to_csv(f"{output_dir}/hamza_retail_agents.csv", index=False)
        hamza_corporate.to_csv(f"{output_dir}/hamza_corporate_agents.csv", index=False)
        
        return ['hamza_retail_agents.csv', 'hamza_corporate_agents.csv']
    
    @staticmethod
    def export_for_nessrine(retail_df: pd.DataFrame, corporate_df: pd.DataFrame, output_dir: str):
        """Export dashboard-ready statistics for Nessrine's visualization"""
        
        dashboard_data = {
            'generation_time': pd.Timestamp.now().isoformat(),
            'retail_stats': {
                'count': len(retail_df),
                'age_distribution': retail_df['age'].describe().to_dict(),
                'income_distribution': retail_df['monthly_income'].describe().to_dict(),
                'governorate_counts': retail_df['governorate'].value_counts().to_dict(),
                'channel_preferences': retail_df['preferred_channel'].value_counts().to_dict()
            },
            'corporate_stats': {
                'count': len(corporate_df),
                'sector_distribution': corporate_df['business_sector'].value_counts().to_dict(),
                'size_distribution': corporate_df['company_size'].value_counts().to_dict(),
                'revenue_stats': corporate_df['annual_revenue'].describe().to_dict()
            }
        }
        
        import json
        with open(f"{output_dir}/nessrine_dashboard_data.json", 'w') as f:
            json.dump(dashboard_data, f, indent=2, default=str)
            
        return ['nessrine_dashboard_data.json']
    
    @staticmethod
    def export_for_maryem(retail_df: pd.DataFrame, corporate_df: pd.DataFrame, output_dir: str):
        """Export scenario-ready segments for Maryem's simulation interface"""
        
        segments = {
            'high_value_retail': retail_df[
                retail_df['monthly_income'] > retail_df['monthly_income'].quantile(0.9)
            ]['client_id'].tolist(),
            
            'young_digital': retail_df[
                (retail_df['age'] < 35) & 
                (retail_df['digital_engagement_score'] > 0.7)
            ]['client_id'].tolist(),
            
            'large_corporates': corporate_df[
                corporate_df['company_size'] == 'large'
            ]['client_id'].tolist(),
            
            'tech_companies': corporate_df[
                corporate_df['business_sector'] == 'technology'
            ]['client_id'].tolist()
        }
        
        import json
        with open(f"{output_dir}/maryem_client_segments.json", 'w') as f:
            json.dump(segments, f, indent=2)
            
        return ['maryem_client_segments.json']

if __name__ == "__main__":
    print("📋 Schemas validated successfully!")
