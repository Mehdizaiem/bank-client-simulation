"""
Comprehensive test suite for integrated bank simulation
Tests Mesa 3.x compatibility, CSV loading, scenarios, and reporting
"""
import sys
import os
import traceback
from pathlib import Path
import logging
import time
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Add src directory to path
src_path = project_root / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

print("🚀 COMPREHENSIVE INTEGRATED BANK SIMULATION TEST SUITE")
print(f"Current directory: {os.getcwd()}")
print(f"Source directory: {src_path}")
print("=" * 80)

# =============================================================================
# MESA 3.X VERIFICATION
# =============================================================================
try:
    import mesa
    print(f"✅ Mesa version {mesa.__version__} and all modules imported successfully")
except ImportError as e:
    print(f"❌ Mesa import failed: {e}")
    sys.exit(1)

# Import our modules
from src.agent_engine.data_loader import AgentDataLoader
from src.agent_engine.mesa_setup import BankSimulationModel
from src.agent_engine.mesa_setup_integrated import IntegratedBankSimulationModel
from src.simulation.scenarios import ScenarioManager

# =============================================================================
# TEST SUITE
# =============================================================================
print("\n🎯 STARTING COMPREHENSIVE TEST SUITE")
print("=" * 80)
print(f"Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")

test_results = {}

# =============================================================================
# TEST 1: MESA 3.X BASIC FUNCTIONALITY
# =============================================================================
def test_mesa_basic():
    """Test basic Mesa 3.x functionality"""
    print("\n" + "="*60)
    print("TEST 1: MESA 3.X BASIC FUNCTIONALITY")
    print("="*60)
    
    try:
        # Test Mesa imports
        from mesa import Model, Agent
        from mesa.datacollection import DataCollector
        print("✅ Mesa 3.x imports working")
        
        # Test basic model creation
        class TestModel(Model):
            def __init__(self):
                super().__init__()
        
        model = TestModel()
        print("✅ Mesa 3.x Model creation working")
        print(f"   - Agents container: {type(model.agents)}")
        print(f"   - Initial agent count: {len(model.agents)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Mesa 3.x test failed: {e}")
        traceback.print_exc()
        return False

# =============================================================================
# TEST 2: CSV DATA LOADING
# =============================================================================
def test_csv_data_loading():
    """Test CSV data loading and agent data preparation"""
    print("\n" + "="*60)
    print("TEST 2: CSV DATA LOADING")
    print("="*60)
    
    try:
        loader = AgentDataLoader()
        
        # Test retail data loading
        retail_agents = loader.load_retail_agents()
        print(f"✅ Loaded {len(retail_agents)} retail agents")
        if retail_agents:
            sample = retail_agents[0]
            print(f"   Sample retail: ID={sample.get('client_id', 'N/A')}, "
                  f"age={sample.get('age', 'N/A')}, "
                  f"governorate={sample.get('governorate', 'N/A')}")
        
        # Test corporate data loading
        corporate_agents = loader.load_corporate_agents()
        print(f"✅ Loaded {len(corporate_agents)} corporate agents")
        if corporate_agents:
            sample = corporate_agents[0]
            print(f"   Sample corporate: ID={sample.get('client_id', 'N/A')}, "
                  f"company={sample.get('company_name', 'N/A')}, "
                  f"sector={sample.get('business_sector', 'N/A')}")
        
        # Test the select_agents method
        selected = loader.select_agents(retail_agents[:100], 50)
        assert len(selected) == 50, f"Expected 50 agents, got {len(selected)}"
        print(f"✅ Agent selection working: selected {len(selected)} from 100")
        
        # Test statistics
        stats = loader.get_statistics()
        print(f"✅ Data statistics computed successfully")
        print(f"   Retail stats: {len(stats.get('retail', {}))} fields")
        print(f"   Corporate stats: {len(stats.get('corporate', {}))} fields")
        
        return True, loader
        
    except Exception as e:
        print(f"❌ CSV data loading failed: {e}")
        traceback.print_exc()
        return False, None

# =============================================================================
# TEST 3: BASIC SIMULATION MODEL
# =============================================================================
def test_basic_simulation_model():
    """Test basic BankSimulationModel without scenarios"""
    print("\n" + "="*60)
    print("TEST 3: BASIC SIMULATION MODEL")
    print("="*60)
    
    try:
        config = {
            'num_agents': 100,
            'retail_ratio': 0.8,
            'time_steps': 10,
            'random_seed': 42
        }
        
        print("Creating basic BankSimulationModel...")
        model = BankSimulationModel(config)
        
        # Test model properties
        print(f"✅ Model created successfully")
        print(f"   - Total agents: {len(model.agents)}")
        print(f"   - Retail agents: {len([a for a in model.agents if a.client_type == 'retail'])}")
        print(f"   - Corporate agents: {len([a for a in model.agents if a.client_type == 'corporate'])}")
        print(f"   - Time steps: {model.time_steps}")
        
        # Run a few steps
        print("\nRunning basic simulation steps...")
        initial_satisfaction = model.get_average_satisfaction()
        
        for i in range(5):
            model.step()
            current_satisfaction = model.get_average_satisfaction()
            print(f"   Step {i+1}: satisfaction {initial_satisfaction:.3f} → {current_satisfaction:.3f}")
        
        # Test data export
        df = model.export_agent_data()
        print(f"✅ Data export successful: {len(df)} agent records")
        
        return True, model
        
    except Exception as e:
        print(f"❌ Basic simulation test failed: {e}")
        traceback.print_exc()
        return False, None

