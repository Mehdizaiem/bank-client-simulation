#!/usr/bin/env python3
"""
Complete test script for Mesa 3.x Bank Simulation Setup
Tests all functionality including agent creation, simulation steps, and data export
"""

import sys
import os
import traceback
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

print(f"Current directory: {current_dir}")
print(f"Source directory: {src_dir}")
print(f"Python path: {sys.path[:3]}...")

try:
    # Test Mesa installation first
    import mesa
    print(f"✅ Mesa version {mesa.__version__} imported successfully")
    
    # Test our custom imports
    from src.agent_engine.mesa_setup import BankSimulationModel
    from src.agent_engine.base_agent import BaseClientAgent
    print("✅ Custom modules imported successfully")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have Mesa installed and src/ directory exists")
    sys.exit(1)

def test_mesa_basic_functionality():
    """Test basic Mesa 3.x functionality"""
    print("\n" + "="*50)
    print("TESTING MESA 3.X BASIC FUNCTIONALITY")
    print("="*50)
    
    try:
        # Test Mesa imports
        import mesa
        from mesa.datacollection import DataCollector
        print("✅ Mesa 3.x imports working")
        
        # Test basic Model creation - FIXED
        class TestModel(mesa.Model):
            def __init__(self):
                super().__init__(seed=42)
                # Mesa 3.x automatically creates self.agents
        
        model = TestModel()
        print("✅ Mesa 3.x Model creation working")
        
        return True
        
    except Exception as e:
        print(f"❌ Mesa basic functionality failed: {e}")
        traceback.print_exc()
        return False

def test_model_creation():
    """Test BankSimulationModel creation"""
    print("\n" + "="*50)
    print("TESTING MODEL CREATION")
    print("="*50)
    
    try:
        config = {
            'num_agents': 10,
            'retail_ratio': 0.8,
            'time_steps': 5,
            'random_seed': 42
        }
        
        print("Creating BankSimulationModel...")
        model = BankSimulationModel(config)
        
        # Test model properties
        assert model.num_agents == 10, f"Expected 10 agents, got {model.num_agents}"
        assert model.retail_ratio == 0.8, f"Expected 0.8 retail ratio, got {model.retail_ratio}"
        assert model.time_steps == 5, f"Expected 5 time steps, got {model.time_steps}"
        assert model.current_step == 0, f"Expected step 0, got {model.current_step}"
        
        print("✅ Model created with correct parameters")
        print(f"   - Agents: {model.num_agents}")
        print(f"   - Retail ratio: {model.retail_ratio}")
        print(f"   - Time steps: {model.time_steps}")
        print(f"   - Current step: {model.current_step}")
        
        return model
        
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        traceback.print_exc()
        return None

def test_agent_creation(model):
    """Test BaseClientAgent creation"""
    print("\n" + "="*50)
    print("TESTING AGENT CREATION")
    print("="*50)
    
    if not model:
        print("❌ Cannot test agents without valid model")
        return []
    
    try:
        agents = []
        
        # Create test agents with different profiles
        test_profiles = [
            {
                'age': 25,
                'income': 1500,
                'governorate': 'Tunis',
                'education_level': 'university',
                'client_type': 'retail'
            },
            {
                'age': 45,
                'income': 3500,
                'governorate': 'Sfax',
                'education_level': 'secondary',
                'client_type': 'retail'
            },
            {
                'age': 35,
                'income': 2800,
                'governorate': 'Sousse',
                'education_level': 'university',
                'client_type': 'retail'
            },
            {
                'age': 55,
                'income': 4200,
                'governorate': 'Kairouan',
                'education_level': 'primary',
                'client_type': 'retail'
            },
            {
                'age': 40,
                'income': 8000,
                'governorate': 'Ariana',
                'education_level': 'graduate',
                'client_type': 'corporate'
            }
        ]
        
        print(f"Creating {len(test_profiles)} test agents...")
        
        for i, profile in enumerate(test_profiles):
            # Mesa 3.x agent creation - no unique_id needed
            agent = BaseClientAgent(model, profile)
            agents.append(agent)
            model.add_agent(agent)  # Our custom tracking
            
            print(f"✅ Agent {agent.unique_id}: {profile['age']}y, {profile['income']} TND, {profile['governorate']}")
            print(f"   - Satisfaction: {agent.satisfaction_level:.2f}")
            print(f"   - Primary channel: {agent.primary_channel}")
            print(f"   - Price sensitivity: {agent.price_sensitivity:.2f}")
        
        print(f"✅ Created and added {len(agents)} agents to model")
        print(f"   - Total agents in model: {len(model.agents)}")
        print(f"   - Retail agents: {len(model.our_agents_by_type['retail'])}")
        print(f"   - Corporate agents: {len(model.our_agents_by_type['corporate'])}")
        
        return agents
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        traceback.print_exc()
        return []

