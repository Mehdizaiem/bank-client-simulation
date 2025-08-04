import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # Add project root to path

import unittest
import pandas as pd
from src.simulation.Orchestrator import SimulationOrchestrator
from src.simulation.simulation_controller import SimulationController

class TestOrchestration(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test."""
        self.config = {"test_mode": True}
        self.orchestrator = SimulationOrchestrator(self.config)
        self.orchestrator.initialize_simulation(n_agents=50000)  # Upscale to 50,000 agents
        self.controller = SimulationController(self.orchestrator)

    def test_initialization_with_mock_data(self):
        """Test initialization with automatically generated mock data."""
        self.orchestrator.initialize_simulation(n_agents=50000)
        self.assertIsNotNone(self.orchestrator.model)
        self.assertEqual(len(self.orchestrator.model), 50000)
        self.assertIn('satisfaction_level', self.orchestrator.model.columns)
        self.assertIn('status', self.orchestrator.model.columns)

    def test_initialization_with_custom_data(self):
        """Test initialization with custom DataFrame."""
        custom_data = pd.DataFrame({
            'unique_id': [1, 2, 3],
            'demographics': ['Tunis_Male', 'Tunis_Female', 'Sfax_Male'],
            'channel_preference': ['mobile', 'branch', 'web']
        })
        self.orchestrator.initialize_simulation(custom_data)
        self.assertEqual(len(self.orchestrator.model), 3)
        self.assertTrue(all(col in self.orchestrator.model.columns for col in ['satisfaction_level', 'status']))

    def test_run_simulation(self):
        """Test running a simulation with a simple scenario."""
        self.orchestrator.initialize_simulation(n_agents=50000)
        results = self.orchestrator.run_simulation("branch_closure_scenario.json", 30)  # Simple scenario
        self.assertEqual(results["steps_completed"], 30)
        self.assertGreater(len(results["steps"]), 0)
        self.assertIn("end_time", results)

    def test_control_interface(self):
        """Test the full control interface functionality."""
        self.controller.start()
        self.assertTrue(self.controller.running)
        self.assertGreater(self.controller.current_step, 0)
        self.controller.pause()
        self.assertFalse(self.controller.running)
        self.controller.stop()
        self.assertEqual(self.controller.current_step, 0)
        self.assertIsNone(self.orchestrator.model)

    def test_adjust_parameters(self):
        """Test parameter adjustment functionality."""
        self.controller.adjust_parameters({"max_steps": 50, "speed_factor": 2.0, "batch_size": 10000})
        self.assertEqual(self.controller.max_steps, 50)
        self.assertEqual(self.controller.speed_factor, 2.0)
        self.assertEqual(self.orchestrator.batch_size, 10000)
        self.controller.adjust_parameters({"invalid_key": 10})  # Should ignore invalid key
        self.assertEqual(self.orchestrator.batch_size, 10000)

    def test_collect_results(self):
        """Test result collection after simulation."""
        self.orchestrator.initialize_simulation(n_agents=50000)
        results = self.orchestrator.run_simulation("branch_closure_scenario.json", 30)
        results = self.orchestrator.collect_results()  # Ensure collect_results returns the latest results
        self.assertIn("avg_satisfaction", results)
        self.assertIn("active_agents", results)
        self.assertIn("churned_agents", results)
        self.assertIn("channel_breakdown", results)
        self.assertIn("client_retention_rate", results)
        self.assertIn("digital_adoption_increase", results)
        self.assertIn("satisfaction_avg", results)
        scenario = self.orchestrator.scenario_manager.get_scenario_by_name("Branch Closure Impact Analysis")
        for outcome in scenario.expected_outcomes:
            if outcome.measurement_steps and 30 in outcome.measurement_steps:
                actual_value = results.get(outcome.metric_name, 0.0)
                self.assertTrue(outcome.validate_outcome(actual_value, 30), f"Validation failed for {outcome.metric_name}")

    def tearDown(self):
        """Clean up after each test."""
        self.orchestrator.model = None
        self.controller.running = False
        self.controller.current_step = 0

if __name__ == "__main__":
    unittest.main()