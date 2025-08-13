"""
Scenario Management System
Author: Maryem - Simulation Interface Lead
Week: 2 - Scenario Management & Templates
"""

import json
import os
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import jsonschema
from pathlib import Path
import logging

from .event_system import EventSystem, BaseEvent
from .event_types import create_event

logger = logging.getLogger(__name__)

@dataclass
class ScenarioMetadata:
    """Metadata for simulation scenarios"""
    name: str
    description: str
    version: str = "1.0"
    author: str = ""
    created_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    tags: List[str] = field(default_factory=list)
    difficulty_level: str = "medium"  # easy, medium, hard, expert
    estimated_duration: int = 100  # simulation steps
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "created_date": self.created_date,
            "tags": self.tags,
            "difficulty_level": self.difficulty_level,
            "estimated_duration": self.estimated_duration
        }

@dataclass
class SimulationParameters:
    """Parameters for simulation execution"""
    duration_steps: int = 100
    warm_up_steps: int = 10
    agent_population: int = 1000
    random_seed: Optional[int] = None
    output_frequency: int = 5
    save_intermediate_results: bool = True
    enable_real_time_visualization: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "duration_steps": self.duration_steps,
            "warm_up_steps": self.warm_up_steps,
            "agent_population": self.agent_population,
            "random_seed": self.random_seed,
            "output_frequency": self.output_frequency,
            "save_intermediate_results": self.save_intermediate_results,
            "enable_real_time_visualization": self.enable_real_time_visualization
        }

@dataclass
class ScenarioEvent:
    """Individual event within a scenario - ENHANCED"""
    
    def __init__(self, event_type: str, step: int, parameters: Dict[str, Any], 
                 event_id: Optional[str] = None, description: Optional[str] = None):
        self.event_type = event_type
        self.step = step
        self.parameters = parameters
        self.event_id = event_id
        self.description = description
    
    def to_base_event(self) -> BaseEvent:
        """Convert to BaseEvent for execution - ENHANCED"""
        try:
            # Use the enhanced create_event function
            return create_event(self.event_type, step=self.step, **self.parameters)
        except Exception as e:
            # Fallback: create basic event with all parameters in extra_params
            from .event_system import BaseEvent
            
            @dataclass
            class GenericEvent(BaseEvent):
                extra_params: Dict[str, Any] = field(default_factory=dict)
                
                def __post_init__(self):
                    super().__post_init__()
                    self.parameters = self.extra_params
            
            return GenericEvent(
                event_type=self.event_type,
                step=self.step,
                extra_params=self.parameters
            )

@dataclass
class ExpectedOutcome:
    """Expected outcomes for scenario validation"""
    metric_name: str
    target_value: Union[float, int, str]
    tolerance: float = 0.1
    measurement_steps: List[int] = field(default_factory=list)
    comparison_type: str = "equals"  # equals, greater_than, less_than, range
    extra_params: Dict[str, Any] = field(default_factory=dict)  # Store extra fields
    
    def __init__(self, metric_name: str, target_value: Union[float, int, str], tolerance: float = 0.1,
                 measurement_steps: List[int] = None, comparison_type: str = "equals", **kwargs):
        self.metric_name = metric_name
        self.target_value = target_value
        self.tolerance = tolerance
        self.measurement_steps = measurement_steps if measurement_steps is not None else []
        self.comparison_type = comparison_type
        self.extra_params = kwargs  # Store any additional parameters
    
    def validate_outcome(self, actual_value: Union[float, int, str], step: int) -> bool:
        """Validate if actual outcome matches expectation"""
        if self.measurement_steps and step not in self.measurement_steps:
            return True  # Don't validate on non-measurement steps
        
        if self.comparison_type == "equals":
            if isinstance(self.target_value, (int, float)):
                return abs(actual_value - self.target_value) <= self.tolerance
            return actual_value == self.target_value
        elif self.comparison_type == "greater_than":
            return actual_value > self.target_value
        elif self.comparison_type == "less_than":
            return actual_value < self.target_value
        
        return False

