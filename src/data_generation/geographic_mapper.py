#!/usr/bin/env python3
"""
COMPLETE TUNISIAN GEOGRAPHIC MAPPING SYSTEM - WEEK 3
Professional implementation with all missing methods completed.
Precise geographic data integration with economic indicators and regional adjustments.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TunisianGeographicMapper:
    """Complete Tunisian geographic data integration with all implementations"""
    
    def __init__(self):
        self.governorate_data = self._initialize_governorate_data()
        self.delegation_data = self._initialize_delegation_data()
        self.economic_indicators = self._initialize_economic_indicators()
        self.regional_multipliers = self._initialize_regional_multipliers()
        
        logger.info("🗺️ Complete Tunisian Geographic Mapper initialized")
    
    def _initialize_governorate_data(self) -> Dict:
        """Initialize comprehensive governorate data with INS Tunisia statistics"""
        
        return {
            'Tunis': {
                'code': 'TUN', 'region': 'North', 'population': 1056247,
                'postal_prefix': '10', 'economic_zone': 'urban_primary',
                'gdp_per_capita_tnd': 12500, 'unemployment_rate': 0.12,
                'banking_penetration': 0.85, 'digital_readiness': 0.78,
                'cost_of_living_index': 1.4, 'business_environment_score': 0.85
            },
            'Ariana': {
                'code': 'ARI', 'region': 'North', 'population': 576088,
                'postal_prefix': '20', 'economic_zone': 'urban_secondary', 
                'gdp_per_capita_tnd': 11200, 'unemployment_rate': 0.14,
                'banking_penetration': 0.82, 'digital_readiness': 0.75,
                'cost_of_living_index': 1.3, 'business_environment_score': 0.80
            },
            'Ben Arous': {
                'code': 'BEN', 'region': 'North', 'population': 631842,
                'postal_prefix': '25', 'economic_zone': 'industrial_secondary',
                'gdp_per_capita_tnd': 10800, 'unemployment_rate': 0.15,
                'banking_penetration': 0.78, 'digital_readiness': 0.70,
                'cost_of_living_index': 1.25, 'business_environment_score': 0.75
            },
            'Sfax': {
                'code': 'SFA', 'region': 'Center', 'population': 955421,
                'postal_prefix': '30', 'economic_zone': 'industrial_primary',
                'gdp_per_capita_tnd': 9800, 'unemployment_rate': 0.16,
                'banking_penetration': 0.75, 'digital_readiness': 0.65,
                'cost_of_living_index': 1.1, 'business_environment_score': 0.78
            },
            'Sousse': {
                'code': 'SOU', 'region': 'Center', 'population': 674971,
                'postal_prefix': '40', 'economic_zone': 'tourism_industrial',
                'gdp_per_capita_tnd': 8900, 'unemployment_rate': 0.18,
                'banking_penetration': 0.72, 'digital_readiness': 0.62,
                'cost_of_living_index': 1.05, 'business_environment_score': 0.72
            },
            'Monastir': {
                'code': 'MON', 'region': 'Center', 'population': 548828,
                'postal_prefix': '50', 'economic_zone': 'tourism_agriculture',
                'gdp_per_capita_tnd': 8200, 'unemployment_rate': 0.19,
                'banking_penetration': 0.68, 'digital_readiness': 0.58,
                'cost_of_living_index': 1.0, 'business_environment_score': 0.68
            },
            'Nabeul': {
                'code': 'NAB', 'region': 'North', 'population': 787920,
                'postal_prefix': '80', 'economic_zone': 'tourism_agriculture',
                'gdp_per_capita_tnd': 8500, 'unemployment_rate': 0.17,
                'banking_penetration': 0.70, 'digital_readiness': 0.60,
                'cost_of_living_index': 1.15, 'business_environment_score': 0.70
            },
            'Kairouan': {
                'code': 'KAI', 'region': 'Center', 'population': 570559,
                'postal_prefix': '31', 'economic_zone': 'agriculture_traditional',
                'gdp_per_capita_tnd': 6800, 'unemployment_rate': 0.22,
                'banking_penetration': 0.58, 'digital_readiness': 0.45,
                'cost_of_living_index': 0.85, 'business_environment_score': 0.60
            },
            'Bizerte': {
                'code': 'BIZ', 'region': 'North', 'population': 568219,
                'postal_prefix': '70', 'economic_zone': 'industrial_tourism',
                'gdp_per_capita_tnd': 7800, 'unemployment_rate': 0.20,
                'banking_penetration': 0.65, 'digital_readiness': 0.55,
                'cost_of_living_index': 0.95, 'business_environment_score': 0.65
            },
            'Gafsa': {
                'code': 'GAF', 'region': 'South', 'population': 337331,
                'postal_prefix': '21', 'economic_zone': 'mining_traditional',
                'gdp_per_capita_tnd': 6200, 'unemployment_rate': 0.25,
                'banking_penetration': 0.52, 'digital_readiness': 0.40,
                'cost_of_living_index': 0.80, 'business_environment_score': 0.55
            }
        }
    
    def _initialize_delegation_data(self) -> Dict:
        """Initialize delegation-level data with economic characteristics"""
        
        return {
            'Tunis': {
                'Tunis': {'economic_activity': 'financial_services', 'development_level': 'high'},
                'La Medina': {'economic_activity': 'tourism_heritage', 'development_level': 'medium'},
                'Bab Bhar': {'economic_activity': 'commercial', 'development_level': 'high'},
                'Omrane': {'economic_activity': 'residential_services', 'development_level': 'medium'}
            },
            'Ariana': {
                'Ariana Ville': {'economic_activity': 'residential_tech', 'development_level': 'high'},
                'Soukra': {'economic_activity': 'residential_upscale', 'development_level': 'high'},
                'Raoued': {'economic_activity': 'industrial_tech', 'development_level': 'medium'},
                'Kalaat Andalous': {'economic_activity': 'residential', 'development_level': 'medium'}
            },
            'Sfax': {
                'Sfax Ville': {'economic_activity': 'industrial_commercial', 'development_level': 'high'},
                'Sfax Sud': {'economic_activity': 'industrial_heavy', 'development_level': 'medium'},
                'Sakiet Eddaier': {'economic_activity': 'industrial_logistics', 'development_level': 'medium'},
                'Hencha': {'economic_activity': 'agriculture_processing', 'development_level': 'low'}
            },
            'Sousse': {
                'Sousse Ville': {'economic_activity': 'tourism_commercial', 'development_level': 'high'},
                'Kalaa Kebira': {'economic_activity': 'agriculture', 'development_level': 'low'},
                'Kondar': {'economic_activity': 'residential', 'development_level': 'medium'},
                'Msaken': {'economic_activity': 'textile_manufacturing', 'development_level': 'medium'}
            },
            'Monastir': {
                'Monastir': {'economic_activity': 'tourism_education', 'development_level': 'high'},
                'Ksar Hellal': {'economic_activity': 'textile_manufacturing', 'development_level': 'medium'},
                'Moknine': {'economic_activity': 'agriculture_fishing', 'development_level': 'low'},
                'Bekalta': {'economic_activity': 'agriculture', 'development_level': 'low'}
            }
        }
    
    def _initialize_economic_indicators(self) -> Dict:
        """Initialize comprehensive economic indicators by region"""
        
        return {
            'regional_indicators': {
                'North': {
                    'average_gdp_per_capita': 11000,
                    'employment_rate': 0.82,
                    'urban_percentage': 0.85,
                    'banking_density_per_1000': 2.1,
                    'digital_infrastructure_index': 0.75
                },
                'Center': {
                    'average_gdp_per_capita': 8200,
                    'employment_rate': 0.78,
                    'urban_percentage': 0.65,
                    'banking_density_per_1000': 1.6,
                    'digital_infrastructure_index': 0.60
                },
                'South': {
                    'average_gdp_per_capita': 6500,
                    'employment_rate': 0.72,
                    'urban_percentage': 0.45,
                    'banking_density_per_1000': 1.1,
                    'digital_infrastructure_index': 0.45
                }
            },
            'sector_concentrations': {
                'financial_services': ['Tunis', 'Ariana', 'Sfax'],
                'manufacturing': ['Sfax', 'Sousse', 'Ben Arous'],
                'tourism': ['Sousse', 'Monastir', 'Nabeul'],
                'agriculture': ['Kairouan', 'Bizerte', 'Gafsa'],
                'technology': ['Tunis', 'Ariana']
            }
        }
    
    def _initialize_regional_multipliers(self) -> Dict:
        """Initialize regional economic multipliers for income/revenue adjustment"""
        
        return {
            'income_multipliers': {
                'Tunis': 1.35,      # Highest salaries
                'Ariana': 1.25,     # High-income suburb
                'Ben Arous': 1.15,  # Industrial zone
                'Sfax': 1.10,       # Major industrial center
                'Nabeul': 1.05,     # Tourism/agriculture
                'Sousse': 1.00,     # Baseline (national average)
                'Monastir': 0.95,   # Tourism/education
                'Bizerte': 0.90,    # Mixed economy
                'Kairouan': 0.80,   # Traditional/agriculture
                'Gafsa': 0.75       # Mining/traditional
            },
            'business_multipliers': {
                'Tunis': 1.40,      # Financial center
                'Ariana': 1.30,     # Tech hub
                'Sfax': 1.25,       # Industrial/commercial
                'Ben Arous': 1.20,  # Industrial
                'Sousse': 1.15,     # Tourism/commerce
                'Nabeul': 1.10,     # Tourism/handicrafts
                'Monastir': 1.05,   # Tourism/textiles
                'Bizerte': 1.00,    # Baseline
                'Kairouan': 0.85,   # Traditional crafts
                'Gafsa': 0.80       # Mining/limited diversity
            },
            'cost_adjustments': {
                'Tunis': 1.45,      # Highest costs
                'Ariana': 1.35,     # High costs
                'Ben Arous': 1.25,  # Moderate-high costs
                'Sfax': 1.15,       # Moderate costs
                'Nabeul': 1.10,     # Moderate costs
                'Sousse': 1.05,     # Slightly above average
                'Monastir': 1.00,   # Average costs
                'Bizerte': 0.95,    # Below average
                'Kairouan': 0.85,   # Low costs
                'Gafsa': 0.80       # Lowest costs
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
        for indicator in ['gdp_per_capita_tnd', 'unemployment_rate', 'banking_penetration', 'digital_readiness']:
            enhanced_df[indicator] = enhanced_df['governorate'].map(
                {gov: data[indicator] for gov, data in self.governorate_data.items()}
            )
        
        # Add regional classification
        enhanced_df['region'] = enhanced_df['governorate'].map(
            {gov: data['region'] for gov, data in self.governorate_data.items()}
        )
        
        # Add economic zone classification
        enhanced_df['economic_zone'] = enhanced_df['governorate'].map(
            {gov: data['economic_zone'] for gov, data in self.governorate_data.items()}
        )
        
        # Add regional economic impact on income/revenue
        if data_type == 'retail' and 'monthly_income' in enhanced_df.columns:
            enhanced_df = self._adjust_income_by_geography(enhanced_df)
        elif data_type == 'corporate' and 'annual_revenue' in enhanced_df.columns:
            enhanced_df = self._adjust_revenue_by_geography(enhanced_df)
        
        # Add cost of living adjustments
        enhanced_df['cost_of_living_index'] = enhanced_df['governorate'].map(
            {gov: data.get('cost_of_living_index', 1.0) for gov, data in self.governorate_data.items()}
        )
        
        # Add business environment scores for corporate clients
        if data_type == 'corporate':
            enhanced_df['business_environment_score'] = enhanced_df['governorate'].map(
                {gov: data.get('business_environment_score', 0.5) for gov, data in self.governorate_data.items()}
            )
        
        logger.info(f"✅ Geographic enhancement completed")
        return enhanced_df
    
    def _generate_postal_code(self, governorate: str) -> str:
        """Generate realistic postal code for governorate"""
        gov_data = self.governorate_data.get(governorate, self.governorate_data['Tunis'])
        prefix = gov_data['postal_prefix']
        suffix = np.random.randint(10, 99)
        return f"{prefix}{suffix:02d}"
    
    def _assign_delegation(self, governorate: str) -> str:
        """Assign delegation based on governorate with realistic distribution"""
        delegation_data = self.delegation_data.get(governorate)
        
        if delegation_data:
            delegations = list(delegation_data.keys())
            # Weight delegations by development level (higher development = more likely)
            weights = []
            for delegation in delegations:
                dev_level = delegation_data[delegation]['development_level']
                weight = {'high': 0.5, 'medium': 0.3, 'low': 0.2}[dev_level]
                weights.append(weight)
            
            # Normalize weights
            total_weight = sum(weights)
            weights = [w/total_weight for w in weights]
            
            return np.random.choice(delegations, p=weights)
        else:
            # Fallback for governorates not in delegation data
            return f"{governorate}_Center"
    
    def _adjust_income_by_geography(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adjust retail client income based on geographic economic factors"""
        
        enhanced_df = df.copy()
        
        # Apply regional income multipliers
        income_multipliers = self.regional_multipliers['income_multipliers']
        cost_adjustments = self.regional_multipliers['cost_adjustments']
        
        for governorate in enhanced_df['governorate'].unique():
            if governorate in income_multipliers:
                # Get multipliers
                income_mult = income_multipliers[governorate]
                cost_mult = cost_adjustments[governorate]
                
                # Apply adjustments
                mask = enhanced_df['governorate'] == governorate
                
                # Adjust base income by regional multiplier
                enhanced_df.loc[mask, 'monthly_income'] *= income_mult
                
                # Add some realistic variation (±15%)
                variation = np.random.normal(1.0, 0.15, mask.sum())
                enhanced_df.loc[mask, 'monthly_income'] *= variation
                
                # Ensure income stays within reasonable bounds
                enhanced_df.loc[mask, 'monthly_income'] = enhanced_df.loc[mask, 'monthly_income'].clip(400, 15000)
                
                # Add cost-adjusted purchasing power indicator
                enhanced_df.loc[mask, 'purchasing_power_index'] = (
                    enhanced_df.loc[mask, 'monthly_income'] / (cost_mult * 1000)
                )
        
        # Add economic context indicators
        enhanced_df['income_percentile_regional'] = enhanced_df.groupby('governorate')['monthly_income'].rank(pct=True)
        
        # Add employment sector adjustments based on regional economy
        enhanced_df = self._adjust_income_by_sector_and_region(enhanced_df)
        
        return enhanced_df
    
    def _adjust_revenue_by_geography(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adjust corporate client revenue based on geographic business environment"""
        
        enhanced_df = df.copy()
        
        business_multipliers = self.regional_multipliers['business_multipliers']
        cost_adjustments = self.regional_multipliers['cost_adjustments']
        
        for governorate in enhanced_df['headquarters_governorate'].unique():
            if governorate in business_multipliers:
                # Get multipliers
                business_mult = business_multipliers[governorate]
                cost_mult = cost_adjustments[governorate]
                
                # Apply adjustments
                mask = enhanced_df['headquarters_governorate'] == governorate
                
                # Adjust base revenue by regional business environment
                enhanced_df.loc[mask, 'annual_revenue'] *= business_mult
                
                # Add sector-specific adjustments
                enhanced_df = self._apply_sector_geographic_adjustments(enhanced_df, mask, governorate)
                
                # Add realistic business variation (±25% for more volatility)
                variation = np.random.lognormal(0, 0.25, mask.sum())
                enhanced_df.loc[mask, 'annual_revenue'] *= variation
                
                # Ensure revenue stays within reasonable bounds for company size
                enhanced_df = self._enforce_size_revenue_bounds(enhanced_df, mask)
                
                # Add business context indicators
                enhanced_df.loc[mask, 'regional_competitiveness_index'] = (
                    enhanced_df.loc[mask, 'annual_revenue'] / 
                    enhanced_df.loc[mask, 'annual_revenue'].median()
                )
        
        # Add market share indicators within region
        enhanced_df['market_position_regional'] = enhanced_df.groupby(['headquarters_governorate', 'business_sector'])['annual_revenue'].rank(pct=True)
        
        return enhanced_df
    
    def _adjust_income_by_sector_and_region(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply sector-specific income adjustments based on regional specializations"""
        
        # Regional sector premiums (sectors that pay more in specific regions)
        sector_regional_premiums = {
            'Tunis': {
                'private': 1.2,      # Financial services premium
                'public': 1.1,       # Government center
                'self_employed': 1.15 # Professional services
            },
            'Ariana': {
                'private': 1.15,     # Tech sector premium
                'self_employed': 1.1  # Tech freelancers
            },
            'Sfax': {
                'private': 1.1,      # Industrial premium
                'self_employed': 1.05 # Commercial activities
            }
        }
        
        for governorate, sector_premiums in sector_regional_premiums.items():
            for sector, premium in sector_premiums.items():
                mask = (df['governorate'] == governorate) & (df['employment_sector'] == sector)
                if mask.any():
                    df.loc[mask, 'monthly_income'] *= premium
        
        return df
    
    def _apply_sector_geographic_adjustments(self, df: pd.DataFrame, mask: pd.Series, governorate: str) -> pd.DataFrame:
        """Apply sector-specific geographic adjustments for corporate revenue"""
        
        # Sector advantages by governorate
        sector_advantages = {
            'Tunis': {
                'services': 1.25,     # Financial services hub
                'technology': 1.30,   # Tech ecosystem
                'retail': 1.15        # Wealthy consumer base
            },
            'Ariana': {
                'technology': 1.35,   # Tech hub
                'services': 1.20      # Business services
            },
            'Sfax': {
                'manufacturing': 1.20, # Industrial center
                'services': 1.10,     # Commercial services
                'retail': 1.05        # Commercial hub
            },
            'Sousse': {
                'services': 1.15,     # Tourism services
                'retail': 1.10,       # Tourism retail
                'manufacturing': 1.05  # Textile industry
            }
        }
        
        if governorate in sector_advantages:
            for sector, multiplier in sector_advantages[governorate].items():
                sector_mask = mask & (df['business_sector'] == sector)
                if sector_mask.any():
                    df.loc[sector_mask, 'annual_revenue'] *= multiplier
        
        return df
    
    def _enforce_size_revenue_bounds(self, df: pd.DataFrame, mask: pd.Series) -> pd.DataFrame:
        """Ensure revenue stays within realistic bounds for company size"""
        
        size_bounds = {
            'micro': (10000, 200000),
            'small': (200000, 2000000),
            'medium': (2000000, 20000000),
            'large': (20000000, 200000000)
        }
        
        for size, (min_rev, max_rev) in size_bounds.items():
            size_mask = mask & (df['company_size'] == size)
            if size_mask.any():
                df.loc[size_mask, 'annual_revenue'] = df.loc[size_mask, 'annual_revenue'].clip(min_rev, max_rev)
        
        return df
    
    def generate_geographic_distribution_report(self, df: pd.DataFrame) -> Dict:
        """Generate comprehensive geographic distribution analysis"""
        
        report = {
            'geographic_analysis': {
                'total_samples': len(df),
                'governorate_distribution': df['governorate'].value_counts().to_dict() if 'governorate' in df.columns else {},
                'regional_distribution': {},
                'postal_code_coverage': len(df['postal_code'].unique()) if 'postal_code' in df.columns else 0,
                'delegation_coverage': len(df['delegation'].unique()) if 'delegation' in df.columns else 0
            },
            'economic_impact_analysis': {},
            'banking_infrastructure_analysis': {},
            'regional_competitiveness': {}
        }
        
        # Regional distribution analysis
        if 'region' in df.columns:
            for region in ['North', 'Center', 'South']:
                region_count = (df['region'] == region).sum()
                report['geographic_analysis']['regional_distribution'][region] = region_count
        
        # Economic impact analysis
        if 'gdp_per_capita_tnd' in df.columns:
            economic_analysis = {
                'average_gdp_per_capita': float(df['gdp_per_capita_tnd'].mean()),
                'gdp_standard_deviation': float(df['gdp_per_capita_tnd'].std()),
                'economic_diversity_index': len(df['governorate'].unique()) / len(self.governorate_data),
                'wealth_concentration': {
                    'high_gdp_regions_percentage': float((df['gdp_per_capita_tnd'] > 10000).mean()),
                    'low_gdp_regions_percentage': float((df['gdp_per_capita_tnd'] < 7000).mean())
                }
            }
            report['economic_impact_analysis'] = economic_analysis
        
        # Banking infrastructure analysis
        if 'banking_penetration' in df.columns:
            banking_analysis = {
                'average_banking_penetration': float(df['banking_penetration'].mean()),
                'digital_readiness_average': float(df['digital_readiness'].mean()) if 'digital_readiness' in df.columns else 0,
                'infrastructure_gaps': {
                    'low_penetration_areas': (df['banking_penetration'] < 0.6).sum(),
                    'high_digital_readiness_areas': (df['digital_readiness'] > 0.7).sum() if 'digital_readiness' in df.columns else 0
                }
            }
            report['banking_infrastructure_analysis'] = banking_analysis
        
        # Regional competitiveness analysis
        if 'business_environment_score' in df.columns:
            competitiveness_analysis = {
                'average_business_environment': float(df['business_environment_score'].mean()),
                'top_business_regions': df.groupby('governorate')['business_environment_score'].first().nlargest(3).to_dict(),
                'investment_attractiveness': {
                    'high_score_regions': (df['business_environment_score'] > 0.75).sum(),
                    'improvement_needed_regions': (df['business_environment_score'] < 0.65).sum()
                }
            }
            report['regional_competitiveness'] = competitiveness_analysis
        
        # Income/Revenue geographic patterns
        if 'monthly_income' in df.columns:
            income_patterns = self._analyze_income_geographic_patterns(df)
            report['income_geographic_patterns'] = income_patterns
        elif 'annual_revenue' in df.columns:
            revenue_patterns = self._analyze_revenue_geographic_patterns(df)
            report['revenue_geographic_patterns'] = revenue_patterns
        
        return report
    
    def _analyze_income_geographic_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze income patterns across geographic regions"""
        
        patterns = {
            'income_by_governorate': df.groupby('governorate')['monthly_income'].agg(['mean', 'median', 'std']).to_dict(),
            'income_by_region': df.groupby('region')['monthly_income'].agg(['mean', 'median']).to_dict() if 'region' in df.columns else {},
            'purchasing_power_analysis': {}
        }
        
        # Purchasing power analysis
        if 'purchasing_power_index' in df.columns:
            patterns['purchasing_power_analysis'] = {
                'average_purchasing_power': float(df['purchasing_power_index'].mean()),
                'highest_purchasing_power_regions': df.groupby('governorate')['purchasing_power_index'].mean().nlargest(3).to_dict(),
                'income_cost_correlation': float(df['monthly_income'].corr(df['cost_of_living_index'])) if 'cost_of_living_index' in df.columns else 0
            }
        
        return patterns
    
    def _analyze_revenue_geographic_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze revenue patterns across geographic regions for corporate clients"""
        
        patterns = {
            'revenue_by_governorate': df.groupby('headquarters_governorate')['annual_revenue'].agg(['mean', 'median', 'std']).to_dict(),
            'revenue_by_region': df.groupby('region')['annual_revenue'].agg(['mean', 'median']).to_dict() if 'region' in df.columns else {},
            'business_competitiveness_analysis': {}
        }
        
        # Business competitiveness analysis
        if 'regional_competitiveness_index' in df.columns:
            patterns['business_competitiveness_analysis'] = {
                'average_competitiveness': float(df['regional_competitiveness_index'].mean()),
                'most_competitive_regions': df.groupby('headquarters_governorate')['regional_competitiveness_index'].mean().nlargest(3).to_dict(),
                'sector_geographic_concentration': self._analyze_sector_geographic_concentration(df)
            }
        
        return patterns
    
    def _analyze_sector_geographic_concentration(self, df: pd.DataFrame) -> Dict:
        """Analyze how business sectors concentrate geographically"""
        
        concentration_analysis = {}
        
        if 'business_sector' in df.columns and 'headquarters_governorate' in df.columns:
            for sector in df['business_sector'].unique():
                sector_data = df[df['business_sector'] == sector]
                gov_distribution = sector_data['headquarters_governorate'].value_counts(normalize=True)
                
                # Calculate concentration index (Herfindahl-Hirschman Index)
                hhi = (gov_distribution ** 2).sum()
                
                concentration_analysis[sector] = {
                    'concentration_index': float(hhi),
                    'concentration_level': 'high' if hhi > 0.25 else 'medium' if hhi > 0.15 else 'low',
                    'top_regions': gov_distribution.head(2).to_dict(),
                    'geographic_spread': len(gov_distribution)
                }
        
        return concentration_analysis
    
    def export_geographic_enhancement_report(self, df: pd.DataFrame, output_path: str) -> str:
        """Export comprehensive geographic enhancement report"""
        
        report = self.generate_geographic_distribution_report(df)
        
        # Add metadata
        report['enhancement_metadata'] = {
            'enhancement_timestamp': datetime.now().isoformat(),
            'total_records_enhanced': len(df),
            'governorates_covered': len(df['governorate'].unique()) if 'governorate' in df.columns else 0,
            'economic_indicators_added': [
                'gdp_per_capita_tnd', 'unemployment_rate', 'banking_penetration', 
                'digital_readiness', 'cost_of_living_index'
            ],
            'geographic_precision_level': 'delegation_level'
        }
        
        # Save report
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"🗺️ Geographic enhancement report exported: {output_path}")
        
        return output_path
    
    def get_governorate_economic_profile(self, governorate: str) -> Dict:
        """Get comprehensive economic profile for a specific governorate"""
        
        if governorate not in self.governorate_data:
            return {'error': f'Governorate {governorate} not found'}
        
        gov_data = self.governorate_data[governorate]
        
        profile = {
            'basic_info': {
                'governorate': governorate,
                'code': gov_data['code'],
                'region': gov_data['region'],
                'population': gov_data['population']
            },
            'economic_indicators': {
                'gdp_per_capita_tnd': gov_data['gdp_per_capita_tnd'],
                'unemployment_rate': gov_data['unemployment_rate'],
                'economic_zone': gov_data['economic_zone']
            },
            'financial_infrastructure': {
                'banking_penetration': gov_data['banking_penetration'],
                'digital_readiness': gov_data['digital_readiness']
            },
            'business_environment': {
                'business_environment_score': gov_data.get('business_environment_score', 0.5),
                'cost_of_living_index': gov_data.get('cost_of_living_index', 1.0)
            },
            'multipliers': {
                'income_multiplier': self.regional_multipliers['income_multipliers'].get(governorate, 1.0),
                'business_multiplier': self.regional_multipliers['business_multipliers'].get(governorate, 1.0),
                'cost_adjustment': self.regional_multipliers['cost_adjustments'].get(governorate, 1.0)
            }
        }
        
        return profile


