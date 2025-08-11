"""
Scenario Manager for Bank Client Simulation
Author: Maryem - Simulation Interface Lead
Week: 2 - Scenario Management & Templates
"""

import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import pandas as pd
from .event_system import EventSystem
from .scenarios import Scenario, ScenarioManager as BaseScenarioManager

logger = logging.getLogger(__name__)

class ScenarioManager(BaseScenarioManager):
    """Extended Scenario Manager with execution and reporting capabilities"""

    def __init__(self, template_directory: str = "configs/scenario_templates"):
        super().__init__(template_directory)
        self.event_system = EventSystem()
        self.execution_results: Dict[str, Dict[str, Any]] = {}
    
    def run_full_simulation(self, scenario: Scenario, output_dir: str = "simulation_outputs") -> Dict[str, Any]:
        """
        Run a full simulation for a scenario
        
        Args:
            scenario: Scenario object to execute
            output_dir: Directory to save simulation outputs
            
        Returns:
            Dict with simulation results
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Starting full simulation for scenario: {scenario.metadata.name}")
        
        # Initialize results
        results = {
            "scenario_name": scenario.metadata.name,
            "start_time": datetime.now().isoformat(),
            "steps_completed": 0,
            "events_processed": 0,
            "validation_results": [],
            "metrics": {}
        }
        
        # Inject scenario events
        execution_summary = self.execute_scenario(scenario, self.event_system)
        results["events_injected"] = execution_summary["events_injected"]
        results["events_failed"] = execution_summary["events_failed"]
        
        # Execute all steps
        for step in range(scenario.simulation_parameters.duration_steps + 1):
            processed_events = self.event_system.process_events(step)
            results["events_processed"] += len(processed_events)
            results["steps_completed"] = step
            
            # Collect metrics at output frequency
            if step % scenario.simulation_parameters.output_frequency == 0:
                self._collect_metrics(scenario, step, results["metrics"])
        
        # Validate outcomes
        results["validation_results"] = self._validate_outcomes(scenario, results["metrics"])
        
        # Save results
        results_file = output_path / f"{scenario.metadata.name.lower().replace(' ', '_')}_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Save event history
        event_history_file = output_path / f"{scenario.metadata.name.lower().replace(' ', '_')}_event_history.json"
        self.event_system.export_event_history(str(event_history_file))
        
        self.execution_results[scenario.metadata.name] = results
        logger.info(f"Simulation completed for {scenario.metadata.name}. Results saved to {results_file}")
        
        return results
    
    def _collect_metrics(self, scenario: Scenario, step: int, metrics: Dict[str, Any]):
        """Collect metrics during simulation (placeholder for integration with other components)"""
        # This is a placeholder - actual metric collection would integrate with agent system
        for metric in scenario.key_metrics:
            if metric not in metrics:
                metrics[metric] = []
            # Simulate metric collection (replace with real data in Week 3)
            metrics[metric].append({
                "step": step,
                "value": 0.0  # Placeholder value
            })
    
    def _validate_outcomes(self, scenario: Scenario, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Validate scenario outcomes against expected results"""
        validation_results = []
        
        for outcome in scenario.expected_outcomes:
            metric_values = metrics.get(outcome.metric_name, [])
            step_results = []
            
            for step in outcome.measurement_steps:
                # Find metric value for the step (placeholder logic)
                value = next((m["value"] for m in metric_values if m["step"] == step), None)
                if value is not None:
                    valid = outcome.validate_outcome(value, step)
                    step_results.append({
                        "step": step,
                        "metric_name": outcome.metric_name,
                        "actual_value": value,
                        "target_value": outcome.target_value,
                        "valid": valid
                    })
                else:
                    step_results.append({
                        "step": step,
                        "metric_name": outcome.metric_name,
                        "actual_value": None,
                        "target_value": outcome.target_value,
                        "valid": False,
                        "error": "Metric not collected for step"
                    })
            
            validation_results.append({
                "metric_name": outcome.metric_name,
                "results": step_results
            })
        
        return validation_results
    
    def generate_report(self, scenario_name: str, output_format: str = "json") -> str:
        """
        Generate a report for a scenario's execution
        
        Args:
            scenario_name: Name of the scenario
            output_format: Format of the report (json, csv, or markdown)
            
        Returns:
            Path to the generated report
        """
        if scenario_name not in self.execution_results:
            raise ValueError(f"No execution results found for scenario: {scenario_name}")
        
        results = self.execution_results[scenario_name]
        output_path = Path("simulation_outputs") / f"{scenario_name.lower().replace(' ', '_')}_report.{output_format}"
        
        if output_format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        
        elif output_format == "csv":
            # Convert validation results to DataFrame
            rows = []
            for validation in results["validation_results"]:
                for result in validation["results"]:
                    rows.append({
                        "scenario_name": scenario_name,
                        "metric_name": validation["metric_name"],
                        "step": result["step"],
                        "actual_value": result["actual_value"],
                        "target_value": result["target_value"],
                        "valid": result["valid"],
                        "error": result.get("error", "")
                    })
            df = pd.DataFrame(rows)
            df.to_csv(output_path, index=False)
        
        elif output_format == "markdown":
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# Simulation Report: {scenario_name}\n\n")
                f.write(f"**Start Time**: {results['start_time']}\n")
                f.write(f"**Steps Completed**: {results['steps_completed']}\n")
                f.write(f"**Events Processed**: {results['events_processed']}\n\n")
                f.write("## Validation Results\n")
                for validation in results["validation_results"]:
                    f.write(f"### {validation['metric_name']}\n")
                    for result in validation["results"]:
                        f.write(f"- Step {result['step']}: Actual={result['actual_value']}, "
                                f"Target={result['target_value']}, Valid={result['valid']}")
                        if "error" in result:
                            f.write(f", Error={result['error']}")
                        f.write("\n")
        
        logger.info(f"Report generated: {output_path}")
        return str(output_path)
    
    def compare_scenarios(self, scenario_names: List[str]) -> Dict[str, Any]:
        """
        Compare multiple scenarios' execution results
        
        Args:
            scenario_names: List of scenario names to compare
            
        Returns:
            Dict with comparison results
        """
        comparison = {
            "scenarios": [],
            "metrics_comparison": {}
        }
        
        for name in scenario_names:
            if name not in self.execution_results:
                logger.warning(f"No results for scenario: {name}")
                continue
            
            results = self.execution_results[name]
            comparison["scenarios"].append({
                "name": name,
                "events_processed": results["events_processed"],
                "steps_completed": results["steps_completed"],
                "validation_summary": {
                    "valid_outcomes": sum(
                        sum(1 for r in v["results"] if r["valid"])
                        for v in results["validation_results"]
                    ),
                    "total_outcomes": sum(
                        len(v["results"])
                        for v in results["validation_results"]
                    )
                }
            })
            
            for validation in results["validation_results"]:
                metric = validation["metric_name"]
                if metric not in comparison["metrics_comparison"]:
                    comparison["metrics_comparison"][metric] = []
                for result in validation["results"]:
                    comparison["metrics_comparison"][metric].append({
                        "scenario": name,
                        "step": result["step"],
                        "value": result["actual_value"],
                        "valid": result["valid"]
                    })
        
        return comparison