class Scenario:
    """Complete simulation scenario with events, parameters, and validation"""
    
    def __init__(self, 
                 metadata: ScenarioMetadata,
                 simulation_parameters: SimulationParameters,
                 events: List[ScenarioEvent],
                 expected_outcomes: Optional[List[ExpectedOutcome]] = None,
                 key_metrics: Optional[List[str]] = None,
                 risk_factors: Optional[List[Dict[str, Any]]] = None):
        
        self.metadata = metadata
        self.simulation_parameters = simulation_parameters
        self.events = events
        self.expected_outcomes = expected_outcomes or []
        self.key_metrics = key_metrics or []
        self.risk_factors = risk_factors or []
        
        # Validation
        self._validate_scenario()
    
    def _validate_scenario(self):
        """Validate scenario structure and data"""
        # Check event steps are within simulation duration
        max_step = max([event.step for event in self.events]) if self.events else 0
        if max_step > self.simulation_parameters.duration_steps:
            logger.warning(f"Event at step {max_step} exceeds simulation duration {self.simulation_parameters.duration_steps}")
        
        # Check for duplicate event steps of same type
        step_type_combinations = [(e.step, e.event_type) for e in self.events]
        if len(step_type_combinations) != len(set(step_type_combinations)):
            logger.warning("Duplicate event types found at same step - may cause conflicts")
        
        # Validate event parameters
        for event in self.events:
            try:
                event.to_base_event()  # This will raise exception if invalid
            except Exception as e:
                raise ValueError(f"Invalid event {event.event_type} at step {event.step}: {str(e)}")
    
    def get_events_by_step(self, step: int) -> List[ScenarioEvent]:
        """Get all events scheduled for a specific step"""
        return [event for event in self.events if event.step == step]
    
    def get_events_by_type(self, event_type: str) -> List[ScenarioEvent]:
        """Get all events of a specific type"""
        return [event for event in self.events if event.event_type == event_type]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert scenario to dictionary for serialization"""
        return {
            "scenario_metadata": self.metadata.to_dict(),
            "simulation_parameters": self.simulation_parameters.to_dict(),
            "events": [event.to_dict() for event in self.events],
            "expected_outcomes": [
                {
                    "metric_name": outcome.metric_name,
                    "target_value": outcome.target_value,
                    "tolerance": outcome.tolerance,
                    "measurement_steps": outcome.measurement_steps,
                    "comparison_type": outcome.comparison_type,
                    **outcome.extra_params  # Include extra parameters
                } for outcome in self.expected_outcomes
            ],
            "key_metrics_to_track": self.key_metrics,
            "risk_factors": self.risk_factors
        }
    
    def export_to_json(self, filepath: str):
        """Export scenario to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        logger.info(f"Scenario exported to {filepath}")

