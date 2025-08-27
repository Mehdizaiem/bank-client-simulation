#!/usr/bin/env python3
"""
Mehdi's Data Generation Pipeline - Week 1 Foundation
Optimized for immediate development and team coordination
"""

import pandas as pd
import numpy as np
import psycopg2
import os
import json
from datetime import datetime, date
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MehdiDataPipeline:
    """Your data generation pipeline for Week 1 deliverables"""
    
    def __init__(self):
        self.db_url = "postgresql://sim_admin:SimBank2024!@localhost:5432/bank_simulation"
        self.output_dir = Path("../../data/processed")
        self.output_dir.mkdir(exist_ok=True)
        
        # Tunisian-specific data
        self.governorates = [
            "Tunis", "Sfax", "Sousse", "Ariana", "Nabeul", "Monastir", 
            "Ben Arous", "Manouba", "Bizerte", "Kairouan", "Mahdia", "Gafsa"
        ]
        
        self.tunisian_first_names = {
            'male': ['Mohamed', 'Ahmed', 'Ali', 'Omar', 'Youssef', 'Karim', 'Slim', 'Nabil'],
            'female': ['Fatma', 'Aicha', 'Leila', 'Samira', 'Nesrine', 'Rahma', 'Sonia', 'Imen']
        }
        
        self.tunisian_last_names = [
            'Ben Ali', 'Trabelsi', 'Jendoubi', 'Sfaxien', 'Souissi', 
            'Kairoui', 'Bizertien', 'Nabeuli', 'Mahdi', 'Gharbi'
        ]
    
    def generate_retail_clients(self, count=1000):
        """Generate realistic Tunisian retail banking clients"""
        logger.info(f"Generating {count} retail clients...")
        
        clients = []
        for i in range(count):
            # Demographics
            age = max(18, min(80, int(np.random.normal(40, 12))))
            gender = np.random.choice(['M', 'F'])
            
            first_name = np.random.choice(
                self.tunisian_first_names['male'] if gender == 'M' 
                else self.tunisian_first_names['female']
            )
            last_name = np.random.choice(self.tunisian_last_names)
            
            # Geographic (realistic distribution)
            governorate_weights = {
                'Tunis': 0.3, 'Sfax': 0.15, 'Sousse': 0.1, 'Ariana': 0.08, 'Nabeul': 0.06
            }
            remaining = [g for g in self.governorates if g not in governorate_weights]
            for gov in remaining:
                governorate_weights[gov] = 0.31 / len(remaining)
            
            governorate = np.random.choice(
                list(governorate_weights.keys()), 
                p=list(governorate_weights.values())
            )
            
            # Income based on location and demographics
            base_income = 1200 if governorate in ['Tunis', 'Ariana'] else 800
            education = np.random.choice(
                ['primary', 'secondary', 'university', 'postgraduate'],
                p=[0.25, 0.45, 0.25, 0.05]
            )
            
            education_multiplier = {
                'primary': 0.8, 'secondary': 1.0, 'university': 1.6, 'postgraduate': 2.5
            }[education]
            
            income = base_income * education_multiplier * (1 + np.random.normal(0, 0.3))
            income = max(400, min(15000, income))
            
            # Banking behavior
            channel_preference = np.random.choice(
                ['mobile', 'branch', 'web', 'whatsapp'],
                p=[0.4, 0.35, 0.15, 0.1]
            )
            
            # Behavioral scores
            satisfaction = np.random.beta(3, 2)  # Slightly positive skew
            digital_engagement = max(0.1, min(1.0, 
                0.5 + (35-age)/70 + np.random.normal(0, 0.2)))
            
            client = {
                'client_id': f'R_{i+1:05d}',
                'first_name': first_name,
                'last_name': last_name,
                'age': age,
                'gender': gender,
                'governorate': governorate,
                'monthly_income': round(income, 2),
                'education_level': education,
                'employment_sector': np.random.choice(
                    ['private', 'public', 'self_employed', 'unemployed'],
                    p=[0.5, 0.25, 0.15, 0.1]
                ),
                'preferred_channel': channel_preference,
                'risk_tolerance': round(np.random.beta(2, 2), 3),
                'satisfaction_score': round(satisfaction, 3),
                'digital_engagement_score': round(digital_engagement, 3)
            }
            clients.append(client)
        
        return pd.DataFrame(clients)
    
    def generate_corporate_clients(self, count=200):
        """Generate realistic Tunisian corporate clients"""
        logger.info(f"Generating {count} corporate clients...")
        
        companies = []
        sectors = {
            'agriculture': 0.15, 'manufacturing': 0.25, 'services': 0.4,
            'retail': 0.15, 'technology': 0.05
        }
        
        for i in range(count):
            sector = np.random.choice(list(sectors.keys()), p=list(sectors.values()))
            
            # Company size (realistic Tunisian distribution)
            company_size = np.random.choice(
                ['micro', 'small', 'medium', 'large'],
                p=[0.85, 0.12, 0.025, 0.005]
            )
            
            # Revenue based on size
            size_revenue = {
                'micro': (10000, 100000),
                'small': (100000, 1000000), 
                'medium': (1000000, 10000000),
                'large': (10000000, 50000000)
            }
            
            min_rev, max_rev = size_revenue[company_size]
            annual_revenue = np.random.uniform(min_rev, max_rev)
            
            # Employee count
            size_employees = {
                'micro': (1, 9), 'small': (10, 49), 
                'medium': (50, 249), 'large': (250, 1000)
            }
            min_emp, max_emp = size_employees[company_size]
            employee_count = np.random.randint(min_emp, max_emp + 1)
            
            # Geographic concentration
            headquarters = np.random.choice(
                ['Tunis', 'Sfax', 'Sousse', 'Ariana', 'Monastir'] + self.governorates[5:],
                p=[0.4, 0.15, 0.1, 0.08, 0.05] + [0.22/7]*7
            )
            
            # Digital maturity based on sector and size
            digital_base = 0.3
            if sector == 'technology':
                digital_base += 0.4
            if company_size in ['medium', 'large']:
                digital_base += 0.2
            
            digital_maturity = min(1.0, max(0.1, digital_base + np.random.normal(0, 0.15)))
            
            company = {
                'client_id': f'C_{i+1:05d}',
                'company_name': f'Company_{sector.title()}_{i+1:03d}',
                'business_sector': sector,
                'company_size': company_size,
                'employee_count': employee_count,
                'annual_revenue': round(annual_revenue, 2),
                'headquarters_governorate': headquarters,
                'credit_rating': np.random.choice(['A', 'B', 'C', 'D'], p=[0.2, 0.4, 0.3, 0.1]),
                'digital_maturity_score': round(digital_maturity, 3),
                'cash_flow_predictability': round(np.random.beta(3, 2), 3),
                'seasonal_variation': round(np.random.beta(2, 3), 3)
            }
            companies.append(company)
        
        return pd.DataFrame(companies)
    
    def save_to_database(self, retail_df, corporate_df):
        """Save data to PostgreSQL database"""
        logger.info("Saving data to database...")
        
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            
            # Insert retail clients
            for _, client in retail_df.iterrows():
                # Get governorate ID
                cursor.execute("SELECT id FROM ref_governorates WHERE name_en = %s", (client['governorate'],))
                result = cursor.fetchone()
                gov_id = result[0] if result else 1
                
                insert_query = """
                INSERT INTO retail_clients (
                    client_id, first_name, last_name, age, gender, governorate_id,
                    monthly_income, education_level, employment_sector, preferred_channel,
                    risk_tolerance, satisfaction_score, digital_engagement_score, data_source
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (client_id) DO NOTHING
                """
                
                cursor.execute(insert_query, (
                    client['client_id'], client['first_name'], client['last_name'],
                    client['age'], client['gender'], gov_id, client['monthly_income'],
                    client['education_level'], client['employment_sector'], 
                    client['preferred_channel'], client['risk_tolerance'],
                    client['satisfaction_score'], client['digital_engagement_score'], 'mehdi_pipeline'
                ))
            
            # Insert corporate clients
            for _, company in corporate_df.iterrows():
                cursor.execute("SELECT id FROM ref_governorates WHERE name_en = %s", 
                             (company['headquarters_governorate'],))
                result = cursor.fetchone()
                gov_id = result[0] if result else 1
                
                insert_query = """
                INSERT INTO corporate_clients (
                    client_id, company_name, business_sector, company_size,
                    employee_count, annual_revenue, headquarters_governorate_id,
                    credit_rating, digital_maturity_score, data_source
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (client_id) DO NOTHING
                """
                
                cursor.execute(insert_query, (
                    company['client_id'], company['company_name'], company['business_sector'],
                    company['company_size'], company['employee_count'], company['annual_revenue'],
                    gov_id, company['credit_rating'], company['digital_maturity_score'], 'mehdi_pipeline'
                ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Saved {len(retail_df)} retail and {len(corporate_df)} corporate clients to database")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database save failed: {e}")
            return False
    
    def export_for_team(self, retail_df, corporate_df):
        """Export data in formats needed by team members"""
        logger.info("Exporting data for team coordination...")
        
        # For Hamza (Agent Engine) - CSV format with agent-ready structure
        hamza_retail = retail_df[['client_id', 'age', 'governorate', 'monthly_income', 
                                'risk_tolerance', 'satisfaction_score', 'digital_engagement_score',
                                'preferred_channel']].copy()
        
        hamza_corporate = corporate_df[['client_id', 'company_name', 'business_sector', 
                                      'company_size', 'annual_revenue', 'digital_maturity_score',
                                      'headquarters_governorate']].copy()
        
        hamza_retail.to_csv(self.output_dir / "hamza_retail_agents.csv", index=False)
        hamza_corporate.to_csv(self.output_dir / "hamza_corporate_agents.csv", index=False)
        
        # For Nessrine (Visualization) - Summary statistics
        nessrine_summary = {
            'generation_time': datetime.now().isoformat(),
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
        
        with open(self.output_dir / "nessrine_dashboard_data.json", 'w') as f:
            json.dump(nessrine_summary, f, indent=2, default=str)
        
        # For Maryem (Simulation) - Client segments for scenario design
        maryem_segments = {
            'high_value_retail': retail_df[retail_df['monthly_income'] > 3000]['client_id'].tolist(),
            'young_digital': retail_df[(retail_df['age'] < 35) & 
                                     (retail_df['digital_engagement_score'] > 0.7)]['client_id'].tolist(),
            'large_corporates': corporate_df[corporate_df['company_size'] == 'large']['client_id'].tolist(),
            'tech_companies': corporate_df[corporate_df['business_sector'] == 'technology']['client_id'].tolist()
        }
        
        with open(self.output_dir / "maryem_client_segments.json", 'w') as f:
            json.dump(maryem_segments, f, indent=2)
        
        logger.info("✅ Exported data for all team members")
        
        return {
            'hamza_files': ['hamza_retail_agents.csv', 'hamza_corporate_agents.csv'],
            'nessrine_files': ['nessrine_dashboard_data.json'],
            'maryem_files': ['maryem_client_segments.json']
        }
    
    def run_week1_pipeline(self):
        """Execute Week 1 deliverables for Mehdi"""
        logger.info("🚀 Running Week 1 Data Generation Pipeline...")
        
        start_time = datetime.now()
        
        # Generate data
        retail_df = self.generate_retail_clients(1000)
        corporate_df = self.generate_corporate_clients(200)
        
        # Save to database
        db_success = self.save_to_database(retail_df, corporate_df)
        
        # Export for team
        export_files = self.export_for_team(retail_df, corporate_df)
        
        # Create pipeline report
        duration = (datetime.now() - start_time).total_seconds()
        report = {
            'pipeline_execution': 'mehdi_week1_foundation',
            'execution_time': duration,
            'retail_clients_generated': len(retail_df),
            'corporate_clients_generated': len(corporate_df),
            'database_save_success': db_success,
            'export_files': export_files,
            'quality_metrics': {
                'income_range': f"{retail_df['monthly_income'].min():.0f}-{retail_df['monthly_income'].max():.0f} TND",
                'age_range': f"{retail_df['age'].min()}-{retail_df['age'].max()}",
                'governorate_coverage': retail_df['governorate'].nunique(),
                'corporate_sectors': corporate_df['business_sector'].nunique()
            }
        }
        
        with open(self.output_dir / "week1_pipeline_report.json", 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"🎉 Week 1 pipeline completed in {duration:.1f} seconds")
        logger.info(f"📊 Generated {len(retail_df)} retail + {len(corporate_df)} corporate clients")
        logger.info(f"📁 Team files available in: {self.output_dir}")
        
        return report

if __name__ == "__main__":
    pipeline = MehdiDataPipeline()
    result = pipeline.run_week1_pipeline()
    
    print("\\n🎯 WEEK 1 DELIVERABLES COMPLETED!")
    print("=" * 50)
    print(f"✅ {result['retail_clients_generated']} retail clients generated")
    print(f"✅ {result['corporate_clients_generated']} corporate clients generated") 
    print(f"✅ Database populated: {result['database_save_success']}")
    print("\\n📦 Files ready for team:")
    for team_member, files in result['export_files'].items():
        print(f"   {team_member}: {', '.join(files)}")
    
    print("\\n🚀 Next: Start Week 2 CTGAN implementation!")
