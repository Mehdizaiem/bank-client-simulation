#!/usr/bin/env python3
"""
Direct Simulation Test - No API or Complex Integration
Just run the simulation and see the output for dashboard
"""
import sys
import os
from pathlib import Path
import json
import pandas as pd
import time

# Setup paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

print("="*80)
print("🏦 DIRECT BANK SIMULATION TEST")
print("="*80)

# ==============================================================================
# TEST 1: Basic Simulation with Output
# ==============================================================================
def test_basic_simulation():
    """Run basic simulation and export data"""
    print("\n1️⃣ TESTING BASIC SIMULATION")
    print("-"*40)
    
    try:
        from src.agent_engine.mesa_setup import BankSimulationModel
        
        # Simple configuration
        config = {
            'num_agents': 100,
            'retail_ratio': 0.8,
            'time_steps': 50,
            'random_seed': 42
        }
        
        print(f"Creating simulation with {config['num_agents']} agents...")
        model = BankSimulationModel(config)
        
        print(f"✅ Model created with {len(model.agents)} agents")
        
        # Collect data during simulation
        simulation_data = {
            'metadata': {
                'start_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'config': config,
                'total_agents': len(model.agents)
            },
            'time_series': {
                'step': [],
                'satisfaction': [],
                'churn_rate': [],
                'digital_adoption': [],
                'active_agents': []
            },
            'final_state': {}
        }
        
        # Run simulation and collect metrics
        print("\nRunning simulation...")
        for step in range(config['time_steps']):
            model.step()
            
            # Collect metrics every 10 steps
            if step % 10 == 0:
                avg_satisfaction = model.get_average_satisfaction()
                churn_rate = model.calculate_churn_rate()
                digital_adoption = model.get_digital_adoption_rate()
                active = len([a for a in model.agents if a.status == 'active'])
                
                simulation_data['time_series']['step'].append(step)
                simulation_data['time_series']['satisfaction'].append(avg_satisfaction)
                simulation_data['time_series']['churn_rate'].append(churn_rate)
                simulation_data['time_series']['digital_adoption'].append(digital_adoption)
                simulation_data['time_series']['active_agents'].append(active)
                
                print(f"  Step {step:3d}: Satisfaction={avg_satisfaction:.3f}, "
                      f"Churn={churn_rate:.3f}, Digital={digital_adoption:.3f}")
        
        # Get final state
        simulation_data['final_state'] = {
            'total_steps_completed': config['time_steps'],
            'final_satisfaction': simulation_data['time_series']['satisfaction'][-1],
            'final_churn_rate': simulation_data['time_series']['churn_rate'][-1],
            'final_digital_adoption': simulation_data['time_series']['digital_adoption'][-1],
            'final_active_agents': simulation_data['time_series']['active_agents'][-1]
        }
        
        simulation_data['metadata']['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Save to JSON for dashboard
        output_file = 'simulation_output_for_dashboard.json'
        with open(output_file, 'w') as f:
            json.dump(simulation_data, f, indent=2)
        
        print(f"\n✅ Simulation complete! Output saved to: {output_file}")
        print("\n📊 Final Metrics:")
        for key, value in simulation_data['final_state'].items():
            print(f"   {key}: {value}")
        
        return simulation_data
        
    except Exception as e:
        print(f"❌ Basic simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

# ==============================================================================
# TEST 2: Simulation with Scenario
# ==============================================================================
def test_scenario_simulation():
    """Test simulation with a scenario"""
    print("\n2️⃣ TESTING SIMULATION WITH SCENARIO")
    print("-"*40)
    
    try:
        from src.agent_engine.mesa_setup_integrated import IntegratedBankSimulationModel
        
        config = {
            'num_agents': 100,
            'retail_ratio': 0.8,
            'time_steps': 50,
            'random_seed': 42
        }
        
        # Try to load with scenario
        scenario_file = 'branch_closure_scenario'
        
        print(f"Creating simulation with scenario: {scenario_file}")
        model = IntegratedBankSimulationModel(config, scenario_file)
        
        if model.current_scenario:
            print(f"✅ Scenario loaded: {model.current_scenario.metadata.name}")
        else:
            print("⚠️ Running without scenario")
        
        # Run and collect data
        scenario_data = {
            'scenario_name': model.current_scenario.metadata.name if model.current_scenario else 'none',
            'events_processed': [],
            'metrics': []
        }
        
        print("\nRunning scenario simulation...")
        for step in range(20):
            model.step()
            
            if step % 5 == 0:
                metrics = {
                    'step': step,
                    'satisfaction': model.get_average_satisfaction(),
                    'events_at_step': len(model.event_system.get_events_at_step(step)) if hasattr(model, 'event_system') else 0
                }
                scenario_data['metrics'].append(metrics)
                print(f"  Step {step}: {metrics}")
        
        # Save scenario output
        output_file = 'scenario_output_for_dashboard.json'
        with open(output_file, 'w') as f:
            json.dump(scenario_data, f, indent=2)
        
        print(f"\n✅ Scenario simulation complete! Output saved to: {output_file}")
        return scenario_data
        
    except Exception as e:
        print(f"⚠️ Scenario simulation couldn't run: {e}")
        print("This is OK if scenario files aren't set up yet")
        return None

# ==============================================================================
# TEST 3: Agent Data Export
# ==============================================================================
def test_agent_export():
    """Test exporting agent data for dashboard"""
    print("\n3️⃣ TESTING AGENT DATA EXPORT")
    print("-"*40)
    
    try:
        from src.agent_engine.mesa_setup import BankSimulationModel
        
        config = {
            'num_agents': 50,
            'retail_ratio': 0.8,
            'time_steps': 10,
            'random_seed': 42
        }
        
        model = BankSimulationModel(config)
        
        # Run a few steps
        for _ in range(5):
            model.step()
        
        # Export agent data
        agent_df = model.export_agent_data()
        
        print(f"Exported {len(agent_df)} agents to DataFrame")
        print(f"Columns: {list(agent_df.columns)}")
        
        # Create dashboard-friendly format
        dashboard_agents = {
            'agent_distribution': {
                'by_type': agent_df['client_type'].value_counts().to_dict(),
                'by_status': agent_df['status'].value_counts().to_dict(),
                'by_channel': agent_df['preferred_channel'].value_counts().to_dict() if 'preferred_channel' in agent_df else {},
                'by_governorate': agent_df['governorate'].value_counts().to_dict() if 'governorate' in agent_df else {}
            },
            'statistics': {
                'avg_satisfaction': agent_df['satisfaction_level'].mean() if 'satisfaction_level' in agent_df else 0,
                'avg_age': agent_df['age'].mean() if 'age' in agent_df else 0,
                'avg_income': agent_df['income'].mean() if 'income' in agent_df else 0
            },
            'sample_agents': agent_df.head(10).to_dict('records')
        }
        
        # Save agent analysis
        output_file = 'agent_analysis_for_dashboard.json'
        with open(output_file, 'w') as f:
            json.dump(dashboard_agents, f, indent=2, default=str)
        
        print(f"\n✅ Agent data exported to: {output_file}")
        print("\n📊 Agent Distribution:")
        for key, value in dashboard_agents['agent_distribution'].items():
            print(f"   {key}: {value}")
        
        # Also save as CSV for easier analysis
        agent_df.to_csv('agents_data.csv', index=False)
        print(f"\n📁 Also saved as CSV: agents_data.csv")
        
        return dashboard_agents
        
    except Exception as e:
        print(f"❌ Agent export failed: {e}")
        import traceback
        traceback.print_exc()
        return None

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print("\n🚀 Starting Direct Simulation Tests...")
    print("="*80)
    
    # Check if data files exist
    data_files = [
        'data/processed/hamza_retail_agents.csv',
        'data/processed/hamza_corporate_agents.csv'
    ]
    
    missing_files = []
    for file_path in data_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("⚠️  WARNING: Missing data files:")
        for f in missing_files:
            print(f"   - {f}")
        print("\nTrying to continue anyway...")
    
    # Run tests
    results = []
    
    # Test 1: Basic Simulation
    basic_result = test_basic_simulation()
    results.append(('Basic Simulation', basic_result is not None))
    
    # Test 2: Scenario Simulation (optional)
    scenario_result = test_scenario_simulation()
    results.append(('Scenario Simulation', scenario_result is not None))
    
    # Test 3: Agent Export
    agent_result = test_agent_export()
    results.append(('Agent Export', agent_result is not None))
    
    # Summary
    print("\n" + "="*80)
    print("📋 TEST SUMMARY")
    print("="*80)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:25} {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed > 0:
        print("\n📊 Generated Output Files:")
        print("   - simulation_output_for_dashboard.json")
        print("   - scenario_output_for_dashboard.json (if scenario worked)")
        print("   - agent_analysis_for_dashboard.json")
        print("   - agents_data.csv")
        print("\n💡 Share these JSON files with Nessrine for the dashboard!")
    
    print("\n✨ Test complete!")