# Mesa 3.x compatible - FINAL CORRECTED VERSION
import mesa
from mesa.datacollection import DataCollector
import pandas as pd
from typing import List, Dict, Any
import logging
import random
import time

class BankSimulationModel(mesa.Model):
    """Mesa 3.x compatible simulation model - FINAL VERSION"""
    
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
        
        # DATA COLLECTION SYSTEM
        self.datacollector = DataCollector(
            model_reporters={
                "Total_Agents": lambda m: len(m.agents),
                "Average_Satisfaction": self.get_average_satisfaction,
                "Churn_Rate": self.calculate_churn_rate,
                "Active_Products": self.count_active_products,
                "Digital_Channel_Usage": self.get_digital_usage_rate
            },
            agent_reporters={
                "Satisfaction": "satisfaction_level",
                "Products_Count": lambda a: len(getattr(a, 'current_products', [])),
                "Channel_Preference": lambda a: getattr(a, 'primary_channel', 'unknown')
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
    
    def add_agent(self, agent):
        """Add agent - Mesa 3.x handles registration automatically via Agent.__init__"""
        # Mesa 3.x automatically adds agents to self.agents and self.agents_by_type
        # We just track our own counts
        if hasattr(agent, 'client_type'):
            self.our_agents_by_type[agent.client_type].append(agent)
        
        self.total_agents_created += 1
        self.logger.debug(f"Added agent {agent.unique_id}")
    
    def add_agents_batch(self, agents: List):
        """Add multiple agents efficiently"""
        for agent in agents:
            self.add_agent(agent)
        
        self.logger.info(f"Added batch of {len(agents)} agents. Total: {self.total_agents_created}")
    
    def step(self):
        """Execute one simulation time step - Mesa 3.x style"""
        step_start_time = time.time()
        
        self.logger.debug(f"Starting simulation step {self.current_step}")
        
        # 1. PROCESS EXTERNAL EVENTS
        self.process_pending_events()
        
        # 2. ACTIVATE ALL AGENTS - MESA 3.X WAY
        self.agents.shuffle_do("step")  # This is the Mesa 3.x way!
        
        # 3. UPDATE GLOBAL MARKET CONDITIONS
        self.update_market_conditions()
        
        # 4. PROCESS SOCIAL INFLUENCE
        self.process_social_influence()
        
        # 5. COLLECT DATA
        self.datacollector.collect(self)
        
        # 6. CHECK TERMINATION CONDITIONS
        if self.current_step >= self.time_steps:
            self.running = False
            self.logger.info(f"Simulation completed after {self.current_step} steps")
        
        # 7. PERFORMANCE TRACKING
        step_duration = time.time() - step_start_time
        self.step_duration_history.append(step_duration)
        
        if step_duration > 1.0:
            self.logger.warning(f"Step {self.current_step} took {step_duration:.2f} seconds")
        
        self.current_step += 1
        
        # 8. PERIODIC LOGGING
        if self.current_step % 10 == 0:
            self.log_simulation_status()
    
    def process_pending_events(self):
        """Process events from Maryem's event system"""
        while self.event_queue:
            event = self.event_queue.pop(0)
            event_type = type(event).__name__
            
            if event_type in self.event_handlers:
                self.logger.info(f"Processing {event_type} event")
                self.event_handlers[event_type](event)
            else:
                self.logger.warning(f"No handler for event type: {event_type}")
    
    def update_market_conditions(self):
        """Update global market conditions"""
        pass
    
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
        
        # Use Mesa 3.x AgentSet aggregation
        import numpy as np
        try:
            return self.agents.agg("satisfaction_level", np.mean)
        except (AttributeError, ValueError):
            # Fallback if agg doesn't work
            satisfactions = [
                agent.satisfaction_level for agent in self.agents 
                if hasattr(agent, 'satisfaction_level')
            ]
            return sum(satisfactions) / len(satisfactions) if satisfactions else 0.5
    
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
            agent.primary_channel in ['online', 'mobile']
        ))
        return digital_users / len(self.agents)
    
    def log_simulation_status(self):
        """Log current simulation status"""
        status = {
            'step': self.current_step,
            'agents': len(self.agents),
            'avg_satisfaction': self.get_average_satisfaction(),
            'churn_rate': self.calculate_churn_rate(),
            'avg_step_time': sum(self.step_duration_history[-10:]) / min(10, len(self.step_duration_history)) if self.step_duration_history else 0
        }
        
        self.logger.info(f"Step {status['step']}: "
                        f"{status['agents']} agents, "
                        f"satisfaction={status['avg_satisfaction']:.2f}, "
                        f"churn={status['churn_rate']:.2f}, "
                        f"step_time={status['avg_step_time']:.3f}s")
    
    def get_results_summary(self) -> Dict[str, Any]:
        """Get simulation results summary"""
        results = {
            'total_steps': self.current_step,
            'total_agents': len(self.agents),
            'final_satisfaction': self.get_average_satisfaction(),
            'final_churn_rate': self.calculate_churn_rate(),
            'agents_by_type': {
                'retail': len(self.our_agents_by_type['retail']),
                'corporate': len(self.our_agents_by_type['corporate'])
            },
            'performance_metrics': {
                'avg_step_time': sum(self.step_duration_history) / len(self.step_duration_history) if self.step_duration_history else 0,
                'total_runtime': sum(self.step_duration_history)
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