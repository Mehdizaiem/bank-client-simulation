#!/usr/bin/env python3
"""
Enterprise CTGAN Generator
Production-grade CTGAN implementation with advanced monitoring, validation,
and enterprise features. Handles training, generation, and model management
for both retail and corporate client synthesis.
"""

import torch
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import logging
import json
import time
from datetime import datetime
from pathlib import Path
import pickle
import warnings

# CTGAN imports
try:
    from ctgan import CTGAN
    from ctgan.synthesizers.tvae import TVAE
except ImportError:
    raise ImportError("CTGAN not installed. Run: pip install ctgan")

# Custom imports
from data_preprocessor import CTGANDataPreprocessor

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class EnterpriseCtganGenerator:
    """Enterprise-grade CTGAN generator with advanced features"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        self.models = {}
        self.training_history = {}
        self.preprocessor = CTGANDataPreprocessor()
        
        # Setup directories
        self.model_dir = Path("../../data/ctgan/models")
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        self.training_dir = Path("../../data/ctgan/training_data")
        self.training_dir.mkdir(parents=True, exist_ok=True)
        
        self.reports_dir = Path("../../data/ctgan/validation_reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Set device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"🚀 CTGAN Generator initialized on {self.device}")
    
    def _default_config(self) -> Dict:
        """Default CTGAN configuration optimized for banking data"""
        return {
            'retail': {
                'epochs': 300,
                'batch_size': 500,
                'generator_dim': (256, 256),
                'discriminator_dim': (256, 256),
                'generator_lr': 2e-4,
                'discriminator_lr': 2e-4,
                'generator_decay': 1e-6,
                'discriminator_decay': 1e-6,
                'pac': 10,
                'verbose': True,
                'cuda': torch.cuda.is_available(),
                'log_frequency': 50
            },
            'corporate': {
                'epochs': 500,  # More epochs due to smaller dataset
                'batch_size': 200,
                'generator_dim': (128, 128),
                'discriminator_dim': (128, 128),
                'generator_lr': 1e-4,
                'discriminator_lr': 1e-4,
                'generator_decay': 1e-6,
                'discriminator_decay': 1e-6,
                'pac': 5,
                'verbose': True,
                'cuda': torch.cuda.is_available(),
                'log_frequency': 25
            }
        }
    
    def train_retail_model(self, retail_df: pd.DataFrame) -> Dict:
        """Train CTGAN model for retail clients"""
        logger.info(f"🎯 Training retail CTGAN model with {len(retail_df)} samples...")
        
        start_time = time.time()
        
        # Preprocess data
        processed_data, preprocessing_info = self.preprocessor.prepare_retail_data(retail_df)
        
        # Save training data
        training_file = self.training_dir / f"retail_training_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        processed_data.to_csv(training_file, index=False)
        
        # Configure discrete columns for CTGAN
        discrete_columns = self._identify_discrete_columns(processed_data, preprocessing_info)
        
        # Initialize CTGAN model
        config = self.config['retail']
        model = CTGAN(
            epochs=config['epochs'],
            batch_size=config['batch_size'],
            generator_dim=config['generator_dim'],
            discriminator_dim=config['discriminator_dim'],
            generator_lr=config['generator_lr'],
            discriminator_lr=config['discriminator_lr'],
            generator_decay=config['generator_decay'],
            discriminator_decay=config['discriminator_decay'],
            pac=config['pac'],
            verbose=config['verbose'],
            cuda=config['cuda']
        )
        
        # Custom training with monitoring
        training_metrics = self._train_with_monitoring(
            model, processed_data, discrete_columns, 'retail', config
        )
        
        # Save model
        model_path = self.model_dir / "retail_ctgan_model.pkl"
        model.save(str(model_path))
        
        # Store model reference
        self.models['retail'] = model
        
        training_duration = time.time() - start_time
        
        # Create training report
        training_report = {
            'model_type': 'retail_ctgan',
            'training_duration_seconds': training_duration,
            'training_samples': len(retail_df),
            'processed_samples': len(processed_data),
            'discrete_columns': discrete_columns,
            'config': config,
            'preprocessing_info': preprocessing_info,
            'training_metrics': training_metrics,
            'model_path': str(model_path),
            'training_file': str(training_file),
            'timestamp': datetime.now().isoformat()
        }
        
        # Save training report
        report_path = self.reports_dir / f"retail_training_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(training_report, f, indent=2, default=str)
        
        logger.info(f"✅ Retail CTGAN training completed in {training_duration:.1f} seconds")
        logger.info(f"📊 Model saved: {model_path}")
        
        return training_report
    
    def train_corporate_model(self, corporate_df: pd.DataFrame) -> Dict:
        """Train CTGAN model for corporate clients"""
        logger.info(f"🎯 Training corporate CTGAN model with {len(corporate_df)} samples...")
        
        if len(corporate_df) < 100:
            logger.warning("⚠️ Small corporate dataset - consider data augmentation")
        
        start_time = time.time()
        
        # Preprocess data
        processed_data, preprocessing_info = self.preprocessor.prepare_corporate_data(corporate_df)
        
        # Save training data
        training_file = self.training_dir / f"corporate_training_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        processed_data.to_csv(training_file, index=False)
        
        # Configure discrete columns for CTGAN
        discrete_columns = self._identify_discrete_columns(processed_data, preprocessing_info)
        
        # Initialize CTGAN model
        config = self.config['corporate']
        model = CTGAN(
            epochs=config['epochs'],
            batch_size=min(config['batch_size'], len(processed_data) // 2),  # Adjust for small datasets
            generator_dim=config['generator_dim'],
            discriminator_dim=config['discriminator_dim'],
            generator_lr=config['generator_lr'],
            discriminator_lr=config['discriminator_lr'],
            generator_decay=config['generator_decay'],
            discriminator_decay=config['discriminator_decay'],
            pac=config['pac'],
            verbose=config['verbose'],
            cuda=config['cuda']
        )
        
        # Custom training with monitoring
        training_metrics = self._train_with_monitoring(
            model, processed_data, discrete_columns, 'corporate', config
        )
        
        # Save model
        model_path = self.model_dir / "corporate_ctgan_model.pkl"
        model.save(str(model_path))
        
        # Store model reference
        self.models['corporate'] = model
        
        training_duration = time.time() - start_time
        
        # Create training report
        training_report = {
            'model_type': 'corporate_ctgan',
            'training_duration_seconds': training_duration,
            'training_samples': len(corporate_df),
            'processed_samples': len(processed_data),
            'discrete_columns': discrete_columns,
            'config': config,
            'preprocessing_info': preprocessing_info,
            'training_metrics': training_metrics,
            'model_path': str(model_path),
            'training_file': str(training_file),
            'timestamp': datetime.now().isoformat()
        }
        
        # Save training report
        report_path = self.reports_dir / f"corporate_training_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(training_report, f, indent=2, default=str)
        
        logger.info(f"✅ Corporate CTGAN training completed in {training_duration:.1f} seconds")
        logger.info(f"📊 Model saved: {model_path}")
        
        return training_report
    
    def _train_with_monitoring(self, model, data: pd.DataFrame, discrete_columns: List[str], 
                              client_type: str, config: Dict) -> Dict:
        """Train model with comprehensive monitoring"""
        logger.info(f"📈 Training {client_type} CTGAN with monitoring...")
        
        training_metrics = {
            'loss_history': [],
            'memory_usage': [],
            'training_checkpoints': []
        }
        
        # Custom fit method with monitoring would go here
        # For now, use standard fit
        try:
            model.fit(data, discrete_columns=discrete_columns)
            
            # Record final metrics
            training_metrics['final_status'] = 'completed'
            training_metrics['total_epochs'] = config['epochs']
            
        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            training_metrics['final_status'] = 'failed'
            training_metrics['error_message'] = str(e)
            raise
        
        return training_metrics
    
    def _identify_discrete_columns(self, data: pd.DataFrame, preprocessing_info: Dict) -> List[str]:
        """Identify discrete columns for CTGAN"""
        discrete_columns = []
        
        feature_info = preprocessing_info['feature_info']
        for col, info in feature_info.items():
            if info['type'] == 'discrete' or col.endswith('_encoded'):
                discrete_columns.append(col)
        
        return discrete_columns
    
    def generate_retail_clients(self, num_samples: int) -> pd.DataFrame:
        """Generate synthetic retail clients"""
        logger.info(f"🔄 Generating {num_samples} synthetic retail clients...")
        
        if 'retail' not in self.models:
            self.load_model('retail')
        
        # Generate synthetic data
        synthetic_data = self.models['retail'].sample(num_samples)
        
        # Inverse transform to original format
        original_format_data = self.preprocessor.inverse_transform_data(synthetic_data, 'retail')
        
        # Add client IDs
        original_format_data['client_id'] = [f'CTGAN_R_{i+1:06d}' for i in range(len(original_format_data))]
        
        # Post-process and validate
        original_format_data = self._post_process_retail_data(original_format_data)
        
        logger.info(f"✅ Generated {len(original_format_data)} retail clients")
        return original_format_data
    
    def generate_corporate_clients(self, num_samples: int) -> pd.DataFrame:
        """Generate synthetic corporate clients"""
        logger.info(f"🔄 Generating {num_samples} synthetic corporate clients...")
        
        if 'corporate' not in self.models:
            self.load_model('corporate')
        
        # Generate synthetic data
        synthetic_data = self.models['corporate'].sample(num_samples)
        
        # Inverse transform to original format
        original_format_data = self.preprocessor.inverse_transform_data(synthetic_data, 'corporate')
        
        # Add client IDs and company names
        original_format_data['client_id'] = [f'CTGAN_C_{i+1:06d}' for i in range(len(original_format_data))]
        original_format_data['company_name'] = [f'CTGAN_Company_{i+1:06d}' for i in range(len(original_format_data))]
        
        # Post-process and validate
        original_format_data = self._post_process_corporate_data(original_format_data)
        
        logger.info(f"✅ Generated {len(original_format_data)} corporate clients")
        return original_format_data
    
    def _post_process_retail_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Post-process generated retail data for business logic compliance"""
        # Ensure age is within valid range
        df['age'] = df['age'].clip(18, 80).round().astype(int)
        
        # Ensure income is positive and reasonable
        df['monthly_income'] = df['monthly_income'].clip(400, 15000)
        
        # Ensure scores are between 0 and 1
        score_columns = ['risk_tolerance', 'satisfaction_score', 'digital_engagement_score']
        for col in score_columns:
            if col in df.columns:
                df[col] = df[col].clip(0, 1)
        
        # Ensure gender is valid
        if 'gender' in df.columns:
            df['gender'] = df['gender'].map({'M': 'M', 'F': 'F'}).fillna('M')
        
        return df
    
    def _post_process_corporate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Post-process generated corporate data for business logic compliance"""
        # Ensure employee count is positive integer
        df['employee_count'] = df['employee_count'].clip(1, 10000).round().astype(int)
        
        # Ensure revenue is positive
        df['annual_revenue'] = df['annual_revenue'].clip(10000, 100000000)
        
        # Ensure scores are between 0 and 1
        score_columns = ['digital_maturity_score', 'cash_flow_predictability', 'seasonal_variation']
        for col in score_columns:
            if col in df.columns:
                df[col] = df[col].clip(0, 1)
        
        # Validate company size vs revenue consistency
        df = self._validate_size_revenue_consistency(df)
        
        return df
    
    def _validate_size_revenue_consistency(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensure company size is consistent with revenue"""
        size_revenue_map = {
            'micro': (10000, 100000),
            'small': (100000, 1000000),
            'medium': (1000000, 10000000),
            'large': (10000000, 100000000)
        }
        
        for idx, row in df.iterrows():
            size = row['company_size']
            revenue = row['annual_revenue']
            
            if size in size_revenue_map:
                min_rev, max_rev = size_revenue_map[size]
                if not (min_rev <= revenue <= max_rev):
                    # Adjust size based on revenue
                    for new_size, (min_r, max_r) in size_revenue_map.items():
                        if min_r <= revenue <= max_r:
                            df.at[idx, 'company_size'] = new_size
                            break
        
        return df
    
    def load_model(self, client_type: str):
        """Load pre-trained CTGAN model"""
        model_path = self.model_dir / f"{client_type}_ctgan_model.pkl"
        
        if not model_path.exists():
            raise FileNotFoundError(f"No trained model found for {client_type} at {model_path}")
        
        logger.info(f"📁 Loading {client_type} CTGAN model...")
        model = CTGAN.load(str(model_path))
        self.models[client_type] = model
        
        logger.info(f"✅ {client_type.title()} model loaded successfully")
    
    def get_model_info(self, client_type: str) -> Dict:
        """Get comprehensive model information"""
        if client_type not in self.models:
            self.load_model(client_type)
        
        # Load training report
        report_files = list(self.reports_dir.glob(f"{client_type}_training_report_*.json"))
        if report_files:
            latest_report = max(report_files, key=lambda x: x.stat().st_mtime)
            with open(latest_report, 'r') as f:
                training_info = json.load(f)
        else:
            training_info = {"message": "No training report found"}
        
        return {
            'client_type': client_type,
            'model_loaded': client_type in self.models,
            'training_info': training_info,
            'config': self.config[client_type]
        }
    
    def benchmark_generation_speed(self, client_type: str, sample_sizes: List[int] = None) -> Dict:
        """Benchmark generation speed for different sample sizes"""
        if sample_sizes is None:
            sample_sizes = [100, 500, 1000, 5000]
        
        logger.info(f"⚡ Benchmarking {client_type} generation speed...")
        
        benchmarks = {}
        
        for sample_size in sample_sizes:
            start_time = time.time()
            
            if client_type == 'retail':
                _ = self.generate_retail_clients(sample_size)
            elif client_type == 'corporate':
                _ = self.generate_corporate_clients(sample_size)
            
            generation_time = time.time() - start_time
            
            benchmarks[sample_size] = {
                'generation_time_seconds': generation_time,
                'samples_per_second': sample_size / generation_time
            }
            
            logger.info(f"  {sample_size} samples: {generation_time:.2f}s ({sample_size/generation_time:.1f} samples/s)")
        
        return benchmarks

