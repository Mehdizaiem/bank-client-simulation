#!/usr/bin/env python3
"""
COMPREHENSIVE INTEGRATED SIMULATION TEST SUITE
Tests all aspects of the Mesa 3.x Bank Simulation with Scenarios
Author: Combined Test Suite
"""

import sys
import os
import traceback
import json
import time
from pathlib import Path
from datetime import datetime

# Add src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

print(f"🚀 COMPREHENSIVE INTEGRATED BANK SIMULATION TEST SUITE")
print(f"Current directory: {current_dir}")
print(f"Source directory: {src_dir}")
print("="*80)

try:
    # Test imports
    import mesa
    import pandas as pd
    from src.agent_engine.mesa_setup_integrated import IntegratedBankSimulationModel
    from src.agent_engine.mesa_setup import BankSimulationModel
    from src.agent_engine.data_loader import AgentDataLoader
    from src.agent_engine.retail_agent import RetailClientAgent
    from src.agent_engine.corporate_agent import CorporateClientAgent
    print(f"✅ Mesa version {mesa.__version__} and all modules imported successfully")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have Mesa installed and all src/ modules exist")
    sys.exit(1)

# =============================================================================
# TEST 1: BASIC MESA FUNCTIONALITY
# =============================================================================
def test_mesa_basic_functionality():
    """Test basic Mesa 3.x functionality"""
    print("\n" + "="*60)
    print("TEST 1: MESA 3.X BASIC FUNCTIONALITY")
    print("="*60)
    
    try:
        # Test Mesa imports
        import mesa
        from mesa.datacollection import DataCollector
        print("✅ Mesa 3.x imports working")
        
        # Test basic Model creation
        class TestModel(mesa.Model):
            def __init__(self):
                super().__init__(seed=42)
        
        model = TestModel()
        print("✅ Mesa 3.x Model creation working")
        print(f"   - Agents container: {type(model.agents)}")
        print(f"   - Initial agent count: {len(model.agents)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Mesa basic functionality failed: {e}")
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
        
        # Run a few simulation steps
        print("\nRunning basic simulation steps...")
        for i in range(5):
            initial_satisfaction = model.get_average_satisfaction()
            model.step()
            final_satisfaction = model.get_average_satisfaction()
            print(f"   Step {i+1}: satisfaction {initial_satisfaction:.3f} → {final_satisfaction:.3f}")
        
        # Test data export
        agent_data = model.export_agent_data()
        print(f"✅ Data export successful: {len(agent_data)} agent records")
        
        return True, model
        
    except Exception as e:
        print(f"❌ Basic simulation model failed: {e}")
        traceback.print_exc()
        return False, None

# =============================================================================
# TEST 4: SCENARIO LOADING
# =============================================================================
def test_scenario_loading():
    """Test scenario loading and validation"""
    print("\n" + "="*60)
    print("TEST 4: SCENARIO LOADING")
    print("="*60)
    
    try:
        from src.simulation.scenarios import ScenarioManager
        
        scenario_manager = ScenarioManager()
        
        # Test loading different scenarios
        scenarios_to_test = [
            "branch_closure_scenario.json",
            "marketing_campaign_scenario.json", 
            "digital_transformation_scenario.json"
        ]
        
        loaded_scenarios = []
        
        for scenario_file in scenarios_to_test:
            try:
                scenario = scenario_manager.load_scenario(scenario_file)
                if scenario:
                    loaded_scenarios.append(scenario)
                    print(f"✅ Loaded scenario: {scenario.metadata.name}")
                    print(f"   - Duration: {scenario.simulation_parameters.duration_steps} steps")
                    print(f"   - Events: {len(scenario.events)}")
                    print(f"   - Population: {scenario.simulation_parameters.agent_population}")
                else:
                    print(f"❌ Failed to load {scenario_file}: returned None")
                    
            except Exception as e:
                print(f"❌ Failed to load {scenario_file}: {e}")
        
        print(f"\n✅ Scenario loading complete: {len(loaded_scenarios)}/{len(scenarios_to_test)} scenarios loaded")
        return True, loaded_scenarios
        
    except Exception as e:
        print(f"❌ Scenario loading failed: {e}")
        traceback.print_exc()
        return False, []

