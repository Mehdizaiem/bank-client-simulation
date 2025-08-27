"""
Base Agent class for Bank Client Simulation
Common attributes and behaviors for all agent types
"""
import mesa
import random
from typing import Dict, Any, List, Optional

class BaseClientAgent(mesa.Agent):
    """Base class for all bank client agents"""
    
    def __init__(self, model, client_data: Dict[str, Any]):
        """
        Initialize base agent with common attributes
        
        Args:
            model: Reference to the BankSimulationModel
            client_data: Dictionary containing agent initialization data
        """
        # Mesa 3.x initialization
        super().__init__(model)
        
        # BASIC ATTRIBUTES (common to all agents)
        self.client_type = client_data.get('client_type', 'retail')
        self.age = client_data.get('age', 35)
        self.income = client_data.get('income', 2000.0)
        self.governorate = client_data.get('governorate', 'Tunis')
        self.education_level = client_data.get('education_level', 'secondary')
        self.employment_sector = client_data.get('employment_sector', 'services')
        
        # BEHAVIORAL ATTRIBUTES
        self.risk_tolerance = client_data.get('risk_tolerance', 0.5)
        self.satisfaction_level = random.uniform(0.4, 0.8)
        self.loyalty_score = random.uniform(0.3, 0.9)
        self.churn_probability = 0.1
        self.status = 'active'
        
        # PRODUCT OWNERSHIP - Initialize with basic products
        self.owned_products = self._initialize_products()
        self.product_usage_frequency = {}
        
        # CHANNEL PREFERENCES
        self.preferred_channel = 'branch'  # branch, mobile, online, phone
        self.digital_engagement_score = random.uniform(0.2, 0.8)
        
        # SOCIAL NETWORK
        self.social_network = []
        self.influence_score = random.uniform(0.1, 0.9)
        
        # FINANCIAL BEHAVIOR
        self.transaction_frequency = random.uniform(5, 50)  # per month
        self.average_transaction_value = self.income * random.uniform(0.1, 0.5)
        
        # SERVICE INTERACTIONS
        self.complaints_count = 0
        self.service_interactions = []
        self.last_interaction_satisfaction = 0.5
    
    def _initialize_products(self) -> List[str]:
        """Initialize agent with basic banking products"""
        products = ['current_account']  # Everyone has a current account
        
        # Add products based on profile
        if self.income > 3000:
            if random.random() > 0.5:
                products.append('savings_account')
            if random.random() > 0.7:
                products.append('credit_card')
        
        if self.age > 30 and self.income > 2000:
            if random.random() > 0.6:
                products.append('personal_loan')
        
        return products
    
    def step(self):
        """Execute one step of agent behavior"""
        # Update satisfaction based on various factors
        self.update_satisfaction()
        
        # Consider product adoption
        self.consider_new_products()
        
        # Update churn probability
        self.update_churn_probability()
        
        # Social influence
        self.apply_social_influence()
    
    def update_satisfaction(self):
        """Update agent satisfaction level"""
        # Base satisfaction drift
        drift = random.gauss(0, 0.02)
        
        # Service quality impact
        if hasattr(self.model, 'service_quality'):
            drift += (self.model.service_quality - 0.5) * 0.01
        
        # Digital experience impact for digital users
        if self.preferred_channel in ['mobile', 'online']:
            if hasattr(self.model, 'digital_service_quality'):
                drift += (self.model.digital_service_quality - 0.5) * 0.02
        
        # Apply change
        self.satisfaction_level = max(0, min(1, self.satisfaction_level + drift))
    
    def consider_new_products(self):
        """Consider adopting new banking products"""
        # Higher satisfaction increases product adoption
        if self.satisfaction_level > 0.7 and random.random() > 0.95:
            available_products = [
                'savings_account', 'credit_card', 'personal_loan',
                'mortgage', 'investment_account', 'insurance'
            ]
            
            # Filter products not owned
            new_products = [p for p in available_products if p not in self.owned_products]
            
            if new_products and random.random() < self.satisfaction_level:
                new_product = random.choice(new_products)
                self.owned_products.append(new_product)
    
    def update_churn_probability(self):
        """Update probability of leaving the bank"""
        # Low satisfaction increases churn risk
        if self.satisfaction_level < 0.3:
            self.churn_probability = min(0.9, self.churn_probability + 0.05)
        elif self.satisfaction_level > 0.7:
            self.churn_probability = max(0.05, self.churn_probability - 0.02)
        
        # Product count reduces churn (switching costs)
        product_factor = len(self.owned_products) * 0.05
        self.churn_probability = max(0.05, self.churn_probability - product_factor)
    
    def apply_social_influence(self):
        """Apply influence from social network"""
        if not self.social_network:
            return
        
        # Average satisfaction of network
        network_satisfaction = sum(
            agent.satisfaction_level for agent in self.social_network
        ) / len(self.social_network)
        
        # Adjust own satisfaction towards network average
        influence_strength = 0.1 * self.influence_score
        self.satisfaction_level += (network_satisfaction - self.satisfaction_level) * influence_strength
        self.satisfaction_level = max(0, min(1, self.satisfaction_level))
    
    def interact_with_service(self, service_type: str, quality: float):
        """Record a service interaction"""
        interaction = {
            'type': service_type,
            'quality': quality,
            'timestamp': self.model.current_step
        }
        self.service_interactions.append(interaction)
        self.last_interaction_satisfaction = quality
        
        # Update overall satisfaction
        satisfaction_impact = (quality - 0.5) * 0.1
        self.satisfaction_level = max(0, min(1, self.satisfaction_level + satisfaction_impact))
    
    def file_complaint(self):
        """File a complaint with the bank"""
        self.complaints_count += 1
        self.satisfaction_level = max(0, self.satisfaction_level - 0.1)
    
    def receive_marketing(self, campaign_type: str, relevance: float):
        """Receive and respond to marketing campaign"""
        # Response depends on relevance and current satisfaction
        response_probability = relevance * self.satisfaction_level
        
        if random.random() < response_probability:
            # Positive response
            self.satisfaction_level = min(1, self.satisfaction_level + 0.05)
            return True
        return False
    
    def add_experience(self, experience_type: str, channel: str, quality: float, description: str):
        """Add a service experience to the agent's history"""
        experience = {
            'type': experience_type,
            'channel': channel,
            'quality': quality,
            'description': description,
            'step': self.model.current_step
        }
        
        # Add to service interactions
        self.service_interactions.append(experience)
        
        # Update satisfaction based on experience quality
        satisfaction_impact = (quality - 0.5) * 0.1
        self.satisfaction_level = max(0, min(1, self.satisfaction_level + satisfaction_impact))
        
        # Update last interaction satisfaction
        self.last_interaction_satisfaction = quality