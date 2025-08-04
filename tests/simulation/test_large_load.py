import sys
import os
import time

# Set the absolute path to the project root
project_root = r"C:\Users\asus\Documents\4DS1\Summer Internship\bank-client-simulation-project\bank-client-simulation"
sys.path.append(project_root)

from src.simulation.Orchestrator import SimulationOrchestrator

config = {"test_mode": True}
orchestrator = SimulationOrchestrator(config)
start_time = time.time()
orchestrator.initialize_simulation(n_agents=50000)
end_time = time.time()
print(f"Loaded {len(orchestrator.model)} agents in {end_time - start_time:.2f} seconds")