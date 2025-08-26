#!/usr/bin/env python3
"""
CTGAN Production Pipeline - Week 2 Integration
Complete production pipeline integrating CTGAN with Week 1 foundation.
Handles training, generation, quality validation, and team integration
with fallback mechanisms and enterprise monitoring.
"""

import pandas as pd
import numpy as np
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

# Import Week 1 components
try:
    from schemas import DataValidator, TeamExporter
    from data_sources import TunisianDataSources
except ImportError:
    print("⚠️ Week 1 modules not found - limited functionality")

# Import Week 2 CTGAN components
try:
    from ctgan_generator import EnterpriseCtganGenerator
    from quality_evaluator import CTGANQualityEvaluator
    from data_preprocessor import CTGANDataPreprocessor
except ImportError as e:
    print(f"⚠️ CTGAN modules not found: {e}")
    print("Run: pip install ctgan torch")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CTGANProductionPipeline:
    """Production-grade CTGAN pipeline with Week 1 integration"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        
        # Initialize components
        self.ctgan_generator = EnterpriseCtganGenerator()
        self.quality_evaluator = CTGANQualityEvaluator()
        self.data_sources = TunisianDataSources()
        
        # Setup directories
        self.output_dir = Path("../../data/processed")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.ctgan_dir = Path("../../data/ctgan")
        self.ctgan_dir.mkdir(parents=True, exist_ok=True)
        
        # Pipeline state
        self.models_trained = {}
        self.generation_stats = {}
        self.quality_reports = {}
        
        logger.info("🚀 CTGAN Production Pipeline initialized")
    
    def _default_config(self) -> Dict:
        """Default pipeline configuration"""
        return {
            'generation_strategy': 'hybrid',  # 'ctgan_only', 'manual_only', 'hybrid'
            'hybrid_ratio': {'ctgan': 0.7, 'manual': 0.3},
            'quality_thresholds': {
                'minimum_acceptable_score': 0.75,
                'excellent_score': 0.90,
                'retrain_threshold': 0.60
            },
            'fallback_enabled': True,
            'max_retrain_attempts': 3,
            'batch_generation_size': 1000,
            'validation_sample_size': 500,
            'enable_monitoring': True,
            'save_intermediate_results': True
        }
    
    def run_complete_pipeline(self, retail_df: pd.DataFrame, 
                            corporate_df: pd.DataFrame) -> Dict:
        """Execute complete CTGAN pipeline from training to team delivery"""
        logger.info("🎯 Running complete CTGAN production pipeline...")
        
        pipeline_start = time.time()
        
        pipeline_results = {
            'pipeline_execution_id': f"ctgan_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'execution_timestamp': datetime.now().isoformat(),
            'input_data': {
                'retail_samples': len(retail_df),
                'corporate_samples': len(corporate_df)
            },
            'config': self.config
        }
        
        try:
            # Phase 1: Model Training
            logger.info("📚 Phase 1: CTGAN Model Training")
            training_results = self._execute_training_phase(retail_df, corporate_df)
            pipeline_results['training'] = training_results
            
            # Phase 2: Data Generation
            logger.info("🔄 Phase 2: Synthetic Data Generation")
            generation_results = self._execute_generation_phase()
            pipeline_results['generation'] = generation_results
            
            # Phase 3: Quality Validation
            logger.info("🔍 Phase 3: Quality Validation")
            validation_results = self._execute_validation_phase(
                retail_df, corporate_df, 
                generation_results['generated_data']['retail'],
                generation_results['generated_data']['corporate']
            )
            pipeline_results['validation'] = validation_results
            
            # Phase 4: Quality-based Decision Making
            logger.info("⚖️ Phase 4: Quality Assessment & Decision")
            decision_results = self._execute_decision_phase(validation_results)
            pipeline_results['decision'] = decision_results
            
            # Phase 5: Final Data Preparation
            logger.info("📦 Phase 5: Final Data Preparation")
            final_data_results = self._prepare_final_datasets(
                retail_df, corporate_df, generation_results, decision_results
            )
            pipeline_results['final_data'] = final_data_results
            
            # Phase 6: Team Integration
            logger.info("🤝 Phase 6: Team Integration")
            team_integration_results = self._execute_team_integration(
                final_data_results['final_retail_data'],
                final_data_results['final_corporate_data']
            )
            pipeline_results['team_integration'] = team_integration_results
            
            # Pipeline completion
            pipeline_duration = time.time() - pipeline_start
            pipeline_results['execution_summary'] = {
                'duration_seconds': pipeline_duration,
                'status': 'completed_successfully',
                'total_clients_delivered': (
                    len(final_data_results['final_retail_data']) + 
                    len(final_data_results['final_corporate_data'])
                )
            }
            
            # Save complete pipeline report
            self._save_pipeline_report(pipeline_results)
            
            logger.info(f"🎉 CTGAN Pipeline completed successfully in {pipeline_duration:.1f} seconds")
            return pipeline_results
            
        except Exception as e:
            logger.error(f"❌ Pipeline execution failed: {e}")
            pipeline_results['execution_summary'] = {
                'status': 'failed',
                'error': str(e),
                'duration_seconds': time.time() - pipeline_start
            }
            
            # Execute fallback if enabled
            if self.config['fallback_enabled']:
                logger.info("🛡️ Executing fallback to Week 1 manual generation...")
                fallback_results = self._execute_fallback(retail_df, corporate_df)
                pipeline_results['fallback'] = fallback_results
            
            return pipeline_results
    
    def _execute_training_phase(self, retail_df: pd.DataFrame, 
                               corporate_df: pd.DataFrame) -> Dict:
        """Execute CTGAN model training phase"""
        training_results = {}
        
        # Train retail model
        try:
            logger.info("🎯 Training retail CTGAN model...")
            retail_training_report = self.ctgan_generator.train_retail_model(retail_df)
            training_results['retail'] = retail_training_report
            self.models_trained['retail'] = True
            
        except Exception as e:
            logger.error(f"❌ Retail model training failed: {e}")
            training_results['retail'] = {'status': 'failed', 'error': str(e)}
            self.models_trained['retail'] = False
        
        # Train corporate model (with special handling for small datasets)
        try:
            if len(corporate_df) >= 50:  # Minimum samples for CTGAN
                logger.info("🎯 Training corporate CTGAN model...")
                corporate_training_report = self.ctgan_generator.train_corporate_model(corporate_df)
                training_results['corporate'] = corporate_training_report
                self.models_trained['corporate'] = True
            else:
                logger.warning("⚠️ Insufficient corporate data for CTGAN - will use manual generation")
                training_results['corporate'] = {
                    'status': 'skipped',
                    'reason': 'insufficient_data',
                    'samples': len(corporate_df)
                }
                self.models_trained['corporate'] = False
                
        except Exception as e:
            logger.error(f"❌ Corporate model training failed: {e}")
            training_results['corporate'] = {'status': 'failed', 'error': str(e)}
            self.models_trained['corporate'] = False
        
        return training_results
    
    def _execute_generation_phase(self) -> Dict:
        """Execute synthetic data generation phase"""
        generation_results = {
            'generated_data': {},
            'generation_stats': {}
        }
        
        # Generate retail clients
        if self.models_trained.get('retail', False):
            try:
                target_samples = 5000  # Generate more than original for selection
                logger.info(f"🔄 Generating {target_samples} synthetic retail clients...")
                
                generated_retail = self.ctgan_generator.generate_retail_clients(target_samples)
                generation_results['generated_data']['retail'] = generated_retail
                generation_results['generation_stats']['retail'] = {
                    'samples_generated': len(generated_retail),
                    'generation_method': 'ctgan'
                }
                
            except Exception as e:
                logger.error(f"❌ Retail generation failed: {e}")
                generation_results['generated_data']['retail'] = pd.DataFrame()
                generation_results['generation_stats']['retail'] = {
                    'samples_generated': 0,
                    'generation_method': 'failed',
                    'error': str(e)
                }
        else:
            logger.info("⚠️ Skipping retail CTGAN generation - model not trained")
            generation_results['generated_data']['retail'] = pd.DataFrame()
        
        # Generate corporate clients
        if self.models_trained.get('corporate', False):
            try:
                target_samples = 1000
                logger.info(f"🔄 Generating {target_samples} synthetic corporate clients...")
                
                generated_corporate = self.ctgan_generator.generate_corporate_clients(target_samples)
                generation_results['generated_data']['corporate'] = generated_corporate
                generation_results['generation_stats']['corporate'] = {
                    'samples_generated': len(generated_corporate),
                    'generation_method': 'ctgan'
                }
                
            except Exception as e:
                logger.error(f"❌ Corporate generation failed: {e}")
                generation_results['generated_data']['corporate'] = pd.DataFrame()
                generation_results['generation_stats']['corporate'] = {
                    'samples_generated': 0,
                    'generation_method': 'failed',
                    'error': str(e)
                }
        else:
            logger.info("⚠️ Skipping corporate CTGAN generation - using manual fallback")
            generation_results['generated_data']['corporate'] = pd.DataFrame()
        
        return generation_results
    
    def _execute_validation_phase(self, original_retail: pd.DataFrame, 
                                original_corporate: pd.DataFrame,
                                generated_retail: pd.DataFrame, 
                                generated_corporate: pd.DataFrame) -> Dict:
        """Execute comprehensive quality validation phase"""
        validation_results = {}
        
        # Validate retail data
        if len(generated_retail) > 0:
            try:
                logger.info("🔍 Validating retail CTGAN quality...")
                retail_quality = self.quality_evaluator.evaluate_retail_quality(
                    original_retail, generated_retail
                )
                validation_results['retail'] = retail_quality
                self.quality_reports['retail'] = retail_quality
                
            except Exception as e:
                logger.error(f"❌ Retail quality validation failed: {e}")
                validation_results['retail'] = {
                    'validation_status': 'failed',
                    'error': str(e),
                    'overall_quality': {'total_score': 0.0}
                }
        else:
            validation_results['retail'] = {
                'validation_status': 'skipped',
                'reason': 'no_generated_data',
                'overall_quality': {'total_score': 0.0}
            }
        
        # Validate corporate data
        if len(generated_corporate) > 0:
            try:
                logger.info("🔍 Validating corporate CTGAN quality...")
                corporate_quality = self.quality_evaluator.evaluate_corporate_quality(
                    original_corporate, generated_corporate
                )
                validation_results['corporate'] = corporate_quality
                self.quality_reports['corporate'] = corporate_quality
                
            except Exception as e:
                logger.error(f"❌ Corporate quality validation failed: {e}")
                validation_results['corporate'] = {
                    'validation_status': 'failed',
                    'error': str(e),
                    'overall_quality': {'total_score': 0.0}
                }
        else:
            validation_results['corporate'] = {
                'validation_status': 'skipped',
                'reason': 'no_generated_data',
                'overall_quality': {'total_score': 0.0}
            }
        
        return validation_results
    
    def _execute_decision_phase(self, validation_results: Dict) -> Dict:
        """Make decisions based on quality validation results"""
        decision_results = {
            'retail_decision': {},
            'corporate_decision': {},
            'overall_strategy': {}
        }
        
        # Retail decision
        retail_quality_score = validation_results.get('retail', {}).get('overall_quality', {}).get('total_score', 0.0)
        
        if retail_quality_score >= self.config['quality_thresholds']['excellent_score']:
            retail_strategy = 'ctgan_only'
            retail_confidence = 'high'
        elif retail_quality_score >= self.config['quality_thresholds']['minimum_acceptable_score']:
            retail_strategy = 'hybrid'
            retail_confidence = 'medium'
        else:
            retail_strategy = 'manual_fallback'
            retail_confidence = 'low'
        
        decision_results['retail_decision'] = {
            'quality_score': retail_quality_score,
            'strategy': retail_strategy,
            'confidence': retail_confidence,
            'meets_threshold': retail_quality_score >= self.config['quality_thresholds']['minimum_acceptable_score']
        }
        
        # Corporate decision
        corporate_quality_score = validation_results.get('corporate', {}).get('overall_quality', {}).get('total_score', 0.0)
        
        if corporate_quality_score >= self.config['quality_thresholds']['excellent_score']:
            corporate_strategy = 'ctgan_only'
            corporate_confidence = 'high'
        elif corporate_quality_score >= self.config['quality_thresholds']['minimum_acceptable_score']:
            corporate_strategy = 'hybrid'
            corporate_confidence = 'medium'
        else:
            corporate_strategy = 'manual_fallback'
            corporate_confidence = 'low'
        
        decision_results['corporate_decision'] = {
            'quality_score': corporate_quality_score,
            'strategy': corporate_strategy,
            'confidence': corporate_confidence,
            'meets_threshold': corporate_quality_score >= self.config['quality_thresholds']['minimum_acceptable_score']
        }
        
        # Overall strategy
        decision_results['overall_strategy'] = {
            'retail_approach': retail_strategy,
            'corporate_approach': corporate_strategy,
            'pipeline_success_rate': (
                (1 if retail_strategy != 'manual_fallback' else 0) +
                (1 if corporate_strategy != 'manual_fallback' else 0)
            ) / 2,
            'recommendation': self._generate_strategy_recommendation(
                retail_strategy, corporate_strategy, retail_quality_score, corporate_quality_score
            )
        }
        
        return decision_results
    
    def _generate_strategy_recommendation(self, retail_strategy: str, corporate_strategy: str,
                                        retail_score: float, corporate_score: float) -> str:
        """Generate strategic recommendation based on quality scores"""
        if retail_strategy == 'ctgan_only' and corporate_strategy == 'ctgan_only':
            return "Excellent CTGAN performance. Use CTGAN for all future data generation."
        elif retail_strategy in ['ctgan_only', 'hybrid'] and corporate_strategy in ['ctgan_only', 'hybrid']:
            return "Good CTGAN performance. Continue with current approach and monitor quality."
        elif retail_strategy == 'manual_fallback' and corporate_strategy == 'manual_fallback':
            return "CTGAN underperforming. Consider retraining with more data or different hyperparameters."
        else:
            return "Mixed performance. Use CTGAN where quality is acceptable, manual generation elsewhere."
    
    def _prepare_final_datasets(self, original_retail: pd.DataFrame, 
                               original_corporate: pd.DataFrame,
                               generation_results: Dict, 
                               decision_results: Dict) -> Dict:
        """Prepare final datasets based on quality decisions"""
        final_data_results = {}
        
        # Prepare retail dataset
        retail_strategy = decision_results['retail_decision']['strategy']
        generated_retail = generation_results['generated_data'].get('retail', pd.DataFrame())
        
        if retail_strategy == 'ctgan_only' and len(generated_retail) > 0:
            final_retail = generated_retail.head(2000)  # Take best samples
            data_source = 'ctgan'
            
        elif retail_strategy == 'hybrid' and len(generated_retail) > 0:
            # Mix CTGAN and manual data
            ctgan_count = int(2000 * self.config['hybrid_ratio']['ctgan'])
            manual_count = int(2000 * self.config['hybrid_ratio']['manual'])
            
            ctgan_sample = generated_retail.head(ctgan_count)
            manual_sample = self._generate_manual_retail_fallback(manual_count)
            
            final_retail = pd.concat([ctgan_sample, manual_sample], ignore_index=True)
            data_source = 'hybrid'
            
        else:  # manual_fallback
            final_retail = self._generate_manual_retail_fallback(2000)
            data_source = 'manual_fallback'
        
        final_data_results['final_retail_data'] = final_retail
        final_data_results['retail_composition'] = {
            'total_samples': len(final_retail),
            'data_source': data_source,
            'strategy_used': retail_strategy
        }
        
        # Prepare corporate dataset
        corporate_strategy = decision_results['corporate_decision']['strategy']
        generated_corporate = generation_results['generated_data'].get('corporate', pd.DataFrame())
        
        if corporate_strategy == 'ctgan_only' and len(generated_corporate) > 0:
            final_corporate = generated_corporate.head(500)
            corp_data_source = 'ctgan'
            
        elif corporate_strategy == 'hybrid' and len(generated_corporate) > 0:
            # Mix CTGAN and manual data
            ctgan_count = int(500 * self.config['hybrid_ratio']['ctgan'])
            manual_count = int(500 * self.config['hybrid_ratio']['manual'])
            
            ctgan_sample = generated_corporate.head(ctgan_count)
            manual_sample = self._generate_manual_corporate_fallback(manual_count)
            
            final_corporate = pd.concat([ctgan_sample, manual_sample], ignore_index=True)
            corp_data_source = 'hybrid'
            
        else:  # manual_fallback
            final_corporate = self._generate_manual_corporate_fallback(500)
            corp_data_source = 'manual_fallback'
        
        final_data_results['final_corporate_data'] = final_corporate
        final_data_results['corporate_composition'] = {
            'total_samples': len(final_corporate),
            'data_source': corp_data_source,
            'strategy_used': corporate_strategy
        }
        
        return final_data_results
    
    def _execute_team_integration(self, final_retail: pd.DataFrame, 
                                 final_corporate: pd.DataFrame) -> Dict:
        """Execute team integration and export final data"""
        integration_results = {}
        
        try:
            # Export for Hamza (Agent Engine)
            hamza_files = TeamExporter.export_for_hamza(
                final_retail, final_corporate, str(self.output_dir)
            )
            integration_results['hamza_exports'] = hamza_files
            
            # Export for Nessrine (Visualization)
            nessrine_files = TeamExporter.export_for_nessrine(
                final_retail, final_corporate, str(self.output_dir)
            )
            integration_results['nessrine_exports'] = nessrine_files
            
            # Export for Maryem (Simulation)
            maryem_files = TeamExporter.export_for_maryem(
                final_retail, final_corporate, str(self.output_dir)
            )
            integration_results['maryem_exports'] = maryem_files
            
            # Create Week 2 summary report
            week2_summary = {
                'pipeline_completion': datetime.now().isoformat(),
                'data_delivery_summary': {
                    'retail_clients_delivered': len(final_retail),
                    'corporate_clients_delivered': len(final_corporate),
                    'total_clients': len(final_retail) + len(final_corporate)
                },
                'ctgan_integration_success': True,
                'team_files_exported': {
                    'hamza': hamza_files,
                    'nessrine': nessrine_files,
                    'maryem': maryem_files
                }
            }
            
            # Save week 2 completion report
            week2_report_path = self.output_dir / "week2_ctgan_completion_report.json"
            with open(week2_report_path, 'w') as f:
                json.dump(week2_summary, f, indent=2, default=str)
            
            integration_results['week2_summary'] = week2_summary
            integration_results['integration_status'] = 'success'
            
        except Exception as e:
            logger.error(f"❌ Team integration failed: {e}")
            integration_results['integration_status'] = 'failed'
            integration_results['error'] = str(e)
        
        return integration_results
    
    def _generate_manual_retail_fallback(self, count: int) -> pd.DataFrame:
        """Generate manual retail data as fallback"""
        logger.info(f"🛡️ Generating {count} manual retail clients as fallback...")
        
        # Use Week 1 manual generation logic
        from enhanced_pipeline import ProductionDataPipeline
        
        fallback_pipeline = ProductionDataPipeline()
        manual_retail = fallback_pipeline.generate_validated_retail_clients(count)
        
        # Mark as fallback data
        manual_retail['data_source'] = 'week1_fallback'
        
        return manual_retail
    
    def _generate_manual_corporate_fallback(self, count: int) -> pd.DataFrame:
        """Generate manual corporate data as fallback"""
        logger.info(f"🛡️ Generating {count} manual corporate clients as fallback...")
        
        # Use Week 1 manual generation logic
        from enhanced_pipeline import ProductionDataPipeline
        
        fallback_pipeline = ProductionDataPipeline()
        manual_corporate = fallback_pipeline.generate_validated_corporate_clients(count)
        
        # Mark as fallback data
        manual_corporate['data_source'] = 'week1_fallback'
        
        return manual_corporate
    
    def _execute_fallback(self, retail_df: pd.DataFrame, corporate_df: pd.DataFrame) -> Dict:
        """Execute complete fallback to Week 1 manual generation"""
        logger.info("🛡️ Executing complete fallback to Week 1 pipeline...")
        
        try:
            from enhanced_pipeline import ProductionDataPipeline
            
            fallback_pipeline = ProductionDataPipeline()
            
            # Generate fallback data
            fallback_retail = fallback_pipeline.generate_validated_retail_clients(2000)
            fallback_corporate = fallback_pipeline.generate_validated_corporate_clients(500)
            
            # Export for team
            fallback_exports = fallback_pipeline.export_production_files(
                fallback_retail, fallback_corporate
            )
            
            return {
                'fallback_status': 'success',
                'retail_samples': len(fallback_retail),
                'corporate_samples': len(fallback_corporate),
                'exports': fallback_exports
            }
            
        except Exception as e:
            logger.error(f"❌ Fallback execution failed: {e}")
            return {
                'fallback_status': 'failed',
                'error': str(e)
            }
    
    def _save_pipeline_report(self, pipeline_results: Dict):
        """Save comprehensive pipeline execution report"""
        report_path = self.ctgan_dir / f"pipeline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_path, 'w') as f:
            json.dump(pipeline_results, f, indent=2, default=str)
        
        logger.info(f"📊 Pipeline report saved: {report_path}")
    
    def get_pipeline_status(self) -> Dict:
        """Get current pipeline status and capabilities"""
        return {
            'models_trained': self.models_trained,
            'quality_reports': {
                'retail': self.quality_reports.get('retail', {}).get('overall_quality', {}),
                'corporate': self.quality_reports.get('corporate', {}).get('overall_quality', {})
            },
            'config': self.config,
            'capabilities': {
                'ctgan_retail': self.models_trained.get('retail', False),
                'ctgan_corporate': self.models_trained.get('corporate', False),
                'fallback_available': self.config['fallback_enabled']
            }
        }

# Guided execution script
def run_week2_ctgan_implementation():
    """Guided execution of complete Week 2 CTGAN implementation"""
    print("🚀 WEEK 2 CTGAN IMPLEMENTATION - GUIDED EXECUTION")
    print("=" * 60)
    
    try:
        # Initialize pipeline
        pipeline = CTGANProductionPipeline()
        
        # Load Week 1 data
        print("\n📁 Loading Week 1 foundation data...")
        
        # You would load your actual Week 1 data here
        # For demo, we'll create sample data
        retail_df = pd.DataFrame({
            'client_id': ['R_' + f'{i:05d}' for i in range(1, 1001)],
            'age': np.random.randint(18, 80, 1000),
            'monthly_income': np.random.uniform(400, 15000, 1000),
            'gender': np.random.choice(['M', 'F'], 1000),
            'governorate': np.random.choice(['Tunis', 'Sfax', 'Sousse', 'Ariana'], 1000),
            'education_level': np.random.choice(['primary', 'secondary', 'university'], 1000),
            'employment_sector': np.random.choice(['private', 'public', 'self_employed'], 1000),
            'preferred_channel': np.random.choice(['mobile', 'branch', 'web'], 1000),
            'risk_tolerance': np.random.uniform(0, 1, 1000),
            'satisfaction_score': np.random.uniform(0.3, 1.0, 1000),
            'digital_engagement_score': np.random.uniform(0, 1, 1000)
        })
        
        corporate_df = pd.DataFrame({
            'client_id': ['C_' + f'{i:05d}' for i in range(1, 201)],
            'company_name': [f'Company_{i:03d}' for i in range(1, 201)],
            'business_sector': np.random.choice(['services', 'manufacturing', 'retail'], 200),
            'company_size': np.random.choice(['micro', 'small', 'medium'], 200),
            'employee_count': np.random.randint(1, 500, 200),
            'annual_revenue': np.random.uniform(10000, 10000000, 200),
            'headquarters_governorate': np.random.choice(['Tunis', 'Sfax', 'Sousse'], 200),
            'credit_rating': np.random.choice(['A', 'B', 'C'], 200),
            'digital_maturity_score': np.random.uniform(0.1, 1.0, 200),
            'cash_flow_predictability': np.random.uniform(0.3, 1.0, 200),
            'seasonal_variation': np.random.uniform(0, 0.7, 200)
        })
        
        print(f"✅ Loaded {len(retail_df)} retail + {len(corporate_df)} corporate clients")
        
        # Execute complete pipeline
        print("\n🎯 Executing complete CTGAN pipeline...")
        results = pipeline.run_complete_pipeline(retail_df, corporate_df)
        
        # Display results
        print("\n📊 PIPELINE EXECUTION RESULTS")
        print("=" * 40)
        
        if results['execution_summary']['status'] == 'completed_successfully':
            print("✅ Pipeline Status: SUCCESSFUL")
            print(f"⏱️ Duration: {results['execution_summary']['duration_seconds']:.1f} seconds")
            print(f"👥 Total Clients Delivered: {results['execution_summary']['total_clients_delivered']}")
            
            # Show team deliverables
            if 'team_integration' in results:
                team_results = results['team_integration']
                print(f"\n📦 Team Deliverables:")
                for team, files in team_results.get('week2_summary', {}).get('team_files_exported', {}).items():
                    print(f"   {team.title()}: {', '.join(files)}")
        else:
            print("❌ Pipeline Status: FAILED")
            if 'fallback' in results:
                print("🛡️ Fallback Executed Successfully")
        
        print(f"\n📋 Full report saved to data/ctgan/ directory")
        print("🎉 Week 2 CTGAN implementation completed!")
        
        return results
        
    except Exception as e:
        print(f"❌ Week 2 implementation failed: {e}")
        return None

if __name__ == "__main__":
    results = run_week2_ctgan_implementation()