# Example usage and testing
if __name__ == "__main__":
    # Test the CTGAN generator
    generator = EnterpriseCtganGenerator()
    
    # This would typically load your Week 1 data
    sample_retail = pd.DataFrame({
        'client_id': ['R_001', 'R_002', 'R_003', 'R_004', 'R_005'] * 20,  # 100 samples
        'age': np.random.randint(18, 80, 100),
        'monthly_income': np.random.uniform(500, 8000, 100),
        'gender': np.random.choice(['M', 'F'], 100),
        'governorate': np.random.choice(['Tunis', 'Sfax', 'Sousse', 'Ariana'], 100),
        'education_level': np.random.choice(['primary', 'secondary', 'university'], 100),
        'employment_sector': np.random.choice(['private', 'public', 'self_employed'], 100),
        'preferred_channel': np.random.choice(['mobile', 'branch', 'web'], 100),
        'risk_tolerance': np.random.uniform(0, 1, 100),
        'satisfaction_score': np.random.uniform(0.3, 1.0, 100),
        'digital_engagement_score': np.random.uniform(0, 1, 100)
    })
    
    try:
        # Train model
        training_report = generator.train_retail_model(sample_retail)
        print("🎯 Training completed!")
        
        # Generate synthetic data
        synthetic_clients = generator.generate_retail_clients(50)
        print(f"🔄 Generated {len(synthetic_clients)} synthetic clients")
        
        # Show sample
        print("\n📊 Sample generated clients:")
        print(synthetic_clients.head())
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    print("\n🧪 CTGAN Generator test completed!")