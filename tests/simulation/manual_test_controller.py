import sys
import os
import time

# Add the project root and src/simulation to the module search path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'src', 'simulation'))

# Import modules using the package-like structure
from src.simulation.Orchestrator import SimulationOrchestrator
from src.simulation.simulation_controller import SimulationController

# Initialize orchestrator and controller
config = {"test_mode": True}
orchestrator = SimulationOrchestrator(config)
orchestrator.initialize_simulation()  # Load mock agents
controller = SimulationController(orchestrator)

# Step 1: Start a 10-step simulation with visible progress
print("Starting 10-step simulation...")
controller.adjust_parameters({"max_steps": 10})  # Set max_steps to 10
controller.start(step_by_step=True, max_steps=10)  # Start with 10 steps

# Step 2: Pause at step 5 (handled in start method)
# No additional input needed here

# Step 3: Adjust max_steps to 20
print("Adjusting max_steps to 20...")
controller.adjust_parameters({"max_steps": 20})

# Step 4: Resume and check status
print("Resuming and checking status...")
controller.start(step_by_step=True)  # Resume with 20 steps from current_step
status = controller.get_status()
print(f"Current Status: {status}")

# Step 5: Stop the simulation
print("Stopping simulation...")
controller.stop()  # Should print stop time and reset
final_status = controller.get_status()
print(f"Final Status: {final_status}")

# After the simulation completes
results = orchestrator.collect_results()
print("\nSimulation Results:")
print(f"- Client Retention Rate: {results.get('client_retention_rate')}")
print(f"- Digital Adoption Increase: {results.get('digital_adoption_increase')}")
print(f"- Satisfaction Average: {results.get('satisfaction_avg')}")