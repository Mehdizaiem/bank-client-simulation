# src/simulation/Orchestrator.py
from .event_system import EventSystem
from .scenarios import ScenarioManager
import pandas as pd
import os
from datetime import datetime
import random

class SimulationOrchestrator:
    def __init__(self, config):
        """Initialize the orchestrator with configuration and core components."""
        self.model = None  # Holds agent data (DataFrame)
        self.event_system = EventSystem()
        self.scenario_manager = ScenarioManager()
        self.config = config or {}  # Default to empty dict if None
        self.current_step = 0
        self.results = {}

    def initialize_simulation(self, agent_data=None):
        """Initialize the simulation with agent data or generate mock data."""
        if agent_data is None:
            if os.path.exists("mock_agents.csv"):
                agent_data = pd.read_csv("mock_agents.csv")
                print(f"Loaded {len(agent_data)} agents from mock_agents.csv at {datetime.now()}")
            else:
                agent_data = self._generate_mock_agents(1000)
                print(f"Generated {len(agent_data)} mock agents at {datetime.now()}")
                agent_data.to_csv("mock_agents.csv", index=False)
        elif isinstance(agent_data, pd.DataFrame):
            print(f"Initialized with {len(agent_data)} provided agents at {datetime.now()}")
        else:
            raise ValueError("agent_data must be a pandas DataFrame or None")
        # Add initial state columns if not present
        for col in ['satisfaction_level', 'status']:
            if col not in agent_data.columns:
                agent_data[col] = 0.0 if col == 'satisfaction_level' else 'active'
        self.model = agent_data
        self.current_step = 0

    def _generate_mock_agents(self, n=1000):
        """Generate mock agent data for testing."""
        data = pd.DataFrame({
            'unique_id': range(n),
            'demographics': [f"Tunis_{'Male' if i % 2 == 0 else 'Female'}" for i in range(n)],
            'channel_preference': ['mobile', 'branch', 'web'] * (n // 3) + ['mobile'] * (n % 3),
            'satisfaction_level': [0.5 for _ in range(n)],
            'status': ['active' for _ in range(n)]
        })
        return data

    def run_simulation(self, scenario_name, steps):
        """Run the simulation for the specified scenario and number of steps."""
        if self.model is None:
            raise RuntimeError("Simulation not initialized. Call initialize_simulation first.")
        
        scenario = self.scenario_manager.load_scenario(scenario_name)
        if steps == 1:  # Single step mode for step-by-step execution
            self.event_system.process_events(self.current_step)
            if 'MarketingCampaignEvent' in [e.type for e in self.event_system.event_queue]:
                self.model['satisfaction_level'] = self.model.apply(
                    lambda row: min(1.0, row['satisfaction_level'] + 0.1) if row['status'] == 'active' else row['satisfaction_level'],
                    axis=1
                )
                self.model['status'] = self.model.apply(
                    lambda row: 'churned' if row['satisfaction_level'] < 0.3 and random.random() < 0.05 else row['status'],
                    axis=1
                )
            return {"steps_completed": 1}
        else:  # Full simulation mode
            print(f"Starting simulation for {scenario_name} with {steps} steps at {datetime.now()}")
            self.results = {
                "scenario": scenario_name,
                "start_time": str(datetime.now()),
                "steps": [],
                "steps_completed": 0
            }

            for step in range(steps):
                self.current_step = step + 1
                self.event_system.process_events(step)

                if 'MarketingCampaignEvent' in [e.type for e in self.event_system.event_queue]:
                    self.model['satisfaction_level'] = self.model.apply(
                        lambda row: min(1.0, row['satisfaction_level'] + 0.1) if row['status'] == 'active' else row['satisfaction_level'],
                        axis=1
                    )
                    self.model['status'] = self.model.apply(
                        lambda row: 'churned' if row['satisfaction_level'] < 0.3 and random.random() < 0.05 else row['status'],
                        axis=1
                    )

                self.results["steps"].append({
                    "step": step + 1,
                    "events_processed": len(self.event_system.event_queue),
                    "active_agents": len(self.model[self.model['status'] == 'active'])
                })

                self.results["steps_completed"] = step + 1

            self.results["end_time"] = str(datetime.now())
            print(f"Simulation completed at {self.results['end_time']}")
            return self.results

    def collect_results(self):
        """Collect and return detailed simulation results."""
        if self.model is None:
            return {"status": "no simulation run", "timestamp": str(datetime.now())}
        return {
            "agent_count": len(self.model),
            "status": "completed",
            "timestamp": str(datetime.now()),
            "avg_satisfaction": self.model['satisfaction_level'].mean(),
            "active_agents": len(self.model[self.model['status'] == 'active']),
            "churned_agents": len(self.model[self.model['status'] == 'churned']),
            "channel_breakdown": self.model['channel_preference'].value_counts().to_dict(),
            "detailed_steps": self.results.get("steps", [])
        }

    def save_results(self, filename="simulation_results.json"):
        """Save results to a JSON file."""
        import json
        if self.results:
            with open(filename, 'w') as f:
                json.dump(self.collect_results(), f, indent=4)
            print(f"Results saved to {filename} at {datetime.now()}")
        else:
            print("No results to save.")