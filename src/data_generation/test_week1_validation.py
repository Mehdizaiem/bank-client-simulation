#!/usr/bin/env python3
"""
MEHDI WEEK 1 VALIDATION TEST SUITE
Comprehensive tests to verify all Week 1 deliverables
"""

import sys
import os
from pathlib import Path
import pandas as pd
import json

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

try:
    from schemas import DataValidator, TeamExporter
    from data_sources import TunisianDataSources
    from enhanced_pipeline import ProductionDataPipeline
except ImportError as e:
    print(f"Import error: {e}")
    print("Some tests will be skipped")

class Week1ValidationSuite:
    """Comprehensive validation for Week 1 deliverables"""
    
    def __init__(self):
        self.test_results = []
        self.output_dir = Path("../../data/processed")
    
    def run_test(self, test_name, test_func):
        """Run individual test with error handling"""
        try:
            test_func()
            self.test_results.append((test_name, True, "PASSED"))
            print(f"✅ {test_name}: PASSED")
        except Exception as e:
            self.test_results.append((test_name, False, str(e)))
            print(f"❌ {test_name}: FAILED - {e}")
    
    def test_file_existence(self):
        """Test 1: Check all required files exist"""
        required_files = [
            "src/data_generation/schemas.py",
            "src/data_generation/data_sources.py", 
            "src/data_generation/enhanced_pipeline.py"
        ]
        
        for file_path in required_files:
            if not Path(file_path).exists():
                raise FileNotFoundError(f"Missing required file: {file_path}")
    
    def test_schema_imports(self):
        """Test 2: Verify schema classes can be imported"""
        from schemas import RetailClientSchema, CorporateClientSchema, DataValidator
        
        # Test basic instantiation doesn't crash
        assert RetailClientSchema
        assert CorporateClientSchema  
        assert DataValidator
    
    def test_data_sources_research(self):
        """Test 3: Verify data sources research is complete"""
        sources = TunisianDataSources()
        
        # Check required sources exist
        source_names = [s['name'] for s in sources.sources]
        required_sources = ['Institut National de la Statistique', 'Central Bank']
        
        for required in required_sources:
            if not any(required in name for name in source_names):
                raise ValueError(f"Missing data source: {required}")
        
        # Check parameters exist
        demo_params = sources.get_demographic_parameters()
        corp_params = sources.get_corporate_parameters()
        
        assert 'population_by_governorate' in demo_params
        assert 'size_distribution' in corp_params
    
    def test_sample_data_generation(self):
        """Test 4: Verify sample data can be generated"""
        pipeline = ProductionDataPipeline()
        
        # Generate small samples
        retail_df = pipeline.generate_validated_retail_clients(10)
        corporate_df = pipeline.generate_validated_corporate_clients(5)
        
        # Basic checks
        assert len(retail_df) == 10
        assert len(corporate_df) == 5
        assert 'client_id' in retail_df.columns
        assert 'client_id' in corporate_df.columns
    
    def test_team_export_files(self):
        """Test 5: Check team export files exist and are valid"""
        required_exports = [
            "hamza_retail_agents.csv",
            "hamza_corporate_agents.csv",
            "nessrine_dashboard_data.json",
            "maryem_client_segments.json"
        ]
        
        for export_file in required_exports:
            file_path = self.output_dir / export_file
            if not file_path.exists():
                raise FileNotFoundError(f"Missing export file: {export_file}")
            
            # Validate file contents
            if export_file.endswith('.csv'):
                df = pd.read_csv(file_path)
                if len(df) == 0:
                    raise ValueError(f"Empty CSV file: {export_file}")
            elif export_file.endswith('.json'):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                if not data:
                    raise ValueError(f"Empty JSON file: {export_file}")
    
    def test_data_validation_functions(self):
        """Test 6: Verify validation functions work"""
        # Create test data
        test_retail = pd.DataFrame({
            'client_id': ['R_001', 'R_002'],
            'age': [25, 45],
            'monthly_income': [1200, 2500],
            'governorate': ['Tunis', 'Sfax']
        })
        
        test_corporate = pd.DataFrame({
            'client_id': ['C_001'],
            'company_size': ['micro'],
            'business_sector': ['services'],
            'annual_revenue': [50000]
        })
        
        # Test validation
        retail_validation = DataValidator.validate_retail_data(test_retail)
        corporate_validation = DataValidator.validate_corporate_data(test_corporate)
        
        assert 'quality_score' in retail_validation
        assert 'quality_score' in corporate_validation
        assert 0 <= retail_validation['quality_score'] <= 1
        assert 0 <= corporate_validation['quality_score'] <= 1
    
    def run_all_tests(self):
        """Run all validation tests"""
        print("🧪 RUNNING WEEK 1 VALIDATION TESTS")
        print("="*50)
        
        tests = [
            ("File Existence Check", self.test_file_existence),
            ("Schema Imports", self.test_schema_imports),
            ("Data Sources Research", self.test_data_sources_research),
            ("Sample Data Generation", self.test_sample_data_generation),
            ("Team Export Files", self.test_team_export_files),
            ("Data Validation Functions", self.test_data_validation_functions)
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        # Summary
        passed = sum(1 for _, success, _ in self.test_results if success)
        total = len(self.test_results)
        
        print(f"\n📊 VALIDATION SUMMARY: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL WEEK 1 DELIVERABLES VALIDATED!")
            print("🚀 Ready for Week 2 CTGAN implementation")
            return True
        else:
            print("⚠️ Some validations failed - review before proceeding")
            return False

if __name__ == "__main__":
    validator = Week1ValidationSuite()
    success = validator.run_all_tests()
    sys.exit(0 if success else 1)
