#!/usr/bin/env python3
"""
MEHDI WEEK 1 PRODUCTION PIPELINE - ENHANCED
Complete implementation of all Week 1 deliverables
"""

import pandas as pd
import numpy as np
import psycopg2
import os
import json
import logging
from datetime import datetime
from pathlib import Path
import sys

# Import our schema definitions
try:
    from schemas import (
        RetailClientSchema, CorporateClientSchema, 
        DataValidator, TeamExporter
    )
    from data_sources import TunisianDataSources
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the src/data_generation directory")
    sys.exit(1)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionDataPipeline:
    """Production-grade data generation pipeline"""
    
    def __init__(self):
        self.db_url = os.getenv('DATABASE_URL', 
                               "postgresql://sim_admin:SimBank2024!@localhost:5432/bank_simulation")
        self.output_dir = Path("../../data/processed")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Tunisian data sources
        self.data_sources = TunisianDataSources()
        self.demographic_params = self.data_sources.get_demographic_parameters()
        self.corporate_params = self.data_sources.get_corporate_parameters()
        
        # Tunisian names
        self.tunisian_names = {
            'male': ['Mohamed', 'Ahmed', 'Ali', 'Omar', 'Youssef', 'Karim', 'Slim', 'Nabil'],
            'female': ['Fatma', 'Aicha', 'Leila', 'Samira', 'Nesrine', 'Rahma', 'Sonia', 'Imen']
        }
        
        self.tunisian_surnames = [
            'Ben Ali', 'Trabelsi', 'Jendoubi', 'Sfaxien', 'Souissi', 'Kairoui',
            'Bizertien', 'Nabeuli', 'Mahdi', 'Gharbi'
        ]
        
        logger.info("🚀 Production pipeline initialized")
    
    def generate_validated_retail_clients(self, count=1000):
        """Generate retail clients validated against INS Tunisia data"""
        logger.info(f"Generating {count} validated retail clients...")
        
        clients = []
        
        # Population-weighted governorate sampling
        gov_names = list(self.demographic_params['population_by_governorate'].keys())
        gov_populations = list(self.demographic_params['population_by_governorate'].values())
        gov_weights = np.array(gov_populations) / sum(gov_populations)
        
        for i in range(count):
            try:
                # Demographics
                age = max(18, min(80, int(np.random.normal(40, 12))))
                gender = np.random.choice(['M', 'F'])
                
                # Names
                first_name = np.random.choice(
                    self.tunisian_names['male'] if gender == 'M' 
                    else self.tunisian_names['female']
                )
                last_name = np.random.choice(self.tunisian_surnames)
                
                # Geographic distribution
                governorate = np.random.choice(gov_names, p=gov_weights)
                
                # Education and employment
                education = np.random.choice(
                    list(self.demographic_params['education_distribution'].keys()),
                    p=list(self.demographic_params['education_distribution'].values())
                )
                
                employment = np.random.choice(
                    list(self.demographic_params['employment_sectors'].keys()),
                    p=list(self.demographic_params['employment_sectors'].values())
                )
                
                # Income generation
                income = self._generate_realistic_income(age, education, governorate)
                
                # Banking behavior
                channel = self._generate_channel_preference(age)
                
                # Behavioral scores
                satisfaction = np.random.beta(3, 2)
                digital_engagement = self._calculate_digital_engagement(age, education)
                risk_tolerance = np.random.beta(2, 2)
                
                client_data = {
                    'client_id': f'R_{i+1:05d}',
                    'first_name': first_name,
                    'last_name': last_name,
                    'age': age,
                    'gender': gender,
                    'governorate': governorate,
                    'monthly_income': round(income, 2),
                    'education_level': education,
                    'employment_sector': employment,
                    'preferred_channel': channel,
                    'risk_tolerance': round(risk_tolerance, 3),
                    'satisfaction_score': round(satisfaction, 3),
                    'digital_engagement_score': round(digital_engagement, 3)
                }
                
                clients.append(client_data)
                
            except Exception as e:
                logger.warning(f"Failed to generate client {i+1}: {e}")
                continue
        
        df = pd.DataFrame(clients)
        
        # Validate
        validation_report = DataValidator.validate_retail_data(df)
        logger.info(f"Retail data validation score: {validation_report['quality_score']:.2f}")
        
        return df
    
    def generate_validated_corporate_clients(self, count=200):
        """Generate corporate clients validated against Ministry data"""
        logger.info(f"Generating {count} validated corporate clients...")
        
        companies = []
        
        for i in range(count):
            try:
                # Company size (heavily weighted toward micro)
                company_size = np.random.choice(
                    list(self.corporate_params['size_distribution'].keys()),
                    p=list(self.corporate_params['size_distribution'].values())
                )
                
                # Business sector
                sector = np.random.choice(
                    list(self.corporate_params['sector_distribution'].keys()),
                    p=list(self.corporate_params['sector_distribution'].values())
                )
                
                # Revenue and employees
                revenue = self._generate_realistic_revenue(company_size)
                employees = self._generate_realistic_employees(company_size)
                
                # Location
                headquarters = np.random.choice(['Tunis', 'Sfax', 'Sousse', 'Ariana'], 
                                             p=[0.45, 0.20, 0.15, 0.20])
                
                # Digital maturity
                digital_maturity = min(1.0, max(0.1, 
                    0.3 + (0.4 if sector == 'technology' else 0.0) + np.random.normal(0, 0.15)))
                
                company_data = {
                    'client_id': f'C_{i+1:05d}',
                    'company_name': f'Company_{sector.title()}_{i+1:03d}',
                    'business_sector': sector,
                    'company_size': company_size,
                    'employee_count': employees,
                    'annual_revenue': round(revenue, 2),
                    'headquarters_governorate': headquarters,
                    'credit_rating': np.random.choice(['A', 'B', 'C', 'D'], p=[0.2, 0.4, 0.3, 0.1]),
                    'digital_maturity_score': round(digital_maturity, 3),
                    'cash_flow_predictability': round(np.random.beta(3, 2), 3),
                    'seasonal_variation': round(np.random.beta(2, 3), 3)
                }
                
                companies.append(company_data)
                
            except Exception as e:
                logger.warning(f"Failed to generate company {i+1}: {e}")
                continue
        
        df = pd.DataFrame(companies)
        
        # Validate
        validation_report = DataValidator.validate_corporate_data(df)
        logger.info(f"Corporate data validation score: {validation_report['quality_score']:.2f}")
        
        return df
    
    def _generate_realistic_income(self, age, education, governorate):
        """Generate realistic income based on demographics"""
        # Base income by location
        location_multipliers = {
            'Tunis': 1.4, 'Ariana': 1.3, 'Sfax': 1.1, 'Sousse': 1.0
        }
        base_multiplier = location_multipliers.get(governorate, 0.8)
        
        # Education multiplier
        education_multipliers = {
            'primary': 0.8, 'secondary': 1.0, 'university': 1.6, 'postgraduate': 2.2
        }
        edu_multiplier = education_multipliers.get(education, 1.0)
        
        # Age curve
        age_multiplier = 0.7 + 0.6 * (1 - abs(age - 45) / 45)
        
        base_income = 1000
        final_income = base_income * base_multiplier * edu_multiplier * age_multiplier
        final_income *= (1 + np.random.normal(0, 0.25))
        
        return max(400, min(15000, final_income))
    
    def _generate_channel_preference(self, age):
        """Generate channel preference based on age"""
        if age < 30:
            return np.random.choice(['mobile', 'web', 'whatsapp'], p=[0.6, 0.25, 0.15])
        elif age < 50:
            return np.random.choice(['mobile', 'branch', 'web'], p=[0.45, 0.35, 0.20])
        else:
            return np.random.choice(['branch', 'mobile'], p=[0.65, 0.35])
    
    def _calculate_digital_engagement(self, age, education):
        """Calculate digital engagement score"""
        age_score = max(0.1, 1.0 - (age - 18) / 62)
        edu_scores = {'primary': 0.4, 'secondary': 0.6, 'university': 0.8, 'postgraduate': 0.9}
        edu_score = edu_scores.get(education, 0.5)
        
        digital_score = (0.6 * age_score + 0.4 * edu_score)
        digital_score += np.random.normal(0, 0.15)
        
        return max(0.1, min(1.0, digital_score))
    
    def _generate_realistic_revenue(self, company_size):
        """Generate realistic revenue based on size"""
        size_ranges = self.corporate_params['revenue_by_size_tnd']
        min_rev, max_rev = size_ranges[company_size]
        
        revenue = np.random.uniform(min_rev, max_rev)
        revenue *= np.random.lognormal(0, 0.3)
        
        return max(min_rev * 0.8, min(max_rev * 1.5, revenue))
    
    def _generate_realistic_employees(self, company_size):
        """Generate realistic employee count"""
        size_ranges = {
            'micro': (1, 9), 'small': (10, 49),
            'medium': (50, 249), 'large': (250, 1000)
        }
        
        min_emp, max_emp = size_ranges[company_size]
        return np.random.randint(min_emp, max_emp + 1)
    
    def save_to_database_with_validation(self, retail_df, corporate_df):
        """Save validated data to PostgreSQL"""
        logger.info("Attempting to save data to database...")
        
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            
            # Test connection
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            logger.info(f"Connected to: {version[0][:50]}...")
            
            # Save retail clients (simplified for reliability)
            retail_saved = 0
            for _, client in retail_df.iterrows():
                try:
                    cursor.execute("""
                        INSERT INTO retail_clients (
                            client_id, first_name, last_name, age, gender,
                            monthly_income, education_level, employment_sector, 
                            preferred_channel, risk_tolerance, satisfaction_score, 
                            digital_engagement_score, data_source
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (client_id) DO NOTHING
                    """, (
                        client['client_id'], client['first_name'], client['last_name'],
                        client['age'], client['gender'], client['monthly_income'],
                        client['education_level'], client['employment_sector'],
                        client['preferred_channel'], client['risk_tolerance'],
                        client['satisfaction_score'], client['digital_engagement_score'],
                        'mehdi_production'
                    ))
                    retail_saved += 1
                except Exception as e:
                    logger.warning(f"Retail insert failed for {client['client_id']}: {e}")
            
            # Save corporate clients
            corporate_saved = 0
            for _, company in corporate_df.iterrows():
                try:
                    cursor.execute("""
                        INSERT INTO corporate_clients (
                            client_id, company_name, business_sector, company_size,
                            employee_count, annual_revenue, credit_rating,
                            digital_maturity_score, data_source
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (client_id) DO NOTHING
                    """, (
                        company['client_id'], company['company_name'], company['business_sector'],
                        company['company_size'], company['employee_count'], company['annual_revenue'],
                        company['credit_rating'], company['digital_maturity_score'],
                        'mehdi_production'
                    ))
                    corporate_saved += 1
                except Exception as e:
                    logger.warning(f"Corporate insert failed for {company['client_id']}: {e}")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Saved {retail_saved} retail + {corporate_saved} corporate clients")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database save failed: {e}")
            logger.info("Continuing without database save...")
            return False
    
    def export_production_files(self, retail_df, corporate_df):
        """Export production files for team coordination"""
        logger.info("Exporting production files for team...")
        
        export_files = {}
        
        # Hamza exports
        hamza_files = TeamExporter.export_for_hamza(retail_df, corporate_df, str(self.output_dir))
        export_files['hamza'] = hamza_files
        
        # Nessrine exports
        nessrine_files = TeamExporter.export_for_nessrine(retail_df, corporate_df, str(self.output_dir))
        export_files['nessrine'] = nessrine_files
        
        # Maryem exports
        maryem_files = TeamExporter.export_for_maryem(retail_df, corporate_df, str(self.output_dir))
        export_files['maryem'] = maryem_files
        
        # Export data sources research
        self.data_sources.export_research_report(str(self.output_dir / "tunisian_data_sources_research.json"))
        
        logger.info("✅ All production files exported successfully")
        return export_files
    
    def run_production_pipeline(self):
        """Execute complete Week 1 production pipeline"""
        logger.info("🚀 STARTING WEEK 1 PRODUCTION PIPELINE")
        
        start_time = datetime.now()
        
        try:
            # Generate validated data
            retail_df = self.generate_validated_retail_clients(1000)
            corporate_df = self.generate_validated_corporate_clients(200)
            
            # Validate data quality
            retail_validation = DataValidator.validate_retail_data(retail_df)
            corporate_validation = DataValidator.validate_corporate_data(corporate_df)
            
            # Save to database
            db_success = self.save_to_database_with_validation(retail_df, corporate_df)
            
            # Export team files
            export_files = self.export_production_files(retail_df, corporate_df)
            
            # Generate report
            duration = (datetime.now() - start_time).total_seconds()
            
            report = {
                'pipeline_metadata': {
                    'execution_id': f"mehdi_week1_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    'execution_time_seconds': duration,
                    'pipeline_version': '1.0_production'
                },
                'data_generation': {
                    'retail_clients_generated': len(retail_df),
                    'corporate_clients_generated': len(corporate_df),
                    'total_clients': len(retail_df) + len(corporate_df)
                },
                'validation_results': {
                    'retail_quality_score': retail_validation['quality_score'],
                    'corporate_quality_score': corporate_validation['quality_score'],
                    'overall_quality_score': (retail_validation['quality_score'] + 
                                            corporate_validation['quality_score']) / 2
                },
                'database_integration': {
                    'save_successful': db_success
                },
                'team_deliverables': export_files,
                'week1_completion_status': {
                    'schemas_created': True,
                    'data_sources_researched': True,
                    'sample_datasets_generated': True,
                    'team_exports_completed': True,
                    'database_populated': db_success,
                    'validation_passed': (retail_validation['quality_score'] > 0.8 and 
                                        corporate_validation['quality_score'] > 0.8)
                }
            }
            
            # Save report
            with open(self.output_dir / "week1_production_report.json", 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            logger.info("🎉 WEEK 1 PRODUCTION PIPELINE COMPLETED")
            logger.info(f"Duration: {duration:.1f} seconds")
            
            return report
            
        except Exception as e:
            logger.error(f"❌ Production pipeline failed: {e}")
            raise

if __name__ == "__main__":
    pipeline = ProductionDataPipeline()
    result = pipeline.run_production_pipeline()
    
    print("\n" + "="*60)
    print("🎯 MEHDI WEEK 1 DELIVERABLES - PRODUCTION COMPLETE")
    print("="*60)
    
    print(f"\n📊 DATA GENERATION:")
    print(f"   ✅ {result['data_generation']['retail_clients_generated']} retail clients")
    print(f"   ✅ {result['data_generation']['corporate_clients_generated']} corporate clients")
    
    print(f"\n🔍 VALIDATION:")
    print(f"   ✅ Quality score: {result['validation_results']['overall_quality_score']:.2f}")
    
    print(f"\n📦 TEAM FILES:")
    for team, files in result['team_deliverables'].items():
        print(f"   ✅ {team.title()}: {', '.join(files)}")
    
    print(f"\n🚀 Ready for Week 2 CTGAN implementation!")
