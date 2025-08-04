import sys
import os
import time

# Set the absolute path to the project root
project_root = r"C:\Users\asus\Documents\4DS1\Summer Internship\bank-client-simulation-project\bank-client-simulation"
sys.path.append(project_root)

from src.simulation.Orchestrator import SimulationOrchestrator

# Configuration
config = {"test_mode": True}
orchestrator = SimulationOrchestrator(config)

# Start simulation
start_time = time.time()
orchestrator.initialize_simulation(n_agents=50000)  # Upscale to 50,000 agents
orchestrator.run_simulation("configs/scenario_templates/advanced/multi_region_campaign_scenario.json", 180)  # Longest scenario
end_time = time.time()

# Output results
print(f"Loaded {len(orchestrator.model)} agents and ran 180 steps in {end_time - start_time:.2f} seconds")
orchestrator.save_results("multi_region_results.json")

# Optional: Adjust batch size if needed
# from src.simulation.simulation_controller import SimulationController
# controller = SimulationController(orchestrator)
# controller.adjust_parameters({"batch_size": 10000})