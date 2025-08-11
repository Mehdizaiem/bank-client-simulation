import datetime
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimulationController:
    def __init__(self, orchestrator):
        """Initialize controller with an orchestrator instance."""
        self.orchestrator = orchestrator
        self.running = False
        self.paused = False
        self.current_step = 0
        self.max_steps = 100
        self.speed_factor = 1.0

    def start(self, step_by_step=False, max_steps=None):
        if not self.running:
            self.running = True
            self.paused = False
            logger.info(f"Simulation started at {datetime.datetime.now()} with speed factor {self.speed_factor}")
            if max_steps is not None:
                self.max_steps = max_steps
            steps = self.max_steps if self.max_steps > 0 else 10
            if step_by_step:
                for step in range(self.current_step, steps):
                    if self.paused:
                        break
                    self.current_step = step + 1
                    self.orchestrator.run_simulation("advanced/multi_region_campaign_scenario.json", 1)
                    time.sleep(1 / self.speed_factor)
                    logger.info(f"Processed step {self.current_step}")
                    if step + 1 == 5:
                        input("Step 5 reached - press Enter to pause...")
                        self.pause()
            else:
                self.orchestrator.run_simulation("advanced/multi_region_campaign_scenario.json", steps)
                self.current_step = steps
                # Do not set running = False here; let stop() or pause() handle it
            # self.running = False  # Comment out or remove this line
        else:
            logger.info("Simulation is already running.")

    def pause(self):
        """Pause the simulation mid-execution."""
        if self.running and not self.paused:
            self.paused = True
            self.running = False
            logger.info(f"Simulation paused at step {self.current_step} at {datetime.datetime.now()}")
        else:
            logger.info("Simulation is not running or already paused.")

    def stop(self):
        """Stop the simulation and reset."""
        if self.running or self.current_step > 0:
            self.running = False
            self.paused = False
            self.current_step = 0
            logger.info(f"Simulation stopped at {datetime.datetime.now()}")
            self.orchestrator.model = None
        else:
            logger.info("No simulation to stop.")

    def adjust_parameters(self, params):
        """Adjust simulation parameters dynamically."""
        if not self.running:
            for key, value in params.items():
                if key == "max_steps" and isinstance(value, int) and value > 0:
                    self.max_steps = value
                    logger.info(f"Max steps updated to {value}")
                elif key == "speed_factor" and isinstance(value, (int, float)) and value > 0:
                    self.speed_factor = value
                    logger.info(f"Speed factor updated to {value}")
                elif key == "batch_size" and isinstance(value, int) and value > 0:
                    self.orchestrator.batch_size = value
                    logger.info(f"Batch size updated to {value}")
                else:
                    logger.info(f"Invalid parameter {key} or value {value}")
        else:
            logger.info("Cannot adjust parameters while simulation is running.")

    def get_status(self):
        """Return current simulation status."""
        return {
            "running": self.running,
            "current_step": self.current_step,
            "max_steps": self.max_steps,
            "speed_factor": self.speed_factor,
            "batch_size": self.orchestrator.batch_size,
            "timestamp": str(datetime.datetime.now())
        }