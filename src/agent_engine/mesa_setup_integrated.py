# src/agent_engine/mesa_setup_integrated.py
"""
INTEGRATED Mesa 3.x Simulation with Scenarios and Client Segments
Combines Mesa simulation with event system and scenario management
"""

from __future__ import annotations

import mesa
from mesa.datacollection import DataCollector
import pandas as pd
import json
from typing import List, Dict, Any, Optional
import logging
import random
import time
from pathlib import Path
from datetime import datetime

# Import our modules
from src.agent_engine.data_loader import AgentDataLoader
from src.agent_engine.retail_agent import RetailClientAgent
from src.agent_engine.corporate_agent import CorporateClientAgent
from src.simulation.event_system import EventSystem, BaseEvent
from src.simulation.scenarios import ScenarioManager, Scenario
from src.simulation.event_types import (
    MarketingCampaignEvent, BranchClosureEvent, DigitalTransformationEvent,
    CompetitorActionEvent, EconomicShockEvent, RegulatoryChangeEvent,
    ProductLaunchEvent,
)


class IntegratedBankSimulationModel(mesa.Model):
    """Mesa 3.x simulation model with integrated scenario and segment support"""

    def __init__(self, config: Dict[str, Any], scenario_file: Optional[str] = None):
        """
        Initialize integrated simulation model

        Args:
            config: Simulation configuration
            scenario_file: Optional scenario file to load (e.g., "branch_closure_scenario.json")
        """
        # Mesa 3.x initialization
        super().__init__(seed=config.get("random_seed", 42))

        # LOGGING (set up early because several init helpers log)
        self.setup_logging()
        self.logger.info("\n===== Initializing IntegratedBankSimulationModel (Mesa 3.x) =====")

        # SIMULATION PARAMETERS
        self.num_agents = config.get("num_agents", 1000)
        self.retail_ratio = config.get("retail_ratio", 0.8)
        self.time_steps = config.get("time_steps", 100)
        self.current_step = 0
        
        # SIMULATION STATE
        self.running = True
        self.total_agents_created = 0
        
        # CLIENT SEGMENTS AND SCENARIOS
        self.client_segments = self.load_client_segments()
        self.agents_by_segment: Dict[str, List] = {}
        self.current_scenario: Optional[Scenario] = None
        
        # EVENT SYSTEM
        self.event_system = EventSystem()
        self.scenario_manager = ScenarioManager()
        self.active_events: Dict[str, Dict] = {}
        
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
                "Average_Satisfaction": "get_average_satisfaction",
                "Churn_Rate": "calculate_churn_rate",
                "Digital_Usage": "get_digital_usage_rate",
                "Active_Products": "count_active_products",
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

    # ----------------------------------------------------------------
    # Setup and configuration
    # ----------------------------------------------------------------
    def setup_logging(self):
        """Setup logging for simulation"""
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler("logs/simulation.log"), logging.StreamHandler()],
        )
        self.logger = logging.getLogger("IntegratedBankSimulation")

    def load_client_segments(self) -> Dict[str, List[str]]:
        """Load client segments from Maryem's segment file"""
        segment_file = (
            Path(__file__).parent.parent.parent / "data" / "processed" / "maryem_client_segments.json"
        )

        try:
            if segment_file.exists():
                with open(segment_file, "r") as f:
                    segments = json.load(f)
                if hasattr(self, "logger"):
                    self.logger.info(f"Loaded client segments from {segment_file}")
                return segments
            else:
                if hasattr(self, "logger"):
                    self.logger.warning(f"Client segments file not found: {segment_file}")
                return {}
        except Exception as e:
            if hasattr(self, "logger"):
                self.logger.error(f"Failed to load client segments: {e}")
            return {}

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
        
        # Log segment assignment
        segment_summary = [(k, len(v)) for k, v in self.agents_by_segment.items()]
        self.logger.info(f"Assigned agents to segments: {segment_summary}")

    def _determine_agent_segments(self, agent) -> List[str]:
        """Determine which segments an agent belongs to"""
        segments = []
        
        # High value retail
        if agent.client_type == "retail" and agent.income > 3000:
            segments.append("high_value_retail")
        
        # Young digital
        if agent.client_type == "retail" and agent.age < 35 and agent.digital_engagement_score > 0.6:
            segments.append("young_digital")
        
        # Large corporates
        if agent.client_type == "corporate" and getattr(agent, 'annual_revenue', 0) > 1000000:
            segments.append("large_corporates")
        
        # Tech companies
        if agent.client_type == "corporate" and getattr(agent, 'business_sector', '') in ['technology', 'IT', 'software']:
            segments.append("tech_companies")
        
        # Standard retail (fallback)
        if agent.client_type == "retail" and not segments:
            segments.append("standard_retail")
        
        # Standard corporate (fallback)
        if agent.client_type == "corporate" and not segments:
            segments.append("standard_corporate")
        
        # Geographic segments
        if hasattr(agent, 'governorate'):
            if agent.governorate.lower() in ['tunis', 'ariana', 'ben arous', 'manouba']:
                segments.append("urban_customers")
            elif agent.governorate.lower() == 'sfax':
                segments.append("sfax_clients")
        
        # Age-based segments
        if agent.client_type == "retail" and 25 <= agent.age <= 40:
            segments.append("young_professionals")
        
        return segments

    def create_social_networks(self):
        """Create social influence networks between agents"""
        # Simple network creation - agents influence nearby agents
        agents_list = list(self.agents)
        
        for agent in agents_list:
            agent.social_connections = []
            
            # Add 3-8 random connections
            num_connections = random.randint(3, 8)
            potential_connections = [a for a in agents_list if a != agent]
            
            if len(potential_connections) >= num_connections:
                connections = random.sample(potential_connections, num_connections)
                agent.social_connections = connections
        
        self.logger.info("Social networks created")

    def register_event_handlers(self):
        """Register handlers for different event types"""
        # Register handlers with the event system
        self.event_system.register_handler("MarketingCampaignEvent", self.handle_marketing_campaign)
        self.event_system.register_handler("BranchClosureEvent", self.handle_branch_closure)
        self.event_system.register_handler("DigitalTransformationEvent", self.handle_digital_transformation)
        self.event_system.register_handler("CompetitorActionEvent", self.handle_competitor_action)
        self.event_system.register_handler("EconomicShockEvent", self.handle_economic_shock)

    # ----------------------------------------------------------------
    # Event handlers
    # ----------------------------------------------------------------
    def handle_marketing_campaign(self, event: MarketingCampaignEvent):
        """Handle marketing campaign events"""
        self.logger.info(f"Processing MarketingCampaignEvent at step {self.current_step}")
        
        # Get target agents
        target_segment = event.parameters.get("target_segment", "all")
        target_agents = self.get_agents_by_segment(target_segment)
        
        # Apply marketing effect
        retention_boost = event.parameters.get("intensity", 1.0)
        affected_count = 0
        
        for agent in target_agents:
            agent.satisfaction_level += retention_boost * 0.1
            agent.satisfaction_level = min(agent.satisfaction_level, 1.0)
            affected_count += 1
        
        self.logger.info(f"Marketing campaign affected {affected_count} agents")

    def handle_branch_closure(self, event: BranchClosureEvent):
        """Handle branch closure events"""
        self.logger.info(f"Processing BranchClosureEvent at step {self.current_step}")
        
        # Reduce satisfaction for affected agents
        affected_governorate = event.parameters.get("affected_region", "")
        impact = event.parameters.get("impact_intensity", 0.2)
        
        affected_count = 0
        for agent in self.agents:
            if hasattr(agent, 'governorate') and agent.governorate.lower() == affected_governorate.lower():
                agent.satisfaction_level -= impact
                agent.satisfaction_level = max(agent.satisfaction_level, 0.0)
                affected_count += 1
        
        self.logger.info(f"Branch closure affected {affected_count} agents")

    def handle_digital_transformation(self, event: DigitalTransformationEvent):
        """Handle digital transformation events"""
        self.logger.info(f"Processing DigitalTransformationEvent at step {self.current_step}")
        
        # Increase digital engagement for all agents
        adoption_increase = event.parameters.get("adoption_increase", 0.3)
        
        for agent in self.agents:
            if hasattr(agent, 'digital_engagement_score'):
                agent.digital_engagement_score += adoption_increase * 0.1
                agent.digital_engagement_score = min(agent.digital_engagement_score, 1.0)

    def handle_competitor_action(self, event: CompetitorActionEvent):
        """Handle competitor action events"""
        self.logger.info(f"Processing CompetitorActionEvent at step {self.current_step}")
        
        # Reduce overall satisfaction
        impact = event.parameters.get("impact_intensity", 0.1)
        
        for agent in self.agents:
            agent.satisfaction_level -= impact * 0.5
            agent.satisfaction_level = max(agent.satisfaction_level, 0.0)

    def handle_economic_shock(self, event: EconomicShockEvent):
        """Handle economic shock events"""
        self.logger.info(f"Processing EconomicShockEvent at step {self.current_step}")
        
        # Adjust market conditions
        severity = event.parameters.get("severity", 0.5)
        self.economic_climate -= severity * 0.3
        self.market_volatility += severity * 0.2

    # ----------------------------------------------------------------
    # Utility methods
    # ----------------------------------------------------------------
    def get_agents_by_segment(self, segment_name: str) -> List:
        """Get all agents in a specific segment"""
        if segment_name == "all":
            return list(self.agents)
        return self.agents_by_segment.get(segment_name, [])

    def get_average_satisfaction(self) -> float:
        """Calculate average satisfaction across all agents"""
        if len(self.agents) == 0:
            return 0.0
        return sum(agent.satisfaction_level for agent in self.agents) / len(self.agents)

    def calculate_churn_rate(self) -> float:
        """Calculate current churn rate"""
        if len(self.agents) == 0:
            return 0.0
        
        churned_agents = sum(1 for agent in self.agents 
                           if hasattr(agent, 'churn_probability') and 
                           agent.churn_probability > 0.8)
        return churned_agents / len(self.agents)

    def get_digital_usage_rate(self) -> float:
        """Calculate average digital usage rate"""
        if len(self.agents) == 0:
            return 0.0
        
        total_digital = sum(getattr(agent, 'digital_engagement_score', 0.5) 
                          for agent in self.agents)
        return total_digital / len(self.agents)

    def count_active_products(self) -> int:
        """Count total active products across all agents"""
        return sum(len(getattr(agent, 'owned_products', [])) for agent in self.agents)

    def get_segment_satisfaction(self) -> Dict[str, float]:
        """Get average satisfaction by segment"""
        segment_satisfaction = {}
        
        for segment, agents in self.agents_by_segment.items():
            if agents:
                avg_satisfaction = sum(agent.satisfaction_level for agent in agents) / len(agents)
                segment_satisfaction[segment] = avg_satisfaction
            else:
                segment_satisfaction[segment] = 0.0
        
        return segment_satisfaction

    # ----------------------------------------------------------------
    # Market dynamics
    # ----------------------------------------------------------------
    def update_market_conditions(self):
        """Update market conditions"""
        # Random market fluctuations
        self.market_volatility += random.uniform(-0.05, 0.05)
        self.market_volatility = max(0.0, min(self.market_volatility, 1.0))
        
        # Economic climate recovery
        self.economic_climate += random.uniform(-0.02, 0.03)
        self.economic_climate = max(0.0, min(self.economic_climate, 1.0))

    def process_social_influence(self):
        """Process social influence between connected agents"""
        for agent in self.agents:
            if hasattr(agent, 'social_connections') and agent.social_connections:
                # Calculate average satisfaction of connections
                connection_satisfaction = sum(conn.satisfaction_level 
                                            for conn in agent.social_connections) / len(agent.social_connections)
                
                # Influence current agent (small effect)
                influence = (connection_satisfaction - agent.satisfaction_level) * 0.05
                agent.satisfaction_level += influence
                agent.satisfaction_level = max(0.0, min(agent.satisfaction_level, 1.0))

    def process_agent_interactions(self):
        """Process interactions between agents"""
        # Random agent interactions
        interaction_pairs = random.sample(list(self.agents), min(len(self.agents), 20))
        
        for i in range(0, len(interaction_pairs) - 1, 2):
            agent1 = interaction_pairs[i]
            agent2 = interaction_pairs[i + 1]
            
            # Small mutual influence
            satisfaction_diff = agent1.satisfaction_level - agent2.satisfaction_level
            influence = satisfaction_diff * 0.02
            
            agent1.satisfaction_level -= influence
            agent2.satisfaction_level += influence
            
            # Keep in bounds
            agent1.satisfaction_level = max(0.0, min(agent1.satisfaction_level, 1.0))
            agent2.satisfaction_level = max(0.0, min(agent2.satisfaction_level, 1.0))

    # ----------------------------------------------------------------
    # Scenario outcomes validation
    # ----------------------------------------------------------------
    def validate_scenario_outcomes(self):
        """Validate current metrics against scenario expected outcomes"""
        if not self.current_scenario or not hasattr(self.current_scenario, 'expected_outcomes'):
            return
            
        for outcome in self.current_scenario.expected_outcomes:
            if self.current_step in outcome.measurement_steps:
                # Get current metric value
                metric_value = self.get_metric_value(outcome.metric_name)

                # Validate
                valid = outcome.validate_outcome(metric_value, self.current_step)

                self.logger.info(
                    f"Outcome validation at step {self.current_step}: "
                    f"{outcome.metric_name} = {metric_value:.3f} "
                    f"(target: {outcome.target_value}, valid: {valid})"
                )

    def get_metric_value(self, metric_name: str) -> float:
        """Get current value of a specific metric"""
        metric_map = {
            "client_retention_rate": lambda: 1 - self.calculate_churn_rate(),
            "digital_adoption_increase": lambda: self.get_digital_usage_rate(),
            "customer_satisfaction_index": lambda: self.get_average_satisfaction(),
            "churn_rate": lambda: self.calculate_churn_rate(),
            "digital_adoption_rate": lambda: self.get_digital_usage_rate(),
            "avg_satisfaction": lambda: self.get_average_satisfaction(),
        }

        if metric_name in metric_map:
            return metric_map[metric_name]()
        return 0.0

    # ----------------------------------------------------------------
    # Scenario reporting
    # ----------------------------------------------------------------
    def generate_scenario_report(self) -> Dict[str, Any]:
        """Generate report for scenario execution"""
        if not self.current_scenario:
            self.logger.warning("No current scenario to generate report for")
            return {}
        
        report = {
            "scenario_name": self.current_scenario.metadata.name,
            "total_steps": self.current_step,
            "events_processed": len(self.event_system.processed_events),
            "final_metrics": {
                "average_satisfaction": self.get_average_satisfaction(),
                "churn_rate": self.calculate_churn_rate(),
                "digital_usage": self.get_digital_usage_rate(),
                "active_products": self.count_active_products(),
            },
            "segment_performance": self.get_segment_satisfaction(),
            "outcome_validation": [],
        }

        # Validate all outcomes
        if hasattr(self.current_scenario, 'expected_outcomes'):
            for outcome in self.current_scenario.expected_outcomes:
                metric_value = self.get_metric_value(outcome.metric_name)
                valid = outcome.validate_outcome(metric_value, self.current_step)
                report["outcome_validation"].append({
                    "metric": outcome.metric_name,
                    "target": outcome.target_value,
                    "actual": metric_value,
                    "valid": valid,
                })

        # Save report
        report_file = Path("simulation_outputs") / f"{self.current_scenario.metadata.name.replace(' ', '_').lower()}_report.json"
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        self.logger.info(f"Scenario report saved to {report_file}")
        return report

    # ----------------------------------------------------------------
    # Main simulation step
    # ----------------------------------------------------------------
    def step(self):
        """Execute one simulation step"""
        step_start_time = time.time()

        # 1. PROCESS SCENARIO EVENTS
        if self.current_scenario:
            processed_events = self.event_system.process_events(self.current_step)
            if processed_events:
                self.logger.info(
                    f"Processed {len(processed_events)} events at step {self.current_step}"
                )

        # 2. UPDATE ACTIVE EVENT EFFECTS
        self.update_active_event_effects()

        # 3. UPDATE MARKET CONDITIONS
        self.update_market_conditions()

        # 4. ACTIVATE ALL AGENTS (Mesa 3.x)
        self.agents.shuffle_do("step")

        # 5. PROCESS SOCIAL INFLUENCE
        self.process_social_influence()

        # 6. PROCESS AGENT INTERACTIONS
        if self.current_step % 3 == 0:
            self.process_agent_interactions()

        # 7. COLLECT DATA
        self.datacollector.collect(self)

        # 8. CHECK SCENARIO OUTCOMES (if scenario is running)
        if self.current_scenario and hasattr(self.current_scenario, "expected_outcomes"):
            self.validate_scenario_outcomes()

        # 9. CHECK TERMINATION CONDITIONS
        if self.current_step >= self.time_steps:
            self.running = False
            self.logger.info(f"Simulation completed after {self.current_step} steps")

        # 10. PERFORMANCE TRACKING
        step_duration = time.time() - step_start_time
        if step_duration > 1.0:
            self.logger.warning(f"Step {self.current_step} took {step_duration:.2f} seconds")

        self.current_step += 1

        # 11. PERIODIC LOGGING
        if self.current_step % 10 == 0:
            self.log_simulation_status()

    def update_active_event_effects(self):
        """Update and remove expired active events"""
        expired_events: List[str] = []

        for event_id, event_info in list(self.active_events.items()):
            # Check if event has expired
            if "duration" in event_info:
                if self.current_step - event_info["step_started"] >= event_info["duration"]:
                    expired_events.append(event_id)

        # Remove expired events
        for event_id in expired_events:
            del self.active_events[event_id]
            self.logger.debug(f"Event {event_id} expired at step {self.current_step}")

    def log_simulation_status(self):
        """Log current simulation status"""
        metrics = self.collect_simulation_metrics()
        
        self.logger.info(
            f"Step {self.current_step}: {len(self.agents)} agents "
            f"({len([a for a in self.agents if a.client_type == 'retail'])}R/"
            f"{len([a for a in self.agents if a.client_type == 'corporate'])}C), "
            f"satisfaction={metrics['agent_metrics']['avg_satisfaction']:.2f}, "
            f"churn={metrics['agent_metrics']['churn_rate']:.2f}, "
            f"digital={metrics['agent_metrics']['digital_usage']:.2f}, "
            f"products={metrics['agent_metrics']['active_products']}"
        )

    def collect_simulation_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive simulation metrics"""
        return {
            "agent_metrics": {
                "avg_satisfaction": self.get_average_satisfaction(),
                "churn_rate": self.calculate_churn_rate(),
                "digital_usage": self.get_digital_usage_rate(),
                "active_products": self.count_active_products(),
            },
            "segment_metrics": {
                segment: {
                    "count": len(agents),
                    "avg_satisfaction": sum(a.satisfaction_level for a in agents) / len(agents) if agents else 0,
                    "churn_rate": sum(1 for a in agents if getattr(a, 'churn_probability', 0) > 0.8) / len(agents) if agents else 0,
                }
                for segment, agents in self.agents_by_segment.items()
            },
            "market_conditions": {
                "volatility": self.market_volatility,
                "economic_climate": self.economic_climate,
            }
        }

    # ----------------------------------------------------------------
    # Data export methods
    # ----------------------------------------------------------------
    def export_agent_data(self) -> pd.DataFrame:
        """Export agent data to DataFrame"""
        agent_data = []
        
        for agent in self.agents:
            data = {
                "unique_id": agent.unique_id,
                "client_type": agent.client_type,
                "age": agent.age,
                "income": agent.income,
                "satisfaction_level": agent.satisfaction_level,
                "digital_engagement_score": getattr(agent, 'digital_engagement_score', 0.5),
                "governorate": getattr(agent, 'governorate', 'Unknown'),
                "owned_products": len(getattr(agent, 'owned_products', [])),
            }
            
            # Add corporate-specific data
            if agent.client_type == "corporate":
                data.update({
                    "annual_revenue": getattr(agent, 'annual_revenue', 0),
                    "business_sector": getattr(agent, 'business_sector', 'Unknown'),
                    "company_name": getattr(agent, 'company_name', 'Unknown'),
                })
            
            agent_data.append(data)
        
        return pd.DataFrame(agent_data)

    def export_simulation_data(self) -> Dict[str, pd.DataFrame]:
        """Export all simulation data"""
        return {
            "agents": self.export_agent_data(),
            "model_data": self.datacollector.get_model_vars_dataframe(),
            "agent_data": self.datacollector.get_agent_vars_dataframe(),
        }