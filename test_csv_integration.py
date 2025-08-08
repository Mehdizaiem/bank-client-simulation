#!/usr/bin/env python3
"""Test script to verify CSV data loading and agent creation"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.agent_engine.data_loader import AgentDataLoader
from src.agent_engine.mesa_setup import BankSimulationModel
from src.agent_engine.retail_agent import RetailClientAgent
from src.agent_engine.corporate_agent import CorporateClientAgent

def test_csv_loading():
    """Test loading data from CSV files"""
    print("Testing CSV data loading...")
    
    loader = AgentDataLoader()
    
    # Test retail data
    retail_agents = loader.load_retail_agents()
    print(f"✅ Loaded {len(retail_agents)} retail agents")
    if retail_agents:
        print(f"   Sample: {retail_agents[0]['client_id']}, "
              f"age={retail_agents[0]['age']}, "
              f"governorate={retail_agents[0]['governorate']}")
    
    # Test corporate data
    corporate_agents = loader.load_corporate_agents()
    print(f"✅ Loaded {len(corporate_agents)} corporate agents")
    if corporate_agents:
        print(f"   Sample: {corporate_agents[0]['client_id']}, "
              f"company={corporate_agents[0]['company_name']}, "
              f"sector={corporate_agents[0]['business_sector']}")
    
    # Test statistics
    stats = loader.get_statistics()
    print(f"✅ Statistics computed successfully")
    
    return loader

def test_simulation_with_csv():
    """Test full simulation with CSV data"""
    print("\nTesting simulation with CSV data...")
    
    config = {
        'num_agents': 100,  # Will load first 100 from CSVs
        'retail_ratio': 0.8,
        'time_steps': 10,
        'random_seed': 42
    }
    
    model = BankSimulationModel(config)
    print(f"✅ Model created with {len(model.agents)} agents")
    
    # Run a few steps
    for i in range(5):
        model.step()
        print(f"   Step {i+1}: satisfaction={model.get_average_satisfaction():.3f}")
    
    # Export some data
    agent_data = model.export_agent_data()
    print(f"✅ Exported data for {len(agent_data)} agents")
    
    # Check that we have both types
    if len(agent_data) > 0:
        retail_count = len(agent_data[agent_data['client_type'] == 'retail'])
        corporate_count = len(agent_data[agent_data['client_type'] == 'corporate'])
        print(f"   Retail: {retail_count}, Corporate: {corporate_count}")
    
    return model

if __name__ == "__main__":
    print("🚀 TESTING CSV DATA INTEGRATION")
    print("="*50)
    
    # Test data loading
    loader = test_csv_loading()
    
    # Test simulation
    model = test_simulation_with_csv()
    
    print("\n✅ CSV integration complete!")
    print("Your agents are now using real data from the CSV files!")