def test_agent_behavior(agents):
    """Test individual agent behavior"""
    print("\n" + "="*50)
    print("TESTING AGENT BEHAVIOR")
    print("="*50)
    
    if not agents:
        print("❌ Cannot test behavior without agents")
        return False
    
    try:
        # Test agent with some experiences
        test_agent = agents[0]
        print(f"Testing agent {test_agent.unique_id} behavior:")
        print(f"Initial satisfaction: {test_agent.satisfaction_level:.3f}")
        
        # Add some banking experiences
        experiences = [
            ('transaction', 'branch', 0.8, 'Good service at branch'),
            ('inquiry', 'online', 0.4, 'Website was slow'),
            ('transaction', 'mobile', 0.9, 'App worked perfectly'),
            ('complaint', 'call_center', 0.3, 'Long wait time'),
            ('transaction', 'branch', 0.7, 'Decent service')
        ]
        
        for exp_type, channel, quality, description in experiences:
            test_agent.add_experience(exp_type, channel, quality, description)
        
        print(f"Added {len(experiences)} experiences")
        print(f"Experience history length: {len(test_agent.recent_experiences)}")
        
        # Test agent step (thinking process)
        initial_satisfaction = test_agent.satisfaction_level
        test_agent.step()
        final_satisfaction = test_agent.satisfaction_level
        
        print(f"After step() call:")
        print(f"  - Satisfaction: {initial_satisfaction:.3f} → {final_satisfaction:.3f}")
        print(f"  - Primary channel: {test_agent.primary_channel}")
        print(f"  - Considering churn: {test_agent.considering_churn}")
        
        # Test data export
        export_data = test_agent.get_export_data()
        print(f"  - Export data keys: {list(export_data.keys())}")
        
        print("✅ Agent behavior test completed")
        return True
        
    except Exception as e:
        print(f"❌ Agent behavior test failed: {e}")
        traceback.print_exc()
        return False

def test_simulation_steps(model):
    """Test simulation execution"""
    print("\n" + "="*50)
    print("TESTING SIMULATION EXECUTION")
    print("="*50)
    
    if not model:
        print("❌ Cannot test simulation without valid model")
        return False
    
    try:
        initial_step = model.current_step
        print(f"Starting simulation from step {initial_step}")
        
        # Run simulation for configured steps
        step_results = []
        
        while model.running and model.current_step < model.time_steps:
            step_start = model.current_step
            
            # Execute one step
            model.step()
            
            # Collect metrics
            metrics = {
                'step': model.current_step,
                'agents': len(model.agents),
                'avg_satisfaction': model.get_average_satisfaction(),
                'churn_rate': model.calculate_churn_rate(),
                'active_products': model.count_active_products(),
                'digital_usage': model.get_digital_usage_rate()
            }
            
            step_results.append(metrics)
            
            print(f"Step {metrics['step']}: "
                  f"satisfaction={metrics['avg_satisfaction']:.3f}, "
                  f"churn={metrics['churn_rate']:.3f}, "
                  f"digital={metrics['digital_usage']:.3f}")
        
        print(f"✅ Simulation completed {len(step_results)} steps")
        print(f"   - Final satisfaction: {step_results[-1]['avg_satisfaction']:.3f}")
        print(f"   - Final churn rate: {step_results[-1]['churn_rate']:.3f}")
        
        return step_results
        
    except Exception as e:
        print(f"❌ Simulation execution failed: {e}")
        traceback.print_exc()
        return []

