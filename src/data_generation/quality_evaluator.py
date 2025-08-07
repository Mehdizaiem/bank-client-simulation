#!/usr/bin/env python3
"""
CTGAN Quality Evaluator
Comprehensive evaluation suite for synthetic data quality assessment.
Includes statistical tests, business rule validation, and privacy evaluation
for enterprise-grade synthetic data validation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import logging
from datetime import datetime
from pathlib import Path
from scipy import stats
from scipy.stats import ks_2samp, chi2_contingency
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
import json
import warnings

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class CTGANQualityEvaluator:
    """Comprehensive quality evaluation for CTGAN-generated data"""
    
    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = Path(output_dir) if output_dir else Path("../../data/ctgan/validation_reports")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Quality thresholds
        self.quality_thresholds = {
            'statistical_similarity': 0.85,  # Minimum acceptable similarity score
            'business_rule_compliance': 0.90,  # Minimum business rule compliance
            'privacy_score': 0.95,  # Minimum privacy preservation score
            'ml_utility': 0.80,  # Minimum ML utility preservation
            'correlation_preservation': 0.75  # Minimum correlation preservation
        }
        
        logger.info("📊 CTGAN Quality Evaluator initialized")
    
    def evaluate_retail_quality(self, original_df: pd.DataFrame, synthetic_df: pd.DataFrame) -> Dict:
        """Comprehensive quality evaluation for retail clients"""
        logger.info(f"🔍 Evaluating retail data quality...")
        logger.info(f"   Original: {len(original_df)} samples")
        logger.info(f"   Synthetic: {len(synthetic_df)} samples")
        
        evaluation_report = {
            'evaluation_timestamp': datetime.now().isoformat(),
            'data_type': 'retail',
            'original_samples': len(original_df),
            'synthetic_samples': len(synthetic_df),
        }
        
        # 1. Statistical Similarity Assessment
        statistical_results = self._evaluate_statistical_similarity(original_df, synthetic_df, 'retail')
        evaluation_report['statistical_similarity'] = statistical_results
        
        # 2. Business Rule Validation
        business_rules_results = self._validate_retail_business_rules(synthetic_df)
        evaluation_report['business_rules'] = business_rules_results
        
        # 3. Privacy Evaluation
        privacy_results = self._evaluate_privacy_preservation(original_df, synthetic_df)
        evaluation_report['privacy'] = privacy_results
        
        # 4. ML Utility Evaluation
        ml_utility_results = self._evaluate_ml_utility(original_df, synthetic_df, 'retail')
        evaluation_report['ml_utility'] = ml_utility_results
        
        # 5. Correlation Preservation
        correlation_results = self._evaluate_correlation_preservation(original_df, synthetic_df)
        evaluation_report['correlation_preservation'] = correlation_results
        
        # 6. Overall Quality Score
        overall_score = self._calculate_overall_quality_score(evaluation_report)
        evaluation_report['overall_quality'] = overall_score
        
        # 7. Generate visualizations
        self._generate_quality_visualizations(original_df, synthetic_df, 'retail')
        
        # Save evaluation report
        self._save_evaluation_report(evaluation_report, 'retail')
        
        logger.info(f"✅ Retail quality evaluation completed")
        logger.info(f"   Overall Quality Score: {overall_score['total_score']:.3f}")
        
        return evaluation_report
    
    def evaluate_corporate_quality(self, original_df: pd.DataFrame, synthetic_df: pd.DataFrame) -> Dict:
        """Comprehensive quality evaluation for corporate clients"""
        logger.info(f"🔍 Evaluating corporate data quality...")
        logger.info(f"   Original: {len(original_df)} samples")
        logger.info(f"   Synthetic: {len(synthetic_df)} samples")
        
        evaluation_report = {
            'evaluation_timestamp': datetime.now().isoformat(),
            'data_type': 'corporate',
            'original_samples': len(original_df),
            'synthetic_samples': len(synthetic_df),
        }
        
        # 1. Statistical Similarity Assessment
        statistical_results = self._evaluate_statistical_similarity(original_df, synthetic_df, 'corporate')
        evaluation_report['statistical_similarity'] = statistical_results
        
        # 2. Business Rule Validation
        business_rules_results = self._validate_corporate_business_rules(synthetic_df)
        evaluation_report['business_rules'] = business_rules_results
        
        # 3. Privacy Evaluation
        privacy_results = self._evaluate_privacy_preservation(original_df, synthetic_df)
        evaluation_report['privacy'] = privacy_results
        
        # 4. ML Utility Evaluation
        ml_utility_results = self._evaluate_ml_utility(original_df, synthetic_df, 'corporate')
        evaluation_report['ml_utility'] = ml_utility_results
        
        # 5. Correlation Preservation
        correlation_results = self._evaluate_correlation_preservation(original_df, synthetic_df)
        evaluation_report['correlation_preservation'] = correlation_results
        
        # 6. Overall Quality Score
        overall_score = self._calculate_overall_quality_score(evaluation_report)
        evaluation_report['overall_quality'] = overall_score
        
        # 7. Generate visualizations
        self._generate_quality_visualizations(original_df, synthetic_df, 'corporate')
        
        # Save evaluation report
        self._save_evaluation_report(evaluation_report, 'corporate')
        
        logger.info(f"✅ Corporate quality evaluation completed")
        logger.info(f"   Overall Quality Score: {overall_score['total_score']:.3f}")
        
        return evaluation_report
    
    def _evaluate_statistical_similarity(self, original_df: pd.DataFrame, 
                                       synthetic_df: pd.DataFrame, data_type: str) -> Dict:
        """Evaluate statistical similarity between original and synthetic data"""
        logger.info("📈 Evaluating statistical similarity...")
        
        results = {
            'numerical_similarity': {},
            'categorical_similarity': {},
            'distribution_tests': {}
        }
        
        # Numerical features similarity
        numerical_cols = original_df.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if col in synthetic_df.columns:
                # KS test for distribution similarity
                ks_stat, ks_pvalue = ks_2samp(original_df[col], synthetic_df[col])
                
                # Basic statistics comparison
                orig_stats = original_df[col].describe()
                synth_stats = synthetic_df[col].describe()
                
                results['numerical_similarity'][col] = {
                    'ks_statistic': float(ks_stat),
                    'ks_pvalue': float(ks_pvalue),
                    'mean_difference': abs(orig_stats['mean'] - synth_stats['mean']),
                    'std_difference': abs(orig_stats['std'] - synth_stats['std']),
                    'similarity_score': 1 - ks_stat  # Higher is better
                }
        
        # Categorical features similarity
        categorical_cols = original_df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            if col in synthetic_df.columns and col != 'client_id':
                # Chi-square test for categorical distribution
                orig_counts = original_df[col].value_counts()
                synth_counts = synthetic_df[col].value_counts()
                
                # Align categories
                all_categories = set(orig_counts.index) | set(synth_counts.index)
                orig_aligned = [orig_counts.get(cat, 0) for cat in all_categories]
                synth_aligned = [synth_counts.get(cat, 0) for cat in all_categories]
                
                if len(all_categories) > 1:
                    try:
                        chi2_stat, chi2_pvalue = stats.chi2_contingency([orig_aligned, synth_aligned])[:2]
                        
                        results['categorical_similarity'][col] = {
                            'chi2_statistic': float(chi2_stat),
                            'chi2_pvalue': float(chi2_pvalue),
                            'category_overlap': len(set(orig_counts.index) & set(synth_counts.index)) / len(all_categories),
                            'similarity_score': max(0, 1 - chi2_stat / 100)  # Normalized similarity
                        }
                    except Exception as e:
                        results['categorical_similarity'][col] = {
                            'error': str(e),
                            'similarity_score': 0.5  # Neutral score for failed tests
                        }
        
        # Overall statistical similarity score
        numerical_scores = [r['similarity_score'] for r in results['numerical_similarity'].values()]
        categorical_scores = [r['similarity_score'] for r in results['categorical_similarity'].values()]
        
        all_scores = numerical_scores + categorical_scores
        overall_similarity = np.mean(all_scores) if all_scores else 0.5
        
        results['overall_statistical_similarity'] = float(overall_similarity)
        
        return results
    
    def _validate_retail_business_rules(self, synthetic_df: pd.DataFrame) -> Dict:
        """Validate business rules for retail clients"""
        logger.info("⚖️ Validating retail business rules...")
        
        rules_results = {}
        total_violations = 0
        total_checks = 0
        
        # Rule 1: Age range validation
        if 'age' in synthetic_df.columns:
            age_violations = ((synthetic_df['age'] < 18) | (synthetic_df['age'] > 80)).sum()
            rules_results['age_range'] = {
                'violations': int(age_violations),
                'compliance_rate': 1 - (age_violations / len(synthetic_df))
            }
            total_violations += age_violations
            total_checks += len(synthetic_df)
        
        # Rule 2: Income range validation
        if 'monthly_income' in synthetic_df.columns:
            income_violations = ((synthetic_df['monthly_income'] < 400) | 
                               (synthetic_df['monthly_income'] > 15000)).sum()
            rules_results['income_range'] = {
                'violations': int(income_violations),
                'compliance_rate': 1 - (income_violations / len(synthetic_df))
            }
            total_violations += income_violations
            total_checks += len(synthetic_df)
        
        # Rule 3: Score range validation (0-1)
        score_columns = ['risk_tolerance', 'satisfaction_score', 'digital_engagement_score']
        for col in score_columns:
            if col in synthetic_df.columns:
                score_violations = ((synthetic_df[col] < 0) | (synthetic_df[col] > 1)).sum()
                rules_results[f'{col}_range'] = {
                    'violations': int(score_violations),
                    'compliance_rate': 1 - (score_violations / len(synthetic_df))
                }
                total_violations += score_violations
                total_checks += len(synthetic_df)
        
        # Rule 4: Gender validation
        if 'gender' in synthetic_df.columns:
            valid_genders = {'M', 'F'}
            gender_violations = (~synthetic_df['gender'].isin(valid_genders)).sum()
            rules_results['gender_validity'] = {
                'violations': int(gender_violations),
                'compliance_rate': 1 - (gender_violations / len(synthetic_df))
            }
            total_violations += gender_violations
            total_checks += len(synthetic_df)
        
        # Rule 5: Income-Education consistency
        if all(col in synthetic_df.columns for col in ['monthly_income', 'education_level']):
            # Higher education should generally correlate with higher income
            edu_income_df = synthetic_df[['monthly_income', 'education_level']].dropna()
            if len(edu_income_df) > 0:
                edu_order = ['primary', 'secondary', 'university', 'postgraduate']
                income_by_edu = {}
                
                for edu in edu_order:
                    if edu in edu_income_df['education_level'].values:
                        income_by_edu[edu] = edu_income_df[edu_income_df['education_level'] == edu]['monthly_income'].median()
                
                # Check if income generally increases with education
                income_consistency_violations = 0
                if len(income_by_edu) >= 2:
                    income_values = [income_by_edu[edu] for edu in edu_order if edu in income_by_edu]
                    for i in range(len(income_values) - 1):
                        if income_values[i] > income_values[i + 1]:
                            income_consistency_violations += 1
                
                rules_results['income_education_consistency'] = {
                    'violations': income_consistency_violations,
                    'compliance_rate': 1 - (income_consistency_violations / max(1, len(income_values) - 1))
                }
        
        # Overall business rule compliance
        overall_compliance = 1 - (total_violations / max(1, total_checks))
        rules_results['overall_compliance'] = float(overall_compliance)
        
        return rules_results
    
    def _validate_corporate_business_rules(self, synthetic_df: pd.DataFrame) -> Dict:
        """Validate business rules for corporate clients"""
        logger.info("⚖️ Validating corporate business rules...")
        
        rules_results = {}
        total_violations = 0
        total_checks = 0
        
        # Rule 1: Employee count validation
        if 'employee_count' in synthetic_df.columns:
            employee_violations = (synthetic_df['employee_count'] < 1).sum()
            rules_results['employee_count_validity'] = {
                'violations': int(employee_violations),
                'compliance_rate': 1 - (employee_violations / len(synthetic_df))
            }
            total_violations += employee_violations
            total_checks += len(synthetic_df)
        
        # Rule 2: Revenue validation
        if 'annual_revenue' in synthetic_df.columns:
            revenue_violations = (synthetic_df['annual_revenue'] < 1000).sum()
            rules_results['revenue_validity'] = {
                'violations': int(revenue_violations),
                'compliance_rate': 1 - (revenue_violations / len(synthetic_df))
            }
            total_violations += revenue_violations
            total_checks += len(synthetic_df)
        
        # Rule 3: Company size-revenue consistency
        if all(col in synthetic_df.columns for col in ['company_size', 'annual_revenue']):
            size_revenue_rules = {
                'micro': (1000, 100000),
                'small': (100000, 1000000),
                'medium': (1000000, 10000000),
                'large': (10000000, 100000000)
            }
            
            consistency_violations = 0
            for _, row in synthetic_df.iterrows():
                size = row['company_size']
                revenue = row['annual_revenue']
                
                if size in size_revenue_rules:
                    min_rev, max_rev = size_revenue_rules[size]
                    if not (min_rev <= revenue <= max_rev):
                        consistency_violations += 1
            
            rules_results['size_revenue_consistency'] = {
                'violations': consistency_violations,
                'compliance_rate': 1 - (consistency_violations / len(synthetic_df))
            }
            total_violations += consistency_violations
            total_checks += len(synthetic_df)
        
        # Rule 4: Score range validation (0-1)
        score_columns = ['digital_maturity_score', 'cash_flow_predictability', 'seasonal_variation']
        for col in score_columns:
            if col in synthetic_df.columns:
                score_violations = ((synthetic_df[col] < 0) | (synthetic_df[col] > 1)).sum()
                rules_results[f'{col}_range'] = {
                    'violations': int(score_violations),
                    'compliance_rate': 1 - (score_violations / len(synthetic_df))
                }
                total_violations += score_violations
                total_checks += len(synthetic_df)
        
        # Overall business rule compliance
        overall_compliance = 1 - (total_violations / max(1, total_checks))
        rules_results['overall_compliance'] = float(overall_compliance)
        
        return rules_results
    
    def _evaluate_privacy_preservation(self, original_df: pd.DataFrame, 
                                     synthetic_df: pd.DataFrame) -> Dict:
        """Evaluate privacy preservation of synthetic data"""
        logger.info("🔒 Evaluating privacy preservation...")
        
        privacy_results = {}
        
        # 1. Record-level similarity (nearest neighbor distance)
        numerical_cols = original_df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            # Normalize data for distance calculation
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            
            orig_numerical = scaler.fit_transform(original_df[numerical_cols])
            synth_numerical = scaler.transform(synthetic_df[numerical_cols])
            
            # Calculate minimum distances
            from sklearn.metrics.pairwise import euclidean_distances
            distances = euclidean_distances(synth_numerical, orig_numerical)
            min_distances = np.min(distances, axis=1)
            
            privacy_results['nearest_neighbor'] = {
                'mean_min_distance': float(np.mean(min_distances)),
                'std_min_distance': float(np.std(min_distances)),
                'min_distance_threshold': 0.1,  # Threshold for privacy concern
                'privacy_at_risk_records': int(np.sum(min_distances < 0.1)),
                'privacy_score': 1 - (np.sum(min_distances < 0.1) / len(min_distances))
            }
        
        # 2. Membership inference vulnerability
        # Simple test: check if synthetic records are too similar to original
        exact_matches = 0
        if len(original_df) > 0 and len(synthetic_df) > 0:
            # Check for exact matches in non-ID columns
            comparison_cols = [col for col in original_df.columns 
                             if col in synthetic_df.columns and col != 'client_id']
            
            if comparison_cols:
                for _, synth_row in synthetic_df[comparison_cols].iterrows():
                    matches = (original_df[comparison_cols] == synth_row).all(axis=1).sum()
                    if matches > 0:
                        exact_matches += 1
        
        privacy_results['membership_inference'] = {
            'exact_matches': exact_matches,
            'exact_match_rate': exact_matches / len(synthetic_df) if len(synthetic_df) > 0 else 0,
            'privacy_score': 1 - (exact_matches / len(synthetic_df)) if len(synthetic_df) > 0 else 1
        }
        
        # Overall privacy score
        privacy_scores = [result['privacy_score'] for result in privacy_results.values() 
                         if isinstance(result, dict) and 'privacy_score' in result]
        overall_privacy_score = np.mean(privacy_scores) if privacy_scores else 0.95
        
        privacy_results['overall_privacy_score'] = float(overall_privacy_score)
        
        return privacy_results
    
    def _evaluate_ml_utility(self, original_df: pd.DataFrame, synthetic_df: pd.DataFrame, 
                           data_type: str) -> Dict:
        """Evaluate ML utility preservation of synthetic data"""
        logger.info("🤖 Evaluating ML utility preservation...")
        
        ml_results = {}
        
        try:
            # Create a prediction task based on data type
            if data_type == 'retail':
                # Predict high income clients
                target_col = 'high_income'
                threshold = original_df['monthly_income'].quantile(0.7)
                original_df_ml = original_df.copy()
                original_df_ml[target_col] = (original_df_ml['monthly_income'] > threshold).astype(int)
                
                synthetic_df_ml = synthetic_df.copy()
                synthetic_df_ml[target_col] = (synthetic_df_ml['monthly_income'] > threshold).astype(int)
                
            elif data_type == 'corporate':
                # Predict large companies
                target_col = 'is_large'
                original_df_ml = original_df.copy()
                original_df_ml[target_col] = (original_df_ml['company_size'] == 'large').astype(int)
                
                synthetic_df_ml = synthetic_df.copy()
                synthetic_df_ml[target_col] = (synthetic_df_ml['company_size'] == 'large').astype(int)
            
            # Prepare features for ML
            feature_cols = original_df_ml.select_dtypes(include=[np.number]).columns
            feature_cols = [col for col in feature_cols if col != target_col and 'client_id' not in col.lower()]
            
            if len(feature_cols) > 0 and target_col in original_df_ml.columns:
                # Encode categorical if needed
                X_orig = original_df_ml[feature_cols].fillna(0)
                y_orig = original_df_ml[target_col]
                
                X_synth = synthetic_df_ml[feature_cols].fillna(0)
                y_synth = synthetic_df_ml[target_col]
                
                # Train model on original data
                X_train_orig, X_test_orig, y_train_orig, y_test_orig = train_test_split(
                    X_orig, y_orig, test_size=0.3, random_state=42, stratify=y_orig
                )
                
                model_orig = RandomForestClassifier(n_estimators=100, random_state=42)
                model_orig.fit(X_train_orig, y_train_orig)
                orig_score = model_orig.score(X_test_orig, y_test_orig)
                
                # Train model on synthetic data
                if len(X_synth) > 50:  # Minimum samples for meaningful ML
                    X_train_synth, X_test_synth, y_train_synth, y_test_synth = train_test_split(
                        X_synth, y_synth, test_size=0.3, random_state=42, 
                        stratify=y_synth if len(np.unique(y_synth)) > 1 else None
                    )
                    
                    model_synth = RandomForestClassifier(n_estimators=100, random_state=42)
                    model_synth.fit(X_train_synth, y_train_synth)
                    synth_score = model_synth.score(X_test_synth, y_test_synth)
                    
                    # Cross-evaluation: model trained on synthetic, tested on original
                    cross_score = model_synth.score(X_test_orig, y_test_orig)
                    
                    ml_results = {
                        'original_model_accuracy': float(orig_score),
                        'synthetic_model_accuracy': float(synth_score),
                        'cross_evaluation_accuracy': float(cross_score),
                        'utility_preservation_score': float(min(synth_score / orig_score, cross_score / orig_score)),
                        'features_used': len(feature_cols),
                        'target_variable': target_col
                    }
                else:
                    ml_results = {
                        'error': 'Insufficient synthetic data for ML evaluation',
                        'utility_preservation_score': 0.5
                    }
            else:
                ml_results = {
                    'error': 'No suitable features or target for ML evaluation',
                    'utility_preservation_score': 0.5
                }
                
        except Exception as e:
            ml_results = {
                'error': f'ML utility evaluation failed: {str(e)}',
                'utility_preservation_score': 0.5
            }
        
        return ml_results
    
    def _evaluate_correlation_preservation(self, original_df: pd.DataFrame, 
                                         synthetic_df: pd.DataFrame) -> Dict:
        """Evaluate preservation of feature correlations"""
        logger.info("🔗 Evaluating correlation preservation...")
        
        correlation_results = {}
        
        # Get numerical columns common to both datasets
        orig_numerical = original_df.select_dtypes(include=[np.number])
        synth_numerical = synthetic_df.select_dtypes(include=[np.number])
        
        common_cols = list(set(orig_numerical.columns) & set(synth_numerical.columns))
        common_cols = [col for col in common_cols if 'client_id' not in col.lower()]
        
        if len(common_cols) >= 2:
            # Calculate correlation matrices
            orig_corr = orig_numerical[common_cols].corr()
            synth_corr = synth_numerical[common_cols].corr()
            
            # Compare correlation matrices
            correlation_differences = []
            significant_differences = 0
            
            for i, col1 in enumerate(common_cols):
                for j, col2 in enumerate(common_cols):
                    if i < j:  # Avoid duplicates and diagonal
                        orig_corr_val = orig_corr.loc[col1, col2]
                        synth_corr_val = synth_corr.loc[col1, col2]
                        
                        diff = abs(orig_corr_val - synth_corr_val)
                        correlation_differences.append(diff)
                        
                        if diff > 0.2:  # Significant difference threshold
                            significant_differences += 1
            
            mean_correlation_diff = np.mean(correlation_differences) if correlation_differences else 0
            correlation_preservation_score = 1 - mean_correlation_diff
            
            correlation_results = {
                'mean_correlation_difference': float(mean_correlation_diff),
                'max_correlation_difference': float(max(correlation_differences)) if correlation_differences else 0,
                'significant_differences': significant_differences,
                'total_correlations_compared': len(correlation_differences),
                'correlation_preservation_score': float(max(0, correlation_preservation_score)),
                'features_analyzed': common_cols
            }
        else:
            correlation_results = {
                'error': 'Insufficient numerical features for correlation analysis',
                'correlation_preservation_score': 0.5
            }
        
        return correlation_results
    
    def _calculate_overall_quality_score(self, evaluation_report: Dict) -> Dict:
        """Calculate overall quality score from all evaluation components"""
        
        # Extract component scores
        statistical_score = evaluation_report.get('statistical_similarity', {}).get('overall_statistical_similarity', 0.5)
        business_rules_score = evaluation_report.get('business_rules', {}).get('overall_compliance', 0.5)
        privacy_score = evaluation_report.get('privacy', {}).get('overall_privacy_score', 0.5)
        ml_utility_score = evaluation_report.get('ml_utility', {}).get('utility_preservation_score', 0.5)
        correlation_score = evaluation_report.get('correlation_preservation', {}).get('correlation_preservation_score', 0.5)
        
        # Weighted overall score
        weights = {
            'statistical_similarity': 0.25,
            'business_rules': 0.25,
            'privacy': 0.20,
            'ml_utility': 0.15,
            'correlation_preservation': 0.15
        }
        
        total_score = (
            statistical_score * weights['statistical_similarity'] +
            business_rules_score * weights['business_rules'] +
            privacy_score * weights['privacy'] +
            ml_utility_score * weights['ml_utility'] +
            correlation_score * weights['correlation_preservation']
        )
        
        # Quality assessment
        if total_score >= 0.9:
            quality_grade = 'Excellent'
        elif total_score >= 0.8:
            quality_grade = 'Good'
        elif total_score >= 0.7:
            quality_grade = 'Acceptable'
        elif total_score >= 0.6:
            quality_grade = 'Poor'
        else:
            quality_grade = 'Unacceptable'
        
        # Check if meets thresholds
        threshold_compliance = {
            'statistical_similarity': statistical_score >= self.quality_thresholds['statistical_similarity'],
            'business_rule_compliance': business_rules_score >= self.quality_thresholds['business_rule_compliance'],
            'privacy_score': privacy_score >= self.quality_thresholds['privacy_score'],
            'ml_utility': ml_utility_score >= self.quality_thresholds['ml_utility'],
            'correlation_preservation': correlation_score >= self.quality_thresholds['correlation_preservation']
        }
        
        return {
            'total_score': float(total_score),
            'quality_grade': quality_grade,
            'component_scores': {
                'statistical_similarity': float(statistical_score),
                'business_rules': float(business_rules_score),
                'privacy': float(privacy_score),
                'ml_utility': float(ml_utility_score),
                'correlation_preservation': float(correlation_score)
            },
            'weights_used': weights,
            'threshold_compliance': threshold_compliance,
            'meets_all_thresholds': all(threshold_compliance.values()),
            'recommendation': self._get_quality_recommendation(total_score, threshold_compliance)
        }
    
    def _get_quality_recommendation(self, total_score: float, threshold_compliance: Dict) -> str:
        """Generate quality improvement recommendations"""
        if total_score >= 0.9:
            return "Excellent quality synthetic data. Ready for production use."
        elif total_score >= 0.8:
            return "Good quality synthetic data. Consider minor improvements in lower-scoring areas."
        elif total_score >= 0.7:
            failed_areas = [area for area, passed in threshold_compliance.items() if not passed]
            return f"Acceptable quality. Focus on improving: {', '.join(failed_areas)}"
        else:
            return "Quality below acceptable threshold. Consider retraining CTGAN with different hyperparameters or more data."
    
    def _generate_quality_visualizations(self, original_df: pd.DataFrame, 
                                       synthetic_df: pd.DataFrame, data_type: str):
        """Generate quality assessment visualizations"""
        logger.info("📊 Generating quality visualizations...")
        
        plt.style.use('default')
        
        # Create comparison plots
        numerical_cols = original_df.select_dtypes(include=[np.number]).columns
        numerical_cols = [col for col in numerical_cols if col in synthetic_df.columns and 'client_id' not in col.lower()]
        
        if len(numerical_cols) >= 2:
            # Distribution comparison plots
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle(f'{data_type.title()} Data Quality Assessment', fontsize=16)
            
            # Plot first 4 numerical features
            plot_cols = numerical_cols[:4]
            
            for i, col in enumerate(plot_cols):
                row, col_idx = i // 2, i % 2
                ax = axes[row, col_idx]
                
                ax.hist(original_df[col], alpha=0.7, label='Original', bins=30, density=True)
                ax.hist(synthetic_df[col], alpha=0.7, label='Synthetic', bins=30, density=True)
                ax.set_title(f'{col} Distribution')
                ax.legend()
                ax.grid(True, alpha=0.3)
            
            # Save plot
            plot_path = self.output_dir / f"{data_type}_distribution_comparison.png"
            plt.tight_layout()
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"📈 Distribution comparison plot saved: {plot_path}")
    
    def _save_evaluation_report(self, evaluation_report: Dict, data_type: str):
        """Save evaluation report to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.output_dir / f"{data_type}_quality_evaluation_{timestamp}.json"
        
        with open(report_path, 'w') as f:
            json.dump(evaluation_report, f, indent=2, default=str)
        
        logger.info(f"💾 Evaluation report saved: {report_path}")
    
    def compare_multiple_models(self, original_df: pd.DataFrame, 
                               synthetic_datasets: Dict[str, pd.DataFrame], 
                               data_type: str) -> Dict:
        """Compare quality across multiple synthetic datasets"""
        logger.info(f"🔄 Comparing multiple {data_type} models...")
        
        comparison_results = {
            'comparison_timestamp': datetime.now().isoformat(),
            'data_type': data_type,
            'models_compared': list(synthetic_datasets.keys()),
            'model_evaluations': {},
            'ranking': {}
        }
        
        # Evaluate each model
        for model_name, synthetic_df in synthetic_datasets.items():
            logger.info(f"  Evaluating {model_name}...")
            
            if data_type == 'retail':
                evaluation = self.evaluate_retail_quality(original_df, synthetic_df)
            else:
                evaluation = self.evaluate_corporate_quality(original_df, synthetic_df)
            
            comparison_results['model_evaluations'][model_name] = evaluation
        
        # Create ranking
        model_scores = {
            model: eval_result['overall_quality']['total_score']
            for model, eval_result in comparison_results['model_evaluations'].items()
        }
        
        ranked_models = sorted(model_scores.items(), key=lambda x: x[1], reverse=True)
        
        comparison_results['ranking'] = {
            'best_model': ranked_models[0][0] if ranked_models else None,
            'model_scores': dict(ranked_models),
            'score_differences': {
                model: ranked_models[0][1] - score 
                for model, score in ranked_models
            } if len(ranked_models) > 1 else {}
        }
        
        # Save comparison report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        comparison_path = self.output_dir / f"{data_type}_model_comparison_{timestamp}.json"
        
        with open(comparison_path, 'w') as f:
            json.dump(comparison_results, f, indent=2, default=str)
        
        logger.info(f"📊 Model comparison completed and saved: {comparison_path}")
        
        return comparison_results

