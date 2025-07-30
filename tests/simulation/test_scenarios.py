"""
Test suite for Scenario Management System
Author: Maryem - Simulation Interface Lead
Week: 2 - Scenario Management & Templates
"""

import unittest
import sys
import os
from datetime import datetime
from pathlib import Path
import json

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from simulation.scenario_manager import ScenarioManager
from simulation.scenarios import Scenario, ScenarioMetadata, SimulationParameters, ScenarioEvent, ExpectedOutcome
from simulation.event_system import EventSystem
from simulation.event_types import MarketingCampaignEvent

class TestScenarioManagement(unittest.TestCase):
    """Test cases for Scenario and ScenarioManager classes"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scenario_manager = ScenarioManager()
        self.event_system = EventSystem()
        
        # Register dummy handler for MarketingCampaignEvent using the correct method
        def dummy_marketing_handler(event: MarketingCampaignEvent):
            pass
        self.event_system.register_event_handler("MarketingCampaignEvent", dummy_marketing_handler)
        
        # Sample scenario data
        self.metadata = ScenarioMetadata(
            name="Test Scenario",
            description="Test scenario for validation",
            tags=["test", "validation"]
        )
        self.parameters = SimulationParameters(
            duration_steps=50,
            warm_up_steps=5,
            agent_population=500
        )
        self.events = [
            ScenarioEvent(
                event_type="MarketingCampaignEvent",
                step=10,
                parameters={
                    "target_segment": "test_segment",
                    "campaign_type": "test_campaign",
                    "intensity": 0.5,
                    "budget": 10000
                }
            )
        ]
        self.outcomes = [
            ExpectedOutcome(
                metric_name="test_metric",
                target_value=0.5,
                tolerance=0.1,
                measurement_steps=[20, 40],
                comparison_type="greater_than"
            )
        ]
        
        self.scenario = Scenario(
            metadata=self.metadata,
            simulation_parameters=self.parameters,
            events=self.events,
            expected_outcomes=self.outcomes,
            key_metrics=["test_metric"],
            risk_factors=[{"risk": "test_risk", "probability": 0.3, "impact": "low"}]
        )
    
    def test_scenario_initialization(self):
        """Test Scenario object initialization"""
        self.assertEqual(self.scenario.metadata.name, "Test Scenario")
        self.assertEqual(len(self.scenario.events), 1)
        self.assertEqual(len(self.scenario.expected_outcomes), 1)
        self.assertEqual(self.scenario.simulation_parameters.duration_steps, 50)
    
    def test_scenario_validation(self):
        """Test scenario validation"""
        validation = self.scenario._validate_scenario()
        self.assertIsNone(validation)  # No return value, raises exception on failure
        
        # Test invalid scenario (event step exceeds duration)
        invalid_event = ScenarioEvent(
            event_type="MarketingCampaignEvent",
            step=100,
            parameters={"target_segment": "test"}
        )
        invalid_scenario = Scenario(
            metadata=self.metadata,
            simulation_parameters=self.parameters,
            events=[invalid_event]
        )
        with self.assertLogs(level='WARNING') as log:
            invalid_scenario._validate_scenario()
            self.assertIn("exceeds simulation duration", log.output[0])
    
    def test_scenario_manager_load(self):
        """Test loading scenario from JSON"""
        # Create temporary JSON file with absolute path
        temp_file = Path(__file__).parents[2] / "configs" / "scenario_templates" / "test_scenario.json"
        self.scenario.export_to_json(temp_file)
        print(f"Debug: Created temp file at: {temp_file}")
        
        loaded_scenario = self.scenario_manager.load_scenario(Path("test_scenario.json"))
        self.assertEqual(loaded_scenario.metadata.name, "Test Scenario")
        self.assertEqual(len(loaded_scenario.events), 1)
        
        # Clean up
        temp_file.unlink()
    
    def test_scenario_execution(self):
        """Test scenario execution"""
        execution_summary = self.scenario_manager.execute_scenario(self.scenario, self.event_system)
        self.assertEqual(execution_summary["events_injected"], 1)
        self.assertEqual(execution_summary["events_failed"], 0)
        self.assertEqual(execution_summary["scenario_name"], "Test Scenario")
    
    def test_scenario_manager_validation(self):
        """Test scenario manager validation"""
        validation = self.scenario_manager.validate_scenario(self.scenario)
        self.assertTrue(validation["valid"])
        self.assertEqual(len(validation["issues"]), 0)
        self.assertEqual(validation["event_count"], 1)
    
    def test_full_simulation(self):
        """Test full simulation run"""
        results = self.scenario_manager.run_full_simulation(self.scenario)
        self.assertEqual(results["scenario_name"], "Test Scenario")
        self.assertEqual(results["steps_completed"], 50)
        self.assertEqual(results["events_injected"], 1)
        self.assertEqual(results["events_processed"], 1)
        self.assertEqual(results["events_failed"], 0)
        self.assertTrue(Path("simulation_outputs/test_scenario_results.json").exists())
        self.assertTrue(Path("simulation_outputs/test_scenario_event_history.json").exists())

    def test_advanced_scenario_load(self):
        """Test loading advanced scenario from JSON"""
        project_root = Path(__file__).parents[2]  # Up from tests/simulation/ to project root
        advanced_scenario_path = project_root / "configs" / "scenario_templates" / "advanced" / "multi_region_campaign_scenario.json"
        print(f"Debug: Checking path: {advanced_scenario_path}")
        self.assertTrue(advanced_scenario_path.exists(), f"Advanced scenario file missing: {advanced_scenario_path}")
        
        # Use the relative path as intended
        loaded_scenario = self.scenario_manager.load_scenario(Path("advanced/multi_region_campaign_scenario.json"))
        self.assertEqual(loaded_scenario.metadata.name, "Multi-Region Digital Campaign")
        self.assertEqual(len(loaded_scenario.events), 6)
        self.assertEqual(len(loaded_scenario.expected_outcomes), 3)
        self.assertEqual(loaded_scenario.simulation_parameters.duration_steps, 180)

if __name__ == "__main__":
    unittest.main(verbosity=2)