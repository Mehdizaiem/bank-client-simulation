# src/simulation/simulation_controller.py
import datetime  # Ensure this is at the top

class SimulationController:
    def __init__(self, orchestrator):
        """Initialize controller with an orchestrator instance."""
        self.orchestrator = orchestrator
        self.running = False
        self.current_step = 0
        self.max_steps = 100  # Default max steps
        self.speed_factor = 1.0  # Simulation speed multiplier

    def start(self):
        """Start the simulation with configurable steps."""
        if not self.running:
            self.running = True
            print(f"Simulation started at {datetime.datetime.now()} with speed factor {self.speed_factor}")
            try:
                steps = self.max_steps if self.max_steps > 0 else 10
                self.orchestrator.run_simulation("advanced/multi_region_campaign_scenario.json", steps)  # Relative path
                self.current_step = steps
            except Exception as e:
                print(f"Simulation failed: {e}")
                self.running = False
        else:
            print("Simulation is already running.")

    def pause(self):
        """Pause the simulation."""
        if self.running:
            self.running = False
            print(f"Simulation paused at step {self.current_step} at {datetime.datetime.now()}")
        else:
            print("Simulation is not running.")

    def stop(self):
        """Stop the simulation and reset."""
        if self.running or self.current_step > 0:
            self.running = False
            self.current_step = 0
            print(f"Simulation stopped at {datetime.datetime.now()}")
            self.orchestrator.model = None  # Reset model
        else:
            print("No simulation to stop.")

    def adjust_parameters(self, params):
        """Adjust simulation parameters dynamically."""
        if not self.running:
            for key, value in params.items():
                if key == "max_steps" and isinstance(value, int) and value > 0:
                    self.max_steps = value
                    print(f"Max steps updated to {value}")
                elif key == "speed_factor" and isinstance(value, (int, float)) and value > 0:
                    self.speed_factor = value
                    print(f"Speed factor updated to {value}")
                else:
                    print(f"Invalid parameter {key} or value {value}")
        else:
            print("Cannot adjust parameters while simulation is running.")

    def get_status(self):
        """Return current simulation status."""
        return {
            "running": self.running,
            "current_step": self.current_step,
            "max_steps": self.max_steps,
            "speed_factor": self.speed_factor,
            "timestamp": str(datetime.datetime.now())
        }