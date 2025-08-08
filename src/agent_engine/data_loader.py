"""
Data loader for retail and corporate agent CSV files
Loads and prepares agent data from Mehdi's processed CSVs
"""
import pandas as pd
import os
from pathlib import Path
from typing import Dict, List, Any
import logging

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
            
            # Take the specified number of each type
            # Use all available if requested more than available
            selected_retail = retail_agents[:min(num_retail, len(retail_agents))]
            selected_corporate = corporate_agents[:min(num_corporate, len(corporate_agents))]
            
            all_agents = selected_retail + selected_corporate
            
            self.logger.info(f"Selected {len(selected_retail)} retail and {len(selected_corporate)} corporate agents")
        
        return all_agents
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about loaded data"""
        stats = {}
        
        if self.retail_data is not None:
            stats['retail'] = {
                'count': len(self.retail_data),
                'avg_age': self.retail_data['age'].mean(),
                'avg_income': self.retail_data['monthly_income'].mean(),
                'avg_satisfaction': self.retail_data['satisfaction_score'].mean(),
                'governorates': self.retail_data['governorate'].unique().tolist(),
                'channels': self.retail_data['preferred_channel'].unique().tolist()
            }
        
        if self.corporate_data is not None:
            stats['corporate'] = {
                'count': len(self.corporate_data),
                'sectors': self.corporate_data['business_sector'].unique().tolist(),
                'avg_revenue': self.corporate_data['annual_revenue'].mean(),
                'avg_digital_maturity': self.corporate_data['digital_maturity_score'].mean(),
                'company_sizes': self.corporate_data['company_size'].unique().tolist()
            }
        
        return stats