# Example usage and testing
if __name__ == "__main__":
    # Test the quality evaluator
    evaluator = CTGANQualityEvaluator()
    
    # Create sample data for testing
    original_retail = pd.DataFrame({
        'client_id': ['R_001', 'R_002', 'R_003', 'R_004', 'R_005'] * 20,
        'age': np.random.randint(18, 80, 100),
        'monthly_income': np.random.uniform(500, 8000, 100),
        'gender': np.random.choice(['M', 'F'], 100),
        'risk_tolerance': np.random.uniform(0, 1, 100),
        'satisfaction_score': np.random.uniform(0.3, 1.0, 100),
        'digital_engagement_score': np.random.uniform(0, 1, 100)
    })
    
    # Create synthetic data (slightly modified original for testing)
    synthetic_retail = original_retail.copy()
    synthetic_retail['client_id'] = ['CTGAN_R_' + f'{i:03d}' for i in range(100)]
    synthetic_retail['age'] += np.random.normal(0, 2, 100)
    synthetic_retail['monthly_income'] *= np.random.normal(1, 0.1, 100)
    
    # Evaluate quality
    try:
        evaluation_report = evaluator.evaluate_retail_quality(original_retail, synthetic_retail)
        print("🎯 Quality evaluation completed!")
        print(f"Overall Quality Score: {evaluation_report['overall_quality']['total_score']:.3f}")
        print(f"Quality Grade: {evaluation_report['overall_quality']['quality_grade']}")
        
    except Exception as e:
        print(f"❌ Evaluation test failed: {e}")
    
    print("\n🧪 Quality Evaluator test completed!")