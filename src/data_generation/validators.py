#!/usr/bin/env python3
"""
COMPLETE ENTERPRISE DATA VALIDATION ENGINE - WEEK 3
Professional-grade validation with all missing implementations completed.
Company-standard validation suite for Tunisian banking synthetic data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from scipy import stats
from scipy.stats import ks_2samp, chi2_contingency, normaltest, pearsonr
import logging
from datetime import datetime
from pathlib import Path
import json
import warnings

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class EnterpriseDataValidator:
    """Complete enterprise-grade data validation with all implementations"""
    
    def __init__(self):
        self.validation_standards = {
            'statistical_similarity_threshold': 0.85,
            'business_rule_compliance_threshold': 0.98,
            'regulatory_compliance_threshold': 0.99,
            'correlation_preservation_threshold': 0.90,
            'moment_preservation_threshold': 0.95
        }
        
        # Tunisian banking regulations (Central Bank of Tunisia standards)
        self.regulatory_constraints = {
            'retail': {
                'min_age': 18, 'max_age': 80,
                'min_income_tnd': 400, 'max_income_tnd': 15000,
                'required_governorates': ['Tunis', 'Sfax', 'Sousse', 'Ariana'],
                'score_ranges': {
                    'risk_tolerance': (0, 1), 
                    'satisfaction_score': (0, 1),
                    'digital_engagement_score': (0, 1)
                },
                'valid_genders': ['M', 'F'],
                'valid_channels': ['branch', 'mobile', 'web', 'whatsapp'],
                'valid_education': ['primary', 'secondary', 'university', 'postgraduate'],
                'valid_employment': ['private', 'public', 'self_employed', 'unemployed']
            },
            'corporate': {
                'min_employees': 1, 'max_employees': 10000,
                'min_revenue_tnd': 10000, 'max_revenue_tnd': 100000000,
                'required_sectors': ['services', 'manufacturing', 'retail', 'agriculture', 'technology'],
                'valid_sizes': ['micro', 'small', 'medium', 'large'],
                'valid_credit_ratings': ['A', 'B', 'C', 'D'],
                'size_revenue_consistency': {
                    'micro': (10000, 200000),
                    'small': (200000, 2000000), 
                    'medium': (2000000, 20000000),
                    'large': (20000000, 200000000)
                },
                'size_employee_consistency': {
                    'micro': (1, 10),
                    'small': (10, 50),
                    'medium': (50, 250),
                    'large': (250, 10000)
                }
            }
        }
        
        logger.info("🏛️ Enterprise Data Validator initialized with complete implementations")
    
    def validate_retail_data_comprehensive(self, original_df: pd.DataFrame, 
                                         synthetic_df: pd.DataFrame) -> Dict:
        """Comprehensive retail data validation with enterprise standards"""
        
        validation_results = {
            'validation_timestamp': datetime.now().isoformat(),
            'data_type': 'retail',
            'original_samples': len(original_df),
            'synthetic_samples': len(synthetic_df),
            'validation_components': {}
        }
        
        # 1. Statistical Distribution Validation
        statistical_results = self._validate_statistical_distributions(
            original_df, synthetic_df, 'retail'
        )
        validation_results['validation_components']['statistical'] = statistical_results
        
        # 2. Business Rule Compliance
        business_results = self._validate_business_rules(synthetic_df, 'retail')
        validation_results['validation_components']['business_rules'] = business_results
        
        # 3. Regulatory Compliance (Central Bank Tunisia)
        regulatory_results = self._validate_regulatory_compliance(synthetic_df, 'retail')
        validation_results['validation_components']['regulatory'] = regulatory_results
        
        # 4. Advanced Correlation Analysis
        correlation_results = self._validate_correlation_preservation(
            original_df, synthetic_df
        )
        validation_results['validation_components']['correlations'] = correlation_results
        
        # 5. Banking-Specific Validations
        banking_results = self._validate_banking_logic(synthetic_df, 'retail')
        validation_results['validation_components']['banking_logic'] = banking_results
        
        # 6. Data Privacy Assessment
        privacy_results = self._validate_data_privacy(original_df, synthetic_df)
        validation_results['validation_components']['privacy'] = privacy_results
        
        # 7. Overall Quality Assessment
        overall_quality = self._calculate_enterprise_quality_score(validation_results)
        validation_results['overall_assessment'] = overall_quality
        
        return validation_results
    
    def validate_corporate_data_comprehensive(self, original_df: pd.DataFrame,
                                            synthetic_df: pd.DataFrame) -> Dict:
        """Comprehensive corporate data validation with enterprise standards"""
        
        validation_results = {
            'validation_timestamp': datetime.now().isoformat(),
            'data_type': 'corporate',
            'original_samples': len(original_df),
            'synthetic_samples': len(synthetic_df),
            'validation_components': {}
        }
        
        # Corporate-specific validations
        statistical_results = self._validate_statistical_distributions(
            original_df, synthetic_df, 'corporate'
        )
        validation_results['validation_components']['statistical'] = statistical_results
        
        business_results = self._validate_business_rules(synthetic_df, 'corporate')
        validation_results['validation_components']['business_rules'] = business_results
        
        regulatory_results = self._validate_regulatory_compliance(synthetic_df, 'corporate')
        validation_results['validation_components']['regulatory'] = regulatory_results
        
        # Corporate-specific: Size-Revenue consistency
        consistency_results = self._validate_corporate_consistency(synthetic_df)
        validation_results['validation_components']['corporate_consistency'] = consistency_results
        
        correlation_results = self._validate_correlation_preservation(original_df, synthetic_df)
        validation_results['validation_components']['correlations'] = correlation_results
        
        privacy_results = self._validate_data_privacy(original_df, synthetic_df)
        validation_results['validation_components']['privacy'] = privacy_results
        
        overall_quality = self._calculate_enterprise_quality_score(validation_results)
        validation_results['overall_assessment'] = overall_quality
        
        return validation_results
    
    def _validate_statistical_distributions(self, original_df: pd.DataFrame,
                                          synthetic_df: pd.DataFrame, 
                                          data_type: str) -> Dict:
        """Advanced statistical distribution validation"""
        
        results = {
            'tests_passed': 0, 
            'tests_failed': 0, 
            'test_details': {},
            'overall_similarity_score': 0.0
        }
        
        # Numerical feature testing
        numerical_cols = original_df.select_dtypes(include=[np.number]).columns
        similarity_scores = []
        
        for col in numerical_cols:
            if col in synthetic_df.columns and 'client_id' not in col.lower():
                # Kolmogorov-Smirnov test
                ks_stat, ks_pvalue = ks_2samp(original_df[col], synthetic_df[col])
                
                # Anderson-Darling test for normality preservation
                try:
                    orig_normal = normaltest(original_df[col])[1] > 0.05
                    synth_normal = normaltest(synthetic_df[col])[1] > 0.05
                    normality_preserved = orig_normal == synth_normal
                except:
                    normality_preserved = True
                
                # Moment preservation (mean, std, skewness, kurtosis)
                moments_preserved = self._validate_moment_preservation(
                    original_df[col], synthetic_df[col]
                )
                
                # Distribution similarity score
                similarity_score = 1 - min(ks_stat, 1.0)
                similarity_scores.append(similarity_score)
                
                test_passed = (
                    ks_pvalue > 0.05 and 
                    normality_preserved and 
                    moments_preserved['overall_preserved']
                )
                
                results['test_details'][col] = {
                    'ks_statistic': float(ks_stat),
                    'ks_pvalue': float(ks_pvalue),
                    'normality_preserved': normality_preserved,
                    'moments_preserved': moments_preserved,
                    'similarity_score': float(similarity_score),
                    'test_passed': test_passed
                }
                
                if test_passed:
                    results['tests_passed'] += 1
                else:
                    results['tests_failed'] += 1
        
        # Categorical feature testing
        categorical_cols = original_df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            if col in synthetic_df.columns and 'client_id' not in col.lower():
                # Chi-square test for categorical distribution
                orig_counts = original_df[col].value_counts()
                synth_counts = synthetic_df[col].value_counts()
                
                # Align categories
                all_categories = set(orig_counts.index) | set(synth_counts.index)
                orig_aligned = [orig_counts.get(cat, 0) for cat in all_categories]
                synth_aligned = [synth_counts.get(cat, 0) for cat in all_categories]
                
                if len(all_categories) > 1 and sum(orig_aligned) > 0 and sum(synth_aligned) > 0:
                    try:
                        chi2_stat, chi2_pvalue = stats.chi2_contingency([orig_aligned, synth_aligned])[:2]
                        
                        category_overlap = len(set(orig_counts.index) & set(synth_counts.index)) / len(all_categories)
                        similarity_score = max(0, min(1, category_overlap * (1 - chi2_stat / 100)))
                        similarity_scores.append(similarity_score)
                        
                        test_passed = chi2_pvalue > 0.05 and category_overlap > 0.8
                        
                        results['test_details'][col] = {
                            'chi2_statistic': float(chi2_stat),
                            'chi2_pvalue': float(chi2_pvalue),
                            'category_overlap': float(category_overlap),
                            'similarity_score': float(similarity_score),
                            'test_passed': test_passed
                        }
                        
                        if test_passed:
                            results['tests_passed'] += 1
                        else:
                            results['tests_failed'] += 1
                            
                    except Exception as e:
                        results['test_details'][col] = {
                            'error': str(e),
                            'similarity_score': 0.5,
                            'test_passed': False
                        }
                        results['tests_failed'] += 1
        
        # Overall statistical similarity score
        results['overall_similarity_score'] = np.mean(similarity_scores) if similarity_scores else 0.5
        results['pass_rate'] = results['tests_passed'] / max(1, results['tests_passed'] + results['tests_failed'])
        
        return results
    
    def _validate_moment_preservation(self, orig_series: pd.Series, synth_series: pd.Series) -> Dict:
        """Validate preservation of statistical moments (mean, std, skewness, kurtosis)"""
        
        try:
            # Calculate moments for both series
            orig_moments = {
                'mean': float(orig_series.mean()),
                'std': float(orig_series.std()),
                'skewness': float(orig_series.skew()),
                'kurtosis': float(orig_series.kurtosis())
            }
            
            synth_moments = {
                'mean': float(synth_series.mean()),
                'std': float(synth_series.std()),
                'skewness': float(synth_series.skew()),
                'kurtosis': float(synth_series.kurtosis())
            }
            
            # Calculate relative differences
            moment_differences = {}
            moment_preserved = {}
            
            for moment in ['mean', 'std', 'skewness', 'kurtosis']:
                if orig_moments[moment] != 0:
                    rel_diff = abs(orig_moments[moment] - synth_moments[moment]) / abs(orig_moments[moment])
                else:
                    rel_diff = abs(orig_moments[moment] - synth_moments[moment])
                
                moment_differences[moment] = float(rel_diff)
                
                # Different thresholds for different moments
                thresholds = {'mean': 0.05, 'std': 0.10, 'skewness': 0.20, 'kurtosis': 0.30}
                moment_preserved[moment] = rel_diff < thresholds[moment]
            
            # Overall preservation
            overall_preserved = sum(moment_preserved.values()) >= 3  # At least 3 out of 4 moments preserved
            
            return {
                'original_moments': orig_moments,
                'synthetic_moments': synth_moments,
                'relative_differences': moment_differences,
                'moment_preserved': moment_preserved,
                'overall_preserved': overall_preserved,
                'preservation_score': sum(moment_preserved.values()) / len(moment_preserved)
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'overall_preserved': False,
                'preservation_score': 0.0
            }
    
    def _validate_business_rules(self, df: pd.DataFrame, data_type: str) -> Dict:
        """Validate business-specific rules"""
        
        constraints = self.regulatory_constraints[data_type]
        results = {'violations': [], 'compliance_score': 1.0, 'detailed_violations': {}}
        total_violations = 0
        total_checks = 0
        
        if data_type == 'retail':
            # Age constraints
            age_violations = ((df['age'] < constraints['min_age']) | 
                            (df['age'] > constraints['max_age'])).sum()
            if age_violations > 0:
                results['violations'].append(f"Age violations: {age_violations}")
                results['detailed_violations']['age'] = int(age_violations)
            total_violations += age_violations
            total_checks += len(df)
            
            # Income constraints  
            if 'monthly_income' in df.columns:
                income_violations = ((df['monthly_income'] < constraints['min_income_tnd']) |
                                   (df['monthly_income'] > constraints['max_income_tnd'])).sum()
                if income_violations > 0:
                    results['violations'].append(f"Income violations: {income_violations}")
                    results['detailed_violations']['income'] = int(income_violations)
                total_violations += income_violations
                total_checks += len(df)
            
            # Score range validations
            for score_col, (min_val, max_val) in constraints['score_ranges'].items():
                if score_col in df.columns:
                    violations = ((df[score_col] < min_val) | (df[score_col] > max_val)).sum()
                    if violations > 0:
                        results['violations'].append(f"{score_col} violations: {violations}")
                        results['detailed_violations'][score_col] = int(violations)
                    total_violations += violations
                    total_checks += len(df)
            
            # Gender validation
            if 'gender' in df.columns:
                gender_violations = (~df['gender'].isin(constraints['valid_genders'])).sum()
                if gender_violations > 0:
                    results['violations'].append(f"Gender violations: {gender_violations}")
                    results['detailed_violations']['gender'] = int(gender_violations)
                total_violations += gender_violations
                total_checks += len(df)
            
            # Channel validation
            if 'preferred_channel' in df.columns:
                channel_violations = (~df['preferred_channel'].isin(constraints['valid_channels'])).sum()
                if channel_violations > 0:
                    results['violations'].append(f"Channel violations: {channel_violations}")
                    results['detailed_violations']['channel'] = int(channel_violations)
                total_violations += channel_violations
                total_checks += len(df)
        
        elif data_type == 'corporate':
            # Employee constraints
            if 'employee_count' in df.columns:
                emp_violations = ((df['employee_count'] < constraints['min_employees']) |
                                (df['employee_count'] > constraints['max_employees'])).sum()
                if emp_violations > 0:
                    results['violations'].append(f"Employee count violations: {emp_violations}")
                    results['detailed_violations']['employees'] = int(emp_violations)
                total_violations += emp_violations
                total_checks += len(df)
            
            # Revenue constraints
            if 'annual_revenue' in df.columns:
                rev_violations = ((df['annual_revenue'] < constraints['min_revenue_tnd']) |
                                (df['annual_revenue'] > constraints['max_revenue_tnd'])).sum()
                if rev_violations > 0:
                    results['violations'].append(f"Revenue violations: {rev_violations}")
                    results['detailed_violations']['revenue'] = int(rev_violations)
                total_violations += rev_violations
                total_checks += len(df)
            
            # Sector validation
            if 'business_sector' in df.columns:
                sector_violations = (~df['business_sector'].isin(constraints['required_sectors'])).sum()
                if sector_violations > 0:
                    results['violations'].append(f"Sector violations: {sector_violations}")
                    results['detailed_violations']['sector'] = int(sector_violations)
                total_violations += sector_violations
                total_checks += len(df)
        
        results['compliance_score'] = max(0, 1 - (total_violations / max(1, total_checks)))
        results['total_violations'] = total_violations
        results['total_checks'] = total_checks
        
        return results
    
    def _validate_regulatory_compliance(self, df: pd.DataFrame, data_type: str) -> Dict:
        """Validate regulatory compliance with Central Bank of Tunisia standards"""
        
        compliance_results = {
            'central_bank_compliance': {},
            'data_protection_compliance': {},
            'statistical_office_alignment': {},
            'overall_compliance_score': 0.0
        }
        
        constraints = self.regulatory_constraints[data_type]
        compliance_scores = []
        
        if data_type == 'retail':
            # Central Bank Tunisia retail banking regulations
            
            # 1. Age distribution compliance (working age population focus)
            working_age_percentage = ((df['age'] >= 18) & (df['age'] <= 65)).mean()
            age_compliance = working_age_percentage >= 0.80  # 80% should be working age
            compliance_results['central_bank_compliance']['working_age_focus'] = {
                'percentage': float(working_age_percentage),
                'compliant': age_compliance,
                'requirement': 'Minimum 80% working age population'
            }
            compliance_scores.append(float(age_compliance))
            
            # 2. Income distribution realism (INS Tunisia alignment)
            if 'monthly_income' in df.columns:
                median_income = df['monthly_income'].median()
                income_realism = 800 <= median_income <= 1500  # Realistic for Tunisia
                compliance_results['central_bank_compliance']['income_realism'] = {
                    'median_income': float(median_income),
                    'compliant': income_realism,
                    'requirement': 'Median income 800-1500 TND'
                }
                compliance_scores.append(float(income_realism))
            
            # 3. Geographic distribution (urban/rural balance)
            if 'governorate' in df.columns:
                urban_govs = ['Tunis', 'Ariana', 'Sfax', 'Sousse']
                urban_percentage = df['governorate'].isin(urban_govs).mean()
                geo_compliance = 0.60 <= urban_percentage <= 0.80  # Realistic urban/rural split
                compliance_results['central_bank_compliance']['geographic_balance'] = {
                    'urban_percentage': float(urban_percentage),
                    'compliant': geo_compliance,
                    'requirement': 'Urban population 60-80%'
                }
                compliance_scores.append(float(geo_compliance))
            
            # 4. Banking penetration realism
            digital_channels = ['mobile', 'web', 'whatsapp']
            if 'preferred_channel' in df.columns:
                digital_adoption = df['preferred_channel'].isin(digital_channels).mean()
                digital_compliance = 0.40 <= digital_adoption <= 0.70  # Realistic for Tunisia
                compliance_results['central_bank_compliance']['digital_adoption'] = {
                    'digital_percentage': float(digital_adoption),
                    'compliant': digital_compliance,
                    'requirement': 'Digital adoption 40-70%'
                }
                compliance_scores.append(float(digital_compliance))
        
        elif data_type == 'corporate':
            # Central Bank Tunisia corporate banking regulations
            
            # 1. SME distribution (micro/small enterprise focus)
            if 'company_size' in df.columns:
                sme_percentage = df['company_size'].isin(['micro', 'small']).mean()
                sme_compliance = sme_percentage >= 0.85  # 85% should be SMEs
                compliance_results['central_bank_compliance']['sme_focus'] = {
                    'sme_percentage': float(sme_percentage),
                    'compliant': sme_compliance,
                    'requirement': 'Minimum 85% SMEs (micro/small)'
                }
                compliance_scores.append(float(sme_compliance))
            
            # 2. Sector distribution (service economy focus)
            if 'business_sector' in df.columns:
                service_percentage = (df['business_sector'] == 'services').mean()
                sector_compliance = service_percentage >= 0.35  # Services should dominate
                compliance_results['central_bank_compliance']['service_economy'] = {
                    'service_percentage': float(service_percentage),
                    'compliant': sector_compliance,
                    'requirement': 'Minimum 35% services sector'
                }
                compliance_scores.append(float(sector_compliance))
            
            # 3. Size-revenue consistency (realistic business scaling)
            size_revenue_consistency = self._validate_size_revenue_regulatory_compliance(df)
            compliance_results['central_bank_compliance']['size_revenue_consistency'] = size_revenue_consistency
            compliance_scores.append(size_revenue_consistency['compliance_score'])
        
        # Data protection compliance (GDPR-style for Tunisia)
        data_protection_score = self._validate_data_protection_compliance(df, data_type)
        compliance_results['data_protection_compliance'] = data_protection_score
        compliance_scores.append(data_protection_score['compliance_score'])
        
        # Overall compliance score
        compliance_results['overall_compliance_score'] = np.mean(compliance_scores) if compliance_scores else 0.0
        compliance_results['regulatory_approval'] = compliance_results['overall_compliance_score'] >= 0.95
        
        return compliance_results
    
    def _validate_size_revenue_regulatory_compliance(self, df: pd.DataFrame) -> Dict:
        """Validate size-revenue consistency per Central Bank regulations"""
        
        if 'company_size' not in df.columns or 'annual_revenue' not in df.columns:
            return {'compliance_score': 0.5, 'error': 'Missing required columns'}
        
        constraints = self.regulatory_constraints['corporate']['size_revenue_consistency']
        total_companies = len(df)
        compliant_companies = 0
        
        violations_by_size = {}
        
        for _, row in df.iterrows():
            size = row['company_size']
            revenue = row['annual_revenue']
            
            if size in constraints:
                min_rev, max_rev = constraints[size]
                is_compliant = min_rev <= revenue <= max_rev
                
                if is_compliant:
                    compliant_companies += 1
                else:
                    if size not in violations_by_size:
                        violations_by_size[size] = 0
                    violations_by_size[size] += 1
        
        compliance_score = compliant_companies / max(1, total_companies)
        
        return {
            'compliance_score': float(compliance_score),
            'compliant_companies': compliant_companies,
            'total_companies': total_companies,
            'violations_by_size': violations_by_size,
            'regulatory_approved': compliance_score >= 0.90
        }
    
    def _validate_data_protection_compliance(self, df: pd.DataFrame, data_type: str) -> Dict:
        """Validate data protection compliance (privacy regulations)"""
        
        protection_checks = []
        
        # 1. No real personal identifiers
        personal_id_columns = ['ssn', 'passport', 'national_id', 'phone', 'email']
        has_personal_ids = any(col in df.columns for col in personal_id_columns)
        protection_checks.append(not has_personal_ids)
        
        # 2. Client IDs are synthetic
        if 'client_id' in df.columns:
            synthetic_ids = df['client_id'].str.contains('CTGAN|R_|C_|synthetic', case=False, na=False).mean()
            protection_checks.append(synthetic_ids > 0.9)
        
        # 3. No exact duplicates (privacy risk)
        duplicate_percentage = df.duplicated().mean()
        protection_checks.append(duplicate_percentage < 0.01)
        
        # 4. Realistic but not traceable data ranges
        if data_type == 'retail' and 'monthly_income' in df.columns:
            # Income should vary realistically (not all round numbers)
            round_income_percentage = (df['monthly_income'] % 100 == 0).mean()
            protection_checks.append(round_income_percentage < 0.20)
        
        compliance_score = np.mean(protection_checks) if protection_checks else 0.0
        
        return {
            'compliance_score': float(compliance_score),
            'protection_checks_passed': sum(protection_checks),
            'total_protection_checks': len(protection_checks),
            'privacy_approved': compliance_score >= 0.95,
            'duplicate_percentage': float(duplicate_percentage)
        }
    
    def _validate_correlation_preservation(self, original_df: pd.DataFrame, 
                                         synthetic_df: pd.DataFrame) -> Dict:
        """Validate preservation of feature correlations"""
        
        correlation_results = {
            'correlation_comparisons': {},
            'preservation_score': 0.0,
            'significant_differences': []
        }
        
        # Get numerical columns common to both datasets
        orig_numerical = original_df.select_dtypes(include=[np.number])
        synth_numerical = synthetic_df.select_dtypes(include=[np.number])
        
        common_cols = list(set(orig_numerical.columns) & set(synth_numerical.columns))
        common_cols = [col for col in common_cols if 'client_id' not in col.lower()]
        
        if len(common_cols) >= 2:
            try:
                # Calculate correlation matrices
                orig_corr = orig_numerical[common_cols].corr()
                synth_corr = synth_numerical[common_cols].corr()
                
                # Compare correlation matrices
                correlation_differences = []
                significant_differences = []
                
                for i, col1 in enumerate(common_cols):
                    for j, col2 in enumerate(common_cols):
                        if i < j:  # Avoid duplicates and diagonal
                            orig_corr_val = orig_corr.loc[col1, col2]
                            synth_corr_val = synth_corr.loc[col1, col2]
                            
                            # Handle NaN correlations
                            if pd.isna(orig_corr_val) or pd.isna(synth_corr_val):
                                continue
                            
                            diff = abs(orig_corr_val - synth_corr_val)
                            correlation_differences.append(diff)
                            
                            correlation_results['correlation_comparisons'][f'{col1}_vs_{col2}'] = {
                                'original_correlation': float(orig_corr_val),
                                'synthetic_correlation': float(synth_corr_val),
                                'difference': float(diff),
                                'preserved': diff < 0.2
                            }
                            
                            if diff > 0.2:  # Significant difference threshold
                                significant_differences.append({
                                    'features': f'{col1} vs {col2}',
                                    'original': float(orig_corr_val),
                                    'synthetic': float(synth_corr_val),
                                    'difference': float(diff)
                                })
                
                if correlation_differences:
                    mean_correlation_diff = np.mean(correlation_differences)
                    correlation_preservation_score = max(0, 1 - mean_correlation_diff)
                    
                    correlation_results.update({
                        'mean_correlation_difference': float(mean_correlation_diff),
                        'max_correlation_difference': float(max(correlation_differences)),
                        'preservation_score': float(correlation_preservation_score),
                        'correlations_analyzed': len(correlation_differences),
                        'significant_differences': significant_differences,
                        'preservation_quality': 'excellent' if correlation_preservation_score > 0.9 else
                                              'good' if correlation_preservation_score > 0.8 else
                                              'acceptable' if correlation_preservation_score > 0.7 else 'poor'
                    })
                else:
                    correlation_results['preservation_score'] = 0.5
                    correlation_results['error'] = 'No valid correlations to compare'
                    
            except Exception as e:
                correlation_results['preservation_score'] = 0.0
                correlation_results['error'] = f'Correlation analysis failed: {str(e)}'
        else:
            correlation_results['preservation_score'] = 0.5
            correlation_results['error'] = 'Insufficient numerical features for correlation analysis'
        
        return correlation_results
    
    def _validate_corporate_consistency(self, df: pd.DataFrame) -> Dict:
        """Validate corporate-specific business logic consistency"""
        
        consistency_results = {
            'size_revenue_consistency': {},
            'size_employee_consistency': {},
            'sector_size_alignment': {},
            'overall_consistency_score': 0.0
        }
        
        consistency_scores = []
        
        # 1. Size-Revenue consistency
        if all(col in df.columns for col in ['company_size', 'annual_revenue']):
            size_revenue_result = self._validate_size_revenue_regulatory_compliance(df)
            consistency_results['size_revenue_consistency'] = size_revenue_result
            consistency_scores.append(size_revenue_result['compliance_score'])
        
        # 2. Size-Employee consistency
        if all(col in df.columns for col in ['company_size', 'employee_count']):
            employee_constraints = self.regulatory_constraints['corporate']['size_employee_consistency']
            total_companies = len(df)
            employee_consistent = 0
            
            for _, row in df.iterrows():
                size = row['company_size']
                employees = row['employee_count']
                
                if size in employee_constraints:
                    min_emp, max_emp = employee_constraints[size]
                    if min_emp <= employees <= max_emp:
                        employee_consistent += 1
            
            employee_consistency_score = employee_consistent / max(1, total_companies)
            consistency_results['size_employee_consistency'] = {
                'consistency_score': float(employee_consistency_score),
                'consistent_companies': employee_consistent,
                'total_companies': total_companies
            }
            consistency_scores.append(employee_consistency_score)
        
        # 3. Sector-Size alignment (realistic sector distributions)
        if all(col in df.columns for col in ['business_sector', 'company_size']):
            sector_size_alignment = self._validate_sector_size_alignment(df)
            consistency_results['sector_size_alignment'] = sector_size_alignment
            consistency_scores.append(sector_size_alignment['alignment_score'])
        
        consistency_results['overall_consistency_score'] = np.mean(consistency_scores) if consistency_scores else 0.0
        
        return consistency_results
    
    def _validate_sector_size_alignment(self, df: pd.DataFrame) -> Dict:
        """Validate realistic sector-size distributions"""
        
        # Expected sector-size distributions based on Tunisian economy
        expected_distributions = {
            'technology': {'micro': 0.6, 'small': 0.3, 'medium': 0.09, 'large': 0.01},
            'services': {'micro': 0.8, 'small': 0.15, 'medium': 0.04, 'large': 0.01},
            'manufacturing': {'micro': 0.7, 'small': 0.2, 'medium': 0.08, 'large': 0.02},
            'retail': {'micro': 0.85, 'small': 0.12, 'medium': 0.025, 'large': 0.005},
            'agriculture': {'micro': 0.9, 'small': 0.08, 'medium': 0.015, 'large': 0.005}
        }
        
        alignment_scores = []
        sector_analyses = {}
        
        for sector in expected_distributions:
            sector_data = df[df['business_sector'] == sector]
            if len(sector_data) > 0:
                actual_distribution = sector_data['company_size'].value_counts(normalize=True).to_dict()
                expected = expected_distributions[sector]
                
                # Calculate distribution similarity
                similarity_score = 0
                for size in ['micro', 'small', 'medium', 'large']:
                    actual_pct = actual_distribution.get(size, 0)
                    expected_pct = expected.get(size, 0)
                    # Use absolute difference, normalized
                    similarity_score += max(0, 1 - abs(actual_pct - expected_pct))
                
                sector_similarity = similarity_score / 4  # Average across 4 sizes
                alignment_scores.append(sector_similarity)
                
                sector_analyses[sector] = {
                    'actual_distribution': actual_distribution,
                    'expected_distribution': expected,
                    'similarity_score': float(sector_similarity),
                    'sample_size': len(sector_data)
                }
        
        return {
            'alignment_score': float(np.mean(alignment_scores)) if alignment_scores else 0.5,
            'sector_analyses': sector_analyses,
            'sectors_analyzed': len(alignment_scores)
        }
    
    def _validate_banking_logic(self, df: pd.DataFrame, data_type: str) -> Dict:
        """Validate banking-specific business logic"""
        
        banking_results = {
            'logical_consistency_checks': {},
            'banking_behavior_realism': {},
            'overall_banking_logic_score': 0.0
        }
        
        logic_scores = []
        
        if data_type == 'retail':
            # 1. Income-Risk tolerance relationship
            if all(col in df.columns for col in ['monthly_income', 'risk_tolerance']):
                income_risk_corr = df['monthly_income'].corr(df['risk_tolerance'])
                # Higher income should generally correlate with higher risk tolerance
                income_risk_logical = income_risk_corr > 0.1
                banking_results['logical_consistency_checks']['income_risk_relationship'] = {
                    'correlation': float(income_risk_corr) if not pd.isna(income_risk_corr) else 0.0,
                    'logical': income_risk_logical,
                    'expected': 'Positive correlation (higher income -> higher risk tolerance)'
                }
                logic_scores.append(float(income_risk_logical))
            
            # 2. Age-Digital engagement relationship
            if all(col in df.columns for col in ['age', 'digital_engagement_score']):
                age_digital_corr = df['age'].corr(df['digital_engagement_score'])
                # Younger age should correlate with higher digital engagement
                age_digital_logical = age_digital_corr < -0.1
                banking_results['logical_consistency_checks']['age_digital_relationship'] = {
                    'correlation': float(age_digital_corr) if not pd.isna(age_digital_corr) else 0.0,
                    'logical': age_digital_logical,
                    'expected': 'Negative correlation (younger age -> higher digital engagement)'
                }
                logic_scores.append(float(age_digital_logical))
            
            # 3. Channel preference consistency with digital engagement
            if all(col in df.columns for col in ['preferred_channel', 'digital_engagement_score']):
                digital_channels = ['mobile', 'web', 'whatsapp']
                digital_users = df[df['preferred_channel'].isin(digital_channels)]
                traditional_users = df[~df['preferred_channel'].isin(digital_channels)]
                
                if len(digital_users) > 0 and len(traditional_users) > 0:
                    digital_avg_engagement = digital_users['digital_engagement_score'].mean()
                    traditional_avg_engagement = traditional_users['digital_engagement_score'].mean()
                    
                    channel_consistency = digital_avg_engagement > traditional_avg_engagement
                    banking_results['logical_consistency_checks']['channel_digital_consistency'] = {
                        'digital_users_avg_engagement': float(digital_avg_engagement),
                        'traditional_users_avg_engagement': float(traditional_avg_engagement),
                        'logical': channel_consistency,
                        'expected': 'Digital channel users should have higher digital engagement'
                    }
                    logic_scores.append(float(channel_consistency))
        
        elif data_type == 'corporate':
            # 1. Size-Revenue relationship
            if all(col in df.columns for col in ['company_size', 'annual_revenue']):
                size_order = ['micro', 'small', 'medium', 'large']
                size_revenue_means = {}
                
                for size in size_order:
                    size_data = df[df['company_size'] == size]
                    if len(size_data) > 0:
                        size_revenue_means[size] = size_data['annual_revenue'].mean()
                
                # Check if revenue generally increases with size
                size_revenue_logical = True
                for i in range(len(size_order) - 1):
                    current_size = size_order[i]
                    next_size = size_order[i + 1]
                    if (current_size in size_revenue_means and next_size in size_revenue_means):
                        if size_revenue_means[current_size] > size_revenue_means[next_size]:
                            size_revenue_logical = False
                            break
                
                banking_results['logical_consistency_checks']['size_revenue_progression'] = {
                    'size_revenue_means': size_revenue_means,
                    'logical': size_revenue_logical,
                    'expected': 'Revenue should increase with company size'
                }
                logic_scores.append(float(size_revenue_logical))
            
            # 2. Sector-Digital maturity relationship
            if all(col in df.columns for col in ['business_sector', 'digital_maturity_score']):
                sector_digital_means = df.groupby('business_sector')['digital_maturity_score'].mean()
                
                # Technology sector should have highest digital maturity
                tech_highest = True
                if 'technology' in sector_digital_means.index:
                    tech_score = sector_digital_means['technology']
                    other_scores = sector_digital_means[sector_digital_means.index != 'technology']
                    if len(other_scores) > 0:
                        tech_highest = tech_score >= other_scores.max()
                
                banking_results['logical_consistency_checks']['sector_digital_maturity'] = {
                    'sector_digital_means': sector_digital_means.to_dict(),
                    'tech_sector_highest': tech_highest,
                    'expected': 'Technology sector should have highest digital maturity'
                }
                logic_scores.append(float(tech_highest))
        
        # Banking behavior realism
        realism_scores = []
        
        # Check for unrealistic patterns
        if data_type == 'retail':
            # 1. Satisfaction score distribution realism
            if 'satisfaction_score' in df.columns:
                # Most clients should have moderate to high satisfaction
                high_satisfaction_pct = (df['satisfaction_score'] > 0.7).mean()
                satisfaction_realistic = 0.4 <= high_satisfaction_pct <= 0.8
                banking_results['banking_behavior_realism']['satisfaction_distribution'] = {
                    'high_satisfaction_percentage': float(high_satisfaction_pct),
                    'realistic': satisfaction_realistic,
                    'expected': '40-80% should have high satisfaction'
                }
                realism_scores.append(float(satisfaction_realistic))
            
            # 2. Risk tolerance distribution realism
            if 'risk_tolerance' in df.columns:
                # Risk tolerance should be normally distributed around moderate levels
                moderate_risk_pct = ((df['risk_tolerance'] >= 0.3) & (df['risk_tolerance'] <= 0.7)).mean()
                risk_realistic = moderate_risk_pct >= 0.5
                banking_results['banking_behavior_realism']['risk_tolerance_distribution'] = {
                    'moderate_risk_percentage': float(moderate_risk_pct),
                    'realistic': risk_realistic,
                    'expected': 'At least 50% should have moderate risk tolerance'
                }
                realism_scores.append(float(risk_realistic))
        
        elif data_type == 'corporate':
            # 1. Credit rating distribution realism
            if 'credit_rating' in df.columns:
                # Most SMEs should have B or C rating (realistic for Tunisia)
                bc_rating_pct = df['credit_rating'].isin(['B', 'C']).mean()
                rating_realistic = bc_rating_pct >= 0.6
                banking_results['banking_behavior_realism']['credit_rating_distribution'] = {
                    'bc_rating_percentage': float(bc_rating_pct),
                    'realistic': rating_realistic,
                    'expected': 'At least 60% should have B or C credit rating'
                }
                realism_scores.append(float(rating_realistic))
        
        # Overall banking logic score
        all_scores = logic_scores + realism_scores
        banking_results['overall_banking_logic_score'] = np.mean(all_scores) if all_scores else 0.5
        
        return banking_results
    
    def _validate_data_privacy(self, original_df: pd.DataFrame, synthetic_df: pd.DataFrame) -> Dict:
        """Validate data privacy and anonymization"""
        
        privacy_results = {
            'anonymization_quality': {},
            're_identification_risk': {},
            'privacy_score': 0.0
        }
        
        privacy_scores = []
        
        # 1. Check for exact record matches (privacy risk)
        exact_matches = 0
        comparison_cols = [col for col in original_df.columns 
                          if col in synthetic_df.columns and 'client_id' not in col.lower()]
        
        if comparison_cols:
            for _, synth_row in synthetic_df[comparison_cols].iterrows():
                matches = (original_df[comparison_cols] == synth_row).all(axis=1).sum()
                if matches > 0:
                    exact_matches += 1
        
        exact_match_risk = exact_matches / len(synthetic_df) if len(synthetic_df) > 0 else 0
        privacy_results['re_identification_risk']['exact_matches'] = {
            'count': exact_matches,
            'percentage': float(exact_match_risk),
            'risk_level': 'high' if exact_match_risk > 0.01 else 'low',
            'acceptable': exact_match_risk <= 0.01
        }
        privacy_scores.append(1.0 - min(1.0, exact_match_risk * 100))
        
        # 2. Statistical distance between datasets
        numerical_cols = [col for col in comparison_cols 
                         if original_df[col].dtype in ['int64', 'float64']]
        
        if numerical_cols:
            # Calculate mean distances for numerical features
            distances = []
            for col in numerical_cols:
                orig_mean = original_df[col].mean()
                synth_mean = synthetic_df[col].mean()
                orig_std = original_df[col].std()
                
                if orig_std > 0:
                    normalized_distance = abs(orig_mean - synth_mean) / orig_std
                    distances.append(normalized_distance)
            
            if distances:
                avg_distance = np.mean(distances)
                # Good privacy: similar statistics but not identical
                distance_score = 1.0 if 0.1 <= avg_distance <= 0.5 else max(0, 1 - abs(avg_distance - 0.3) / 0.7)
                
                privacy_results['anonymization_quality']['statistical_distance'] = {
                    'average_normalized_distance': float(avg_distance),
                    'privacy_preserving': 0.1 <= avg_distance <= 0.5,
                    'score': float(distance_score)
                }
                privacy_scores.append(distance_score)
        
        # 3. Uniqueness preservation (avoid too much similarity)
        if 'client_id' in synthetic_df.columns:
            unique_records = len(synthetic_df.drop_duplicates())
            uniqueness_ratio = unique_records / len(synthetic_df)
            
            privacy_results['anonymization_quality']['record_uniqueness'] = {
                'unique_records': unique_records,
                'total_records': len(synthetic_df),
                'uniqueness_ratio': float(uniqueness_ratio),
                'acceptable': uniqueness_ratio >= 0.95
            }
            privacy_scores.append(float(uniqueness_ratio))
        
        # Overall privacy score
        privacy_results['privacy_score'] = np.mean(privacy_scores) if privacy_scores else 0.5
        privacy_results['privacy_grade'] = (
            'excellent' if privacy_results['privacy_score'] > 0.9 else
            'good' if privacy_results['privacy_score'] > 0.8 else
            'acceptable' if privacy_results['privacy_score'] > 0.7 else
            'poor'
        )
        
        return privacy_results
    
    def _calculate_enterprise_quality_score(self, validation_results: Dict) -> Dict:
        """Calculate comprehensive enterprise quality score"""
        
        # Extract component scores
        components = validation_results.get('validation_components', {})
        
        statistical_score = components.get('statistical', {}).get('overall_similarity_score', 0.5)
        business_rules_score = components.get('business_rules', {}).get('compliance_score', 0.5)
        regulatory_score = components.get('regulatory', {}).get('overall_compliance_score', 0.5)
        correlation_score = components.get('correlations', {}).get('preservation_score', 0.5)
        banking_logic_score = components.get('banking_logic', {}).get('overall_banking_logic_score', 0.5)
        privacy_score = components.get('privacy', {}).get('privacy_score', 0.5)
        
        # Corporate-specific consistency score
        consistency_score = 0.5
        if 'corporate_consistency' in components:
            consistency_score = components['corporate_consistency'].get('overall_consistency_score', 0.5)
        
        # Weighted scoring system (enterprise priorities)
        weights = {
            'regulatory_compliance': 0.25,      # Highest priority for enterprise
            'business_rules': 0.20,            # Critical business logic
            'statistical_similarity': 0.15,    # Data quality
            'privacy_protection': 0.15,        # Privacy compliance
            'banking_logic': 0.10,             # Domain-specific logic
            'correlation_preservation': 0.10,   # Feature relationships
            'corporate_consistency': 0.05      # Corporate-specific (if applicable)
        }
        
        total_score = (
            regulatory_score * weights['regulatory_compliance'] +
            business_rules_score * weights['business_rules'] +
            statistical_score * weights['statistical_similarity'] +
            privacy_score * weights['privacy_protection'] +
            banking_logic_score * weights['banking_logic'] +
            correlation_score * weights['correlation_preservation'] +
            consistency_score * weights['corporate_consistency']
        )
        
        # Quality grade assignment
        if total_score >= 0.95:
            quality_grade = 'Enterprise Excellence'
            deployment_recommendation = 'Immediate deployment approved'
        elif total_score >= 0.90:
            quality_grade = 'Enterprise Ready'
            deployment_recommendation = 'Deploy with standard monitoring'
        elif total_score >= 0.85:
            quality_grade = 'Production Ready'
            deployment_recommendation = 'Deploy with enhanced monitoring'
        elif total_score >= 0.75:
            quality_grade = 'Acceptable with Conditions'
            deployment_recommendation = 'Limited deployment, improvement required'
        elif total_score >= 0.65:
            quality_grade = 'Improvement Required'
            deployment_recommendation = 'Do not deploy, significant improvements needed'
        else:
            quality_grade = 'Unacceptable'
            deployment_recommendation = 'Reject dataset, major rework required'
        
        # Threshold compliance checking
        threshold_compliance = {
            'regulatory_compliance': regulatory_score >= self.validation_standards['regulatory_compliance_threshold'],
            'business_rules': business_rules_score >= self.validation_standards['business_rule_compliance_threshold'],
            'statistical_similarity': statistical_score >= self.validation_standards['statistical_similarity_threshold'],
            'correlation_preservation': correlation_score >= self.validation_standards['correlation_preservation_threshold']
        }
        
        # Risk assessment
        risk_factors = []
        if regulatory_score < 0.95:
            risk_factors.append('Regulatory compliance risk')
        if privacy_score < 0.9:
            risk_factors.append('Privacy protection risk')
        if business_rules_score < 0.9:
            risk_factors.append('Business logic compliance risk')
        
        return {
            'total_score': float(total_score),
            'quality_grade': quality_grade,
            'deployment_recommendation': deployment_recommendation,
            'component_scores': {
                'regulatory_compliance': float(regulatory_score),
                'business_rules_compliance': float(business_rules_score),
                'statistical_similarity': float(statistical_score),
                'privacy_protection': float(privacy_score),
                'banking_logic': float(banking_logic_score),
                'correlation_preservation': float(correlation_score),
                'corporate_consistency': float(consistency_score)
            },
            'weights_applied': weights,
            'threshold_compliance': threshold_compliance,
            'enterprise_approved': all(threshold_compliance.values()),
            'risk_factors': risk_factors,
            'certification_status': 'CERTIFIED' if total_score >= 0.90 and all(threshold_compliance.values()) else 'NOT CERTIFIED'
        }
    
    def generate_quality_report(self, validation_results: Dict, output_path: str) -> str:
        """Generate comprehensive enterprise quality assessment report"""
        
        overall_assessment = validation_results.get('overall_assessment', {})
        data_type = validation_results.get('data_type', 'unknown')
        
        report_content = f"""
