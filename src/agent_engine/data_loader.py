"""
Data loader for retail and corporate agent CSV files
Loads and prepares agent data from Hamza's processed CSVs
"""
import pandas as pd
import os
from pathlib import Path
from typing import Dict, List, Any
import logging
import random

class AgentDataLoader:
    """Load and prepare agent data from CSV files"""
    
    def __init__(self, data_dir: str = None):
        """Initialize data loader with path to data directory"""
        if data_dir is None:
            # Auto-detect data directory
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / 'data' / 'processed'
        
        self.data_dir = Path(data_dir)
        self.logger = logging.getLogger('AgentDataLoader')
        
        # File paths
        self.retail_file = self.data_dir / 'hamza_retail_agents.csv'
        self.corporate_file = self.data_dir / 'hamza_corporate_agents.csv'
        
        # Loaded data
        self.retail_data = None
        self.corporate_data = None
        
        self.logger.info(f"Data loader initialized with directory: {self.data_dir}")
    
    def load_retail_agents(self) -> List[Dict[str, Any]]:
        """Load retail agent data from CSV"""
        try:
            if self.retail_data is None:
                self.logger.info(f"Loading retail agents from {self.retail_file}")
                self.retail_data = pd.read_csv(self.retail_file)
                self.logger.info(f"Loaded {len(self.retail_data)} retail agents")
            
            # Convert to list of dictionaries with proper typing
            agents_list = []
            for _, row in self.retail_data.iterrows():
                agent_dict = {
                    'client_id': row['client_id'],
                    'age': int(row['age']),
                    'governorate': row['governorate'],
                    'monthly_income': float(row['monthly_income']),
                    'risk_tolerance': float(row['risk_tolerance']),
                    'satisfaction_score': float(row['satisfaction_score']),
                    'digital_engagement_score': float(row['digital_engagement_score']),
                    'preferred_channel': row['preferred_channel'],
                    'client_type': 'retail'
                }
                agents_list.append(agent_dict)
            
            return agents_list
            
        except FileNotFoundError:
            self.logger.error(f"Retail agents file not found: {self.retail_file}")
            return []
        except Exception as e:
            self.logger.error(f"Error loading retail agents: {e}")
            return []
    
    def load_corporate_agents(self) -> List[Dict[str, Any]]:
        """Load corporate agent data from CSV"""
        try:
            if self.corporate_data is None:
                self.logger.info(f"Loading corporate agents from {self.corporate_file}")
                self.corporate_data = pd.read_csv(self.corporate_file)
                self.logger.info(f"Loaded {len(self.corporate_data)} corporate agents")
            
            # Convert to list of dictionaries
            agents_list = []
            for _, row in self.corporate_data.iterrows():
                agent_dict = {
                    'client_id': row['client_id'],
                    'company_name': row['company_name'],
                    'business_sector': row['business_sector'],
                    'company_size': row['company_size'],
                    'annual_revenue': float(row['annual_revenue']),
                    'digital_maturity_score': float(row['digital_maturity_score']),
                    'headquarters_governorate': row['headquarters_governorate'],
                    'client_type': 'corporate'
                }
                agents_list.append(agent_dict)
            
            return agents_list
            
        except FileNotFoundError:
            self.logger.error(f"Corporate agents file not found: {self.corporate_file}")
            return []
        except Exception as e:
            self.logger.error(f"Error loading corporate agents: {e}")
            return []
    
    def select_agents(self, agent_list: List[Dict[str, Any]], num_agents: int) -> List[Dict[str, Any]]:
        """
        Select a specified number of agents from the list
        
        Args:
            agent_list: List of agent dictionaries to select from
            num_agents: Number of agents to select
        
        Returns:
            List of selected agent dictionaries
        """
        if len(agent_list) <= num_agents:
            return agent_list
        
        # Random selection without replacement
        selected = random.sample(agent_list, num_agents)
        self.logger.info(f"Selected {len(selected)} agents from {len(agent_list)} available")
        return selected
    
    def load_all_agents(self, num_agents: int = None, retail_ratio: float = 0.8) -> List[Dict[str, Any]]:
        """
        Load both retail and corporate agents
        
        Args:
            num_agents: Total number of agents to load (None = load all)
            retail_ratio: Ratio of retail to corporate agents
        
        Returns:
            Combined list of agent data dictionaries
        """
        retail_agents = self.load_retail_agents()
        corporate_agents = self.load_corporate_agents()
        
        if num_agents is None:
            # Return all agents
            all_agents = retail_agents + corporate_agents
        else:
            # Calculate how many of each type to load
            num_retail = int(num_agents * retail_ratio)
            num_corporate = num_agents - num_retail
            
            # Select the specified number of each type
            selected_retail = self.select_agents(retail_agents, num_retail)
            selected_corporate = self.select_agents(corporate_agents, num_corporate)
            
            all_agents = selected_retail + selected_corporate
            
        self.logger.info(f"Selected {len([a for a in all_agents if a['client_type'] == 'retail'])} retail and "
                        f"{len([a for a in all_agents if a['client_type'] == 'corporate'])} corporate agents")
        
        return all_agents
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about loaded data"""
        stats = {}
        
        # Load data if not already loaded
        if self.retail_data is None:
            self.load_retail_agents()
        if self.corporate_data is None:
            self.load_corporate_agents()
        
        # Retail statistics
        if self.retail_data is not None and len(self.retail_data) > 0:
            stats['retail'] = {
                'count': len(self.retail_data),
                'avg_age': self.retail_data['age'].mean(),
                'avg_income': self.retail_data['monthly_income'].mean(),
                'avg_satisfaction': self.retail_data['satisfaction_score'].mean(),
                'governorates': self.retail_data['governorate'].unique().tolist(),
                'preferred_channels': self.retail_data['preferred_channel'].value_counts().to_dict()
            }
        
        # Corporate statistics
        if self.corporate_data is not None and len(self.corporate_data) > 0:
            stats['corporate'] = {
                'count': len(self.corporate_data),
                'avg_revenue': self.corporate_data['annual_revenue'].mean(),
                'sectors': self.corporate_data['business_sector'].unique().tolist(),
                'company_sizes': self.corporate_data['company_size'].value_counts().to_dict(),
                'avg_digital_maturity': self.corporate_data['digital_maturity_score'].mean()
            }
        
        return stats
    
    def reset(self):
        """Reset loaded data"""
        self.retail_data = None
        self.corporate_data = None
        self.logger.info("Data loader reset")