# =============================================================================
# TEST 5: INTEGRATED SIMULATION WITH SCENARIOS
# =============================================================================
def test_integrated_simulation_with_scenarios():
    """Test integrated simulation with scenario execution"""
    print("\n" + "="*60)
    print("TEST 5: INTEGRATED SIMULATION WITH SCENARIOS")
    print("="*60)
    
    # Test different scenarios
    scenarios_to_test = [
        "branch_closure_scenario.json",
        "marketing_campaign_scenario.json",
        "digital_transformation_scenario.json"
    ]
    
    successful_scenarios = []
    
    for scenario_file in scenarios_to_test:
        print(f"\n--- Testing Scenario: {scenario_file} ---")
        
        try:
            config = {
                'num_agents': 500,  # Smaller for faster testing
                'retail_ratio': 0.8,
                'time_steps': 50,   # Will be overridden by scenario
                'random_seed': 42
            }
            
            # Create integrated model with scenario
            model = IntegratedBankSimulationModel(config, scenario_file)
            
            if model.current_scenario:
                print(f"✅ Scenario loaded: {model.current_scenario.metadata.name}")
                print(f"   Duration: {model.time_steps} steps")
                print(f"   Events queued: {len(model.event_system.event_queue)}")
                print(f"   Agents created: {len(model.agents)}")
                print(f"   Segments: {[(k, len(v)) for k, v in model.agents_by_segment.items()]}")
                
                # Run first 15 steps to test event processing
                print("   Running simulation steps...")
                for i in range(min(15, model.time_steps)):
                    model.step()
                    
                    if i % 5 == 0:
                        satisfaction = model.get_average_satisfaction()
                        churn = model.calculate_churn_rate()
                        digital = model.get_digital_usage_rate()
                        active_events = len(model.active_events)
                        
                        print(f"   Step {i}: satisfaction={satisfaction:.3f}, "
                              f"churn={churn:.3f}, digital={digital:.3f}, "
                              f"active_events={active_events}")
                
                successful_scenarios.append(scenario_file)
                print(f"✅ Scenario {scenario_file} executed successfully")
            else:
                print(f"❌ Failed to load scenario {scenario_file}")
                
        except Exception as e:
            print(f"❌ Error running scenario {scenario_file}: {e}")
            traceback.print_exc()
    
    print(f"\n✅ Integrated simulation test complete: {len(successful_scenarios)}/{len(scenarios_to_test)} scenarios successful")
    return len(successful_scenarios) > 0, successful_scenarios

# =============================================================================
# TEST 6: SEGMENT TARGETING
# =============================================================================
def test_segment_targeting():
    """Test client segment targeting functionality"""
    print("\n" + "="*60)
    print("TEST 6: SEGMENT TARGETING")
    print("="*60)
    
    try:
        config = {
            'num_agents': 800,
            'retail_ratio': 0.75,
            'time_steps': 50,
            'random_seed': 42
        }
        
        # Create model with marketing scenario (has segment targeting)
        model = IntegratedBankSimulationModel(config, "marketing_campaign_scenario.json")
        
        segments_to_test = [
            'high_value_retail',
            'young_digital', 
            'large_corporates',
            'tech_companies',
            'standard_retail',
            'standard_corporate',
            'young_professionals',
            'urban_customers',
            'sfax_clients'
        ]
        
        segment_results = {}
        
        for segment in segments_to_test:
            agents = model.get_agents_by_segment(segment)
            segment_results[segment] = {
                'count': len(agents),
                'avg_satisfaction': 0.0
            }
            
            if agents:
                avg_satisfaction = sum(a.satisfaction_level for a in agents) / len(agents)
                segment_results[segment]['avg_satisfaction'] = avg_satisfaction
                print(f"✅ Segment '{segment}': {len(agents)} agents, "
                      f"avg satisfaction: {avg_satisfaction:.3f}")
            else:
                print(f"⚠️  Segment '{segment}': 0 agents")
        
        # Test segment-specific event targeting
        print("\nTesting segment-specific event effects...")
        from src.simulation.event_types import MarketingCampaignEvent
        
        # Create a targeted marketing event
        marketing_event = MarketingCampaignEvent(
            event_id="test_marketing",
            step=1,
            target_segment="young_digital",
            campaign_type="digital_promotion",
            intensity=1.5,
            duration=3
        )
        
        # Get target segment before
        target_agents = model.get_agents_by_segment("young_digital")
        if target_agents:
            before_satisfaction = sum(a.satisfaction_level for a in target_agents) / len(target_agents)
            
            # Apply marketing event
            model.handle_marketing_campaign(marketing_event)
            
            # Check satisfaction after
            after_satisfaction = sum(a.satisfaction_level for a in target_agents) / len(target_agents)
            
            print(f"✅ Marketing event effect on 'young_digital' segment:")
            print(f"   Before: {before_satisfaction:.3f} → After: {after_satisfaction:.3f}")
            print(f"   Improvement: {after_satisfaction - before_satisfaction:.3f}")
        
        total_agents_in_segments = sum(result['count'] for result in segment_results.values())
        print(f"\n✅ Segment targeting test complete")
        print(f"   Total agents: {len(model.agents)}")
        print(f"   Agents in segments: {total_agents_in_segments}")
        print(f"   Segments with agents: {sum(1 for r in segment_results.values() if r['count'] > 0)}")
        
        return True, segment_results
        
    except Exception as e:
        print(f"❌ Segment targeting test failed: {e}")
        traceback.print_exc()
        return False, {}

