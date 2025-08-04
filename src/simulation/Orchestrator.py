from .event_system import EventSystem
from .scenarios import ScenarioManager
import pandas as pd
import os
from datetime import datetime
import random
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimulationOrchestrator:
    def __init__(self, config):
        """Initialize the orchestrator with configuration and core components."""
        self.model = None  # Holds agent data (DataFrame)
        self.event_system = EventSystem()
        self.scenario_manager = ScenarioManager()
        self.config = config or {}  # Default to empty dict if None
        self.current_step = 0
        self.results = {}
        self.batch_size = 5000  # Batch size for processing large agent sets
        self.random_state = self.config.get("random_state", 42)


    def initialize_simulation(self, agent_data=None, n_agents=50000):
        """Initialize the simulation with agent data or generate mock data."""
        if agent_data is None:
            if os.path.exists("mock_agents_large.csv"):
                agent_data = pd.read_csv("mock_agents_large.csv")
                logger.info(f"Loaded {len(agent_data)} agents from mock_agents_large.csv at {datetime.now()}")
            else:
                agent_data = self._generate_mock_agents(n_agents)
                logger.info(f"Generated {len(agent_data)} mock agents at {datetime.now()}")
                agent_data.to_csv("mock_agents_large.csv", index=False)
        elif isinstance(agent_data, pd.DataFrame):
            logger.info(f"Initialized with {len(agent_data)} provided agents at {datetime.now()}")
        else:
            raise ValueError("agent_data must be a pandas DataFrame or None")
        # Add initial state columns if not present
        for col in ['satisfaction_level', 'status']:
            if col not in agent_data.columns:
                agent_data[col] = 0.0 if col == 'satisfaction_level' else 'active'
        self.model = agent_data
        self.current_step = 0

    def _generate_mock_agents(self, n=50000):
        """Generate mock agent data for testing with diverse attributes."""
        data = pd.DataFrame({
            'unique_id': range(n),
            'demographics': [f"{random.choice(['Tunis', 'Sfax', 'Sousse', 'Djerba'])}_{'Male' if i % 2 == 0 else 'Female'}" for i in range(n)],
            'channel_preference': [random.choice(['mobile', 'branch', 'web']) for _ in range(n)],
            'satisfaction_level': [random.uniform(0.3, 0.7) for _ in range(n)],
            'status': ['active' for _ in range(n)],
            'income_level': [random.choice(['low', 'medium', 'high']) for _ in range(n)],
            'transaction_frequency': [random.randint(1, 10) for _ in range(n)],
            'region': [random.choice(['Tunis', 'Sfax', 'Sousse', 'Djerba']) for _ in range(n)]
        })
        return data

    def run_simulation(self, scenario_name, steps):
        """Run the simulation for the specified scenario and number of steps."""
        if self.model is None:
            raise RuntimeError("Simulation not initialized. Call initialize_simulation first.")
        
        scenario = self.scenario_manager.load_scenario(scenario_name)
        if steps == 1:  # Single step mode for step-by-step execution
            processed_events = self.event_system.process_events(self.current_step)
            self._update_agent_states(processed_events)
            return {"steps_completed": 1}
        else:  # Full simulation mode
            logger.info(f"Starting simulation for {scenario_name} with {steps} steps at {datetime.now()}")
            self.results = {
                "scenario": scenario_name,
                "start_time": str(datetime.now()),
                "steps": [],
                "steps_completed": 0,
                "metrics": {}  # Cumulative metrics
            }

            # Pre-inject all scenario events
            for event in scenario.events:
                try:
                    base_event = event.to_base_event()
                    self.event_system.inject_event(base_event)
                except Exception as e:
                    logger.warning(f"Failed to inject event {event.event_type} at step 0: {e}")

            for step in range(steps):
                self.current_step = step + 1
                # Process events for this step
                processed_events = self.event_system.process_events(step)
                if processed_events:
                    step_metrics = self._update_agent_states(processed_events)
                    self.results["metrics"].update(step_metrics)
                    self.results["steps"].append({
                        "step": step + 1,
                        "events_processed": len(processed_events),
                        "active_agents": step_metrics["active_agents"],
                        "churned_agents": step_metrics["churned_agents"],
                        "satisfaction_avg": step_metrics["satisfaction_avg"],
                        "client_retention_rate": step_metrics["client_retention_rate"]
                    })
                else:
                    self.results["steps"].append({
                        "step": step + 1,
                        "events_processed": 0,
                        "active_agents": len(self.model[self.model['status'] == 'active']),
                        "churned_agents": 0,
                        "satisfaction_avg": self.model[self.model['status'] == 'active']['satisfaction_level'].mean(),
                        "client_retention_rate": 0.0
                    })
                self.results["steps_completed"] = step + 1

            self.results["end_time"] = str(datetime.now())
            logger.info(f"Simulation completed at {self.results['end_time']}")
            return self.results

    def _update_agent_states(self, processed_events):
        """Vectorized update of agent states based on processed events."""
        np.random.seed(self.random_state + self.current_step)
        if not processed_events:
            return {
                "churned_agents": 0, 
                "active_agents": len(self.model[self.model['status'] == 'active']),
                "satisfaction_avg": self.model['satisfaction_level'].mean(),
                "client_retention_rate": 0.0,
                "digital_adoption_increase": 0.0
            }
        mask = self.model['status'] == 'active'
        churned_count = 0
        retention_rate = 0.0
        adoption_increase = 0.0

        for event in processed_events:
            results = event.metadata.get("results", {})
            target_mask = mask.copy()

            if event.event_type == 'MarketingCampaignEvent':
                target_mask &= self.model['region'] == event.parameters.get('target_segment', '')
                retention_boost = results.get("client_retention_rate", 0.0)  # Use handler result
                satisfaction_boost = retention_boost * 0.5  # Convert retention to satisfaction impact
                self.model.loc[target_mask, 'satisfaction_level'] = np.minimum(
                    1.0, self.model.loc[target_mask, 'satisfaction_level'] + satisfaction_boost
                )
                retention_rate = max(retention_rate, retention_boost)  # Update cumulative retention
                churn_prob = 0.05
                churn_mask = target_mask & (self.model['satisfaction_level'] < 0.3)
                churned = np.random.random(len(self.model[churn_mask])) < churn_prob
                churned_count += np.sum(churned)
                self.model.loc[churn_mask, 'status'] = np.where(churned, 'churned', self.model.loc[churn_mask, 'status'])

            elif event.event_type == 'BranchClosureEvent':
                target_mask &= self.model['region'] == event.parameters.get('location', '')
                satisfaction_drop = -0.2
                self.model.loc[target_mask, 'satisfaction_level'] = np.maximum(
                    0.0, self.model.loc[target_mask, 'satisfaction_level'] + satisfaction_drop
                )
                churn_prob = 0.1
                churn_mask = target_mask & (self.model['satisfaction_level'] < 0.3)
                churned = np.random.random(len(self.model[churn_mask])) < churn_prob
                churned_count += np.sum(churned)
                self.model.loc[churn_mask, 'status'] = np.where(churned, 'churned', self.model.loc[churn_mask, 'status'])

            elif event.event_type == 'DigitalTransformationEvent':
                adoption_boost = results.get("digital_adoption_increase", 0.0)
                self.model.loc[target_mask, 'satisfaction_level'] = np.minimum(
                    1.0, self.model.loc[target_mask, 'satisfaction_level'] + adoption_boost * 0.3
                )
                adoption_increase = max(adoption_increase, adoption_boost)

            elif event.event_type == 'CompetitorActionEvent':
                target_mask &= self.model['region'] == event.parameters.get('affected_region', '')
                retention_effect = results.get("client_retention_rate", 1.0)
                satisfaction_drop = - (1.0 - retention_effect) * 0.4
                self.model.loc[target_mask, 'satisfaction_level'] = np.maximum(
                    0.0, self.model.loc[target_mask, 'satisfaction_level'] + satisfaction_drop
                )
                churn_prob = 0.08
                churn_mask = target_mask & (self.model['satisfaction_level'] < 0.3)
                churned = np.random.random(len(self.model[churn_mask])) < churn_prob
                churned_count += np.sum(churned)
                self.model.loc[churn_mask, 'status'] = np.where(churned, 'churned', self.model.loc[churn_mask, 'status'])

            elif event.event_type == 'EconomicShockEvent':
                target_mask &= self.model['income_level'].isin(['low', 'medium'])
                satisfaction_drop = -event.parameters.get('severity', 0.0) * 0.3
                self.model.loc[target_mask, 'satisfaction_level'] = np.maximum(
                    0.0, self.model.loc[target_mask, 'satisfaction_level'] + satisfaction_drop
                )
                churn_prob = 0.07
                churn_mask = target_mask & (self.model['satisfaction_level'] < 0.3)
                churned = np.random.random(len(self.model[churn_mask])) < churn_prob
                churned_count += np.sum(churned)
                self.model.loc[churn_mask, 'status'] = np.where(churned, 'churned', self.model.loc[churn_mask, 'status'])

            elif event.event_type == 'RegulatoryChangeEvent':
                target_mask &= mask
                satisfaction_drop = -event.parameters.get('impact_severity', 0.0) * 0.2
                self.model.loc[target_mask, 'satisfaction_level'] = np.maximum(
                    0.0, self.model.loc[target_mask, 'satisfaction_level'] + satisfaction_drop
                )

            elif event.event_type == 'ProductLaunchEvent':
                target_mask &= self.model['region'].isin(event.parameters.get('launch_governorates', []))
                self.model.loc[target_mask, 'satisfaction_level'] = np.minimum(
                    1.0, self.model.loc[target_mask, 'satisfaction_level'] + 0.15
                )

        active_count = len(self.model[self.model['status'] == 'active'])
        return {
            "churned_agents": churned_count,
            "active_agents": active_count,
            "satisfaction_avg": self.model[mask]['satisfaction_level'].mean(),
            "client_retention_rate": retention_rate,
            "digital_adoption_increase": adoption_increase
        }

    def collect_results(self):
        """Collect and return detailed simulation results with all required metrics."""
        if self.model is None:
            return {"status": "no simulation run", "timestamp": str(datetime.now())}
        
        # Initialize metric aggregators
        retention_rates = []
        adoption_increases = []
        satisfaction_values = []
        
        # Process detailed steps to collect metrics
        for step in self.results.get("steps", []):
            if step.get('client_retention_rate', 0) > 0:
                retention_rates.append(step['client_retention_rate'])
            if step.get('digital_adoption_increase', 0) > 0:
                adoption_increases.append(step['digital_adoption_increase'])
            if 'satisfaction_avg' in step:
                satisfaction_values.append(step['satisfaction_avg'])
        
        # Calculate averages
        avg_retention = sum(retention_rates)/len(retention_rates) if retention_rates else 0.0
        avg_adoption = sum(adoption_increases)/len(adoption_increases) if adoption_increases else 0.0
        avg_satisfaction = sum(satisfaction_values)/len(satisfaction_values) if satisfaction_values else 0.0
        
        # Get current active agents' satisfaction
        current_satisfaction = self.model['satisfaction_level'].mean()
        
        return {
            "agent_count": len(self.model),
            "status": "completed",
            "timestamp": str(datetime.now()),
            "avg_satisfaction": current_satisfaction,  # Current overall satisfaction
            "satisfaction_avg": avg_satisfaction,      # Average across all steps
            "active_agents": len(self.model[self.model['status'] == 'active']),
            "churned_agents": len(self.model[self.model['status'] == 'churned']),
            "channel_breakdown": self.model['channel_preference'].value_counts().to_dict(),
            "detailed_steps": self.results.get("steps", []),
            "client_retention_rate": avg_retention,
            "digital_adoption_increase": avg_adoption
        }

    def save_results(self, filename="simulation_results.json"):
        """Save results to a JSON file."""
        import json
        if self.results:
            with open(filename, 'w') as f:
                json.dump(self.collect_results(), f, indent=4)
            logger.info(f"Results saved to {filename} at {datetime.now()}")
        else:
            logger.info("No results to save.")