class ScenarioManager:
    """Manages scenario loading, validation, and execution"""
    
    # JSON Schema for scenario validation
    SCENARIO_SCHEMA = {
        "type": "object",
        "required": ["scenario_metadata", "simulation_parameters", "events"],
        "properties": {
            "scenario_metadata": {
                "type": "object",
                "required": ["name", "description"],
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "description": {"type": "string", "minLength": 1},
                    "version": {"type": "string", "pattern": r"^\d+\.\d+$"},
                    "author": {"type": "string"},
                    "created_date": {"type": "string", "format": "date"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "difficulty_level": {"type": "string", "enum": ["easy", "medium", "hard", "expert"]},
                    "estimated_duration": {"type": "integer", "minimum": 1}
                }
            },
            "simulation_parameters": {
                "type": "object",
                "properties": {
                    "duration_steps": {"type": "integer", "minimum": 1},
                    "warm_up_steps": {"type": "integer", "minimum": 0},
                    "agent_population": {"type": "integer", "minimum": 1},
                    "random_seed": {"type": ["integer", "null"]},
                    "output_frequency": {"type": "integer", "minimum": 1},
                    "save_intermediate_results": {"type": "boolean"},
                    "enable_real_time_visualization": {"type": "boolean"}
                }
            },
            "events": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["event_type", "step", "parameters"],
                    "properties": {
                        "event_type": {"type": "string"},
                        "step": {"type": "integer", "minimum": 0},
                        "parameters": {"type": "object"},
                        "event_id": {"type": ["string", "null"]},
                        "description": {"type": ["string", "null"]}
                    }
                }
            }
        }
    }
    
    def __init__(self, template_directory: str = "configs/scenario_templates"):
        # Set template_directory to an absolute path from the project root
        # Use parents[2] to move from src/simulation to the project root, then append template_directory
        self.template_directory = Path(__file__).resolve().parents[2] / template_directory
        logger.debug(f"Initialized template_directory: {self.template_directory}")
        self.loaded_scenarios: Dict[str, Scenario] = {}
        self.scenario_cache: Dict[str, Dict[str, Any]] = {}
        
        # Ensure template directory exists
        self.template_directory.mkdir(parents=True, exist_ok=True)
    
    def load_scenario(self, scenario_file: Union[str, Path]) -> Scenario:
        """
        Load scenario from JSON template file
        
        Args:
            scenario_file: Path to JSON scenario file
            
        Returns:
            Scenario: Loaded and validated scenario
        """
        # Convert scenario_file to Path object
        scenario_path = Path(scenario_file) if not isinstance(scenario_file, Path) else scenario_file
        
        # If not absolute, join with template_directory
        if not scenario_path.is_absolute():
            scenario_path = self.template_directory / scenario_path
        else:
            # If absolute, ensure it’s within template_directory
            relative_path = scenario_path.relative_to(self.template_directory.parent) if self.template_directory.parent in scenario_path.parents else scenario_path
            scenario_path = self.template_directory / relative_path
        
        # Resolve to absolute path and normalize
        scenario_path = scenario_path.resolve()
        logger.debug(f"Resolved scenario path: {scenario_path}")
        
        # Check if file exists
        if not scenario_path.exists():
            raise FileNotFoundError(f"Scenario file not found: {scenario_file} (checked at {scenario_path})")
        
        # Load JSON data
        try:
            with open(scenario_path, 'r', encoding='utf-8') as f:
                scenario_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in scenario file {scenario_path}: {str(e)}")
        
        # Validate against schema
        try:
            jsonschema.validate(scenario_data, self.SCENARIO_SCHEMA)
        except jsonschema.ValidationError as e:
            raise ValueError(f"Schema validation failed: {str(e)}")
        
        # Create scenario objects
        metadata = ScenarioMetadata(**scenario_data["scenario_metadata"])
        parameters = SimulationParameters(**scenario_data["simulation_parameters"])
        
        # Create events
        events = []
        for event_data in scenario_data["events"]:
            events.append(ScenarioEvent(**event_data))
        
        # Fix for expected_outcomes: handle list of outcomes
        expected_outcomes = []
        if "expected_outcomes" in scenario_data and isinstance(scenario_data["expected_outcomes"], list):
            for outcome_data in scenario_data["expected_outcomes"]:
                expected_outcomes.append(ExpectedOutcome(**outcome_data))
        
        # Create scenario
        scenario = Scenario(
            metadata=metadata,
            simulation_parameters=parameters,
            events=events,
            expected_outcomes=expected_outcomes,
            key_metrics=scenario_data.get("key_metrics_to_track", []),
            risk_factors=scenario_data.get("risk_factors", [])
        )
        
        # Cache the scenario
        self.loaded_scenarios[metadata.name] = scenario
        self.scenario_cache[scenario_path.name] = scenario_data
        
        logger.info(f"Successfully loaded scenario: {metadata.name}")
        return scenario
    
    def validate_scenario(self, scenario: Union[Scenario, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate scenario structure and logic
        
        Args:
            scenario: Scenario object or dictionary
            
        Returns:
            Dict with validation results
        """
        issues = []
        warnings = []
        
        if isinstance(scenario, dict):
            # Validate JSON structure
            try:
                jsonschema.validate(scenario, self.SCENARIO_SCHEMA)
            except jsonschema.ValidationError as e:
                issues.append(f"Schema validation failed: {str(e)}")
                return {"valid": False, "issues": issues, "warnings": warnings}
        
        scenario_obj = scenario if isinstance(scenario, Scenario) else self._dict_to_scenario(scenario)
        
        # Business logic validation
        
        # Check event timing
        duration = scenario_obj.simulation_parameters.duration_steps
        late_events = [e for e in scenario_obj.events if e.step >= duration]
        if late_events:
            warnings.append(f"{len(late_events)} events scheduled after simulation end")
        
        # Check for conflicting events
        step_groups = {}
        for event in scenario_obj.events:
            if event.step not in step_groups:
                step_groups[event.step] = []
            step_groups[event.step].append(event)
        
        conflict_steps = []
        for step, events in step_groups.items():
            if len(events) > 1:
                # Check for potential conflicts
                event_types = [e.event_type for e in events]
                if "BranchClosureEvent" in event_types and "MarketingCampaignEvent" in event_types:
                    conflict_steps.append(step)
        
        if conflict_steps:
            warnings.append(f"Potential event conflicts at steps: {conflict_steps}")
        
        # Validate expected outcomes
        for outcome in scenario_obj.expected_outcomes:
            if outcome.measurement_steps:
                invalid_steps = [s for s in outcome.measurement_steps if s >= duration]
                if invalid_steps:
                    issues.append(f"Outcome measurement steps {invalid_steps} exceed simulation duration")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "event_count": len(scenario_obj.events),
            "duration": duration,
            "complexity_score": self._calculate_complexity(scenario_obj)
        }
    
    def _calculate_complexity(self, scenario: Scenario) -> float:
        """Calculate scenario complexity score (0-1)"""
        complexity = 0.0
        
        # Event count factor
        complexity += min(len(scenario.events) / 20, 0.3)
        
        # Event type diversity
        unique_types = len(set(event.event_type for event in scenario.events))
        complexity += min(unique_types / 7, 0.2)  # Max 7 event types
        
        # Duration factor
        complexity += min(scenario.simulation_parameters.duration_steps / 200, 0.2)
        
        # Agent population factor
        complexity += min(scenario.simulation_parameters.agent_population / 5000, 0.2)
        
        # Expected outcomes factor
        complexity += min(len(scenario.expected_outcomes) / 10, 0.1)
        
        return min(complexity, 1.0)
    
    def _dict_to_scenario(self, data: Dict[str, Any]) -> Scenario:
        """Convert dictionary to Scenario object"""
        metadata = ScenarioMetadata(**data["scenario_metadata"])
        parameters = SimulationParameters(**data["simulation_parameters"])
        events = [ScenarioEvent(**event_data) for event_data in data["events"]]
        
        expected_outcomes = []
        if "expected_outcomes" in data:
            expected_outcomes = [ExpectedOutcome(**outcome) for outcome in data["expected_outcomes"]]
        
        return Scenario(
            metadata=metadata,
            simulation_parameters=parameters,
            events=events,
            expected_outcomes=expected_outcomes,
            key_metrics=data.get("key_metrics_to_track", []),
            risk_factors=data.get("risk_factors", [])
        )
    
    def execute_scenario(self, scenario: Scenario, event_system: EventSystem) -> Dict[str, Any]:
        """
        Execute scenario by injecting events into the simulation
        
        Args:
            scenario: Scenario to execute
            event_system: EventSystem instance
            
        Returns:
            Dict with execution results
        """
        logger.info(f"Executing scenario: {scenario.metadata.name}")
        
        # Clear existing events
        event_system.clear_events()
        
        # Inject scenario events
        injected_count = 0
        failed_injections = []
        
        for scenario_event in scenario.events:
            try:
                base_event = scenario_event.to_base_event()
                if event_system.inject_event(base_event):
                    injected_count += 1
                else:
                    failed_injections.append(scenario_event)
            except Exception as e:
                logger.error(f"Failed to inject event {scenario_event.event_type}: {str(e)}")
                failed_injections.append(scenario_event)
        
        execution_summary = {
            "scenario_name": scenario.metadata.name,
            "events_injected": injected_count,
            "events_failed": len(failed_injections),
            "total_events": len(scenario.events),
            "execution_timestamp": datetime.now().isoformat(),
            "simulation_parameters": scenario.simulation_parameters.to_dict(),
            "failed_events": [event.to_dict() for event in failed_injections]
        }
        
        logger.info(f"Scenario execution complete: {injected_count}/{len(scenario.events)} events injected")
        
        return execution_summary
    
    def list_available_scenarios(self) -> List[Dict[str, Any]]:
        """List all available scenario templates"""
        scenarios = []
        
        for json_file in self.template_directory.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "scenario_metadata" in data:
                    metadata = data["scenario_metadata"]
                    scenarios.append({
                        "filename": json_file.name,
                        "name": metadata.get("name", "Unknown"),
                        "description": metadata.get("description", ""),
                        "tags": metadata.get("tags", []),
                        "difficulty": metadata.get("difficulty_level", "medium"),
                        "duration": data.get("simulation_parameters", {}).get("duration_steps", 0),
                        "event_count": len(data.get("events", []))
                    })
            except Exception as e:
                logger.warning(f"Could not read scenario file {json_file}: {str(e)}")
        
        return sorted(scenarios, key=lambda x: x["name"])
    
    def create_scenario_template(self, name: str, description: str, 
                               events: List[Dict[str, Any]], **kwargs) -> str:
        """Create a new scenario template file"""
        
        # Generate filename
        filename = f"{name.lower().replace(' ', '_')}_scenario.json"
        filepath = self.template_directory / filename
        
        # Create scenario data
        scenario_data = {
            "scenario_metadata": {
                "name": name,
                "description": description,
                "version": "1.0",
                "author": kwargs.get("author", ""),
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "tags": kwargs.get("tags", []),
                "difficulty_level": kwargs.get("difficulty", "medium"),
                "estimated_duration": kwargs.get("duration", 100)
            },
            "simulation_parameters": {
                "duration_steps": kwargs.get("duration", 100),
                "warm_up_steps": kwargs.get("warm_up", 10),
                "agent_population": kwargs.get("population", 1000),
                "random_seed": kwargs.get("seed", None),
                "output_frequency": kwargs.get("output_freq", 5),
                "save_intermediate_results": True,
                "enable_real_time_visualization": False
            },
            "events": events,
            "expected_outcomes": kwargs.get("expected_outcomes", []),
            "key_metrics_to_track": kwargs.get("key_metrics", []),
            "risk_factors": kwargs.get("risk_factors", [])
        }
        
        # Validate before saving
        validation = self.validate_scenario(scenario_data)
        if not validation["valid"]:
            raise ValueError(f"Scenario validation failed: {validation['issues']}")
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(scenario_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Created scenario template: {filepath}")
        return str(filepath)
    
    def get_scenario_by_name(self, name: str) -> Optional[Scenario]:
        """Get loaded scenario by name"""
        return self.loaded_scenarios.get(name)
    
    def clear_cache(self):
        """Clear loaded scenario cache"""
        self.loaded_scenarios.clear()
        self.scenario_cache.clear()
        logger.info("Scenario cache cleared")