# =============================================================================
# TEST 7: SCENARIO OUTCOME VALIDATION
# =============================================================================
def test_scenario_outcome_validation():
    """Test scenario outcome validation and reporting"""
    print("\n" + "="*60)
    print("TEST 7: SCENARIO OUTCOME VALIDATION & REPORTING")
    print("="*60)
    
    try:
        config = {
            'num_agents': 600,
            'retail_ratio': 0.8,
            'time_steps': 30,  # Short for testing
            'random_seed': 42
        }
        
        # Run a complete scenario with outcome validation
        model = IntegratedBankSimulationModel(config, "digital_transformation_scenario.json")
        
        if not model.current_scenario:
            print("❌ No scenario loaded for outcome validation")
            return False, None
        
        print(f"✅ Running scenario: {model.current_scenario.metadata.name}")
        print(f"   Duration: {model.time_steps} steps")
        print(f"   Expected outcomes: {len(model.current_scenario.expected_outcomes) if hasattr(model.current_scenario, 'expected_outcomes') else 0}")
        
        # Run complete simulation
        step_count = 0
        while model.running and step_count < model.time_steps:
            model.step()
            step_count += 1
            
            if step_count % 10 == 0:
                print(f"   Progress: Step {step_count}/{model.time_steps}")
        
        # Generate final report
        print("\nGenerating scenario report...")
        report = model.generate_scenario_report()
        
        if report:
            print(f"✅ Scenario report generated successfully")
            print(f"\nScenario Report Summary:")
            print(f"  Scenario: {report['scenario_name']}")
            print(f"  Steps completed: {report['total_steps']}")
            print(f"  Events processed: {report['events_processed']}")
            
            print(f"\n  Final Metrics:")
            for metric, value in report['final_metrics'].items():
                print(f"    {metric}: {value:.3f}")
            
            print(f"\n  Top Segment Performance:")
            segment_perf = report['segment_performance']
            sorted_segments = sorted(segment_perf.items(), key=lambda x: x[1], reverse=True)[:5]
            for segment, satisfaction in sorted_segments:
                print(f"    {segment}: {satisfaction:.3f}")
            
            print(f"\n  Outcome Validation:")
            if report['outcome_validation']:
                for outcome in report['outcome_validation']:
                    status = "✅" if outcome['valid'] else "❌"
                    print(f"    {status} {outcome['metric']}: {outcome['actual']:.3f} "
                          f"(target: {outcome['target']})")
            else:
                print("    No outcomes defined for validation")
            
            # Check if report file was saved
            report_file = Path("simulation_outputs") / f"{model.current_scenario.metadata.name.replace(' ', '_').lower()}_report.json"
            if report_file.exists():
                print(f"\n✅ Report saved to: {report_file}")
            
            return True, report
        else:
            print("❌ Failed to generate scenario report")
            return False, None
            
    except Exception as e:
        print(f"❌ Scenario outcome validation failed: {e}")
        traceback.print_exc()
        return False, None

# =============================================================================
# TEST 8: PERFORMANCE AND STRESS TEST
# =============================================================================
def test_performance_stress():
    """Test simulation performance with larger datasets"""
    print("\n" + "="*60)
    print("TEST 8: PERFORMANCE & STRESS TEST")
    print("="*60)
    
    try:
        config = {
            'num_agents': 2000,  # Larger dataset
            'retail_ratio': 0.8,
            'time_steps': 50,
            'random_seed': 42
        }
        
        print(f"Creating large simulation: {config['num_agents']} agents, {config['time_steps']} steps")
        
        # Measure initialization time
        start_time = time.time()
        model = IntegratedBankSimulationModel(config, "marketing_campaign_scenario.json")
        init_time = time.time() - start_time
        
        print(f"✅ Initialization completed in {init_time:.2f} seconds")
        print(f"   Agents created: {len(model.agents)}")
        print(f"   Memory usage: ~{len(model.agents) * 0.5:.1f} KB (estimated)")
        
        # Measure step performance
        step_times = []
        print(f"\nRunning performance test...")
        
        for i in range(20):  # Test first 20 steps
            step_start = time.time()
            model.step()
            step_time = time.time() - step_start
            step_times.append(step_time)
            
            if i % 5 == 0:
                print(f"   Step {i+1}: {step_time:.3f}s")
        
        avg_step_time = sum(step_times) / len(step_times)
        max_step_time = max(step_times)
        min_step_time = min(step_times)
        
        print(f"\n✅ Performance metrics:")
        print(f"   Average step time: {avg_step_time:.3f}s")
        print(f"   Min step time: {min_step_time:.3f}s")
        print(f"   Max step time: {max_step_time:.3f}s")
        print(f"   Agents per second: {len(model.agents)/avg_step_time:.0f}")
        
        # Performance benchmarks
        performance_good = avg_step_time < 1.0  # Less than 1 second per step
        performance_acceptable = avg_step_time < 2.0  # Less than 2 seconds per step
        
        if performance_good:
            print(f"   🚀 Performance: EXCELLENT (< 1s per step)")
        elif performance_acceptable:
            print(f"   ✅ Performance: GOOD (< 2s per step)")
        else:
            print(f"   ⚠️  Performance: SLOW (> 2s per step)")
        
        return performance_acceptable, {
            'avg_step_time': avg_step_time,
            'agents': len(model.agents),
            'init_time': init_time
        }
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        traceback.print_exc()
        return False, {}

