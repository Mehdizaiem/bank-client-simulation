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
        self.loaded_agent_data = []
        
        # DATA COLLECTION SYSTEM
        self.datacollector = DataCollector(
            model_reporters={
                "Total_Agents": lambda m: len(m.agents),
                "Average_Satisfaction": self.get_average_satisfaction,
                "Churn_Rate": self.calculate_churn_rate,
                "Active_Products": self.count_active_products,
                "Digital_Channel_Usage": self.get_digital_usage_rate,
                "Retail_Count": lambda m: len(m.our_agents_by_type['retail']),
                "Corporate_Count": lambda m: len(m.our_agents_by_type['corporate']),
                "Average_Income": self.get_average_income,
                "Average_Digital_Engagement": self.get_average_digital_engagement
            },
            agent_reporters={
                "Satisfaction": "satisfaction_level",
                "Products_Count": lambda a: len(getattr(a, 'current_products', [])),
                "Channel_Preference": lambda a: getattr(a, 'primary_channel', 'unknown'),
                "Considering_Churn": lambda a: getattr(a, 'considering_churn', False),
                "Client_Type": lambda a: getattr(a, 'client_type', 'unknown')
            }
        )
        
        # LOGGING SYSTEM
        self.setup_logging()
        self.logger.info(f"Initialized BankSimulationModel with Mesa 3.x (seed={config.get('random_seed', 42)})")
        
        # EVENT SYSTEM
        self.event_queue = []
        self.event_handlers = {}
        
        # PERFORMANCE TRACKING
        self.step_duration_history = []
        
        # MARKET CONDITIONS
        self.market_conditions = {
            'interest_rate': 0.05,
            'economic_growth': 0.02,
            'inflation_rate': 0.03,
            'unemployment_rate': 0.15  # Tunisia context
        }
        
        # LOAD AGENTS FROM CSV DATA
        self.load_agents_from_csv()
        
        # ESTABLISH SOCIAL NETWORKS
        self.create_social_networks()
        
        self.logger.info(f"Model initialization complete with {len(self.agents)} agents")
    
    def setup_logging(self):
        """Setup logging system"""
        import os
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/simulation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('BankSimulation')
    
    def load_agents_from_csv(self):
        """Load agents from CSV files and create agent objects"""
        self.logger.info("Loading agents from CSV files...")
        
        # Load agent data from CSVs
        self.loaded_agent_data = self.data_loader.load_all_agents(
            num_agents=self.num_agents,
            retail_ratio=self.retail_ratio
        )
        
        if not self.loaded_agent_data:
            self.logger.warning("No agent data loaded from CSV files! Creating synthetic agents...")
            self.create_synthetic_agents()
            return
        
        # Create agent objects from loaded data
        retail_created = 0
        corporate_created = 0
        
        for agent_data in self.loaded_agent_data:
            try:
                if agent_data['client_type'] == 'retail':
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
        self.logger.info(f"Successfully created {self.total_agents_created} agents from CSV:")
        self.logger.info(f"  - Retail: {retail_created} agents")
        self.logger.info(f"  - Corporate: {corporate_created} agents")
        
        if 'retail' in stats:
            self.logger.info(f"  Retail stats: avg age={stats['retail']['avg_age']:.1f}, "
                           f"avg income={stats['retail']['avg_income']:.0f} TND")
        if 'corporate' in stats:
            self.logger.info(f"  Corporate stats: avg revenue={stats['corporate']['avg_revenue']:.0f} TND, "
                           f"sectors={len(stats['corporate']['sectors'])} unique")
    
    def create_synthetic_agents(self):
        """Fallback: Create synthetic agents if CSV loading fails"""
        self.logger.info("Creating synthetic agents as fallback...")
        
        num_retail = int(self.num_agents * self.retail_ratio)
        num_corporate = self.num_agents - num_retail
        
        # Create synthetic retail agents
        for i in range(num_retail):
            agent_data = {
                'client_id': f'R_SYNTH_{i}',
                'age': random.randint(18, 70),
                'governorate': random.choice(['Tunis', 'Sfax', 'Sousse', 'Kairouan', 'Bizerte']),
                'monthly_income': random.uniform(800, 5000),
                'risk_tolerance': random.uniform(0.2, 0.8),
                'satisfaction_score': random.uniform(0.4, 0.8),
                'digital_engagement_score': random.uniform(0.2, 0.9),
                'preferred_channel': random.choice(['branch', 'mobile', 'online']),
                'client_type': 'retail'
            }
            agent = RetailClientAgent(self, agent_data)
            self.our_agents_by_type['retail'].append(agent)
        
        # Create synthetic corporate agents
        for i in range(num_corporate):
            agent_data = {
                'client_id': f'C_SYNTH_{i}',
                'company_name': f'Company_{i}',
                'business_sector': random.choice(['services', 'manufacturing', 'retail', 'technology']),
                'company_size': random.choice(['small', 'medium', 'large']),
                'annual_revenue': random.uniform(100000, 5000000),
                'digital_maturity_score': random.uniform(0.3, 0.9),
                'headquarters_governorate': random.choice(['Tunis', 'Sfax', 'Sousse']),
                'client_type': 'corporate'
            }
            agent = CorporateClientAgent(self, agent_data)
            self.our_agents_by_type['corporate'].append(agent)
        
        self.total_agents_created = num_retail + num_corporate
        self.logger.info(f"Created {self.total_agents_created} synthetic agents")
    
    def create_social_networks(self):
        """Create social networks between agents"""
        self.logger.info("Creating social networks...")
        
        # Retail agents have social networks (more connections)
        for agent in self.our_agents_by_type['retail']:
            # Each retail agent connects to 2-5 other agents
            num_connections = random.randint(2, 5)
            
            # Prefer connections within same governorate
            same_governorate_agents = [
                a for a in self.our_agents_by_type['retail']
                if a.governorate == agent.governorate and a != agent
            ]
            
            if same_governorate_agents:
                num_local = min(num_connections - 1, len(same_governorate_agents))
                agent.social_network.extend(random.sample(same_governorate_agents, num_local))
            
            # Add some random connections
            other_agents = [
                a for a in self.our_agents_by_type['retail']
                if a != agent and a not in agent.social_network
            ]
            
            if other_agents:
                num_random = min(1, len(other_agents))
                agent.social_network.extend(random.sample(other_agents, num_random))
        
        # Corporate agents have business networks (fewer connections)
        for agent in self.our_agents_by_type['corporate']:
            # Each corporate agent connects to 1-3 other corporates
            num_connections = random.randint(1, 3)
            
            # Prefer connections within same sector
            same_sector_agents = [
                a for a in self.our_agents_by_type['corporate']
                if a.business_sector == agent.business_sector and a != agent
            ]
            
            if same_sector_agents:
                num_sector = min(num_connections, len(same_sector_agents))
                agent.social_network.extend(random.sample(same_sector_agents, num_sector))
        
        self.logger.info("Social networks created")
    
    def step(self):
        """Execute one simulation time step - Mesa 3.x style"""
        step_start_time = time.time()
        
        self.logger.debug(f"Starting simulation step {self.current_step}")
        
        # 1. PROCESS EXTERNAL EVENTS
        self.process_pending_events()
        
        # 2. UPDATE MARKET CONDITIONS (before agent activation)
        self.update_market_conditions()
        
        # 3. ACTIVATE ALL AGENTS - MESA 3.X WAY
        self.agents.shuffle_do("step")  # This is the Mesa 3.x way!
        
        # 4. PROCESS SOCIAL INFLUENCE
        self.process_social_influence()
        
        # 5. PROCESS AGENT INTERACTIONS
        if self.current_step % 3 == 0:
            self.process_agent_interactions()
        
        # 6. COLLECT DATA
        self.datacollector.collect(self)
        
        # 7. CHECK TERMINATION CONDITIONS
        if self.current_step >= self.time_steps:
            self.running = False
            self.logger.info(f"Simulation completed after {self.current_step} steps")
        
        # 8. PERFORMANCE TRACKING
        step_duration = time.time() - step_start_time
        self.step_duration_history.append(step_duration)
        
        if step_duration > 1.0:
            self.logger.warning(f"Step {self.current_step} took {step_duration:.2f} seconds")
        
        self.current_step += 1
        
        # 9. PERIODIC LOGGING
        if self.current_step % 10 == 0:
            self.log_simulation_status()
    
    def process_pending_events(self):
        """Process events from the event system"""
        while self.event_queue:
            event = self.event_queue.pop(0)
            event_type = type(event).__name__
            
            if event_type in self.event_handlers:
                self.logger.info(f"Processing {event_type} event")
                self.event_handlers[event_type](event)
            else:
                self.logger.warning(f"No handler for event type: {event_type}")
    
    def update_market_conditions(self):
        """Update global market conditions that affect all agents"""
        # Small random walk for market conditions
        self.market_conditions['interest_rate'] += random.uniform(-0.001, 0.001)
        self.market_conditions['economic_growth'] += random.uniform(-0.002, 0.002)
        self.market_conditions['inflation_rate'] += random.uniform(-0.001, 0.001)
        
        # Keep within reasonable bounds
        self.market_conditions['interest_rate'] = max(0.01, min(0.15, self.market_conditions['interest_rate']))
        self.market_conditions['economic_growth'] = max(-0.05, min(0.10, self.market_conditions['economic_growth']))
        self.market_conditions['inflation_rate'] = max(0.0, min(0.20, self.market_conditions['inflation_rate']))
        
        # Economic growth affects unemployment
        if self.market_conditions['economic_growth'] > 0.03:
            self.market_conditions['unemployment_rate'] *= 0.99
        elif self.market_conditions['economic_growth'] < 0:
            self.market_conditions['unemployment_rate'] *= 1.01
        
        self.market_conditions['unemployment_rate'] = max(0.05, min(0.30, self.market_conditions['unemployment_rate']))
    
    def process_social_influence(self):
        """Handle social influence between agents"""
        if self.current_step % 5 == 0:
            self.logger.debug("Processing social influence")
            
            # Use Mesa 3.x AgentSet filtering
            changed_agents = self.agents.select(
                lambda agent: hasattr(agent, 'satisfaction_changed') and agent.satisfaction_changed
            )
            
            for agent in changed_agents:
                if hasattr(agent, 'influence_network'):
                    agent.propagate_influence()
                    agent.satisfaction_changed = False
    
    def process_agent_interactions(self):
        """Process interactions between agents"""
        # Sample some agents for interactions
        if len(self.agents) > 10:
            interacting_agents = random.sample(list(self.agents), min(20, len(self.agents)))
            
            for agent in interacting_agents:
                if hasattr(agent, 'social_network') and agent.social_network:
                    # Agent learns from network
                    agent.learn_from_social_network()
    
    def register_event_handler(self, event_type: str, handler_function):
        """Register handler for specific event types"""
        self.event_handlers[event_type] = handler_function
        self.logger.info(f"Registered handler for {event_type}")
    
    def inject_event(self, event):
        """Add event to processing queue"""
        self.event_queue.append(event)
        self.logger.info(f"Event {type(event).__name__} added to queue")
    
    # DATA COLLECTION METHODS
    def get_average_satisfaction(self) -> float:
        """Calculate average satisfaction using Mesa 3.x AgentSet"""
        if not self.agents or len(self.agents) == 0:
            return 0.5
        
        satisfactions = [
            agent.satisfaction_level for agent in self.agents 
            if hasattr(agent, 'satisfaction_level')
        ]
        return sum(satisfactions) / len(satisfactions) if satisfactions else 0.5
    
    def get_average_income(self) -> float:
        """Calculate average income across all agents"""
        if not self.agents or len(self.agents) == 0:
            return 0.0
        
        incomes = [
            agent.income for agent in self.agents 
            if hasattr(agent, 'income')
        ]
        return sum(incomes) / len(incomes) if incomes else 0.0
    
    def get_average_digital_engagement(self) -> float:
        """Calculate average digital engagement for retail agents"""
        retail_agents = self.our_agents_by_type['retail']
        if not retail_agents:
            return 0.0
        
        engagements = [
            agent.digital_engagement_score for agent in retail_agents
            if hasattr(agent, 'digital_engagement_score')
        ]
        return sum(engagements) / len(engagements) if engagements else 0.0
    
    def calculate_churn_rate(self) -> float:
        """Calculate current churn rate"""
        if not self.agents or len(self.agents) == 0:
            return 0.0
        
        churning_agents = len(self.agents.select(
            lambda agent: hasattr(agent, 'considering_churn') and agent.considering_churn
        ))
        return churning_agents / len(self.agents)
    
    def count_active_products(self) -> int:
        """Count total active products"""
        return sum(
            len(getattr(agent, 'current_products', [])) 
            for agent in self.agents
        )
    
    def get_digital_usage_rate(self) -> float:
        """Calculate digital channel usage rate""" 
        if not self.agents or len(self.agents) == 0:
            return 0.0
        
        digital_users = len(self.agents.select(
            lambda agent: hasattr(agent, 'primary_channel') and 
            agent.primary_channel in ['online', 'mobile', 'whatsapp']
        ))
        return digital_users / len(self.agents)
    
    def get_product_distribution(self) -> Dict[str, int]:
        """Get distribution of products across all agents"""
        product_counts = {}
        
        for agent in self.agents:
            if hasattr(agent, 'current_products'):
                for product in agent.current_products:
                    product_counts[product] = product_counts.get(product, 0) + 1
        
        return product_counts
    
    def get_channel_distribution(self) -> Dict[str, int]:
        """Get distribution of primary channels"""
        channel_counts = {}
        
        for agent in self.agents:
            if hasattr(agent, 'primary_channel'):
                channel = agent.primary_channel
                channel_counts[channel] = channel_counts.get(channel, 0) + 1
        
        return channel_counts
    
    def get_governorate_statistics(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics by governorate"""
        gov_stats = {}
        
        for agent in self.agents:
            if hasattr(agent, 'governorate'):
                gov = agent.governorate
                if gov not in gov_stats:
                    gov_stats[gov] = {
                        'count': 0,
                        'total_satisfaction': 0,
                        'total_income': 0,
                        'churn_count': 0
                    }
                
                gov_stats[gov]['count'] += 1
                gov_stats[gov]['total_satisfaction'] += agent.satisfaction_level
                gov_stats[gov]['total_income'] += agent.income
                if agent.considering_churn:
                    gov_stats[gov]['churn_count'] += 1
        
        # Calculate averages
        for gov, stats in gov_stats.items():
            if stats['count'] > 0:
                stats['avg_satisfaction'] = stats['total_satisfaction'] / stats['count']
                stats['avg_income'] = stats['total_income'] / stats['count']
                stats['churn_rate'] = stats['churn_count'] / stats['count']
        
        return gov_stats
    
    def log_simulation_status(self):
        """Log current simulation status"""
        status = {
            'step': self.current_step,
            'agents': len(self.agents),
            'retail': len(self.our_agents_by_type['retail']),
            'corporate': len(self.our_agents_by_type['corporate']),
            'avg_satisfaction': self.get_average_satisfaction(),
            'churn_rate': self.calculate_churn_rate(),
            'digital_usage': self.get_digital_usage_rate(),
            'active_products': self.count_active_products(),
            'avg_step_time': sum(self.step_duration_history[-10:]) / min(10, len(self.step_duration_history)) if self.step_duration_history else 0
        }
        
        self.logger.info(f"Step {status['step']}: "
                        f"{status['agents']} agents ({status['retail']}R/{status['corporate']}C), "
                        f"satisfaction={status['avg_satisfaction']:.2f}, "
                        f"churn={status['churn_rate']:.2f}, "
                        f"digital={status['digital_usage']:.2f}, "
                        f"products={status['active_products']}, "
                        f"step_time={status['avg_step_time']:.3f}s")
        
        # Log market conditions periodically
        if self.current_step % 50 == 0:
            self.logger.info(f"Market conditions: "
                           f"interest={self.market_conditions['interest_rate']:.3f}, "
                           f"growth={self.market_conditions['economic_growth']:.3f}, "
                           f"inflation={self.market_conditions['inflation_rate']:.3f}, "
                           f"unemployment={self.market_conditions['unemployment_rate']:.3f}")
    
    def get_results_summary(self) -> Dict[str, Any]:
        """Get comprehensive simulation results summary"""
        results = {
            'simulation_parameters': {
                'total_steps': self.current_step,
                'total_agents': len(self.agents),
                'retail_agents': len(self.our_agents_by_type['retail']),
                'corporate_agents': len(self.our_agents_by_type['corporate']),
                'configured_agents': self.num_agents,
                'configured_ratio': self.retail_ratio
            },
            'satisfaction_metrics': {
                'final_satisfaction': self.get_average_satisfaction(),
                'retail_satisfaction': sum(a.satisfaction_level for a in self.our_agents_by_type['retail']) / len(self.our_agents_by_type['retail']) if self.our_agents_by_type['retail'] else 0,
                'corporate_satisfaction': sum(a.satisfaction_level for a in self.our_agents_by_type['corporate']) / len(self.our_agents_by_type['corporate']) if self.our_agents_by_type['corporate'] else 0
            },
            'churn_metrics': {
                'final_churn_rate': self.calculate_churn_rate(),
                'churning_agents': sum(1 for a in self.agents if hasattr(a, 'considering_churn') and a.considering_churn)
            },
            'product_metrics': {
                'total_active_products': self.count_active_products(),
                'avg_products_per_agent': self.count_active_products() / len(self.agents) if self.agents else 0,
                'product_distribution': self.get_product_distribution()
            },
            'channel_metrics': {
                'digital_usage_rate': self.get_digital_usage_rate(),
                'channel_distribution': self.get_channel_distribution()
            },
            'geographic_metrics': self.get_governorate_statistics(),
            'market_conditions': self.market_conditions.copy(),
            'performance_metrics': {
                'avg_step_time': sum(self.step_duration_history) / len(self.step_duration_history) if self.step_duration_history else 0,
                'total_runtime': sum(self.step_duration_history),
                'steps_completed': self.current_step
            }
        }
        
        return results
    
    def export_agent_data(self) -> pd.DataFrame:
        """Export current agent data for analysis"""
        agent_data = []
        
        for agent in self.agents:
            if hasattr(agent, 'get_export_data'):
                agent_data.append(agent.get_export_data())
        
        return pd.DataFrame(agent_data)
    
    def export_historical_data(self) -> pd.DataFrame:
        """Export historical simulation data"""
        return self.datacollector.get_model_vars_dataframe()
    
    def export_detailed_results(self, output_dir: str = 'results'):
        """Export detailed results to files"""
        import os
        import json
        from datetime import datetime
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Export summary
        summary = self.get_results_summary()
        with open(output_path / f'summary_{timestamp}.json', 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        # Export agent data
        agent_df = self.export_agent_data()
        agent_df.to_csv(output_path / f'agents_{timestamp}.csv', index=False)
        
        # Export historical data
        history_df = self.export_historical_data()
        history_df.to_csv(output_path / f'history_{timestamp}.csv', index=False)
        
        self.logger.info(f"Results exported to {output_path}")
        
        return {
            'summary_file': f'summary_{timestamp}.json',
            'agents_file': f'agents_{timestamp}.csv',
            'history_file': f'history_{timestamp}.csv'
        }