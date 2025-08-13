#!/usr/bin/env python3
"""
Tunisian Geographic Mapping System - Week 3  
Precise geographic data integration with postal codes,
economic indicators, and regional characteristics.
"""

from venv import logger
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
import logging

class TunisianGeographicMapper:
    """Comprehensive Tunisian geographic data integration"""
    
    def __init__(self):
        self.governorate_data = self._initialize_governorate_data()
        self.delegation_data = self._initialize_delegation_data()
        self.economic_indicators = self._initialize_economic_indicators()
        
        logger.info("🗺️ Tunisian Geographic Mapper initialized")
    
    def _initialize_governorate_data(self) -> Dict:
        """Initialize comprehensive governorate data with INS Tunisia statistics"""
        
        return {
            'Tunis': {
                'code': 'TUN', 'region': 'North', 'population': 1056247,
                'postal_prefix': '10', 'economic_zone': 'urban_primary',
                'gdp_per_capita_tnd': 12500, 'unemployment_rate': 0.12,
                'banking_penetration': 0.85, 'digital_readiness': 0.78
            },
            'Ariana': {
                'code': 'ARI', 'region': 'North', 'population': 576088,
                'postal_prefix': '20', 'economic_zone': 'urban_secondary', 
                'gdp_per_capita_tnd': 11200, 'unemployment_rate': 0.14,
                'banking_penetration': 0.82, 'digital_readiness': 0.75
            },
            'Sfax': {
                'code': 'SFA', 'region': 'Center', 'population': 955421,
                'postal_prefix': '30', 'economic_zone': 'industrial_primary',
                'gdp_per_capita_tnd': 9800, 'unemployment_rate': 0.16,
                'banking_penetration': 0.75, 'digital_readiness': 0.65
            },
            'Sousse': {
                'code': 'SOU', 'region': 'Center', 'population': 674971,
                'postal_prefix': '40', 'economic_zone': 'tourism_industrial',
                'gdp_per_capita_tnd': 8900, 'unemployment_rate': 0.18,
                'banking_penetration': 0.72, 'digital_readiness': 0.62
            },
            'Monastir': {
                'code': 'MON', 'region': 'Center', 'population': 548828,
                'postal_prefix': '50', 'economic_zone': 'tourism_agriculture',
                'gdp_per_capita_tnd': 8200, 'unemployment_rate': 0.19,
                'banking_penetration': 0.68, 'digital_readiness': 0.58
            }
        }
    
    def enhance_geographic_precision(self, df: pd.DataFrame, 
                                   data_type: str) -> pd.DataFrame:
        """Add precise geographic data with economic context"""
        
        logger.info(f"🗺️ Enhancing geographic precision for {len(df)} {data_type} records...")
        
        enhanced_df = df.copy()
        
        # Add postal codes
        enhanced_df['postal_code'] = enhanced_df.apply(
            lambda row: self._generate_postal_code(row.get('governorate', 'Tunis')), axis=1
        )
        
        # Add delegation information
        enhanced_df['delegation'] = enhanced_df.apply(
            lambda row: self._assign_delegation(row.get('governorate', 'Tunis')), axis=1
        )
        
        # Add economic indicators
        for indicator in ['gdp_per_capita_tnd', 'unemployment_rate', 'banking_penetration']:
            enhanced_df[indicator] = enhanced_df['governorate'].map(
                {gov: data[indicator] for gov, data in self.governorate_data.items()}
            )
        
        # Add regional economic impact on income/revenue
        if data_type == 'retail' and 'monthly_income' in enhanced_df.columns:
            enhanced_df = self._adjust_income_by_geography(enhanced_df)
        elif data_type == 'corporate' and 'annual_revenue' in enhanced_df.columns:
            enhanced_df = self._adjust_revenue_by_geography(enhanced_df)
        
        logger.info(f"✅ Geographic enhancement completed")
        return enhanced_df
    
    def _generate_postal_code(self, governorate: str) -> str:
        """Generate realistic postal code for governorate"""
        gov_data = self.governorate_data.get(governorate, self.governorate_data['Tunis'])
        prefix = gov_data['postal_prefix']
        suffix = np.random.randint(10, 99)
        return f"{prefix}{suffix:02d}"
    
    def _assign_delegation(self, governorate: str) -> str:
        """Assign delegation based on governorate"""
        delegation_mapping = {
            'Tunis': ['Tunis', 'La Medina', 'Bab Bhar', 'Omrane'],
            'Ariana': ['Ariana Ville', 'Soukra', 'Raoued', 'Kalaat Andalous'],
            'Sfax': ['Sfax Ville', 'Sfax Sud', 'Sakiet Eddaier', 'Hencha'],
            'Sousse': ['Sousse Ville', 'Kalaa Kebira', 'Kondar', 'Msaken'],
            'Monastir': ['Monastir', 'Ksar Hellal', 'Moknine', 'Bekalta']
        }
        
        delegations = delegation_mapping.get(governorate, delegation_mapping['Tunis'])
        return np.random.choice(delegations)
    
    def generate_geographic_distribution_report(self, df: pd.DataFrame) -> Dict:
        """Generate comprehensive geographic distribution analysis"""
        
        report = {
            'geographic_analysis': {
                'total_samples': len(df),
                'governorate_distribution': df['governorate'].value_counts().to_dict(),
                'regional_distribution': {},
                'postal_code_coverage': len(df['postal_code'].unique()) if 'postal_code' in df.columns else 0
            },
            'economic_impact_analysis': {},
            'banking_infrastructure_analysis': {}
        }
        
        # Regional distribution
        for region in ['North', 'Center', 'South']:
            region_govs = [gov for gov, data in self.governorate_data.items() 
                          if data['region'] == region]
            region_count = df[df['governorate'].isin(region_govs)].shape[0]
            report['geographic_analysis']['regional_distribution'][region] = region_count
        
        # Economic impact analysis
        if 'gdp_per_capita_tnd' in df.columns:
            report['economic_impact_analysis'] = {
                'avg_gdp_per_capita': float(df['gdp_per_capita_tnd'].mean()),
                'economic_diversity_index': len(df['governorate'].unique()) / len(self.governorate_data)
            }
        
        return report