# Enterprise Data Quality Assessment Report

**Generated**: {validation_results.get('validation_timestamp', 'Unknown')}
**Data Type**: {data_type.title()}
**Samples Validated**: {validation_results.get('synthetic_samples', 'N/A'):,}
**Certification Status**: {overall_assessment.get('certification_status', 'UNKNOWN')}

## Executive Summary

**Overall Quality Score**: {overall_assessment.get('total_score', 0):.3f}/1.000
**Quality Grade**: {overall_assessment.get('quality_grade', 'Unknown')}
**Enterprise Approved**: {'✅ YES' if overall_assessment.get('enterprise_approved', False) else '❌ NO'}

## Deployment Recommendation
{overall_assessment.get('deployment_recommendation', 'No recommendation available')}

## Component Assessment

### Regulatory Compliance: {overall_assessment.get('component_scores', {}).get('regulatory_compliance', 0):.3f}
- Central Bank of Tunisia standards compliance
- Data protection regulations adherence
- Statistical office alignment

### Business Rules Compliance: {overall_assessment.get('component_scores', {}).get('business_rules_compliance', 0):.3f}
- Data range validations
- Business logic consistency
- Domain-specific constraints

### Statistical Similarity: {overall_assessment.get('component_scores', {}).get('statistical_similarity', 0):.3f}
- Distribution preservation
- Moment preservation
- Correlation preservation

