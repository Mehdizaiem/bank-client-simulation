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

        # Agent tracking (our own lists, since Mesa's agents_by_type is read-only)
        self.our_agents_by_type: Dict[str, List[mesa.Agent]] = {
            "retail": [],
            "corporate": [],
        }

        # CLIENT SEGMENTS (from Maryem's segments)
        self.client_segments = self.load_client_segments()
        self.agents_by_segment: Dict[str, List[mesa.Agent]] = {
            "high_value_retail": [],
            "young_digital": [],
            "large_corporates": [],
            "tech_companies": [],
            "standard_retail": [],
            "standard_corporate": [],
        }

        # EVENT SYSTEM INTEGRATION
        self.event_system = EventSystem()
        self.scenario_manager = ScenarioManager()
        self.current_scenario: Optional[Scenario] = None
        self.active_events: Dict[str, Dict[str, Any]] = {}  # Track active events and their effects

        # MARKET CONDITIONS
        self.market_conditions = {
            "interest_rate": 0.05,
            "economic_growth": 0.02,
            "inflation_rate": 0.03,
            "unemployment_rate": 0.15,  # Tunisia context
        }

        # DATA LOADING
        self.data_loader = AgentDataLoader()

        # DATA COLLECTION
        self.datacollector = DataCollector(
            model_reporters={
                "Total_Agents": lambda m: len(m.agents),
                "Average_Satisfaction": self.get_average_satisfaction,
                "Churn_Rate": self.calculate_churn_rate,
                "Active_Products": self.count_active_products,
                "Digital_Channel_Usage": self.get_digital_usage_rate,
                "Retail_Count": lambda m: len(m.our_agents_by_type["retail"]),
                "Corporate_Count": lambda m: len(m.our_agents_by_type["corporate"]),
                # Scenario-specific metrics
                "Active_Events": lambda m: len(m.active_events),
                "Campaign_Impact": self.get_campaign_impact,
                "Segment_Satisfaction": self.get_segment_satisfaction,
            },
            agent_reporters={
                "Satisfaction": "satisfaction_level",
                "Products_Count": lambda a: len(getattr(a, "current_products", [])),
                "Channel_Preference": lambda a: getattr(a, "primary_channel", "unknown"),
                "Considering_Churn": lambda a: getattr(a, "considering_churn", False),
                "Client_Type": lambda a: getattr(a, "client_type", "unknown"),
                "Segment": lambda a: getattr(a, "segment", "standard"),
            },
        )

        # Load scenario if provided
        if scenario_file:
            self.load_and_prepare_scenario(scenario_file)

        # Load agents
        self.load_agents_from_csv()

        # Assign agents to segments
        self.assign_agents_to_segments()

        # Create social networks
        self.create_social_networks()

        # Register event handlers
        self.register_event_handlers()

        self.logger.info(f"Model initialization complete with {len(self.agents)} agents\n")

    # ---------------------------------------------------------------------
    # Initialization helpers
    # ---------------------------------------------------------------------
    def setup_logging(self):
        """Setup logging system"""
        import os

        os.makedirs("logs", exist_ok=True)
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
                # logger may not be ready if this is called super-early; guard it
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
        """Load a scenario and prepare it for execution - ENHANCED"""
        try:
            self.current_scenario = self.scenario_manager.load_scenario(scenario_file)
            
            if self.current_scenario:
                scenario_params = self.current_scenario.simulation_parameters
                self.time_steps = scenario_params.duration_steps
                self.num_agents = scenario_params.agent_population
                
                self.logger.info(f"Loaded scenario: {self.current_scenario.metadata.name}")
                self.logger.info(f"Scenario duration: {self.time_steps} steps")
                self.logger.info(f"Scenario events: {len(self.current_scenario.events)}")
                
                # Pre-inject all scenario events with enhanced error handling
                successful_injections = 0
                failed_injections = []
                
                for event in self.current_scenario.events:
                    try:
                        base_event = event.to_base_event()
                        if self.event_system.inject_event(base_event):
                            successful_injections += 1
                        else:
                            failed_injections.append(event.event_type)
                    except Exception as e:
                        self.logger.warning(f"Failed to inject event {event.event_type}: {e}")
                        failed_injections.append(event.event_type)
                
                self.logger.info(f"Successfully injected {successful_injections}/{len(self.current_scenario.events)} events")
                if failed_injections:
                    self.logger.warning(f"Failed to inject events: {failed_injections}")
                    
        except Exception as e:
            self.logger.error(f"Failed to load scenario {scenario_file}: {e}")
            self.current_scenario = None

    def load_agents_from_csv(self):
        """Load agents from CSV files and create agent objects"""
        self.logger.info("Loading agents from CSV files...")

        loaded_agent_data = self.data_loader.load_all_agents(
            num_agents=self.num_agents, retail_ratio=self.retail_ratio
        )

        if not loaded_agent_data:
            self.logger.warning("No agent data loaded from CSV files! Creating synthetic agents...")
            self.create_synthetic_agents()
            return

        retail_created = 0
        corporate_created = 0

        for agent_data in loaded_agent_data:
            try:
                if agent_data["client_type"] == "retail":
                    agent = RetailClientAgent(self, agent_data)
                    retail_created += 1
                else:  # corporate
                    agent = CorporateClientAgent(self, agent_data)
                    corporate_created += 1

                # Track in our custom lists
                self.our_agents_by_type[agent.client_type].append(agent)
                self.total_agents_created += 1

            except Exception as e:
                self.logger.error(f"Error creating agent from data: {e}")
                continue

        # Log statistics
        stats = self.data_loader.get_statistics()
        self.logger.info(
            f"Created {self.total_agents_created} agents from CSV: retail={retail_created}, corporate={corporate_created}"
        )
        if "retail" in stats:
            self.logger.info(
                f"  Retail stats: avg age={stats['retail']['avg_age']:.1f}, avg income={stats['retail']['avg_income']:.0f} TND"
            )
        if "corporate" in stats:
            self.logger.info(
                f"  Corporate stats: avg revenue={stats['corporate']['avg_revenue']:.0f} TND, sectors={len(stats['corporate']['sectors'])} unique"
            )

    def create_synthetic_agents(self):
        """Fallback: Create synthetic agents if CSV loading fails"""
        self.logger.info("Creating synthetic agents as fallback...")

        num_retail = int(self.num_agents * self.retail_ratio)
        num_corporate = self.num_agents - num_retail

        # Synthetic retail
        for i in range(num_retail):
            agent_data = {
                "client_id": f"R_SYNTH_{i}",
                "age": random.randint(18, 70),
                "governorate": random.choice(["Tunis", "Sfax", "Sousse", "Kairouan", "Bizerte"]),
                "monthly_income": random.uniform(800, 5000),
                "risk_tolerance": random.uniform(0.2, 0.8),
                "satisfaction_score": random.uniform(0.4, 0.8),
                "digital_engagement_score": random.uniform(0.2, 0.9),
                "preferred_channel": random.choice(["branch", "mobile", "online"]),
                "client_type": "retail",
            }
            agent = RetailClientAgent(self, agent_data)
            self.our_agents_by_type["retail"].append(agent)

        # Synthetic corporate
        for i in range(num_corporate):
            agent_data = {
                "client_id": f"C_SYNTH_{i}",
                "company_name": f"Company_{i}",
                "business_sector": random.choice(["services", "manufacturing", "retail", "technology"]),
                "company_size": random.choice(["small", "medium", "large"]),
                "annual_revenue": random.uniform(100_000, 5_000_000),
                "digital_maturity_score": random.uniform(0.3, 0.9),
                "headquarters_governorate": random.choice(["Tunis", "Sfax", "Sousse"]),
                "client_type": "corporate",
            }
            agent = CorporateClientAgent(self, agent_data)
            self.our_agents_by_type["corporate"].append(agent)

        self.total_agents_created = num_retail + num_corporate
        self.logger.info(f"Created {self.total_agents_created} synthetic agents")

    def create_social_networks(self):
        """Create social/business networks between agents"""
        self.logger.info("Creating social networks...")

        # Retail agents have denser social networks
        for agent in self.our_agents_by_type["retail"]:
            # Each retail agent connects to 2-5 other retail agents, preferring same governorate
            num_connections = random.randint(2, 5)

            same_gov = [a for a in self.our_agents_by_type["retail"] if a.governorate == agent.governorate and a is not agent]
            if same_gov:
                take_local = min(max(0, num_connections - 1), len(same_gov))
                agent.social_network.extend(random.sample(same_gov, take_local))

            others = [a for a in self.our_agents_by_type["retail"] if a is not agent and a not in agent.social_network]
            if others:
                take_other = min(1, len(others))
                agent.social_network.extend(random.sample(others, take_other))

        # Corporate agents connect within sector (1-3)
        for agent in self.our_agents_by_type["corporate"]:
            num_connections = random.randint(1, 3)
            same_sector = [a for a in self.our_agents_by_type["corporate"] if a.business_sector == agent.business_sector and a is not agent]
            if same_sector:
                take = min(num_connections, len(same_sector))
                agent.social_network.extend(random.sample(same_sector, take))

        self.logger.info("Social networks created")

    def register_event_handlers(self):
        """Register handlers for different event types"""

        # Marketing Campaign Handler
        def handle_marketing_campaign(event: BaseEvent):
            self.logger.info(f"Processing MarketingCampaignEvent at step {self.current_step}")

            target_segment = event.parameters.get("target_segment", "all_clients")
            intensity = event.parameters.get("intensity", 0.5)
            channels = event.parameters.get("channels", [])

            # Get target agents based on segment
            target_agents = self.get_agents_by_segment(target_segment)

            # Apply campaign effects
            for agent in target_agents:
                # Increase satisfaction based on intensity
                satisfaction_boost = intensity * 0.3
                agent.satisfaction_level = min(1.0, agent.satisfaction_level + satisfaction_boost)

                # If campaign uses agent's preferred channel, extra boost
                if getattr(agent, "primary_channel", None) in channels:
                    agent.satisfaction_level = min(1.0, agent.satisfaction_level + 0.1)

                # Add experience
                agent.add_experience(
                    "marketing_campaign",
                    getattr(agent, "primary_channel", "branch"),
                    0.5 + intensity * 0.5,
                    f"Campaign: {event.parameters.get('message', '')}",
                )

            # Track campaign in active events
            self.active_events[event.event_id] = {
                "type": "marketing_campaign",
                "step_started": self.current_step,
                "duration": event.parameters.get("duration", 10),
                "affected_agents": len(target_agents),
            }

            self.logger.info(f"Marketing campaign affected {len(target_agents)} agents")

        # Branch Closure Handler
        def handle_branch_closure(event: BaseEvent):
            self.logger.info(f"Processing BranchClosureEvent at step {self.current_step}")

            location = event.parameters.get("location", "")
            digital_migration_support = event.parameters.get("digital_migration_support", False)

            # Get affected agents
            affected_agents = [
                a for a in self.agents if hasattr(a, "governorate") and a.governorate == location
            ]

            for agent in affected_agents:
                # Negative impact on satisfaction
                agent.satisfaction_level = max(0, agent.satisfaction_level - 0.2)

                # If digital migration support, boost digital channel preference
                if digital_migration_support and hasattr(agent, "channel_preferences"):
                    agent.channel_preferences["mobile"] = agent.channel_preferences.get("mobile", 0.1) + 0.2
                    agent.channel_preferences["online"] = agent.channel_preferences.get("online", 0.1) + 0.1
                    agent.channel_preferences["branch"] = max(
                        0.1, agent.channel_preferences.get("branch", 0.1) - 0.3
                    )

                    # Normalize
                    total = sum(agent.channel_preferences.values())
                    agent.channel_preferences = {k: v / total for k, v in agent.channel_preferences.items()}
                    agent.primary_channel = max(agent.channel_preferences, key=agent.channel_preferences.get)

                # Some agents may consider churning
                if agent.satisfaction_level < 0.3:
                    agent.considering_churn = True

            self.active_events[event.event_id] = {
                "type": "branch_closure",
                "step_started": self.current_step,
                "location": location,
                "affected_agents": len(affected_agents),
            }

            self.logger.info(f"Branch closure in {location} affected {len(affected_agents)} agents")

        # Digital Transformation Handler
        def handle_digital_transformation(event: BaseEvent):
            self.logger.info(f"Processing DigitalTransformationEvent at step {self.current_step}")

            service_type = event.parameters.get("service_type", "")
            user_experience_score = event.parameters.get("user_experience_score", 0.7)
            target_regions = event.parameters.get("target_regions", [])

            # Get target agents
            if target_regions:
                target_agents = [
                    a for a in self.agents if hasattr(a, "governorate") and a.governorate in target_regions
                ]
            else:
                target_agents = list(self.agents)

            # Apply digital transformation effects
            for agent in target_agents:
                # Increase digital engagement for retail agents
                if hasattr(agent, "digital_engagement_score"):
                    agent.digital_engagement_score = min(1.0, agent.digital_engagement_score + 0.2)

                # Increase satisfaction based on UX score
                satisfaction_boost = user_experience_score * 0.2
                agent.satisfaction_level = min(1.0, agent.satisfaction_level + satisfaction_boost)

                # Shift channel preferences toward digital
                if hasattr(agent, "channel_preferences"):
                    agent.channel_preferences["mobile"] = agent.channel_preferences.get("mobile", 0.1) + 0.1
                    agent.channel_preferences["online"] = agent.channel_preferences.get("online", 0.1) + 0.1
                    total = sum(agent.channel_preferences.values())
                    agent.channel_preferences = {k: v / total for k, v in agent.channel_preferences.items()}
                    agent.primary_channel = max(agent.channel_preferences, key=agent.channel_preferences.get)

            self.active_events[event.event_id] = {
                "type": "digital_transformation",
                "step_started": self.current_step,
                "service": service_type,
                "affected_agents": len(target_agents),
            }

        # Competitor Action Handler
        def handle_competitor_action(event: BaseEvent):
            self.logger.info(f"Processing CompetitorActionEvent at step {self.current_step}")

            affected_region = event.parameters.get("affected_region", "")
            impact_intensity = event.parameters.get("impact_intensity", 0.5)

            # Get affected agents
            affected_agents = [
                a for a in self.agents if hasattr(a, "governorate") and a.governorate == affected_region
            ]

            for agent in affected_agents:
                # Negative impact on satisfaction and loyalty
                impact = impact_intensity * random.uniform(0.1, 0.3)
                agent.satisfaction_level = max(0, agent.satisfaction_level - impact)

                if hasattr(agent, "brand_loyalty"):
                    agent.brand_loyalty = max(0, agent.brand_loyalty - impact * 0.5)

                # Some agents may consider switching
                if agent.satisfaction_level < 0.4 and random.random() < impact_intensity * 0.2:
                    agent.considering_churn = True

            self.active_events[event.event_id] = {
                "type": "competitor_action",
                "step_started": self.current_step,
                "duration": event.parameters.get("duration", 10),
                "affected_agents": len(affected_agents),
            }

        # Economic Shock Handler
        def handle_economic_shock(event: BaseEvent):
            self.logger.info(f"Processing EconomicShockEvent at step {self.current_step}")

            severity = event.parameters.get("severity", 0.5)
            affected_sectors = event.parameters.get("affected_sectors", [])

            # Update market conditions
            self.market_conditions["economic_growth"] -= severity * 0.05
            self.market_conditions["unemployment_rate"] += severity * 0.05

            # Affect agents based on their sector
            for agent in self.agents:
                if hasattr(agent, "employment_sector") and agent.employment_sector in affected_sectors:
                    impact = severity * 0.3
                elif hasattr(agent, "business_sector") and agent.business_sector in affected_sectors:
                    impact = severity * 0.4
                else:
                    impact = severity * 0.1  # General economic impact

                # Reduce satisfaction and increase risk aversion
                agent.satisfaction_level = max(0, agent.satisfaction_level - impact)

                if hasattr(agent, "risk_tolerance"):
                    agent.risk_tolerance = max(0.1, agent.risk_tolerance - impact * 0.5)

            self.active_events[event.event_id] = {
                "type": "economic_shock",
                "step_started": self.current_step,
                "duration": event.parameters.get("duration", 20),
                "severity": severity,
            }

        # Register all handlers
        self.event_system.register_event_handler("MarketingCampaignEvent", handle_marketing_campaign)
        self.event_system.register_event_handler("BranchClosureEvent", handle_branch_closure)
        self.event_system.register_event_handler("DigitalTransformationEvent", handle_digital_transformation)
        self.event_system.register_event_handler("CompetitorActionEvent", handle_competitor_action)
        self.event_system.register_event_handler("EconomicShockEvent", handle_economic_shock)

    # ---------------------------------------------------------------------
    # Segments & helpers
    # ---------------------------------------------------------------------
    def get_agents_by_segment(self, segment: str) -> List[mesa.Agent]:
        """Get agents belonging to a specific segment or category"""
        if segment == "all_clients":
            return list(self.agents)
        elif segment == "young_professionals":
            return [
                a
                for a in self.agents
                if hasattr(a, "age")
                and a.age < 35
                and hasattr(a, "income")
                and a.income > 1500
            ]
        elif segment == "urban_customers":
            urban_govs = ["Tunis", "Sfax", "Sousse", "Ariana", "Ben Arous"]
            return [a for a in self.agents if hasattr(a, "governorate") and a.governorate in urban_govs]
        elif segment == "savings_clients":
            return [a for a in self.agents if hasattr(a, "current_products") and "savings_account" in a.current_products]
        elif segment == "sfax_clients":
            return [a for a in self.agents if hasattr(a, "governorate") and a.governorate == "Sfax"]
        elif segment in self.agents_by_segment:
            return self.agents_by_segment[segment]
        else:
            # Try to match by governorate
            return [
                a
                for a in self.agents
                if hasattr(a, "governorate") and a.governorate.lower() == segment.lower()
            ]

    def assign_agents_to_segments(self):
        """Assign agents to segments based on Maryem's segmentation"""
        # High value retail
        if "high_value_retail" in self.client_segments:
            for agent_id in self.client_segments["high_value_retail"]:
                agent = self.find_agent_by_original_id(agent_id)
                if agent:
                    agent.segment = "high_value_retail"
                    self.agents_by_segment["high_value_retail"].append(agent)

        # Young digital
        if "young_digital" in self.client_segments:
            for agent_id in self.client_segments["young_digital"]:
                agent = self.find_agent_by_original_id(agent_id)
                if agent:
                    agent.segment = "young_digital"
                    self.agents_by_segment["young_digital"].append(agent)

        # Large corporates
        if "large_corporates" in self.client_segments:
            for agent_id in self.client_segments["large_corporates"]:
                agent = self.find_agent_by_original_id(agent_id)
                if agent:
                    agent.segment = "large_corporates"
                    self.agents_by_segment["large_corporates"].append(agent)

        # Tech companies
        if "tech_companies" in self.client_segments:
            for agent_id in self.client_segments["tech_companies"]:
                agent = self.find_agent_by_original_id(agent_id)
                if agent:
                    agent.segment = "tech_companies"
                    self.agents_by_segment["tech_companies"].append(agent)

        # Assign remaining agents to standard segments
        for agent in self.agents:
            if not hasattr(agent, "segment"):
                if getattr(agent, "client_type", "retail") == "retail":
                    agent.segment = "standard_retail"
                    self.agents_by_segment["standard_retail"].append(agent)
                else:
                    agent.segment = "standard_corporate"
                    self.agents_by_segment["standard_corporate"].append(agent)

        self.logger.info(
            "Assigned agents to segments: "
            + str([(k, len(v)) for k, v in self.agents_by_segment.items()])
        )

    def find_agent_by_original_id(self, original_id: str) -> Optional[mesa.Agent]:
        """Find agent by their original CSV ID"""
        for agent in self.agents:
            if hasattr(agent, "original_client_id") and agent.original_client_id == original_id:
                return agent
        return None

    # ---------------------------------------------------------------------
    # Simulation loop
    # ---------------------------------------------------------------------
    def step(self):
        """Execute one simulation time step with event processing"""
        step_start_time = time.time()

        self.logger.debug(f"Starting simulation step {self.current_step}")

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
        if self.current_scenario and getattr(self.current_scenario, "expected_outcomes", None):
            self.validate_scenario_outcomes()

        # 9. CHECK TERMINATION CONDITIONS
        if self.current_step >= self.time_steps:
            self.running = False
            self.logger.info(f"Simulation completed after {self.current_step} steps")

            # Generate scenario report if applicable
            if self.current_scenario:
                self.generate_scenario_report()

        # 10. PERFORMANCE TRACKING
        step_duration = time.time() - step_start_time
        if step_duration > 1.0:
            self.logger.warning(f"Step {self.current_step} took {step_duration:.2f} seconds")

        self.current_step += 1

        # 11. PERIODIC LOGGING
        if self.current_step % 10 == 0:
            self.log_simulation_status()

    # ---------------------------------------------------------------------
    # Dynamics
    # ---------------------------------------------------------------------
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

    def validate_scenario_outcomes(self):
        """Validate current metrics against scenario expected outcomes"""
        for outcome in self.current_scenario.expected_outcomes:
            if self.current_step in outcome.measurement_steps:
                # Get current metric value
                metric_value = self.get_metric_value(outcome.metric_name)

                # Validate
                valid = outcome.validate_outcome(metric_value, self.current_step)

                self.logger.info(
                    f"Outcome validation at step {self.current_step}: "
                    f"{outcome.metric_name} = {metric_value} "
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

    # ---------------------------------------------------------------------
    # Metrics helpers
    # ---------------------------------------------------------------------
    def get_campaign_impact(self) -> float:
        """Calculate current campaign impact"""
        campaign_events = [e for e in self.active_events.values() if e["type"] == "marketing_campaign"]
        if campaign_events and len(self.agents) > 0:
            return sum(e.get("affected_agents", 0) for e in campaign_events) / len(self.agents)
        return 0.0

    def get_segment_satisfaction(self) -> Dict[str, float]:
        """Get satisfaction by segment"""
        segment_satisfaction: Dict[str, float] = {}
        for segment_name, agents in self.agents_by_segment.items():
            if agents:
                avg_satisfaction = sum(a.satisfaction_level for a in agents) / len(agents)
                segment_satisfaction[segment_name] = avg_satisfaction
        return segment_satisfaction

    def get_average_satisfaction(self) -> float:
        if not self.agents or len(self.agents) == 0:
            return 0.5
        vals = [a.satisfaction_level for a in self.agents if hasattr(a, "satisfaction_level")]
        return sum(vals) / len(vals) if vals else 0.5

    def calculate_churn_rate(self) -> float:
        if not self.agents or len(self.agents) == 0:
            return 0.0
        churning = len(
            self.agents.select(lambda a: hasattr(a, "considering_churn") and a.considering_churn)
        )
        return churning / len(self.agents)

    def count_active_products(self) -> int:
        return sum(len(getattr(a, "current_products", [])) for a in self.agents)

    def get_digital_usage_rate(self) -> float:
        if not self.agents or len(self.agents) == 0:
            return 0.0
        digital_users = len(
            self.agents.select(
                lambda a: hasattr(a, "primary_channel")
                and a.primary_channel in ["online", "mobile", "whatsapp"]
            )
        )
        return digital_users / len(self.agents)

    # ---------------------------------------------------------------------
    # Market & interactions
    # ---------------------------------------------------------------------
    def update_market_conditions(self):
        """Update global market conditions that affect all agents"""
        # Small random walk for market conditions
        self.market_conditions["interest_rate"] += random.uniform(-0.001, 0.001)
        self.market_conditions["economic_growth"] += random.uniform(-0.002, 0.002)
        self.market_conditions["inflation_rate"] += random.uniform(-0.001, 0.001)

        # Keep within reasonable bounds
        self.market_conditions["interest_rate"] = max(0.01, min(0.15, self.market_conditions["interest_rate"]))
        self.market_conditions["economic_growth"] = max(-0.05, min(0.10, self.market_conditions["economic_growth"]))
        self.market_conditions["inflation_rate"] = max(0.0, min(0.20, self.market_conditions["inflation_rate"]))

        # Economic growth affects unemployment
        if self.market_conditions["economic_growth"] > 0.03:
            self.market_conditions["unemployment_rate"] *= 0.99
        elif self.market_conditions["economic_growth"] < 0:
            self.market_conditions["unemployment_rate"] *= 1.01

        self.market_conditions["unemployment_rate"] = max(
            0.05, min(0.30, self.market_conditions["unemployment_rate"])
        )

    def process_social_influence(self):
        """Handle social influence between agents"""
        if self.current_step % 5 == 0:
            self.logger.debug("Processing social influence")
            changed_agents = self.agents.select(
                lambda a: hasattr(a, "satisfaction_changed") and a.satisfaction_changed
            )
            for agent in changed_agents:
                if hasattr(agent, "social_network"):
                    agent.propagate_influence()
                    agent.satisfaction_changed = False

    def process_agent_interactions(self):
        """Process interactions between agents"""
        if len(self.agents) > 10:
            interacting_agents = random.sample(list(self.agents), min(20, len(self.agents)))
            for agent in interacting_agents:
                if hasattr(agent, "social_network") and agent.social_network:
                    agent.learn_from_social_network()

    # ---------------------------------------------------------------------
    # Reporting & export
    # ---------------------------------------------------------------------
    def log_simulation_status(self):
        status = {
            "step": self.current_step,
            "agents": len(self.agents),
            "retail": len(self.our_agents_by_type["retail"]),
            "corporate": len(self.our_agents_by_type["corporate"]),
            "avg_satisfaction": self.get_average_satisfaction(),
            "churn_rate": self.calculate_churn_rate(),
            "digital_usage": self.get_digital_usage_rate(),
            "active_products": self.count_active_products(),
        }
        self.logger.info(
            f"Step {status['step']}: {status['agents']} agents ("
            f"{status['retail']}R/{status['corporate']}C), "
            f"satisfaction={status['avg_satisfaction']:.2f}, "
            f"churn={status['churn_rate']:.2f}, "
            f"digital={status['digital_usage']:.2f}, "
            f"products={status['active_products']}"
        )

        if self.current_step % 50 == 0:
            self.logger.info(
                "Market conditions: "
                f"interest={self.market_conditions['interest_rate']:.3f}, "
                f"growth={self.market_conditions['economic_growth']:.3f}, "
                f"inflation={self.market_conditions['inflation_rate']:.3f}, "
                f"unemployment={self.market_conditions['unemployment_rate']:.3f}"
            )

    def export_agent_data(self) -> pd.DataFrame:
        data = []
        for agent in self.agents:
            if hasattr(agent, "get_export_data"):
                data.append(agent.get_export_data())
        return pd.DataFrame(data)

    def export_historical_data(self) -> pd.DataFrame:
        return self.datacollector.get_model_vars_dataframe()

    def export_detailed_results(self, output_dir: str = "results") -> Dict[str, str]:
        import os

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Export summary (lightweight)
        summary = {
            "total_steps": self.current_step,
            "total_agents": len(self.agents),
            "retail_agents": len(self.our_agents_by_type["retail"]),
            "corporate_agents": len(self.our_agents_by_type["corporate"]),
            "avg_satisfaction": self.get_average_satisfaction(),
            "churn_rate": self.calculate_churn_rate(),
            "digital_usage": self.get_digital_usage_rate(),
            "market_conditions": self.market_conditions.copy(),
        }
        with open(output_path / f"summary_{timestamp}.json", "w") as f:
            json.dump(summary, f, indent=2)

        # Export agent data & history
        self.export_agent_data().to_csv(output_path / f"agents_{timestamp}.csv", index=False)
        self.export_historical_data().to_csv(output_path / f"history_{timestamp}.csv", index=False)

        self.logger.info(f"Results exported to {output_path}")
        return {
            "summary_file": f"summary_{timestamp}.json",
            "agents_file": f"agents_{timestamp}.csv",
            "history_file": f"history_{timestamp}.csv",
        }

def get_enhanced_metrics(self) -> Dict[str, Any]:
    """Get comprehensive metrics for analysis"""
    metrics = {
        'timestamp': datetime.now().isoformat(),
        'step': self.current_step,
        'agent_metrics': {
            'total_agents': len(self.agents),
            'retail_agents': len(self.our_agents_by_type['retail']),
            'corporate_agents': len(self.our_agents_by_type['corporate']),
            'avg_satisfaction': self.get_average_satisfaction(),
            'churn_rate': self.calculate_churn_rate(),
            'digital_usage': self.get_digital_usage_rate(),
            'active_products': self.count_active_products()
        },
        'segment_metrics': {
            segment: {
                'count': len(agents),
                'avg_satisfaction': sum(a.satisfaction_level for a in agents) / len(agents) if agents else 0,
                'churn_rate': sum(1 for a in agents if getattr(a, 'considering_churn', False)) / len(agents) if agents else 0
            }
            for segment, agents in self.agents_by_segment.items()
        },
        'market_conditions': self.market_conditions.copy(),
        'active_events': len(self.active_events),
        'scenario_info': {
            'name': self.current_scenario.metadata.name if self.current_scenario else None,
            'events_processed': len(self.event_system.processed_events),
            'events_pending': len(self.event_system.event_queue)
        }
    }
    
    return metrics


def log_simulation_status(self):
    """Enhanced simulation status logging"""
    metrics = self.get_enhanced_metrics()
    
    self.logger.info(
        f"Step {self.current_step}: "
        f"{metrics['agent_metrics']['total_agents']} agents "
        f"({metrics['agent_metrics']['retail_agents']}R/"
        f"{metrics['agent_metrics']['corporate_agents']}C), "
        f"satisfaction={metrics['agent_metrics']['avg_satisfaction']:.2f}, "
        f"churn={metrics['agent_metrics']['churn_rate']:.2f}, "
        f"digital={metrics['agent_metrics']['digital_usage']:.2f}, "
        f"products={metrics['agent_metrics']['active_products']}"
    )
    
    # Log segment performance
    if self.current_step % 20 == 0:
        self.logger.info("Segment performance:")
        for segment, metrics_data in metrics['segment_metrics'].items():
            if metrics_data['count'] > 0:
                self.logger.info(
                    f"  {segment}: {metrics_data['count']} agents, "
                    f"satisfaction={metrics_data['avg_satisfaction']:.2f}, "
                    f"churn={metrics_data['churn_rate']:.2f}"
                )

    # ---------------------------------------------------------------------
    # Scenario reporting
    # ---------------------------------------------------------------------
    def generate_scenario_report(self) -> Dict[str, Any]:
        """Generate report for scenario execution"""
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
        for outcome in self.current_scenario.expected_outcomes:
            metric_value = self.get_metric_value(outcome.metric_name)
            valid = outcome.validate_outcome(metric_value, self.current_step)
            report["outcome_validation"].append(
                {
                    "metric": outcome.metric_name,
                    "target": outcome.target_value,
                    "actual": metric_value,
                    "valid": valid,
                }
            )

        # Save report
        report_file = Path("simulation_outputs") / f"{self.current_scenario.metadata.name}_report.json"
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        self.logger.info(f"Scenario report saved to {report_file}")
        return report