# Example usage and testing
if __name__ == "__main__":
    # Test the complete geographic mapper
    mapper = TunisianGeographicMapper()
    
    # Create sample data for testing
    sample_retail = pd.DataFrame({
        'client_id': ['R_001', 'R_002', 'R_003', 'R_004', 'R_005'] * 20,
        'governorate': np.random.choice(['Tunis', 'Sfax', 'Sousse', 'Ariana'], 100),
        'monthly_income': np.random.uniform(800, 5000, 100),
        'employment_sector': np.random.choice(['private', 'public', 'self_employed'], 100)
    })
    
    sample_corporate = pd.DataFrame({
        'client_id': ['C_001', 'C_002', 'C_003', 'C_004', 'C_005'] * 10,
        'headquarters_governorate': np.random.choice(['Tunis', 'Sfax', 'Sousse', 'Ariana'], 50),
        'annual_revenue': np.random.uniform(100000, 5000000, 50),
        'business_sector': np.random.choice(['services', 'manufacturing', 'retail'], 50),
        'company_size': np.random.choice(['micro', 'small', 'medium'], 50)
    })
    
    try:
        # Test retail enhancement
        enhanced_retail = mapper.enhance_geographic_precision(sample_retail, 'retail')
        print("🎯 Retail geographic enhancement completed!")
        print(f"Enhanced columns: {list(enhanced_retail.columns)}")
        
        # Test corporate enhancement
        enhanced_corporate = mapper.enhance_geographic_precision(sample_corporate, 'corporate')
        print("🎯 Corporate geographic enhancement completed!")
        
        # Generate reports
        retail_report = mapper.generate_geographic_distribution_report(enhanced_retail)
        corporate_report = mapper.generate_geographic_distribution_report(enhanced_corporate)
        
        print(f"📊 Reports generated successfully!")
        print(f"Retail governorates covered: {len(retail_report['geographic_analysis']['governorate_distribution'])}")
        print(f"Corporate regions covered: {len(corporate_report['geographic_analysis']['regional_distribution'])}")
        
        # Test economic profile
        tunis_profile = mapper.get_governorate_economic_profile('Tunis')
        print(f"🏛️ Tunis economic profile: GDP per capita = {tunis_profile['economic_indicators']['gdp_per_capita_tnd']} TND")
        
    except Exception as e:
        print(f"❌ Geographic mapper test failed: {e}")
    
    print("\n🧪 Complete Geographic Mapper test completed!")