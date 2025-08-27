# Mesa 3.x compatible - COMPLETE VERSION WITH CSV DATA LOADING
import mesa
from mesa.datacollection import DataCollector
import pandas as pd
from typing import List, Dict, Any
import logging
import random
import time
from pathlib import Path

# Import our custom modules
from src.agent_engine.data_loader import AgentDataLoader
from src.agent_engine.retail_agent import RetailClientAgent
from src.agent_engine.corporate_agent import CorporateClientAgent

class BankSimulationModel(mesa.Model):
    """Mesa 3.x compatible simulation model with CSV data loading"""
    
    def __init__(self, config: Dict[str, Any]):
        # Mesa 3.x proper initialization with seed
        super().__init__(seed=config.get('random_seed', 42))
        
        # SIMULATION PARAMETERS
        self.num_agents = config.get('num_agents', 1000)
        self.retail_ratio = config.get('retail_ratio', 0.8)
        self.time_steps = config.get('time_steps', 100)
        self.current_step = 0
        
        # NOTE: Mesa 3.x automatically creates:
        # - self.agents (AgentSet of all agents)
        # - self.agents_by_type (read-only property, automatically maintained)
        self.agent_id_counter = 0
        
        # SIMULATION STATE
        self.running = True
        self.total_agents_created = 0
        
        # Our own tracking (since agents_by_type is read-only)
        self.our_agents_by_type = {
            'retail': [],
            'corporate': []
        }
        
        # DATA LOADING SYSTEM
        self.data_loader = AgentDataLoader()
        
        # Setup logging
        self.logger = logging.getLogger('BankSimulation')
        self.logger.info(f"Initialized BankSimulationModel with Mesa 3.x (seed={config.get('random_seed', 42)})")
        
        # Load agents from CSV
        self.logger.info("Loading agents from CSV files...")
        self.load_agents_from_csv()
        
        # Create social networks
        self.logger.info("Creating social networks...")
        self.create_social_networks()
        
        # Setup data collection
        self.datacollector = DataCollector(
            model_reporters={
                "Average_Satisfaction": self.get_average_satisfaction,
                "Total_Agents": lambda m: len(m.agents),
                "Active_Retail": lambda m: len([a for a in m.agents if a.client_type == 'retail']),
                "Active_Corporate": lambda m: len([a for a in m.agents if a.client_type == 'corporate'])
            },
            agent_reporters={
                "Satisfaction": "satisfaction_level",
                "Income": "income",
                "Age": "age",
                "Type": "client_type"
            }
        )
        
        self.logger.info(f"Model initialization complete with {len(self.agents)} agents")
    
    def load_agents_from_csv(self):
        """Load agents from CSV files and create agent objects"""
        # Calculate how many of each type we need
        target_retail = int(self.num_agents * self.retail_ratio)
        target_corporate = self.num_agents - target_retail
        
        # Load and select agents
        all_agents_data = self.data_loader.load_all_agents(
            num_agents=self.num_agents,
            retail_ratio=self.retail_ratio
        )
        
        self.logger.info(f"Selected {len(all_agents_data)} agents")
        
        # Create agent objects
        for agent_data in all_agents_data:
            if agent_data['client_type'] == 'retail':
                agent = RetailClientAgent(self, agent_data)
                self.our_agents_by_type['retail'].append(agent)
            else:
                agent = CorporateClientAgent(self, agent_data)
                self.our_agents_by_type['corporate'].append(agent)
            
            self.total_agents_created += 1
        
        actual_retail = len(self.our_agents_by_type['retail'])
        actual_corporate = len(self.our_agents_by_type['corporate'])
        
        self.logger.info(f"Successfully created {self.total_agents_created} agents from CSV:")
        self.logger.info(f"  - Retail: {actual_retail} agents")
        self.logger.info(f"  - Corporate: {actual_corporate} agents")
        
        # Log some statistics about the loaded agents
        if actual_retail > 0:
            avg_age = sum(a.age for a in self.our_agents_by_type['retail']) / actual_retail
            avg_income = sum(a.income for a in self.our_agents_by_type['retail']) / actual_retail
            self.logger.info(f"  Retail stats: avg age={avg_age:.1f}, avg income={avg_income:.0f} TND")
        
        if actual_corporate > 0:
            avg_revenue = sum(a.annual_revenue for a in self.our_agents_by_type['corporate']) / actual_corporate
            sectors = set(a.business_sector for a in self.our_agents_by_type['corporate'])
            self.logger.info(f"  Corporate stats: avg revenue={avg_revenue:.0f} TND, sectors={len(sectors)} unique")
    
    def create_social_networks(self):
        """Create social network connections between agents"""
        # Simple random network creation
        for agent in self.agents:
            # Each agent gets 2-5 random connections
            num_connections = random.randint(2, 5)
            possible_connections = [a for a in self.agents if a != agent]
            
            if possible_connections:
                connections = random.sample(
                    possible_connections,
                    min(num_connections, len(possible_connections))
                )
                agent.social_network = connections
        
        self.logger.info("Social networks created")
    
    def step(self):
        """Execute one step of the model"""
        self.current_step += 1
        
        # Activate all agents in random order (Mesa 3.x style)
        self.agents.shuffle_do("step")
        
        # Collect data
        self.datacollector.collect(self)
    
    def get_average_satisfaction(self):
        """Get average satisfaction across all agents"""
        if len(self.agents) == 0:
            return 0
        return sum(a.satisfaction_level for a in self.agents) / len(self.agents)
    
    def calculate_churn_rate(self) -> float:
        """Calculate proportion of agents at churn risk (satisfaction < 0.3)."""
        if len(self.agents) == 0:
            return 0.0
        at_risk = sum(1 for a in self.agents if getattr(a, 'satisfaction_level', 0) < 0.3)
        return at_risk / len(self.agents)

    def get_digital_adoption_rate(self) -> float:
        """Average digital engagement across agents (0-1)."""
        digital_agents = [a for a in self.agents if hasattr(a, 'digital_engagement_score')]
        if not digital_agents:
            return 0.0
        return sum(getattr(a, 'digital_engagement_score', 0.0) for a in digital_agents) / len(digital_agents)
    
    def export_agent_data(self, filename: str = None):
        """Export current agent data to CSV"""
        if filename is None:
            filename = f"agent_data_step_{self.current_step}.csv"
        
        agent_data = []
        for agent in self.agents:
            agent_data.append({
                'agent_id': agent.unique_id,
                'client_type': agent.client_type,
                'satisfaction_level': agent.satisfaction_level,
                'age': getattr(agent, 'age', None),
                'income': getattr(agent, 'income', None),
                'products': len(getattr(agent, 'owned_products', [])),  # Safe access
                'status': getattr(agent, 'status', 'active'),
                'preferred_channel': getattr(agent, 'preferred_channel', None),
                'governorate': getattr(agent, 'governorate', None)
            })
        
        df = pd.DataFrame(agent_data)
        df.to_csv(filename, index=False)
        return df