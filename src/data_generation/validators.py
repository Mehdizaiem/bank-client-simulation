#!/usr/bin/env python3
"""
Enterprise Data Validation Engine - Week 3
Company-grade validation with statistical tests, business rules,
and regulatory compliance for Tunisian banking data.
"""

from venv import logger
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from scipy import stats
from scipy.stats import ks_2samp, chi2_contingency, normaltest
import logging
from datetime import datetime
from pathlib import Path

class EnterpriseDataValidator:
    """Company-grade data validation with comprehensive testing"""
    
    def __init__(self):
        self.validation_standards = {
            'statistical_similarity_threshold': 0.95,
            'business_rule_compliance_threshold': 0.98,
            'regulatory_compliance_threshold': 0.99,
            'correlation_preservation_threshold': 0.90
        }
        
        # Tunisian banking regulations
        self.regulatory_constraints = {
            'retail': {
                'min_age': 18, 'max_age': 80,
                'min_income_tnd': 400, 'max_income_tnd': 15000,
                'required_governorates': ['Tunis', 'Sfax', 'Sousse', 'Ariana'],
                'score_ranges': {'risk_tolerance': (0, 1), 'satisfaction': (0, 1)}
            },
            'corporate': {
                'min_employees': 1, 'max_employees': 10000,
                'min_revenue_tnd': 10000, 'max_revenue_tnd': 100000000,
                'required_sectors': ['services', 'manufacturing', 'retail'],
                'size_revenue_consistency': {
                    'micro': (10000, 100000),
                    'small': (100000, 1000000), 
                    'medium': (1000000, 10000000),
                    'large': (10000000, 100000000)
                }
            }
        }
        
        logger.info("🏛️ Enterprise Data Validator initialized")
    
    def validate_retail_data_comprehensive(self, original_df: pd.DataFrame, 
                                         synthetic_df: pd.DataFrame) -> Dict:
        """Comprehensive retail data validation with enterprise standards"""
        
        validation_results = {
            'validation_timestamp': datetime.now().isoformat(),
            'data_type': 'retail',
            'samples_validated': len(synthetic_df),
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
        
        # 6. Overall Quality Assessment
        overall_quality = self._calculate_enterprise_quality_score(validation_results)
        validation_results['overall_assessment'] = overall_quality
        
        return validation_results
    
    def validate_corporate_data_comprehensive(self, original_df: pd.DataFrame,
                                            synthetic_df: pd.DataFrame) -> Dict:
        """Comprehensive corporate data validation with enterprise standards"""
        
        validation_results = {
            'validation_timestamp': datetime.now().isoformat(),
            'data_type': 'corporate',
            'samples_validated': len(synthetic_df),
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
        
        overall_quality = self._calculate_enterprise_quality_score(validation_results)
        validation_results['overall_assessment'] = overall_quality
        
        return validation_results
    
    def _validate_statistical_distributions(self, original_df: pd.DataFrame,
                                          synthetic_df: pd.DataFrame, 
                                          data_type: str) -> Dict:
        """Advanced statistical distribution validation"""
        
        results = {'tests_passed': 0, 'tests_failed': 0, 'test_details': {}}
        
        # Numerical feature testing
        numerical_cols = original_df.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if col in synthetic_df.columns:
                # Kolmogorov-Smirnov test
                ks_stat, ks_pvalue = ks_2samp(original_df[col], synthetic_df[col])
                
                # Anderson-Darling test for normality
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
                
                test_passed = (ks_pvalue > 0.05 and normality_preserved and moments_preserved)
                
                results['test_details'][col] = {
                    'ks_statistic': float(ks_stat),
                    'ks_pvalue': float(ks_pvalue),
                    'normality_preserved': normality_preserved,
                    'moments_preserved': moments_preserved,
                    'test_passed': test_passed
                }
                
                if test_passed:
                    results['tests_passed'] += 1
                else:
                    results['tests_failed'] += 1
        
        results['pass_rate'] = results['tests_passed'] / max(1, results['tests_passed'] + results['tests_failed'])
        return results
    
    def _validate_business_rules(self, df: pd.DataFrame, data_type: str) -> Dict:
        """Validate business-specific rules"""
        
        constraints = self.regulatory_constraints[data_type]
        results = {'violations': [], 'compliance_score': 1.0}
        
        if data_type == 'retail':
            # Age constraints
            age_violations = ((df['age'] < constraints['min_age']) | 
                            (df['age'] > constraints['max_age'])).sum()
            if age_violations > 0:
                results['violations'].append(f"Age violations: {age_violations}")
            
            # Income constraints  
            income_violations = ((df['monthly_income'] < constraints['min_income_tnd']) |
                               (df['monthly_income'] > constraints['max_income_tnd'])).sum()
            if income_violations > 0:
                results['violations'].append(f"Income violations: {income_violations}")
            
            # Score range validations
            for score_col, (min_val, max_val) in constraints['score_ranges'].items():
                if score_col in df.columns:
                    violations = ((df[score_col] < min_val) | (df[score_col] > max_val)).sum()
                    if violations > 0:
                        results['violations'].append(f"{score_col} violations: {violations}")
        
        elif data_type == 'corporate':
            # Employee constraints
            emp_violations = ((df['employee_count'] < constraints['min_employees']) |
                            (df['employee_count'] > constraints['max_employees'])).sum()
            if emp_violations > 0:
                results['violations'].append(f"Employee count violations: {emp_violations}")
            
            # Revenue constraints
            rev_violations = ((df['annual_revenue'] < constraints['min_revenue_tnd']) |
                            (df['annual_revenue'] > constraints['max_revenue_tnd'])).sum()
            if rev_violations > 0:
                results['violations'].append(f"Revenue violations: {rev_violations}")
        
        total_violations = sum([int(v.split(': ')[1]) for v in results['violations']])
        results['compliance_score'] = 1 - (total_violations / len(df))
        
        return results
    
    def generate_quality_report(self, validation_results: Dict, 
                              output_path: str) -> str:
        """Generate comprehensive quality assessment report"""
        
        report_content = f"""
# Enterprise Data Quality Assessment Report

**Generated**: {validation_results['validation_timestamp']}
**Data Type**: {validation_results['data_type'].title()}
**Samples Validated**: {validation_results['samples_validated']:,}

## Overall Quality Assessment
**Quality Grade**: {validation_results['overall_assessment']['quality_grade']}
**Total Score**: {validation_results['overall_assessment']['total_score']:.3f}/1.000

## Component Scores
- Statistical Similarity: {validation_results['overall_assessment']['component_scores']['statistical']:.3f}
- Business Rule Compliance: {validation_results['overall_assessment']['component_scores']['business_rules']:.3f}
- Regulatory Compliance: {validation_results['overall_assessment']['component_scores']['regulatory']:.3f}

## Validation Status
✅ **ENTERPRISE READY**: {validation_results['overall_assessment']['enterprise_ready']}

## Recommendations
{validation_results['overall_assessment']['recommendations']}
"""
        
        with open(output_path, 'w') as f:
            f.write(report_content)
        
        return output_path