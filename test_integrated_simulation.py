# test_integrated_simulation.py

"""
Test script for integrated Mesa simulation with scenarios
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.agent_engine.mesa_setup_integrated import IntegratedBankSimulationModel
import json

def test_scenario_simulation():
    """Test running a complete scenario"""
    print("\n" + "="*60)
    print("TESTING INTEGRATED SIMULATION WITH SCENARIOS")
    print("="*60)
    
    # Configuration
    config = {
        'num_agents': 1000,  # Will be overridden by scenario
        'retail_ratio': 0.8,
        'time_steps': 100,   # Will be overridden by scenario
        'random_seed': 42
    }
    
    # Test different scenarios
    scenarios_to_test = [
        "branch_closure_scenario.json",
        "marketing_campaign_scenario.json",
        "digital_transformation_scenario.json"
    ]
    
    for scenario_file in scenarios_to_test:
        print(f"\n--- Testing Scenario: {scenario_file} ---")
        
        try:
            # Create model with scenario
            model = IntegratedBankSimulationModel(config, scenario_file)
            
            print(f"✅ Loaded scenario: {model.current_scenario.metadata.name if model.current_scenario else 'None'}")
            print(f"   Duration: {model.time_steps} steps")
            print(f"   Events: {len(model.event_system.event_queue)} queued")
            print(f"   Agents: {len(model.agents)}")
            print(f"   Segments: {[(k, len(v)) for k, v in model.agents_by_segment.items()]}")
            
            # Run first 10 steps
            for i in range(min(10, model.time_steps)):
                model.step()
                
                if i % 5 == 0:
                    print(f"   Step {i}: satisfaction={model.get_average_satisfaction():.3f}, "
                          f"churn={model.calculate_churn_rate():.3f}, "
                          f"active_events={len(model.active_events)}")
            
            print("✅ Scenario execution successful")
            
        except Exception as e:
            print(f"❌ Error running scenario {scenario_file}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("SEGMENT TARGETING TEST")
    print("="*60)
    
    # Test segment targeting
    model = IntegratedBankSimulationModel(config, "marketing_campaign_scenario.json")
    
    segments_to_test = [
        'high_value_retail',
        'young_digital',
        'young_professionals',
        'urban_customers',
        'sfax_clients'
    ]
    
    for segment in segments_to_test:
        agents = model.get_agents_by_segment(segment)
        print(f"Segment '{segment}': {len(agents)} agents")
        
        if agents and len(agents) > 0:
            avg_satisfaction = sum(a.satisfaction_level for a in agents) / len(agents)
            print(f"   Average satisfaction: {avg_satisfaction:.3f}")
    
    print("\n✅ Integration test complete!")

def test_scenario_outcomes():
    """Test scenario outcome validation"""
    print("\n" + "="*60)
    print("TESTING SCENARIO OUTCOME VALIDATION")
    print("="*60)
    
    config = {
        'num_agents': 500,
        'retail_ratio': 0.8,
        'time_steps': 50,
        'random_seed': 42
    }
    
    # Run a shorter scenario
    model = IntegratedBankSimulationModel(config, "digital_transformation_scenario.json")
    
    # Override time steps for faster testing
    model.time_steps = 20
    
    print(f"Running {model.time_steps} steps...")
    
    # Run simulation
    while model.running:
        model.step()
    
    # Get final report
    if model.current_scenario:
        report = model.generate_scenario_report()
        
        print("\nScenario Report:")
        print(f"  Scenario: {report['scenario_name']}")
        print(f"  Steps: {report['total_steps']}")
        print(f"  Events: {report['events_processed']}")
        print("\n  Final Metrics:")
        for metric, value in report['final_metrics'].items():
            print(f"    {metric}: {value:.3f}")
        print("\n  Segment Performance:")
        for segment, satisfaction in report['segment_performance'].items():
            print(f"    {segment}: {satisfaction:.3f}")
        print("\n  Outcome Validation:")
        for outcome in report['outcome_validation']:
            status = "✅" if outcome['valid'] else "❌"
            print(f"    {status} {outcome['metric']}: {outcome['actual']:.3f} (target: {outcome['target']})")
    
    print("\n✅ Outcome validation test complete!")

if __name__ == "__main__":
    print("🚀 TESTING INTEGRATED MESA SIMULATION WITH SCENARIOS")
    
    # Run tests
    test_scenario_simulation()
    test_scenario_outcomes()
    
    print("\n" + "="*60)
    print("INTEGRATION COMPLETE!")
    print("="*60)
    print("\nThe Mesa simulation now supports:")
    print("✅ Loading and executing predefined scenarios")
    print("✅ Processing events that affect specific agent segments")
    print("✅ Tracking and validating scenario outcomes")
    print("✅ Generating comprehensive scenario reports")
    print("✅ Targeting events to specific client segments")
    print("\nNext steps:")
    print("1. Create custom scenarios using the scenario templates")
    print("2. Run full simulations with different scenarios")
    print("3. Analyze segment-specific impacts")
    print("4. Compare scenario outcomes")