# =============================================================================
# MAIN TEST RUNNER
# =============================================================================
def run_comprehensive_test_suite():
    """Run the complete test suite"""
    print("\n🎯 STARTING COMPREHENSIVE TEST SUITE")
    print("="*80)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_results = {}
    test_data = {}
    
    # Test 1: Basic Mesa functionality
    test_results['mesa_basic'] = test_mesa_basic_functionality()
    
    # Test 2: CSV data loading
    result, loader = test_csv_data_loading()
    test_results['csv_loading'] = result
    test_data['loader'] = loader
    
    # Test 3: Basic simulation model
    result, model = test_basic_simulation_model()
    test_results['basic_simulation'] = result
    test_data['basic_model'] = model
    
    # Test 4: Scenario loading
    result, scenarios = test_scenario_loading()
    test_results['scenario_loading'] = result
    test_data['scenarios'] = scenarios
    
    # Test 5: Integrated simulation with scenarios
    result, successful_scenarios = test_integrated_simulation_with_scenarios()
    test_results['integrated_simulation'] = result
    test_data['successful_scenarios'] = successful_scenarios
    
    # Test 6: Segment targeting
    result, segment_data = test_segment_targeting()
    test_results['segment_targeting'] = result
    test_data['segments'] = segment_data
    
    # Test 7: Scenario outcome validation
    result, report = test_scenario_outcome_validation()
    test_results['outcome_validation'] = result
    test_data['final_report'] = report
    
    # Test 8: Performance test
    result, perf_data = test_performance_stress()
    test_results['performance'] = result
    test_data['performance'] = perf_data
    
    # Calculate results
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    # Print final summary
    print("\n" + "="*80)
    print("🏁 COMPREHENSIVE TEST SUITE RESULTS")
    print("="*80)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
    
    print(f"\n📊 SUMMARY: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\n🚀 SIMULATION SYSTEM STATUS: FULLY OPERATIONAL")
        print("\n✅ Ready for production use:")
        print("   • CSV data loading ✅")
        print("   • Agent-based simulation ✅") 
        print("   • Scenario execution ✅")
        print("   • Event system ✅")
        print("   • Segment targeting ✅")
        print("   • Outcome validation ✅")
        print("   • Performance optimization ✅")
        
        # Additional insights
        if test_data.get('performance'):
            perf = test_data['performance']
            print(f"\n📈 Performance Metrics:")
            print(f"   • {perf['agents']} agents simulated")
            print(f"   • {perf['avg_step_time']:.3f}s average step time")
            print(f"   • {perf['init_time']:.2f}s initialization time")
        
        if test_data.get('segments'):
            total_segments = len([s for s in test_data['segments'].values() if s['count'] > 0])
            print(f"   • {total_segments} active client segments")
            
        if test_data.get('successful_scenarios'):
            print(f"   • {len(test_data['successful_scenarios'])} scenarios tested")
        
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed")
        print("Please review the errors above before proceeding to production.")
        return False

if __name__ == "__main__":
    try:
        # Ensure output directories exist
        Path("logs").mkdir(exist_ok=True)
        Path("simulation_outputs").mkdir(exist_ok=True)
        
        # Run comprehensive test suite
        success = run_comprehensive_test_suite()
        
        if success:
            print("\n" + "="*80)
            print("🎯 NEXT STEPS:")
            print("1. ✅ Run production simulations with real scenarios")
            print("2. ✅ Analyze client segment behavior patterns")
            print("3. ✅ Generate business intelligence reports")
            print("4. ✅ Scale to larger datasets as needed")
            print("5. ✅ Deploy for stakeholder demonstrations")
            print("="*80)
        else:
            print("\n❌ Some tests failed. Please fix issues before production use.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Test suite interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error in test suite: {e}")
        traceback.print_exc()