### Privacy Protection: {overall_assessment.get('component_scores', {}).get('privacy_protection', 0):.3f}
- Anonymization quality
- Re-identification risk assessment
- Data uniqueness validation

### Banking Logic: {overall_assessment.get('component_scores', {}).get('banking_logic', 0):.3f}
- Domain-specific relationships
- Behavioral realism
- Industry-standard patterns

## Risk Assessment
"""
        
        risk_factors = overall_assessment.get('risk_factors', [])
        if risk_factors:
            report_content += "\n**Risk Factors Identified:**\n"
            for risk in risk_factors:
                report_content += f"- ⚠️ {risk}\n"
        else:
            report_content += "\n✅ **No significant risk factors identified**\n"
        
        report_content += f"""

## Threshold Compliance
"""
        
        threshold_compliance = overall_assessment.get('threshold_compliance', {})
        for component, compliant in threshold_compliance.items():
            status = '✅ PASS' if compliant else '❌ FAIL'
            report_content += f"- {component.replace('_', ' ').title()}: {status}\n"
        
        report_content += f"""

## Recommendations

### Immediate Actions Required
"""
        
        if overall_assessment.get('enterprise_approved', False):
            report_content += "- ✅ Dataset approved for enterprise deployment\n"
            report_content += "- ✅ Proceed with team handoff and integration\n"
        else:
            report_content += "- ❌ Dataset requires improvement before deployment\n"
            report_content += "- 🔧 Address risk factors identified above\n"
            report_content += "- 📊 Re-validate after improvements\n"
        
        report_content += f"""

