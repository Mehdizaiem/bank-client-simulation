"""
Main Integration Controller
Connects data generation, simulation, and dashboard output
"""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import pandas as pd
import logging

from src.simulation.bank_simulation_model import BankSimulationModel
from src.simulation.integrated_bank_simulation_model import IntegratedBankSimulationModel
from src.simulation.scenario_manager import ScenarioManager
from src.agent_engine.data_loader import DataLoader
from src.reporting.simulation_reporter import SimulationReporter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimulationController:
    """Main controller for simulation workflow integration"""
    
    def __init__(self, config_path: str = "configs/simulation_config.yaml"):
        """Initialize the simulation controller"""
        self.config_path = config_path
        self.base_path = Path(__file__).resolve().parents[2]
        self.output_dir = self.base_path / "output" / "simulation_results"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.data_loader = DataLoader()
        self.scenario_manager = ScenarioManager()
        self.reporter = SimulationReporter()
        
        # Store current simulation state
        self.current_model = None
        self.current_scenario = None
        self.simulation_results = {}
        
    def load_simulation_config(self) -> Dict[str, Any]:
        """Load simulation configuration"""
        import yaml
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def prepare_agent_data(self) -> Dict[str, pd.DataFrame]:
        """Load and prepare agent data from CSV files"""
        logger.info("Loading agent data from CSV files...")
        
        # Load retail agents
        retail_path = self.base_path / "data" / "processed" / "hamza_retail_agents.csv"
        retail_df = pd.read_csv(retail_path)
        
        # Load corporate agents
        corporate_path = self.base_path / "data" / "processed" / "hamza_corporate_agents.csv"
        corporate_df = pd.read_csv(corporate_path)
        
        logger.info(f"Loaded {len(retail_df)} retail agents and {len(corporate_df)} corporate agents")
        
        return {
            'retail': retail_df,
            'corporate': corporate_df
        }
    
    def initialize_simulation(self, scenario_name: Optional[str] = None, 
                            custom_config: Optional[Dict] = None) -> BankSimulationModel:
        """
        Initialize simulation model with optional scenario
        
        Args:
            scenario_name: Name of scenario to load (optional)
            custom_config: Custom configuration to override defaults
            
        Returns:
            Initialized simulation model
        """
        # Load base configuration
        config = self.load_simulation_config()
        
        # Override with custom config if provided
        if custom_config:
            config['simulation'].update(custom_config)
        
        # Load agent data
        agent_data = self.prepare_agent_data()
        
        # Create model based on scenario presence
        if scenario_name:
            logger.info(f"Initializing simulation with scenario: {scenario_name}")
            scenario_file = f"{scenario_name}.json"
            self.current_model = IntegratedBankSimulationModel(
                config['simulation'],
                scenario_file,
                agent_data=agent_data
            )
            self.current_scenario = self.scenario_manager.load_scenario(scenario_file)
        else:
            logger.info("Initializing basic simulation without scenario")
            self.current_model = BankSimulationModel(
                config['simulation'],
                agent_data=agent_data
            )
            
        return self.current_model
    
    def run_simulation(self, steps: Optional[int] = None, 
                      output_frequency: int = 10) -> Dict[str, Any]:
        """
        Run the simulation and collect results
        
        Args:
            steps: Number of steps to run (uses config if not specified)
            output_frequency: How often to collect metrics
            
        Returns:
            Simulation results dictionary
        """
        if not self.current_model:
            raise ValueError("Model not initialized. Call initialize_simulation first.")
        
        # Determine number of steps
        if steps is None:
            config = self.load_simulation_config()
            steps = config['simulation']['time_steps']
        
        logger.info(f"Running simulation for {steps} steps...")
        
        # Initialize results collection
        results = {
            'metadata': {
                'start_time': datetime.now().isoformat(),
                'total_steps': steps,
                'output_frequency': output_frequency,
                'scenario': self.current_scenario.metadata.name if self.current_scenario else 'basic_simulation'
            },
            'metrics': [],
            'events': [],
            'agent_states': []
        }
        
        # Run simulation
        for step in range(steps):
            # Execute step
            self.current_model.step()
            
            # Collect metrics at specified frequency
            if step % output_frequency == 0 or step == steps - 1:
                metrics = self._collect_metrics(step)
                results['metrics'].append(metrics)
                
                # Collect sample agent states
                agent_sample = self._sample_agent_states(sample_size=100)
                results['agent_states'].append({
                    'step': step,
                    'agents': agent_sample
                })
            
            # Log progress
            if step % 50 == 0:
                logger.info(f"Completed step {step}/{steps}")
        
        results['metadata']['end_time'] = datetime.now().isoformat()
        self.simulation_results = results
        
        logger.info("Simulation completed successfully")
        return results
    
    def _collect_metrics(self, step: int) -> Dict[str, Any]:
        """Collect current simulation metrics"""
        return {
            'step': step,
            'timestamp': datetime.now().isoformat(),
            'average_satisfaction': self.current_model.get_average_satisfaction(),
            'churn_rate': self.current_model.calculate_churn_rate(),
            'digital_adoption_rate': self.current_model.get_digital_adoption_rate(),
            'branch_utilization': self.current_model.get_branch_utilization(),
            'active_agents': len([a for a in self.current_model.agents if a.status == 'active']),
            'churned_agents': len([a for a in self.current_model.agents if a.status == 'churned'])
        }
    
    def _sample_agent_states(self, sample_size: int = 100) -> List[Dict]:
        """Sample agent states for visualization"""
        import random
        agents = list(self.current_model.agents)
        sample = random.sample(agents, min(sample_size, len(agents)))
        
        return [{
            'id': agent.unique_id,
            'type': agent.client_type,
            'satisfaction': agent.satisfaction_level,
            'channel': agent.preferred_channel,
            'status': agent.status,
            'governorate': getattr(agent, 'governorate', 'unknown')
        } for agent in sample]
    
    def export_for_dashboard(self, format: str = 'json') -> str:
        """
        Export simulation results for dashboard consumption
        
        Args:
            format: Output format ('json', 'api', 'websocket')
            
        Returns:
            Path to exported file or API endpoint
        """
        if not self.simulation_results:
            raise ValueError("No simulation results available. Run simulation first.")
        
        logger.info(f"Exporting results for dashboard in {format} format...")
        
        # Prepare dashboard-specific data structure
        dashboard_data = self._prepare_dashboard_data()
        
        if format == 'json':
            # Export to JSON file
            output_file = self.output_dir / f"dashboard_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(dashboard_data, f, indent=2, default=str)
            logger.info(f"Dashboard data exported to: {output_file}")
            return str(output_file)
            
        elif format == 'api':
            # Prepare for API endpoint
            return self._setup_api_endpoint(dashboard_data)
            
        elif format == 'websocket':
            # Prepare for real-time streaming
            return self._setup_websocket_stream(dashboard_data)
            
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _prepare_dashboard_data(self) -> Dict[str, Any]:
        """Prepare data structure optimized for dashboard visualization"""
        results = self.simulation_results
        
        # Extract time series data for charts
        time_series = {
            'timestamps': [],
            'satisfaction': [],
            'churn_rate': [],
            'digital_adoption': [],
            'active_agents': []
        }
        
        for metric in results['metrics']:
            time_series['timestamps'].append(metric['step'])
            time_series['satisfaction'].append(metric['average_satisfaction'])
            time_series['churn_rate'].append(metric['churn_rate'])
            time_series['digital_adoption'].append(metric['digital_adoption_rate'])
            time_series['active_agents'].append(metric['active_agents'])
        
        # Prepare scenario configuration for controls
        scenario_config = {}
        if self.current_scenario:
            scenario_config = {
                'name': self.current_scenario.metadata.name,
                'description': self.current_scenario.metadata.description,
                'duration': self.current_scenario.simulation_parameters.duration_steps,
                'events': [
                    {
                        'step': event.step,
                        'type': event.event_type,
                        'description': event.description
                    } for event in self.current_scenario.events
                ]
            }
        
        # Agent distribution analysis
        final_agent_states = results['agent_states'][-1]['agents'] if results['agent_states'] else []
        agent_distribution = self._analyze_agent_distribution(final_agent_states)
        
        return {
            'simulation_id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'metadata': results['metadata'],
            'scenario_config': scenario_config,
            'time_series': time_series,
            'agent_distribution': agent_distribution,
            'final_metrics': {
                'total_steps_completed': results['metadata']['total_steps'],
                'final_satisfaction': time_series['satisfaction'][-1] if time_series['satisfaction'] else 0,
                'final_churn_rate': time_series['churn_rate'][-1] if time_series['churn_rate'] else 0,
                'final_digital_adoption': time_series['digital_adoption'][-1] if time_series['digital_adoption'] else 0
            },
            'events_log': results.get('events', [])
        }
    
    def _analyze_agent_distribution(self, agent_states: List[Dict]) -> Dict[str, Any]:
        """Analyze agent distribution for visualization"""
        if not agent_states:
            return {}
            
        df = pd.DataFrame(agent_states)
        
        return {
            'by_type': df['type'].value_counts().to_dict(),
            'by_status': df['status'].value_counts().to_dict(),
            'by_channel': df['channel'].value_counts().to_dict(),
            'by_governorate': df['governorate'].value_counts().to_dict() if 'governorate' in df else {},
            'satisfaction_histogram': df['satisfaction'].describe().to_dict()
        }
    
    def _setup_api_endpoint(self, data: Dict) -> str:
        """Setup API endpoint for dashboard (placeholder)"""
        # This would integrate with Flask/FastAPI
        endpoint = "http://localhost:8000/api/simulation/results"
        logger.info(f"API endpoint would be available at: {endpoint}")
        return endpoint
    
    def _setup_websocket_stream(self, data: Dict) -> str:
        """Setup WebSocket for real-time streaming (placeholder)"""
        # This would integrate with WebSocket server
        ws_url = "ws://localhost:8000/simulation/stream"
        logger.info(f"WebSocket stream would be available at: {ws_url}")
        return ws_url