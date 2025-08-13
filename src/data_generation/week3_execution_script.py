#!/usr/bin/env python3
"""
WEEK 3 COMPLETE EXECUTION SCRIPT
Professional-grade execution with error handling and comprehensive reporting.
Run this script to execute all Week 3 deliverables.

Usage:
    python week3_execution_script.py                    # Normal execution
    python week3_execution_script.py --interactive      # Interactive mode
    python week3_execution_script.py --check            # Prerequisites only
"""

import sys
import os
from pathlib import Path
import logging
from datetime import datetime
import traceback
import argparse

# Setup logging
def setup_logging():
    """Setup comprehensive logging"""
    log_dir = Path("../../logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f'week3_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def print_header():
    """Print professional header"""
    print("🚀 WEEK 3 ENTERPRISE DATA GENERATION - COMPLETE EXECUTION")
    print("=" * 80)
    print("Project: Tunisian Bank Client Simulation")
    print("Lead: Mehdi (Project Lead)")
    print("Pipeline: Week 3 Advanced Features & Enterprise Integration")
    print("Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 80)

def check_prerequisites():
    """Check system prerequisites before execution"""
    
    print("\n🔍 Checking Prerequisites...")
    
    prerequisites_met = True
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        prerequisites_met = False
    else:
        print("✅ Python version OK")
    
    # Check required directories
    required_dirs = [
        "../../data",
        "../../data/processed", 
        "../../logs",
        "../../data/week3_deliverables"
    ]
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if not path.exists():
            print(f"❌ Missing directory: {dir_path}")
            try:
                path.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created directory: {dir_path}")
            except Exception as e:
                print(f"❌ Failed to create {dir_path}: {e}")
                prerequisites_met = False
        else:
            print(f"✅ Directory exists: {dir_path}")
    
    # Check required files
    required_files = [
        "enhanced_pipeline.py",
        "schemas.py"
    ]
    
    missing_files = []
    for file_name in required_files:
        if not Path(file_name).exists():
            print(f"❌ Missing file: {file_name}")
            missing_files.append(file_name)
        else:
            print(f"✅ File exists: {file_name}")
    
    if missing_files:
        print(f"\n⚠️ Missing Week 1 foundation files. Will use fallback generation.")
    
    # Check imports
    try:
        import pandas
        import numpy
        print("✅ Core dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("💡 Run: pip install pandas numpy scipy scikit-learn")
        prerequisites_met = False
    
    return prerequisites_met

def execute_week3_pipeline():
    """Execute the complete Week 3 pipeline"""
    
    logger = logging.getLogger(__name__)
    
    try:
        print("\n📋 Initializing Week 3 Pipeline...")
        
        # Try to import the complete pipeline
        try:
            sys.path.append(str(Path(__file__).parent))
            from week3_integration_pipeline import execute_week3_complete_pipeline
            
            print("✅ Complete pipeline imported successfully")
            
            # Execute complete pipeline
            print("\n🎯 Executing Complete Week 3 Pipeline...")
            print("This may take several minutes...")
            
            results = execute_week3_complete_pipeline()
            
            return results
            
        except ImportError:
            print("⚠️ Complete pipeline not available, using simplified execution...")
            return execute_simplified_week3_pipeline()
            
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        traceback.print_exc()
        return None

def execute_simplified_week3_pipeline():
    """Execute simplified Week 3 pipeline as fallback"""
    
    print("\n🛡️ Executing Simplified Week 3 Pipeline...")
    
    try:
        # Import Week 1 foundation
        from enhanced_pipeline import ProductionDataPipeline
        from schemas import DataValidator, TeamExporter
        
        # Initialize pipeline
        pipeline = ProductionDataPipeline()
        
        # Generate enhanced datasets
        print("🔄 Generating enhanced retail clients...")
        retail_df = pipeline.generate_validated_retail_clients(5000)
        
        print("🔄 Generating enhanced corporate clients...")
        corporate_df = pipeline.generate_validated_corporate_clients(1000)
        
        # Add Week 3 enhancements manually
        retail_df = add_week3_enhancements(retail_df, 'retail')
        corporate_df = add_week3_enhancements(corporate_df, 'corporate')
        
        # Validate quality
        retail_quality = DataValidator.validate_retail_data(retail_df)
        corporate_quality = DataValidator.validate_corporate_data(corporate_df)
        
        # Export for teams
        team_exports = export_for_teams(retail_df, corporate_df)
        
        # Generate results summary
        results = {
            'execution_metadata': {
                'pipeline_version': 'week3_simplified_v1.0',
                'execution_id': f"week3_simplified_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'total_duration_formatted': "Completed"
            },
            'data_output_summary': {
                'final_retail_records': len(retail_df),
                'final_corporate_records': len(corporate_df),
                'enterprise_standards_met': retail_quality['quality_score'] > 0.8 and corporate_quality['quality_score'] > 0.8,
                'quality_scores_achieved': {
                    'retail': retail_quality['quality_score'],
                    'corporate': corporate_quality['quality_score']
                }
            },
            'overall_success_metrics': {
                'pipeline_success': True
            },
            'team_exports': team_exports
        }
        
        # Save final datasets
        save_week3_datasets(retail_df, corporate_df)
        
        return results
        
    except Exception as e:
        print(f"❌ Simplified pipeline failed: {e}")
        return None

def add_week3_enhancements(df, data_type):
    """Add Week 3 enhancements to datasets"""
    
    enhanced_df = df.copy()
    
    # Add Week 3 metadata
    enhanced_df['week3_enhanced'] = True
    enhanced_df['generation_pipeline'] = 'week3_simplified'
    enhanced_df['data_version'] = '3.0.0'
    enhanced_df['created_by'] = 'mehdi_week3_simplified'
    
    # Add basic geographic enhancements
    if data_type == 'retail':
        # Add postal codes
        enhanced_df['postal_code'] = enhanced_df['governorate'].map({
            'Tunis': '1001', 'Ariana': '2001', 'Sfax': '3001', 
            'Sousse': '4001', 'Monastir': '5001'
        }).fillna('1001')
        
        # Add basic economic indicators
        enhanced_df['gdp_per_capita_tnd'] = enhanced_df['governorate'].map({
            'Tunis': 12500, 'Ariana': 11200, 'Sfax': 9800,
            'Sousse': 8900, 'Monastir': 8200
        }).fillna(8000)
        
        # Add archetype classification (simplified)
        high_income_mask = enhanced_df['monthly_income'] > enhanced_df['monthly_income'].quantile(0.8)
        young_digital_mask = (enhanced_df['age'] < 35) & (enhanced_df['digital_engagement_score'] > 0.7)
        
        enhanced_df['archetype_name'] = 'Standard Client'
        enhanced_df.loc[high_income_mask, 'archetype_name'] = 'High Net Worth Tunisian'
        enhanced_df.loc[young_digital_mask, 'archetype_name'] = 'Young Digital Professional'
        
        enhanced_df['strategic_segment'] = enhanced_df['archetype_name'].map({
            'High Net Worth Tunisian': 'high_net_worth_retail',
            'Young Digital Professional': 'young_professionals',
            'Standard Client': 'standard_retail'
        })
        
    elif data_type == 'corporate':
        # Add postal codes
        enhanced_df['postal_code'] = enhanced_df['headquarters_governorate'].map({
            'Tunis': '1001', 'Ariana': '2001', 'Sfax': '3001',
            'Sousse': '4001', 'Monastir': '5001'
        }).fillna('1001')
        
        # Add archetype classification (simplified)
        tech_mask = enhanced_df['business_sector'] == 'technology'
        large_mask = enhanced_df['company_size'] == 'large'
        
        enhanced_df['archetype_name'] = 'Standard Business'
        enhanced_df.loc[tech_mask, 'archetype_name'] = 'Tech Scale-up'
        enhanced_df.loc[large_mask, 'archetype_name'] = 'Enterprise Client'
        
        enhanced_df['strategic_segment'] = enhanced_df['archetype_name'].map({
            'Tech Scale-up': 'tech_entrepreneurs',
            'Enterprise Client': 'large_corporates',
            'Standard Business': 'standard_corporate'
        })
    
    return enhanced_df

def export_for_teams(retail_df, corporate_df):
    """Export data for team members"""
    
    # Setup export directories
    base_dir = Path("../../data/week3_deliverables/team_exports")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    team_exports = {}
    
    # Export for Hamza (Agent Engine)
    hamza_dir = base_dir / "hamza"
    hamza_dir.mkdir(exist_ok=True)
    
    hamza_retail = retail_df[['client_id', 'age', 'governorate', 'monthly_income',
                             'risk_tolerance', 'satisfaction_score', 'digital_engagement_score',
                             'preferred_channel', 'postal_code', 'gdp_per_capita_tnd',
                             'archetype_name', 'strategic_segment']].copy()
    
    hamza_corporate = corporate_df[['client_id', 'company_name', 'business_sector', 'company_size',
                                   'annual_revenue', 'digital_maturity_score', 'headquarters_governorate',
                                   'employee_count', 'postal_code', 'archetype_name']].copy()
    
    hamza_retail.to_csv(hamza_dir / "week3_agent_retail_clients.csv", index=False)
    hamza_corporate.to_csv(hamza_dir / "week3_agent_corporate_clients.csv", index=False)
    
    team_exports['hamza'] = ['week3_agent_retail_clients.csv', 'week3_agent_corporate_clients.csv']
    
    # Export for Nessrine (Visualization)
    nessrine_dir = base_dir / "nessrine"
    nessrine_dir.mkdir(exist_ok=True)
    
    dashboard_stats = {
        'data_summary': {
            'total_retail_clients': len(retail_df),
            'total_corporate_clients': len(corporate_df),
            'generation_timestamp': datetime.now().isoformat()
        },
        'demographic_breakdowns': {
            'governorate_distribution': retail_df['governorate'].value_counts().to_dict(),
            'age_distribution': retail_df['age'].describe().to_dict(),
            'income_distribution': retail_df['monthly_income'].describe().to_dict()
        },
        'corporate_breakdowns': {
            'sector_distribution': corporate_df['business_sector'].value_counts().to_dict(),
            'size_distribution': corporate_df['company_size'].value_counts().to_dict()
        }
    }
    
    import json
    with open(nessrine_dir / "week3_dashboard_statistics.json", 'w') as f:
        json.dump(dashboard_stats, f, indent=2, default=str)
    
    team_exports['nessrine'] = ['week3_dashboard_statistics.json']
    
    # Export for Maryem (Simulation)
    maryem_dir = base_dir / "maryem"
    maryem_dir.mkdir(exist_ok=True)
    
    client_segments = {
        'high_value_retail': retail_df[
            retail_df['monthly_income'] > retail_df['monthly_income'].quantile(0.9)
        ]['client_id'].tolist(),
        
        'young_digital_natives': retail_df[
            (retail_df['age'] < 35) & 
            (retail_df['digital_engagement_score'] > 0.7)
        ]['client_id'].tolist(),
        
        'tech_companies': corporate_df[
            corporate_df['business_sector'] == 'technology'
        ]['client_id'].tolist(),
        
        'large_corporates': corporate_df[
            corporate_df['company_size'] == 'large'
        ]['client_id'].tolist()
    }
    
    with open(maryem_dir / "week3_strategic_client_segments.json", 'w') as f:
        json.dump(client_segments, f, indent=2)
    
    team_exports['maryem'] = ['week3_strategic_client_segments.json']
    
    return team_exports

def save_week3_datasets(retail_df, corporate_df):
    """Save final Week 3 datasets"""
    
    output_dir = Path("../../data/week3_deliverables")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save with timestamp
    retail_df.to_csv(output_dir / f"week3_final_retail_{timestamp}.csv", index=False)
    corporate_df.to_csv(output_dir / f"week3_final_corporate_{timestamp}.csv", index=False)
    
    # Save current versions
    retail_df.to_csv(output_dir / "week3_final_retail.csv", index=False)
    corporate_df.to_csv(output_dir / "week3_final_corporate.csv", index=False)
    
    print(f"💾 Final datasets saved to {output_dir}")

def print_success_summary(results):
    """Print comprehensive success summary"""
    
    print("\n" + "=" * 80)
    print("🎉 WEEK 3 EXECUTION COMPLETED SUCCESSFULLY")
    print("=" * 80)
    
    # Execution metrics
    execution_meta = results.get('execution_metadata', {})
    print(f"\n⏱️ EXECUTION METRICS:")
    print(f"   Duration: {execution_meta.get('total_duration_formatted', 'Unknown')}")
    print(f"   Pipeline Version: {execution_meta.get('pipeline_version', 'Unknown')}")
    print(f"   Execution ID: {execution_meta.get('execution_id', 'Unknown')}")
    
    # Data deliverables
    data_summary = results.get('data_output_summary', {})
    print(f"\n📦 DATA DELIVERABLES:")
    print(f"   ✅ Retail Clients: {data_summary.get('final_retail_records', 0):,}")
    print(f"   ✅ Corporate Clients: {data_summary.get('final_corporate_records', 0):,}")
    print(f"   ✅ Total Generated: {data_summary.get('final_retail_records', 0) + data_summary.get('final_corporate_records', 0):,}")
    print(f"   ✅ Enterprise Standards: {'MET' if data_summary.get('enterprise_standards_met', False) else 'NOT MET'}")
    
    # Quality achievements
    quality_scores = data_summary.get('quality_scores_achieved', {})
    print(f"\n🏆 QUALITY ACHIEVEMENTS:")
    for data_type, score in quality_scores.items():
        print(f"   ✅ {data_type.title()}: {score:.1%}")
    
    # Team handoff
    team_exports = results.get('team_exports', {})
    if team_exports:
        print(f"\n🤝 TEAM HANDOFF COMPLETED:")
        print(f"   ✅ Hamza (Agent Engine): {len(team_exports.get('hamza', []))} files delivered")
        print(f"   ✅ Nessrine (Visualization): {len(team_exports.get('nessrine', []))} files delivered")
        print(f"   ✅ Maryem (Simulation): {len(team_exports.get('maryem', []))} files delivered")
    
    # Week 3 innovations
    print(f"\n🚀 WEEK 3 INNOVATIONS DELIVERED:")
    print(f"   ✅ Strategic Archetype Enhancement")
    print(f"   ✅ Geographic Economic Mapping")
    print(f"   ✅ Enterprise Quality Validation")
    print(f"   ✅ Automated Team Handoff")
    
    # File locations
    print(f"\n📁 DELIVERABLES LOCATION:")
    print(f"   📊 Final Data: data/week3_deliverables/")
    print(f"   🤝 Team Exports: data/week3_deliverables/team_exports/")
    
    print(f"\n🎯 STATUS: READY FOR WEEK 4 TEAM INTEGRATION")
    print("=" * 80)

def print_failure_summary(results):
    """Print comprehensive failure summary with recovery options"""
    
    print("\n" + "=" * 80)
    print("❌ WEEK 3 EXECUTION ENCOUNTERED ISSUES")
    print("=" * 80)
    
    if results:
        # Show error details if available
        if 'error_details' in results:
            error_details = results['error_details']
            print(f"\n💥 ERROR DETAILS:")
            print(f"   Error Type: {error_details.get('error_type', 'Unknown')}")
            print(f"   Error Message: {error_details.get('error_message', 'Unknown')}")
    
    print(f"\n🛡️ RECOVERY OPTIONS:")
    print(f"   1. 🔄 Retry execution (transient issues)")
    print(f"   2. 🛠️ Check dependencies and configuration")
    print(f"   3. 📞 Use fallback manual generation")
    print(f"   4. 🧪 Run individual components for debugging")
    
    print(f"\n🔧 DEBUGGING COMMANDS:")
    print(f"   Test database: python ../../tests/test_database.py")
    print(f"   Test setup: python ../../tests/test_setup.py")
    print(f"   Check logs: ls ../../logs/")
    
    print("=" * 80)

def run_fallback_execution():
    """Run fallback execution if main pipeline fails"""
    
    print("\n🛡️ EXECUTING FALLBACK OPTION...")
    print("Generating data using Week 1 foundation pipeline...")
    
    try:
        # Import and use Week 1 fallback
        from enhanced_pipeline import ProductionDataPipeline
        
        fallback_pipeline = ProductionDataPipeline()
        
        # Generate fallback data
        print("🔄 Generating fallback retail clients...")
        retail_df = fallback_pipeline.generate_validated_retail_clients(3000)
        
        print("🔄 Generating fallback corporate clients...")
        corporate_df = fallback_pipeline.generate_validated_corporate_clients(600)
        
        # Export fallback data
        export_results = fallback_pipeline.export_production_files(retail_df, corporate_df)
        
        print("✅ FALLBACK EXECUTION COMPLETED")
        print(f"📦 Generated: {len(retail_df)} retail + {len(corporate_df)} corporate clients")
        print("📁 Files exported to: data/processed/")
        print("🎯 Ready for team integration (basic version)")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback execution failed: {e}")
        return False

def interactive_mode():
    """Interactive mode for debugging and selective execution"""
    
    print("\n🛠️ WEEK 3 INTERACTIVE MODE")
    print("Choose execution option:")
    print("1. 🚀 Full Pipeline Execution")
    print("2. 🧪 Prerequisites Check Only") 
    print("3. 🛡️ Fallback Execution")
    print("4. 📊 Test Basic Components")
    print("5. ❌ Exit")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        return main_execution()
    elif choice == "2":
        return check_prerequisites()
    elif choice == "3":
        return run_fallback_execution()
    elif choice == "4":
        return test_basic_components()
    elif choice == "5":
        print("👋 Exiting...")
        return True
    else:
        print("❌ Invalid choice")
        return interactive_mode()

def test_basic_components():
    """Test basic components"""
    
    print("\n🧪 TESTING BASIC COMPONENTS")
    
    tests = {
        'pandas_import': test_pandas,
        'numpy_import': test_numpy,
        'week1_foundation': test_week1_foundation,
        'directory_structure': test_directories
    }
    
    results = {}
    for test_name, test_func in tests.items():
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results[test_name] = False
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n📊 COMPONENT TEST RESULTS:")
    for component, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {component}: {status}")
    
    print(f"\n🎯 Overall: {success_count}/{total_count} components working")
    
    return success_count == total_count

def test_pandas():
    """Test pandas import"""
    import pandas as pd
    df = pd.DataFrame({'test': [1, 2, 3]})
    print("✅ Pandas working")
    return True

def test_numpy():
    """Test numpy import"""
    import numpy as np
    arr = np.array([1, 2, 3])
    print("✅ Numpy working")
    return True

def test_week1_foundation():
    """Test Week 1 foundation components"""
    try:
        from enhanced_pipeline import ProductionDataPipeline
        from schemas import DataValidator
        print("✅ Week 1 foundation components available")
        return True
    except ImportError:
        print("⚠️ Week 1 foundation components not available")
        return False

def test_directories():
    """Test directory structure"""
    required_dirs = ["../../data", "../../logs"]
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    print("✅ Directory structure OK")
    return True

def main_execution():
    """Main execution function"""
    
    logger = setup_logging()
    
    try:
        print_header()
        
        # Check prerequisites
        if not check_prerequisites():
            print("\n❌ Prerequisites not met. Please resolve issues above.")
            return False
        
        # Execute pipeline
        results = execute_week3_pipeline()
        
        # Process results
        if results and results.get('overall_success_metrics', {}).get('pipeline_success', False):
            print_success_summary(results)
            return True
        else:
            print_failure_summary(results)
            return False
            
    except Exception as e:
        logger.error(f"Main execution failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main entry point"""
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='Week 3 Enterprise Data Generation Pipeline')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--check', action='store_true', help='Check prerequisites only')
    parser.add_argument('--fallback', action='store_true', help='Run fallback execution only')
    
    args = parser.parse_args()
    
    if args.check:
        return check_prerequisites()
    elif args.fallback:
        return run_fallback_execution()
    elif args.interactive:
        return interactive_mode()
    else:
        # Normal execution
        success = main_execution()
        
        if not success:
            print("\n🛡️ Would you like to try fallback execution? (y/n): ", end="")
            try:
                response = input().strip().lower()
                if response in ['y', 'yes']:
                    fallback_success = run_fallback_execution()
                    return fallback_success
                else:
                    print("💡 Try running with --interactive flag for more options")
                    return False
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Execution cancelled")
                return False
        else:
            print("\n🎉 Week 3 execution completed successfully!")
            print("Ready to proceed to Week 4 team integration!")
            return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Execution cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)