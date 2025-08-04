# Mesa 3.x compatible base agent - COMPLETE VERSION WITH ALL METHODS
import mesa
import random
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime

class BaseClientAgent(mesa.Agent):
    """
    Base class for all bank clients (retail and corporate) - Mesa 3.x compatible
    COMPLETE VERSION with all required methods
    """
    
    def __init__(self, model, client_data: Dict[str, Any]):
        """
        Initialize base client agent - Mesa 3.x way
        
        Args:
            model: Reference to the BankSimulationModel
            client_data: Dictionary containing client information from Mehdi's synthetic data
        """
        # Mesa 3.x automatically assigns unique_id and registers with model
        super().__init__(model)
        
        # BASIC DEMOGRAPHICS (from Mehdi's synthetic data)
        self.age = client_data.get('age', 35)
        self.income = client_data.get('income', 2000.0)  # TND
        self.governorate = client_data.get('governorate', 'Tunis')
        self.education_level = client_data.get('education_level', 'secondary')
        self.employment_sector = client_data.get('employment_sector', 'services')
        
        # CLIENT TYPE IDENTIFICATION
        self.client_type = client_data.get('client_type', 'retail')
        
        # PSYCHOLOGICAL PROFILE
        self.satisfaction_level = 0.5
        self.trust_level = random.uniform(0.4, 0.8)
        self.price_sensitivity = self.calculate_price_sensitivity()
        self.risk_tolerance = client_data.get('risk_tolerance', random.uniform(0.2, 0.8))
        self.brand_loyalty = self.calculate_brand_loyalty()
        
        # BEHAVIORAL STATE
        self.current_products = []
        self.product_history = []
        self.interaction_history = []
        self.considering_churn = False
        self.satisfaction_changed = False
        
        # CHANNEL PREFERENCES
        self.channel_preferences = self.initialize_channel_preferences()
        self.primary_channel = max(self.channel_preferences, key=self.channel_preferences.get)
        
        # SOCIAL NETWORK
        self.social_network = []
        self.influence_strength = random.uniform(0.1, 0.5)
        self.influence_susceptibility = random.uniform(0.1, 0.5)
        
        # FINANCIAL STATE
        self.lifetime_value = 0.0
        self.credit_score = self.calculate_initial_credit_score()
        self.monthly_expenses = self.income * random.uniform(0.6, 0.9)
        
        # DECISION MAKING PARAMETERS
        self.decision_threshold = random.uniform(0.3, 0.7)
        self.evaluation_frequency = random.randint(1, 12)
        self.last_evaluation_step = 0
        
        # EXPERIENCE TRACKING
        self.recent_experiences = []
        self.complaint_history = []
        
        # GEOGRAPHIC CONTEXT
        self.regional_loyalty_factor = self.get_regional_loyalty_factor()
        
        # LOGGING
        self.creation_timestamp = datetime.now()
        self.total_interactions = 0
    
    def calculate_price_sensitivity(self) -> float:
        """Calculate how sensitive this agent is to pricing"""
        base_sensitivity = max(0.1, 1.0 - (self.income / 10000))
        
        if self.age < 30:
            age_factor = 1.2
        elif self.age > 60:
            age_factor = 0.8
        else:
            age_factor = 1.0
            
        return min(1.0, base_sensitivity * age_factor)
    
    def calculate_brand_loyalty(self) -> float:
        """Calculate initial brand loyalty based on demographics"""
        age_loyalty = min(1.0, self.age / 100)
        regional_loyalty = self.get_regional_loyalty_factor()
        income_loyalty = min(1.0, self.income / 5000) * 0.3
        return (age_loyalty + regional_loyalty + income_loyalty) / 3
    
    def get_regional_loyalty_factor(self) -> float:
        """Get loyalty factor based on governorate"""
        loyalty_by_region = {
            'Tunis': 0.6, 'Sfax': 0.8, 'Sousse': 0.7, 'Kairouan': 0.9,
            'Bizerte': 0.7, 'Ariana': 0.5, 'Ben Arous': 0.6, 'Manouba': 0.7
        }
        return loyalty_by_region.get(self.governorate, 0.7)
    
    def initialize_channel_preferences(self) -> Dict[str, float]:
        """Initialize channel preferences based on demographics"""
        preferences = {
            'branch': 0.4,
            'online': 0.2,
            'mobile': 0.2,
            'call_center': 0.1,
            'atm': 0.1
        }
        
        # Age-based adjustments
        if self.age < 30:
            preferences['mobile'] += 0.3
            preferences['online'] += 0.2
            preferences['branch'] -= 0.3
        elif self.age > 60:
            preferences['branch'] += 0.4
            preferences['mobile'] -= 0.2
            preferences['online'] -= 0.2
        
        # Education level adjustments
        if self.education_level in ['university', 'graduate']:
            preferences['online'] += 0.2
            preferences['mobile'] += 0.1
        
        # Income adjustments
        if self.income > 5000:
            preferences['call_center'] += 0.1
            preferences['branch'] += 0.1
        
        # Normalize to sum to 1.0
        total = sum(preferences.values())
        return {k: v/total for k, v in preferences.items()}
    
    def calculate_initial_credit_score(self) -> float:
        """Calculate initial credit score based on demographics"""
        base_score = min(0.9, self.income / 10000)
        
        if 25 <= self.age <= 55:
            age_factor = 1.0
        elif self.age < 25:
            age_factor = 0.7
        else:
            age_factor = 0.9
        
        education_factor = {
            'primary': 0.8, 'secondary': 0.9, 
            'university': 1.0, 'graduate': 1.1
        }.get(self.education_level, 0.9)
        
        random_factor = random.uniform(0.8, 1.2)
        credit_score = base_score * age_factor * education_factor * random_factor
        return min(1.0, max(0.1, credit_score))
    
    def step(self):
        """Main agent behavior - called by Mesa 3.x via shuffle_do("step")"""
        # 1. EVALUATE CURRENT SITUATION
        self.evaluate_satisfaction()
        
        # 2. CONSIDER MAJOR DECISIONS (not every step)
        if self.should_make_major_evaluation():
            self.evaluate_product_portfolio()
            self.consider_churn_decision()
        
        # 3. PROCESS RECENT EXPERIENCES
        self.process_recent_experiences()
        
        # 4. UPDATE PREFERENCES (gradual learning)
        self.update_preferences()
        
        # 5. SOCIAL LEARNING (learn from network)
        self.learn_from_social_network()
        
        # 6. RANDOM BEHAVIOR (some unpredictability)
        if random.random() < 0.01:  # 1% chance
            self.random_behavior()
        
        # 7. TRACK ACTIVITY
        self.total_interactions += 1
    
    def should_make_major_evaluation(self) -> bool:
        """Determine if agent should make major decisions this step"""
        steps_since_last = self.model.current_step - self.last_evaluation_step
        return steps_since_last >= self.evaluation_frequency
    
    def evaluate_satisfaction(self):
        """Evaluate current satisfaction level based on recent experiences"""
        if not self.recent_experiences:
            return
        
        # Weight recent experiences more heavily
        weighted_satisfaction = 0
        total_weight = 0
        
        for i, experience in enumerate(self.recent_experiences):
            # More recent experiences have higher weight
            weight = (i + 1) / len(self.recent_experiences)
            weighted_satisfaction += experience['quality'] * weight
            total_weight += weight
        
        if total_weight > 0:
            new_satisfaction = weighted_satisfaction / total_weight
            
            # Smooth transition (don't change too rapidly)
            learning_rate = 0.1
            old_satisfaction = self.satisfaction_level
            self.satisfaction_level = (
                (1 - learning_rate) * old_satisfaction + 
                learning_rate * new_satisfaction
            )
            
            # Flag if satisfaction changed significantly
            if abs(self.satisfaction_level - old_satisfaction) > 0.1:
                self.satisfaction_changed = True
    
    def evaluate_product_portfolio(self):
        """Evaluate current products and consider changes"""
        # This will be implemented in child classes (RetailClientAgent, CorporateClientAgent)
        pass
    
    def consider_churn_decision(self):
        """Consider whether to switch banks"""
        # Simple churn logic based on satisfaction
        if self.satisfaction_level < 0.3:
            churn_probability = 0.1  # 10% chance if very dissatisfied
        elif self.satisfaction_level < 0.5:
            churn_probability = 0.02  # 2% chance if somewhat dissatisfied
        else:
            churn_probability = 0.005  # 0.5% baseline churn
        
        # Brand loyalty reduces churn probability
        churn_probability *= (1 - self.brand_loyalty)
        
        self.considering_churn = random.random() < churn_probability
        
        # Update last evaluation step
        self.last_evaluation_step = self.model.current_step
    
    def process_recent_experiences(self):
        """Process and learn from recent bank interactions"""
        # Remove old experiences (only keep last 10)
        if len(self.recent_experiences) > 10:
            self.recent_experiences = self.recent_experiences[-10:]
        
        # Update channel preferences based on experience quality
        for experience in self.recent_experiences[-3:]:  # Last 3 experiences
            channel = experience.get('channel')
            quality = experience.get('quality', 0.5)
            
            if channel in self.channel_preferences:
                # Adjust preference based on experience
                adjustment = (quality - 0.5) * 0.05  # Small adjustments
                self.channel_preferences[channel] += adjustment
                
                # Keep preferences positive
                self.channel_preferences[channel] = max(0.01, self.channel_preferences[channel])
        
        # Renormalize preferences
        total = sum(self.channel_preferences.values())
        if total > 0:
            self.channel_preferences = {k: v/total for k, v in self.channel_preferences.items()}
            self.primary_channel = max(self.channel_preferences, key=self.channel_preferences.get)
    
    def update_preferences(self):
        """Gradual evolution of preferences over time"""
        # Preferences can drift slowly over time
        # Add small random changes
        for channel in self.channel_preferences:
            change = random.uniform(-0.01, 0.01)
            self.channel_preferences[channel] += change
            self.channel_preferences[channel] = max(0.01, self.channel_preferences[channel])
        
        # Renormalize
        total = sum(self.channel_preferences.values())
        self.channel_preferences = {k: v/total for k, v in self.channel_preferences.items()}
        self.primary_channel = max(self.channel_preferences, key=self.channel_preferences.get)
    
    def learn_from_social_network(self):
        """Learn from other agents in social network"""
        if not self.social_network:
            return
        
        # Influenced by network satisfaction
        network_satisfaction = sum(
            agent.satisfaction_level for agent in self.social_network 
            if hasattr(agent, 'satisfaction_level')
        ) / len(self.social_network)
        
        # Small influence from network
        influence_strength = self.influence_susceptibility * 0.01
        satisfaction_influence = (network_satisfaction - self.satisfaction_level) * influence_strength
        self.satisfaction_level += satisfaction_influence
        
        # Keep satisfaction in valid range
        self.satisfaction_level = max(0, min(1, self.satisfaction_level))
    
    def random_behavior(self):
        """Occasional random behavior to add unpredictability"""
        # Small random changes to add realism
        self.satisfaction_level += random.uniform(-0.05, 0.05)
        self.satisfaction_level = max(0, min(1, self.satisfaction_level))
    
    def add_experience(self, interaction_type: str, channel: str, quality: float, description: str = ""):
        """
        Add a new interaction experience
        
        Args:
            interaction_type: Type of interaction (transaction, complaint, inquiry, etc.)
            channel: Channel used (branch, online, mobile, etc.)
            quality: Quality score 0-1 (0=terrible, 1=excellent)
            description: Optional description
        """
        experience = {
            'timestamp': self.model.current_step,
            'type': interaction_type,
            'channel': channel,
            'quality': quality,
            'description': description
        }
        
        self.recent_experiences.append(experience)
        self.interaction_history.append(experience)
    
    def propagate_influence(self):
        """Propagate influence to social network (for social influence processing)"""
        if not self.social_network:
            return
        
        # Influence others based on my satisfaction
        my_influence = self.influence_strength * 0.1
        
        for connected_agent in self.social_network:
            if hasattr(connected_agent, 'satisfaction_level'):
                # If I'm happy, slightly increase their satisfaction
                # If I'm unhappy, slightly decrease their satisfaction
                influence_effect = (self.satisfaction_level - 0.5) * my_influence
                connected_agent.satisfaction_level += influence_effect
                connected_agent.satisfaction_level = max(0, min(1, connected_agent.satisfaction_level))
    
    def get_export_data(self) -> Dict[str, Any]:
        """Export agent data for analysis (used by Nessrine's dashboard)"""
        return {
            'agent_id': self.unique_id,
            'client_type': self.client_type,
            'age': self.age,
            'income': self.income,
            'governorate': self.governorate,
            'satisfaction_level': self.satisfaction_level,
            'trust_level': self.trust_level,
            'primary_channel': self.primary_channel,
            'num_products': len(self.current_products),
            'considering_churn': self.considering_churn,
            'total_interactions': self.total_interactions,
            'credit_score': self.credit_score,
            'lifetime_value': self.lifetime_value
        }
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.unique_id}, {self.governorate}, satisfaction={self.satisfaction_level:.2f})"