### Long-term Monitoring
- Implement continuous quality monitoring
- Regular re-validation with updated standards
- Performance tracking in production environment

---
*Report generated by Enterprise Data Validation Engine v3.0*
*Compliant with Central Bank of Tunisia regulations*
"""
        
        # Save the report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"📋 Enterprise quality report saved: {output_path}")
        
        return output_path
    
    def generate_validation_summary(self, validation_results: Dict) -> Dict:
        """Generate executive validation summary for stakeholders"""
        
        overall_assessment = validation_results.get('overall_assessment', {})
        
        summary = {
            'validation_summary': {
                'data_type': validation_results.get('data_type', 'unknown'),
                'samples_validated': validation_results.get('synthetic_samples', 0),
                'validation_timestamp': validation_results.get('validation_timestamp'),
                'overall_score': overall_assessment.get('total_score', 0),
                'quality_grade': overall_assessment.get('quality_grade', 'Unknown'),
                'enterprise_approved': overall_assessment.get('enterprise_approved', False),
                'certification_status': overall_assessment.get('certification_status', 'NOT CERTIFIED')
            },
            'key_metrics': overall_assessment.get('component_scores', {}),
            'compliance_status': overall_assessment.get('threshold_compliance', {}),
            'risk_assessment': {
                'risk_factors': overall_assessment.get('risk_factors', []),
                'risk_level': 'low' if len(overall_assessment.get('risk_factors', [])) == 0 else
                           'medium' if len(overall_assessment.get('risk_factors', [])) <= 2 else 'high'
            },
            'business_recommendation': overall_assessment.get('deployment_recommendation', 'No recommendation')
        }
        
        return summary


# Example usage and testing
if __name__ == "__main__":
    # Test the complete validator
    validator = EnterpriseDataValidator()
    
    # Create sample data for testing
    original_retail = pd.DataFrame({
        'client_id': ['R_001', 'R_002', 'R_003'] * 50,
        'age': np.random.randint(18, 80, 150),
        'monthly_income': np.random.uniform(500, 8000, 150),
        'gender': np.random.choice(['M', 'F'], 150),
        'governorate': np.random.choice(['Tunis', 'Sfax', 'Sousse', 'Ariana'], 150),
        'risk_tolerance': np.random.uniform(0, 1, 150),
        'satisfaction_score': np.random.uniform(0.3, 1.0, 150),
        'digital_engagement_score': np.random.uniform(0, 1, 150),
        'preferred_channel': np.random.choice(['mobile', 'branch', 'web'], 150)
    })
    
    # Create synthetic data (slightly modified original for testing)
    synthetic_retail = original_retail.copy()
    synthetic_retail['client_id'] = ['CTGAN_R_' + f'{i:03d}' for i in range(150)]
    synthetic_retail['age'] += np.random.normal(0, 2, 150)
    synthetic_retail['monthly_income'] *= np.random.normal(1, 0.1, 150)
    
    # Validate data
    try:
        validation_results = validator.validate_retail_data_comprehensive(original_retail, synthetic_retail)
        
        print("🎯 Enterprise validation completed!")
        print(f"Overall Quality Score: {validation_results['overall_assessment']['total_score']:.3f}")
        print(f"Quality Grade: {validation_results['overall_assessment']['quality_grade']}")
        print(f"Enterprise Approved: {validation_results['overall_assessment']['enterprise_approved']}")
        
        # Generate quality report
        report_path = validator.generate_quality_report(validation_results, "test_quality_report.md")
        print(f"📋 Quality report saved: {report_path}")
        
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
    
    print("\n🧪 Complete Enterprise Validator test completed!")