# =============================================================================
# TEST 4: SCENARIO LOADING
# =============================================================================
def test_scenario_loading():
    """Test scenario loading functionality"""
    print("\n" + "="*60)
    print("TEST 4: SCENARIO LOADING")
    print("="*60)
    
    try:
        manager = ScenarioManager()
        scenarios_loaded = 0
        
        scenario_files = [
            "branch_closure_scenario.json",
            "marketing_campaign_scenario.json", 
            "digital_transformation_scenario.json"
        ]
        
        for scenario_file in scenario_files:
            scenario = manager.load_scenario(scenario_file)
            if scenario:
                print(f"✅ Loaded scenario: {scenario.metadata.name}")
                print(f"   - Duration: {scenario.simulation_parameters.duration_steps} steps")
                print(f"   - Events: {len(scenario.events)}")
                print(f"   - Population: {scenario.simulation_parameters.agent_population}")
                scenarios_loaded += 1
        
        print(f"\n✅ Scenario loading complete: {scenarios_loaded}/{len(scenario_files)} scenarios loaded")
        
        return scenarios_loaded > 0, manager
        
    except Exception as e:
        print(f"❌ Scenario loading test failed: {e}")
        traceback.print_exc()
        return False, None

# =============================================================================
# TEST 5: INTEGRATED SIMULATION WITH SCENARIOS
# =============================================================================
def test_integrated_simulation_with_scenarios():
    """Test integrated simulation with different scenarios"""
    print("\n" + "="*60)
    print("TEST 5: INTEGRATED SIMULATION WITH SCENARIOS")
    print("="*60)
    
    config = {
        'num_agents': 100,
        'retail_ratio': 0.8, 
        'time_steps': 10,
        'random_seed': 42
    }
    
    scenarios = [
        "branch_closure_scenario.json",
        "marketing_campaign_scenario.json",
        "digital_transformation_scenario.json"
    ]
    
    successful = 0
    
    for scenario_file in scenarios:
        print(f"\n--- Testing Scenario: {scenario_file} ---")
        try:
            model = IntegratedBankSimulationModel(config, scenario_file)
            
            # Run a few steps
            for i in range(3):
                model.step()
            
            # Check metrics
            avg_satisfaction = model.get_average_satisfaction()
            churn_rate = model.calculate_churn_rate()
            
            print(f"✅ Scenario executed successfully")
            print(f"   - Average satisfaction: {avg_satisfaction:.3f}")
            print(f"   - Churn rate: {churn_rate:.3f}")
            print(f"   - Total agents: {len(model.agents)}")
            
            successful += 1
            
        except Exception as e:
            print(f"❌ Error running scenario {scenario_file}: {e}")
            traceback.print_exc()
    
    print(f"\n✅ Integrated simulation test complete: {successful}/{len(scenarios)} scenarios successful")
    
    return successful > 0

# =============================================================================
# TEST 6: SEGMENT TARGETING
# =============================================================================
def test_segment_targeting():
    """Test segment-based targeting capabilities"""
    print("\n" + "="*60)
    print("TEST 6: SEGMENT TARGETING")
    print("="*60)
    
    try:
        config = {
            'num_agents': 500,
            'retail_ratio': 0.8,
            'time_steps': 20,
            'random_seed': 42
        }
        
        model = IntegratedBankSimulationModel(config, "marketing_campaign_scenario.json")
        
        # Check segment assignments
        print("✅ Segment assignments:")
        for segment, agents in model.agents_by_segment.items():
            if agents:
                print(f"   - {segment}: {len(agents)} agents")
        
        # Test targeting a segment
        if 'digital_first' in model.agents_by_segment and model.agents_by_segment['digital_first']:
            initial_satisfaction = sum(a.satisfaction_level for a in model.agents_by_segment['digital_first']) / len(model.agents_by_segment['digital_first'])
            
            model.target_segment('digital_first', {
                'type': 'marketing',
                'impact': 0.1
            })
            
            final_satisfaction = sum(a.satisfaction_level for a in model.agents_by_segment['digital_first']) / len(model.agents_by_segment['digital_first'])
            
            print(f"✅ Segment targeting successful")
            print(f"   - Initial satisfaction: {initial_satisfaction:.3f}")
            print(f"   - Final satisfaction: {final_satisfaction:.3f}")
            print(f"   - Improvement: {(final_satisfaction - initial_satisfaction):.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Segment targeting test failed: {e}")
        traceback.print_exc()
        return False

