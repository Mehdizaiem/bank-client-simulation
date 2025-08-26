#!/usr/bin/env python3
"""
Tunisian Data Sources Research - Week 1 Foundation
Comprehensive documentation of official Tunisian statistical and financial data sources
"""

import json
from datetime import datetime

class TunisianDataSources:
    """Comprehensive catalog of official Tunisian data sources"""
    
    def __init__(self):
        self.research_date = "2025-08-04"
        self.sources = self._initialize_sources()
    
    def _initialize_sources(self):
        """Initialize all verified Tunisian data sources"""
        return [
            {
                'name': 'Institut National de la Statistique (INS)',
                'organization': 'Ministry of Development, Investment and International Cooperation',
                'url': 'http://www.ins.tn',
                'data_types': [
                    'Population demographics by governorate',
                    'Household income surveys',
                    'Employment statistics by sector',
                    'Education level distribution',
                    'Urban/rural population distribution'
                ],
                'update_frequency': 'Annual',
                'reliability_score': 0.95,
                'notes': 'Primary source for demographic modeling'
            },
            {
                'name': 'Central Bank of Tunisia (BCT) Banking Statistics',
                'organization': 'Banque Centrale de Tunisie',
                'url': 'https://www.bct.gov.tn',
                'data_types': [
                    'Banking penetration rates by governorate',
                    'Credit distribution by sector and size',
                    'Digital banking adoption statistics',
                    'SME financing patterns',
                    'Branch network distribution'
                ],
                'update_frequency': 'Quarterly',
                'reliability_score': 0.98,
                'notes': 'Essential for banking behavior patterns'
            },
            {
                'name': 'World Bank Tunisia Data',
                'organization': 'World Bank Group',
                'url': 'https://data.worldbank.org/country/tunisia',
                'data_types': [
                    'GDP per capita by region',
                    'Financial inclusion indicators',
                    'Digital development index',
                    'Enterprise surveys'
                ],
                'update_frequency': 'Annual',
                'reliability_score': 0.90,
                'notes': 'Good for benchmarking against international standards'
            }
        ]
    
    def get_demographic_parameters(self):
        """Extract key parameters for synthetic data generation"""
        return {
            'population_by_governorate': {
                'Tunis': 1056247,
                'Sfax': 955421,
                'Sousse': 674971,
                'Ariana': 576088,
                'Nabeul': 787920,
                'Monastir': 548828
            },
            'household_income_ranges_tnd': {
                'very_low': (400, 800),
                'low': (800, 1200),
                'middle': (1200, 2500),
                'upper_middle': (2500, 5000),
                'high': (5000, 15000)
            },
            'education_distribution': {
                'primary': 0.25,
                'secondary': 0.45,
                'university': 0.25,
                'postgraduate': 0.05
            },
            'employment_sectors': {
                'private': 0.50,
                'public': 0.25,
                'self_employed': 0.15,
                'unemployed': 0.10
            }
        }
    
    def get_corporate_parameters(self):
        """Corporate sector parameters from Ministry of Industry data"""
        return {
            'size_distribution': {
                'micro': 0.85,
                'small': 0.12,
                'medium': 0.025,
                'large': 0.005
            },
            'sector_distribution': {
                'services': 0.40,
                'manufacturing': 0.25,
                'retail': 0.20,
                'agriculture': 0.10,
                'technology': 0.05
            },
            'revenue_by_size_tnd': {
                'micro': (10000, 100000),
                'small': (100000, 1000000),
                'medium': (1000000, 10000000),
                'large': (10000000, 100000000)
            }
        }
    
    def export_research_report(self, output_path):
        """Export comprehensive research documentation"""
        report = {
            'research_metadata': {
                'research_date': self.research_date,
                'researcher': 'Mehdi (Project Lead)',
                'purpose': 'Week 1 foundation for bank client simulation',
                'total_sources_verified': len(self.sources)
            },
            'data_sources': self.sources,
            'demographic_parameters': self.get_demographic_parameters(),
            'corporate_parameters': self.get_corporate_parameters(),
            'quality_standards': {
                'minimum_sample_size': 1000,
                'income_validation_range': '400-15000 TND',
                'age_validation_range': '18-80 years',
                'minimum_quality_score': 0.85
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Research report exported to: {output_path}")

if __name__ == "__main__":
    sources = TunisianDataSources()
    sources.export_research_report("tunisian_data_sources_research.json")
    print("🔍 Tunisian data sources research completed!")