def test_data_collection(model):
    """Test data collection and export"""
    print("\n" + "="*50)
    print("TESTING DATA COLLECTION")
    print("="*50)
    
    if not model:
        print("❌ Cannot test data collection without valid model")
        return False
    
    try:
        # Test results summary
        results = model.get_results_summary()
        print("Results summary:")
        for key, value in results.items():
            print(f"  - {key}: {value}")
        
        # Test agent data export
        agent_data = model.export_agent_data()
        print(f"\nAgent data export:")
        print(f"  - Rows: {len(agent_data)}")
        print(f"  - Columns: {list(agent_data.columns) if len(agent_data) > 0 else 'No data'}")
        
        # Test historical data export
        historical_data = model.export_historical_data()
        print(f"\nHistorical data export:")
        print(f"  - Rows: {len(historical_data)}")
        print(f"  - Columns: {list(historical_data.columns) if len(historical_data) > 0 else 'No data'}")
        
        if len(historical_data) > 0:
            print("  - Sample data:")
            print(historical_data.head().to_string())
        
        print("✅ Data collection test completed")
        return True
        
    except Exception as e:
        print(f"❌ Data collection test failed: {e}")
        traceback.print_exc()
        return False

def test_event_system(model):
    """Test event system integration"""
    print("\n" + "="*50)
    print("TESTING EVENT SYSTEM")
    print("="*50)
    
    if not model:
        print("❌ Cannot test events without valid model")
        return False
    
    try:
        # Create a simple test event
        class TestEvent:
            def __init__(self, message):
                self.message = message
        
        # Register event handler
        def test_event_handler(event):
            print(f"  Handled event: {event.message}")
            return True
        
        model.register_event_handler('TestEvent', test_event_handler)
        
        # Inject test event
        test_event = TestEvent("Test event message")
        model.inject_event(test_event)
        
        print("Event injected, processing...")
        
        # Process events (this happens in model.step())
        model.process_pending_events()
        
        print("✅ Event system test completed")
        return True
        
    except Exception as e:
        print(f"❌ Event system test failed: {e}")
        traceback.print_exc()
        return False

def run_comprehensive_test():
    """Run all tests"""
    print("🚀 STARTING COMPREHENSIVE MESA 3.X TEST SUITE")
    print("="*60)
    
    test_results = {
        'mesa_basic': False,
        'model_creation': False,
        'agent_creation': False,
        'agent_behavior': False,
        'simulation_steps': False,
        'data_collection': False,
        'event_system': False
    }
    
    # Test 1: Mesa basic functionality
    test_results['mesa_basic'] = test_mesa_basic_functionality()
    
    # Test 2: Model creation
    model = test_model_creation()
    test_results['model_creation'] = model is not None
    
    # Test 3: Agent creation
    agents = test_agent_creation(model)
    test_results['agent_creation'] = len(agents) > 0
    
    # Test 4: Agent behavior
    test_results['agent_behavior'] = test_agent_behavior(agents)
    
    # Test 5: Simulation steps
    simulation_results = test_simulation_steps(model)
    test_results['simulation_steps'] = len(simulation_results) > 0
    
    # Test 6: Data collection
    test_results['data_collection'] = test_data_collection(model)
    
    # Test 7: Event system
    test_results['event_system'] = test_event_system(model)
    
    # Print final results
    print("\n" + "="*60)
    print("FINAL TEST RESULTS")
    print("="*60)
    
    passed = sum(test_results.values())
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print(f"\nOVERALL: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your Mesa 3.x setup is working perfectly!")
        print("\n🚀 Ready for Week 2: Retail & Corporate Agent Development")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the errors above.")
        return False

if __name__ == "__main__":
    try:
        success = run_comprehensive_test()
        
        if success:
            print("\n" + "="*60)
            print("NEXT STEPS:")
            print("1. ✅ Mesa 3.x setup is complete")
            print("2. 🔨 Ready to build RetailClientAgent (Week 2)")
            print("3. 🔨 Ready to build CorporateClientAgent (Week 2)")
            print("4. 🔗 Ready for team integration")
            print("="*60)
        else:
            print("\n❌ Some tests failed. Please fix the issues before proceeding.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        traceback.print_exc()