# =============================================================================
# TEST 7: SCENARIO OUTCOME VALIDATION & REPORTING
# =============================================================================
def test_scenario_outcome_validation():
    """Test scenario outcome validation and reporting"""
    print("\n" + "="*60)
    print("TEST 7: SCENARIO OUTCOME VALIDATION & REPORTING")
    print("="*60)
    
    try:
        config = {
            'num_agents': 200,
            'retail_ratio': 0.7,
            'time_steps': 30,
            'random_seed': 42
        }
        
        model = IntegratedBankSimulationModel(config, "digital_transformation_scenario.json")
        
        # Run simulation
        print("Running simulation...")
        final_report = model.run_simulation()
        
        # Validate report structure
        required_fields = ['scenario_name', 'agent_metrics', 'segment_performance', 'market_conditions']
        missing_fields = [field for field in required_fields if field not in final_report]
        
        if missing_fields:
            print(f"❌ Missing report fields: {missing_fields}")
            return False
        
        print("✅ Scenario report generated successfully")
        print(f"   - Scenario: {final_report['scenario_name']}")
        print(f"   - Final satisfaction: {final_report['agent_metrics']['average_satisfaction']:.3f}")
        print(f"   - Churn rate: {final_report['agent_metrics']['churn_rate']:.3f}")
        print(f"   - Digital usage: {final_report['agent_metrics']['digital_usage_rate']:.3f}")
        
        # Check segment performance
        if final_report['segment_performance']:
            print("   - Segment performance:")
            for segment, metrics in final_report['segment_performance'].items():
                print(f"     • {segment}: {metrics['size']} agents, satisfaction={metrics['avg_satisfaction']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Scenario outcome validation failed: {e}")
        traceback.print_exc()
        return False

# =============================================================================
# TEST 8: PERFORMANCE & STRESS TEST
# =============================================================================
def test_performance_stress():
    """Test simulation performance with larger agent populations"""
    print("\n" + "="*60)
    print("TEST 8: PERFORMANCE & STRESS TEST")
    print("="*60)
    
    try:
        config = {
            'num_agents': 2000,
            'retail_ratio': 0.85,
            'time_steps': 50,
            'random_seed': 42
        }
        
        print(f"Creating large simulation: {config['num_agents']} agents, {config['time_steps']} steps")
        
        start_time = time.time()
        model = IntegratedBankSimulationModel(config, "marketing_campaign_scenario.json")
        init_time = time.time() - start_time
        
        print(f"✅ Model initialized in {init_time:.2f} seconds")
        print(f"   - Agents created: {len(model.agents)}")
        print(f"   - Segments: {len(model.agents_by_segment)}")
        
        # Run simulation steps
        step_times = []
        for i in range(10):
            step_start = time.time()
            model.step()
            step_time = time.time() - step_start
            step_times.append(step_time)
        
        avg_step_time = sum(step_times) / len(step_times)
        print(f"✅ Performance metrics:")
        print(f"   - Average step time: {avg_step_time:.3f} seconds")
        print(f"   - Estimated full simulation time: {avg_step_time * config['time_steps']:.1f} seconds")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        traceback.print_exc()
        return False

# =============================================================================
# RUN ALL TESTS
# =============================================================================
def run_all_tests():
    """Run all tests and generate summary"""
    
    # Test 1: Mesa Basic
    test_results['mesa_basic'] = test_mesa_basic()
    
    # Test 2: CSV Loading
    csv_result, loader = test_csv_data_loading()
    test_results['csv_loading'] = csv_result
    
    # Test 3: Basic Simulation
    basic_result, model = test_basic_simulation_model()
    test_results['basic_simulation'] = basic_result
    
    # Test 4: Scenario Loading
    scenario_result, manager = test_scenario_loading()
    test_results['scenario_loading'] = scenario_result
    
    # Test 5: Integrated Simulation
    test_results['integrated_simulation'] = test_integrated_simulation_with_scenarios()
    
    # Test 6: Segment Targeting
    test_results['segment_targeting'] = test_segment_targeting()
    
    # Test 7: Outcome Validation
    test_results['outcome_validation'] = test_scenario_outcome_validation()
    
    # Test 8: Performance
    test_results['performance'] = test_performance_stress()
    
    # Generate summary
    print("\n" + "="*80)
    print("🏁 COMPREHENSIVE TEST SUITE RESULTS")
    print("="*80)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
    
    passed = sum(1 for r in test_results.values() if r)
    total = len(test_results)
    success_rate = (passed / total) * 100
    
    print(f"\n📊 SUMMARY: {passed}/{total} tests passed ({success_rate:.1f}%)")
    
    if passed < total:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("Please review the errors above before proceeding to production.")
    else:
        print("\n🎉 All tests passed! System is ready for production use.")
    
    return passed == total

# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n✅ All tests passed successfully!")
    else:
        print("\n❌ Some tests failed. Please fix issues before production use.")
    
    sys.exit(0 if success else 1)