#!/usr/bin/env python3
"""
Advanced Data Preprocessor for CTGAN Training
Transforms Week 1 manual data into ML-ready format with proper encoding,
normalization, and correlation preservation for high-quality CTGAN training.
Company-grade preprocessing with extensive validation and monitoring.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle
import logging
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class CTGANDataPreprocessor:
    """Enterprise-grade data preprocessor for CTGAN training"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        self.preprocessors = {}
        self.feature_info = {}
        self.is_fitted = False
        
        # Setup output directories
        self.model_dir = Path("../../data/ctgan/models")
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("🔧 CTGAN Data Preprocessor initialized")
    
    def _default_config(self) -> Dict:
        """Default preprocessing configuration"""
        return {
            'retail': {
                'numerical_features': [
                    'age', 'monthly_income', 'risk_tolerance', 
                    'satisfaction_score', 'digital_engagement_score'
                ],
                'categorical_features': [
                    'gender', 'governorate', 'education_level', 
                    'employment_sector', 'preferred_channel'
                ],
                'normalization_method': 'standard',  # 'standard', 'minmax', 'robust'
                'handle_outliers': True,
                'outlier_method': 'iqr',  # 'iqr', 'zscore'
                'categorical_encoding': 'label'  # 'label', 'onehot'
            },
            'corporate': {
                'numerical_features': [
                    'employee_count', 'annual_revenue', 'digital_maturity_score',
                    'cash_flow_predictability', 'seasonal_variation'
                ],
                'categorical_features': [
                    'business_sector', 'company_size', 'headquarters_governorate', 'credit_rating'
                ],
                'normalization_method': 'standard',
                'handle_outliers': True,
                'outlier_method': 'iqr',
                'categorical_encoding': 'label'
            }
        }
    
    def prepare_retail_data(self, retail_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Prepare retail client data for CTGAN training"""
        logger.info(f"📊 Preprocessing {len(retail_df)} retail clients for CTGAN...")
        
        df = retail_df.copy()
        config = self.config['retail']
        
        # Data quality checks
        quality_report = self._assess_data_quality(df, 'retail')
        
        # Handle missing values
        df = self._handle_missing_values(df, config)
        
        # Handle outliers
        if config['handle_outliers']:
            df = self._handle_outliers(df, config['numerical_features'], config['outlier_method'])
        
        # Feature engineering
        df = self._engineer_retail_features(df)
        
        # Encode categorical variables
        df, categorical_mappings = self._encode_categorical_features(
            df, config['categorical_features'], config['categorical_encoding']
        )
        
        # Normalize numerical features
        df, numerical_scalers = self._normalize_numerical_features(
            df, config['numerical_features'], config['normalization_method']
        )
        
        # Store preprocessing info
        preprocessing_info = {
            'categorical_mappings': categorical_mappings,
            'numerical_scalers': numerical_scalers,
            'feature_info': self._get_feature_info(df),
            'quality_report': quality_report,
            'config': config
        }
        
        # Save preprocessing artifacts
        self._save_preprocessing_info(preprocessing_info, 'retail')
        
        logger.info(f"✅ Retail data preprocessed: {df.shape[0]} samples, {df.shape[1]} features")
        return df, preprocessing_info
    
    def prepare_corporate_data(self, corporate_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Prepare corporate client data for CTGAN training"""
        logger.info(f"📊 Preprocessing {len(corporate_df)} corporate clients for CTGAN...")
        
        df = corporate_df.copy()
        config = self.config['corporate']
        
        # Data quality checks
        quality_report = self._assess_data_quality(df, 'corporate')
        
        # Handle missing values
        df = self._handle_missing_values(df, config)
        
        # Handle outliers (especially important for revenue)
        if config['handle_outliers']:
            df = self._handle_outliers(df, config['numerical_features'], config['outlier_method'])
        
        # Feature engineering
        df = self._engineer_corporate_features(df)
        
        # Encode categorical variables
        df, categorical_mappings = self._encode_categorical_features(
            df, config['categorical_features'], config['categorical_encoding']
        )
        
        # Normalize numerical features
        df, numerical_scalers = self._normalize_numerical_features(
            df, config['numerical_features'], config['normalization_method']
        )
        
        # Store preprocessing info
        preprocessing_info = {
            'categorical_mappings': categorical_mappings,
            'numerical_scalers': numerical_scalers,
            'feature_info': self._get_feature_info(df),
            'quality_report': quality_report,
            'config': config
        }
        
        # Save preprocessing artifacts
        self._save_preprocessing_info(preprocessing_info, 'corporate')
        
        logger.info(f"✅ Corporate data preprocessed: {df.shape[0]} samples, {df.shape[1]} features")
        return df, preprocessing_info
    
    def _assess_data_quality(self, df: pd.DataFrame, client_type: str) -> Dict:
        """Comprehensive data quality assessment"""
        return {
            'total_records': len(df),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicate_records': df.duplicated().sum(),
            'numerical_stats': df.select_dtypes(include=[np.number]).describe().to_dict(),
            'categorical_stats': {col: df[col].value_counts().to_dict() 
                                for col in df.select_dtypes(include=['object']).columns},
            'correlation_matrix': df.select_dtypes(include=[np.number]).corr().to_dict(),
            'data_types': df.dtypes.to_dict()
        }
    
    def _handle_missing_values(self, df: pd.DataFrame, config: Dict) -> pd.DataFrame:
        """Handle missing values with business logic"""
        # For numerical features, use median imputation
        for col in config['numerical_features']:
            if col in df.columns and df[col].isnull().any():
                df[col].fillna(df[col].median(), inplace=True)
                logger.info(f"Imputed {col} missing values with median")
        
        # For categorical features, use mode imputation
        for col in config['categorical_features']:
            if col in df.columns and df[col].isnull().any():
                df[col].fillna(df[col].mode()[0], inplace=True)
                logger.info(f"Imputed {col} missing values with mode")
        
        return df
    
    def _handle_outliers(self, df: pd.DataFrame, numerical_cols: List[str], method: str) -> pd.DataFrame:
        """Handle outliers using specified method"""
        for col in numerical_cols:
            if col not in df.columns:
                continue
                
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Cap outliers instead of removing them
                df[col] = df[col].clip(lower_bound, upper_bound)
                
            elif method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                df[col] = df[col].mask(z_scores > 3, df[col].median())
        
        return df
    
    def _engineer_retail_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer additional features for retail clients"""
        # Age groups
        df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 50, 65, 100], 
                                labels=['young', 'young_adult', 'middle_age', 'senior', 'elderly'])
        
        # Income quintiles
        df['income_quintile'] = pd.qcut(df['monthly_income'], q=5, labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])
        
        # Digital adoption score (combination of age and engagement)
        df['digital_adoption'] = (df['digital_engagement_score'] * 0.7 + 
                                 (1 - (df['age'] - 18) / 62) * 0.3)
        
        # Risk-return preference
        df['risk_income_ratio'] = df['risk_tolerance'] * np.log1p(df['monthly_income'])
        
        return df
    
    def _engineer_corporate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer additional features for corporate clients"""
        # Revenue per employee
        df['revenue_per_employee'] = df['annual_revenue'] / df['employee_count']
        
        # Company maturity (based on size and digital score)
        size_scores = {'micro': 1, 'small': 2, 'medium': 3, 'large': 4}
        df['company_maturity'] = (df['company_size'].map(size_scores) + 
                                 df['digital_maturity_score'] * 4) / 2
        
        # Business volatility (inverse of cash flow predictability)
        df['business_volatility'] = 1 - df['cash_flow_predictability']
        
        # Digital readiness
        df['digital_readiness'] = (df['digital_maturity_score'] * 0.8 + 
                                  (1 - df['seasonal_variation']) * 0.2)
        
        return df
    
    def _encode_categorical_features(self, df: pd.DataFrame, categorical_cols: List[str], 
                                   encoding_method: str) -> Tuple[pd.DataFrame, Dict]:
        """Encode categorical features for CTGAN"""
        categorical_mappings = {}
        
        for col in categorical_cols:
            if col not in df.columns:
                continue
                
            if encoding_method == 'label':
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                categorical_mappings[col] = {
                    'encoder': le,
                    'classes': le.classes_.tolist()
                }
                
        return df, categorical_mappings
    
    def _normalize_numerical_features(self, df: pd.DataFrame, numerical_cols: List[str], 
                                    method: str) -> Tuple[pd.DataFrame, Dict]:
        """Normalize numerical features"""
        numerical_scalers = {}
        
        for col in numerical_cols:
            if col not in df.columns:
                continue
                
            if method == 'standard':
                scaler = StandardScaler()
            elif method == 'minmax':
                scaler = MinMaxScaler()
            else:
                continue
                
            df[col] = scaler.fit_transform(df[[col]]).flatten()
            numerical_scalers[col] = scaler
        
        return df, numerical_scalers
    
    def _get_feature_info(self, df: pd.DataFrame) -> Dict:
        """Get feature information for CTGAN configuration"""
        feature_info = {}
        
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                feature_info[col] = {
                    'type': 'continuous',
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'std': float(df[col].std())
                }
            else:
                feature_info[col] = {
                    'type': 'discrete',
                    'categories': int(df[col].nunique())
                }
        
        return feature_info
    
    def _save_preprocessing_info(self, preprocessing_info: Dict, client_type: str):
        """Save preprocessing information for later use"""
        output_path = self.model_dir / f"{client_type}_preprocessing_info.pkl"
        
        with open(output_path, 'wb') as f:
            pickle.dump(preprocessing_info, f)
        
        logger.info(f"💾 Preprocessing info saved: {output_path}")
    
    def load_preprocessing_info(self, client_type: str) -> Dict:
        """Load preprocessing information"""
        input_path = self.model_dir / f"{client_type}_preprocessing_info.pkl"
        
        with open(input_path, 'rb') as f:
            preprocessing_info = pickle.load(f)
        
        logger.info(f"📁 Preprocessing info loaded: {input_path}")
        return preprocessing_info
    
    def inverse_transform_data(self, generated_df: pd.DataFrame, client_type: str) -> pd.DataFrame:
        """Transform CTGAN generated data back to original format"""
        logger.info(f"🔄 Inverse transforming {client_type} data...")
        
        # Load preprocessing info
        preprocessing_info = self.load_preprocessing_info(client_type)
        
        df = generated_df.copy()
        
        # Inverse transform numerical features
        numerical_scalers = preprocessing_info['numerical_scalers']
        for col, scaler in numerical_scalers.items():
            if col in df.columns:
                df[col] = scaler.inverse_transform(df[[col]]).flatten()
        
        # Inverse transform categorical features
        categorical_mappings = preprocessing_info['categorical_mappings']
        for col, mapping_info in categorical_mappings.items():
            if col in df.columns:
                encoder = mapping_info['encoder']
                # Ensure values are within valid range
                df[col] = np.clip(df[col].round().astype(int), 0, len(encoder.classes_) - 1)
                df[col] = encoder.inverse_transform(df[col])
        
        logger.info(f"✅ Inverse transformation completed")
        return df

# Example usage and testing
if __name__ == "__main__":
    # Test with sample data
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).parent))
    
    # This would typically load your Week 1 data
    sample_retail = pd.DataFrame({
        'client_id': ['R_001', 'R_002', 'R_003'],
        'age': [25, 45, 60],
        'monthly_income': [1200, 2500, 1800],
        'gender': ['M', 'F', 'M'],
        'governorate': ['Tunis', 'Sfax', 'Sousse'],
        'risk_tolerance': [0.7, 0.3, 0.5],
        'satisfaction_score': [0.8, 0.9, 0.6],
        'digital_engagement_score': [0.9, 0.5, 0.3]
    })
    
    preprocessor = CTGANDataPreprocessor()
    processed_data, info = preprocessor.prepare_retail_data(sample_retail)
    
    print("🧪 Preprocessing test completed successfully!")
    print(f"Original shape: {sample_retail.shape}")
    print(f"Processed shape: {processed_data.shape}")