"""
Integrated Bank Simulation Model with Mesa 3.x
Combines all components: agents, events, scenarios, segments
"""
import mesa
from mesa.datacollection import DataCollector
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path
import json
import random
import time

# Import our components
from src.agent_engine.data_loader import AgentDataLoader
from src.agent_engine.retail_agent import RetailClientAgent
from src.agent_engine.corporate_agent import CorporateClientAgent
from src.simulation.event_system import EventSystem, BaseEvent
from src.simulation.scenarios import ScenarioManager

# Create a simple reporter if the module doesn't exist
try:
    from src.reporting.simulation_reporter import SimulationReporter
except ImportError:
    # Fallback simple reporter
    class SimulationReporter:
        def __init__(self, output_dir: str = "simulation_outputs"):
            self.output_dir = Path(output_dir)
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
        def start_report(self, scenario_name: str, metadata: Dict = None):
            pass
            
        def add_metric(self, step: int, metric_name: str, value: float):
            pass
            
        def add_event(self, step: int, event_type: str, description: str, impact: Dict = None):
            pass
            
        def finalize_report(self, final_metrics: Dict, outcome_validation: List = None):
            pass

class IntegratedBankSimulationModel(mesa.Model):
    """Mesa 3.x compatible integrated simulation model"""
    
    def __init__(self, config: Dict[str, Any], scenario_file: str = None):
        """Initialize integrated model with configuration and optional scenario"""
        
        # Mesa 3.x initialization with seed
        super().__init__(seed=config.get('random_seed', 42))
        
        # Setup logging
        self.setup_logging()
        self.logger.info("\n===== Initializing IntegratedBankSimulationModel (Mesa 3.x) =====")
        
        # SIMULATION PARAMETERS
        self.num_agents = config.get('num_agents', 1000)
        self.retail_ratio = config.get('retail_ratio', 0.8)
        self.time_steps = config.get('time_steps', 100)
        self.current_step = 0
        self.running = True
        
        # CLIENT SEGMENTS (from Maryem's work)
        self.client_segments = self.load_client_segments()
        self.agents_by_segment = {}
        
        # EVENT SYSTEM
        self.event_system = EventSystem()
        
        # SCENARIO MANAGEMENT
        self.scenario_manager = ScenarioManager()
        self.current_scenario = None
        
        # REPORTING
        self.reporter = SimulationReporter()
        
        # MARKET CONDITIONS
        self.market_satisfaction_modifier = 0.0
        self.market_volatility = 0.1
        self.economic_climate = 0.5
        
        # DATA LOADING SYSTEM
        self.data_loader = AgentDataLoader()
        
        # LOAD SCENARIO (if provided)
        if scenario_file:
            self.load_and_prepare_scenario(scenario_file)
        
        # LOAD AGENTS FROM CSV
        self.logger.info("Loading agents from CSV files...")
        self.load_agents_from_csv()
        
        # ASSIGN AGENTS TO SEGMENTS
        self.assign_agents_to_segments()
        
        # CREATE SOCIAL NETWORKS
        self.logger.info("Creating social networks...")
        self.create_social_networks()
        
        # REGISTER EVENT HANDLERS
        self.register_event_handlers()
        
        # DATA COLLECTION
        self.datacollector = DataCollector(
            model_reporters={
                "Average_Satisfaction": self.get_average_satisfaction,
                "Churn_Rate": self.calculate_churn_rate,
                "Digital_Usage": self.get_digital_usage_rate,
                "Active_Products": self.count_active_products,
                "Market_Volatility": lambda m: m.market_volatility,
                "Economic_Climate": lambda m: m.economic_climate,
            },
            agent_reporters={
                "Satisfaction": "satisfaction_level",
                "Digital_Usage": "digital_engagement_score",
                "Product_Count": lambda a: len(a.owned_products),
                "Age": "age",
                "Income": "income",
                "Client_Type": "client_type",
            }
        )
        
        self.logger.info(f"Model initialization complete with {len(self.agents)} agents")
    
    def setup_logging(self):
        """Setup logging for simulation"""
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("logs/simulation.log"),
                logging.StreamHandler()
            ],
        )
        self.logger = logging.getLogger("IntegratedBankSimulation")
    
    def load_client_segments(self) -> Dict[str, List[str]]:
        """Load client segments from Maryem's segment file"""
        segment_file = Path(__file__).parent.parent.parent / "data" / "processed" / "maryem_client_segments.json"
        
        try:
            if segment_file.exists():
                with open(segment_file, "r") as f:
                    segments = json.load(f)
                self.logger.info(f"Loaded client segments from {segment_file}")
                return segments
            else:
                self.logger.warning(f"Client segments file not found: {segment_file}")
                # Return default segments
                return {
                    'digital_first': [],
                    'high_value': [],
                    'young_professionals': [],
                    'sme': [],
                    'traditional': []
                }
        except Exception as e:
            self.logger.error(f"Failed to load client segments: {e}")
            return {
                'digital_first': [],
                'high_value': [],
                'young_professionals': [],
                'sme': [],
                'traditional': []
            }
    
    def load_and_prepare_scenario(self, scenario_file: str):
        """Load a scenario and prepare it for execution"""
        try:
            self.current_scenario = self.scenario_manager.load_scenario(scenario_file)
            
            if self.current_scenario:
                scenario_params = self.current_scenario.simulation_parameters
                self.time_steps = scenario_params.duration_steps
                self.num_agents = scenario_params.agent_population
                
                self.logger.info(f"Loaded scenario: {self.current_scenario.metadata.name}")
                self.logger.info(f"Scenario duration: {self.time_steps} steps")
                self.logger.info(f"Scenario events: {len(self.current_scenario.events)}")
                
                # Start report for this scenario
                self.reporter.start_report(
                    self.current_scenario.metadata.name,
                    self.current_scenario.metadata.to_dict()
                )
                
                # Inject scenario events
                injected_events = self.scenario_manager.execute_scenario(
                    self.current_scenario, self.event_system
                )
                
                self.logger.info(f"Successfully injected {injected_events['events_injected']}/{len(self.current_scenario.events)} events")
                
        except Exception as e:
            self.logger.error(f"Failed to load scenario {scenario_file}: {e}")
            self.current_scenario = None
    
    def load_agents_from_csv(self):
        """Load agents from CSV files and create agent objects"""
        # Calculate how many of each type we need
        target_retail = int(self.num_agents * self.retail_ratio)
        target_corporate = self.num_agents - target_retail
        
        # Load retail agents
        retail_data = self.data_loader.load_retail_agents()
        selected_retail = self.data_loader.select_agents(retail_data, target_retail)
        
        # Load corporate agents  
        corporate_data = self.data_loader.load_corporate_agents()
        selected_corporate = self.data_loader.select_agents(corporate_data, target_corporate)
        
        self.logger.info(f"Selected {len(selected_retail)} retail and {len(selected_corporate)} corporate agents")
        
        # Create retail agents
        for retail_record in selected_retail:
            agent = RetailClientAgent(self, retail_record)
            # Mesa 3.x automatically adds agents to self.agents
        
        # Create corporate agents
        for corporate_record in selected_corporate:
            agent = CorporateClientAgent(self, corporate_record)
            # Mesa 3.x automatically adds agents to self.agents
        
        actual_retail = len([a for a in self.agents if a.client_type == "retail"])
        actual_corporate = len([a for a in self.agents if a.client_type == "corporate"])
        
        self.logger.info(f"Created {len(self.agents)} agents from CSV: retail={actual_retail}, corporate={actual_corporate}")
        
        # Log some statistics
        if actual_retail > 0:
            avg_age = sum(a.age for a in self.agents if a.client_type == "retail") / actual_retail
            avg_income = sum(a.income for a in self.agents if a.client_type == "retail") / actual_retail
            self.logger.info(f"  Retail stats: avg age={avg_age:.1f}, avg income={avg_income:.0f} TND")
        
        if actual_corporate > 0:
            avg_revenue = sum(a.annual_revenue for a in self.agents if a.client_type == "corporate") / actual_corporate
            sectors = set(a.business_sector for a in self.agents if a.client_type == "corporate")
            self.logger.info(f"  Corporate stats: avg revenue={avg_revenue:.0f} TND, sectors={len(sectors)} unique")
    
    def assign_agents_to_segments(self):
        """Assign agents to client segments based on their characteristics"""
        self.agents_by_segment = {}
        
        # Initialize segment lists
        for segment in self.client_segments.keys():
            self.agents_by_segment[segment] = []
        
        # Assign each agent to appropriate segments
        for agent in self.agents:
            assigned_segments = self._determine_agent_segments(agent)
            for segment in assigned_segments:
                if segment in self.agents_by_segment:
                    self.agents_by_segment[segment].append(agent)
        
        # Log segment assignments
        for segment, agents in self.agents_by_segment.items():
            if agents:  # Only log segments with agents
                self.logger.info(f"Segment '{segment}': {len(agents)} agents")
    
    def _determine_agent_segments(self, agent) -> List[str]:
        """Determine which segments an agent belongs to"""
        segments = []
        
        # Digital-first segment
        if hasattr(agent, 'digital_engagement_score') and agent.digital_engagement_score > 0.7:
            segments.append('digital_first')
        
        # High-value segment
        if agent.client_type == 'retail' and hasattr(agent, 'income') and agent.income > 2000:
            segments.append('high_value')
        elif agent.client_type == 'corporate' and hasattr(agent, 'annual_revenue') and agent.annual_revenue > 500000:
            segments.append('high_value')
        
        # Young professionals segment
        if agent.client_type == 'retail' and hasattr(agent, 'age'):
            if 25 <= agent.age <= 40:
                segments.append('young_professionals')
        
        # SME segment
        if agent.client_type == 'corporate' and hasattr(agent, 'company_size'):
            if agent.company_size in ['small', 'medium']:
                segments.append('sme')
        
        # Traditional segment (low digital engagement)
        if hasattr(agent, 'digital_engagement_score') and agent.digital_engagement_score < 0.3:
            segments.append('traditional')
        
        return segments
    
    def create_social_networks(self):
        """Create social network connections between agents"""
        for agent in self.agents:
            # Each agent gets 3-7 random connections
            num_connections = random.randint(3, 7)
            possible_connections = [a for a in self.agents if a != agent]
            
            if possible_connections:
                connections = random.sample(
                    possible_connections,
                    min(num_connections, len(possible_connections))
                )
                agent.social_network = connections
    
    def register_event_handlers(self):
        """Register event handlers for different event types"""
        
        def handle_marketing_campaign(event: BaseEvent):
            """Handle marketing campaign events"""
            self.logger.info(f"Processing marketing campaign: {event.event_type}")
            # Target specific segments
            target_segments = event.parameters.get('target_segments', ['digital_first'])
            effectiveness = event.parameters.get('effectiveness', 0.2)
            
            for segment in target_segments:
                if segment in self.agents_by_segment:
                    for agent in self.agents_by_segment[segment]:
                        # Increase satisfaction based on campaign effectiveness
                        agent.satisfaction_level = min(1.0, agent.satisfaction_level + effectiveness * random.random())
            
            # Report event
            self.reporter.add_event(
                self.current_step,
                'MarketingCampaignEvent',
                f"Marketing campaign targeting {target_segments}",
                {'target_segments': target_segments, 'effectiveness': effectiveness}
            )
        
        def handle_branch_closure(event: BaseEvent):
            """Handle branch closure events"""
            self.logger.info(f"Processing branch closure: {event.event_type}")
            impact = event.parameters.get('satisfaction_impact', -0.1)
            
            # Affect traditional segment most
            if 'traditional' in self.agents_by_segment:
                for agent in self.agents_by_segment['traditional']:
                    agent.satisfaction_level = max(0, agent.satisfaction_level + impact)
            
            self.reporter.add_event(
                self.current_step,
                'BranchClosureEvent',
                f"Branch closure with impact {impact}",
                {'impact': impact}
            )
        
        def handle_digital_transformation(event: BaseEvent):
            """Handle digital transformation events"""
            self.logger.info(f"Processing digital transformation: {event.event_type}")
            
            # Increase digital engagement across the board
            for agent in self.agents:
                if hasattr(agent, 'digital_engagement_score'):
                    improvement = event.parameters.get('engagement_boost', 0.1)
                    agent.digital_engagement_score = min(1.0, agent.digital_engagement_score + improvement)
            
            self.reporter.add_event(
                self.current_step,
                'DigitalTransformationEvent',
                f"Digital transformation with boost {improvement}",
                {'engagement_boost': event.parameters.get('engagement_boost', 0.1)}
            )
        
        # Register handlers
        self.event_system.register_event_handler('MarketingCampaignEvent', handle_marketing_campaign)
        self.event_system.register_event_handler('BranchClosureEvent', handle_branch_closure)
        self.event_system.register_event_handler('DigitalTransformationEvent', handle_digital_transformation)
    
    def step(self):
        """Execute one step of the simulation"""
        self.current_step += 1
        
        # Process any scheduled events
        processed_events = self.event_system.process_events(self.current_step)
        if processed_events:
            self.logger.debug(f"Processed {len(processed_events)} events at step {self.current_step}")
        
        # Market dynamics
        self.update_market_conditions()
        
        # Agent actions (Mesa 3.x style)
        self.agents.shuffle_do("step")
        
        # Collect data
        self.datacollector.collect(self)
        
        # Report metrics periodically
        if self.current_step % 10 == 0:
            self.reporter.add_metric(self.current_step, 'average_satisfaction', self.get_average_satisfaction())
            self.reporter.add_metric(self.current_step, 'churn_rate', self.calculate_churn_rate())
            self.reporter.add_metric(self.current_step, 'digital_usage', self.get_digital_usage_rate())
    
    def update_market_conditions(self):
        """Update market-wide conditions"""
        # Random walk for market volatility
        self.market_volatility += random.gauss(0, 0.01)
        self.market_volatility = max(0, min(1, self.market_volatility))
        
        # Economic climate fluctuation
        self.economic_climate += random.gauss(0, 0.02)
        self.economic_climate = max(0, min(1, self.economic_climate))
        
        # Market satisfaction modifier based on economic climate
        self.market_satisfaction_modifier = (self.economic_climate - 0.5) * 0.1
    
    def get_average_satisfaction(self) -> float:
        """Calculate average satisfaction across all agents"""
        if len(self.agents) == 0:
            return 0
        return sum(a.satisfaction_level for a in self.agents) / len(self.agents)
    
    def calculate_churn_rate(self) -> float:
        """Calculate current churn rate"""
        if len(self.agents) == 0:
            return 0
        at_risk = sum(1 for a in self.agents if a.satisfaction_level < 0.3)
        return at_risk / len(self.agents)
    
    def get_digital_usage_rate(self) -> float:
        """Calculate average digital engagement"""
        digital_agents = [a for a in self.agents if hasattr(a, 'digital_engagement_score')]
        if not digital_agents:
            return 0
        return sum(a.digital_engagement_score for a in digital_agents) / len(digital_agents)
    
    def count_active_products(self) -> float:
        """Count average number of products per agent"""
        if len(self.agents) == 0:
            return 0
        return sum(len(a.owned_products) for a in self.agents) / len(self.agents)
    
    def get_segment_satisfaction(self) -> Dict[str, Dict[str, float]]:
        """Get detailed segment performance metrics"""
        segment_performance = {}
        for segment, agents in self.agents_by_segment.items():
            if agents:
                avg_satisfaction = sum(a.satisfaction_level for a in agents) / len(agents)
                segment_performance[segment] = {
                    'size': len(agents),
                    'avg_satisfaction': avg_satisfaction
                }
            else:
                segment_performance[segment] = {
                    'size': 0,
                    'avg_satisfaction': 0.0
                }
        return segment_performance
    
    def target_segment(self, segment_name: str, action: Dict[str, Any]):
        """Apply targeted action to a specific segment"""
        if segment_name not in self.agents_by_segment:
            self.logger.warning(f"Segment '{segment_name}' not found")
            return
        
        agents = self.agents_by_segment[segment_name]
        self.logger.info(f"Targeting segment '{segment_name}' with {len(agents)} agents")
        
        for agent in agents:
            # Apply action based on type
            if action.get('type') == 'marketing':
                agent.satisfaction_level = min(1.0, agent.satisfaction_level + action.get('impact', 0.1))
            elif action.get('type') == 'product_offer':
                # Add product to agent's portfolio
                product = action.get('product', 'new_product')
                if product not in agent.owned_products:
                    agent.owned_products.append(product)
            elif action.get('type') == 'service_improvement':
                # Improve service metrics
                if hasattr(agent, 'service_quality_perception'):
                    agent.service_quality_perception = min(1.0, agent.service_quality_perception + action.get('improvement', 0.15))
    
    def generate_scenario_report(self) -> Dict[str, Any]:
        """Generate comprehensive report for current scenario"""
        report = {
            'scenario_name': self.current_scenario.metadata.name if self.current_scenario else 'Unknown',
            'total_steps': self.current_step,
            'events_processed': len(self.event_system.processed_events) if hasattr(self.event_system, 'processed_events') else 0,
            'agent_metrics': {
                'total_agents': len(self.agents),
                'retail_agents': len([a for a in self.agents if a.client_type == 'retail']),
                'corporate_agents': len([a for a in self.agents if a.client_type == 'corporate']),
                'average_satisfaction': self.get_average_satisfaction(),
                'churn_rate': self.calculate_churn_rate(),
                'digital_usage_rate': self.get_digital_usage_rate(),
                'active_products': self.count_active_products(),
            },
            'final_metrics': {
                'average_satisfaction': self.get_average_satisfaction(),
                'churn_rate': self.calculate_churn_rate(),
                'digital_usage': self.get_digital_usage_rate(),
                'active_products': self.count_active_products(),
            },
            'segment_performance': self.get_segment_satisfaction(),
            'outcome_validation': [],
            'market_conditions': {
                'volatility': self.market_volatility,
                'economic_climate': self.economic_climate,
            }
        }
        
        # Validate outcomes if defined
        if self.current_scenario and hasattr(self.current_scenario, 'expected_outcomes'):
            for outcome in self.current_scenario.expected_outcomes:
                metric_value = report['final_metrics'].get(outcome.metric_name, 0)
                valid = outcome.validate_outcome(metric_value, self.current_step)
                report['outcome_validation'].append({
                    'metric': outcome.metric_name,
                    'target': outcome.target_value,
                    'actual': metric_value,
                    'valid': valid,
                })
        
        # Finalize reporter
        self.reporter.finalize_report(report['final_metrics'], report['outcome_validation'])
        
        # Save report to file
        report_file = Path("simulation_outputs") / f"{report['scenario_name'].replace(' ', '_').lower()}_report.json"
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Scenario report saved to {report_file}")
        return report
    
    def run_simulation(self):
        """Run the complete simulation"""
        self.logger.info(f"Starting simulation run for {self.time_steps} steps")
        
        for step in range(self.time_steps):
            self.step()
            
            # Log progress every 10 steps
            if (step + 1) % 10 == 0:
                avg_satisfaction = self.get_average_satisfaction()
                self.logger.info(f"Step {step + 1}/{self.time_steps}: Avg satisfaction = {avg_satisfaction:.3f}")
        
        self.logger.info("Simulation complete")
        
        # Generate final report
        final_report = self.generate_scenario_report()
        return final_report
    