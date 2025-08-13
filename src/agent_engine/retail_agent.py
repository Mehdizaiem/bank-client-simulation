"""
Retail Client Agent implementation
Uses actual data from hamza_retail_agents.csv
"""
from src.agent_engine.base_agent import BaseClientAgent
import random
from typing import Dict, Any, List

class RetailClientAgent(BaseClientAgent):
    """Retail banking client with specific behaviors and needs"""
    
    def __init__(self, model, client_data: Dict[str, Any]):
        """
        Initialize retail client from CSV data
        
        Args:
            model: Reference to BankSimulationModel
            client_data: Dictionary from hamza_retail_agents.csv
        """
        # Prepare data for base class
        base_data = {
            'client_type': 'retail',
            'age': client_data.get('age', 35),
            'income': client_data.get('monthly_income', 2000.0),
            'governorate': client_data.get('governorate', 'Tunis'),
            'education_level': self.infer_education_level(client_data),
            'employment_sector': self.infer_employment_sector(client_data),
            'risk_tolerance': client_data.get('risk_tolerance', 0.5)
        }
        
        # Initialize base class
        super().__init__(model, base_data)
        
        # RETAIL-SPECIFIC ATTRIBUTES FROM CSV
        self.original_client_id = client_data.get('client_id', f'R_{self.unique_id}')
        self.satisfaction_level = client_data.get('satisfaction_score', 0.5)
        self.digital_engagement_score = client_data.get('digital_engagement_score', 0.5)
        self.csv_preferred_channel = client_data.get('preferred_channel', 'branch')
        
        # Update channel preferences based on CSV data
        self.update_channel_from_csv()
        
        # RETAIL-SPECIFIC BEHAVIORAL TRAITS
        self.product_appetite = self.calculate_product_appetite()
        self.digital_adoption_rate = self.digital_engagement_score
        self.service_expectations = self.calculate_service_expectations()
        
        # RETAIL PRODUCT PORTFOLIO
        self.initialize_retail_products()
        
        # PRODUCT HISTORY TRACKING
        self.product_history = []
        
        # SOCIAL INFLUENCE SUSCEPTIBILITY
        self.influence_susceptibility = random.uniform(0.1, 0.8)
        
        # TRUST AND PRICE SENSITIVITY
        self.trust_level = random.uniform(0.3, 0.9)
        self.price_sensitivity = random.uniform(0.2, 0.8)
        
        # LIFE EVENTS TRACKING
        self.life_events = []
        self.next_life_event_check = random.randint(10, 30)
    
    def infer_education_level(self, data: Dict) -> str:
        """Infer education level from income and digital engagement"""
        income = data.get('monthly_income', 2000)
        digital_score = data.get('digital_engagement_score', 0.5)
        
        if income > 4000 and digital_score > 0.7:
            return 'graduate'
        elif income > 2500 or digital_score > 0.6:
            return 'university'
        elif income > 1500:
            return 'secondary'
        else:
            return 'primary'
    
    def infer_employment_sector(self, data: Dict) -> str:
        """Infer employment sector from income and risk tolerance"""
        income = data.get('monthly_income', 2000)
        risk = data.get('risk_tolerance', 0.5)
        
        if income > 3000 and risk < 0.4:
            return 'government'
        elif income > 2500:
            return 'services'
        elif risk > 0.6:
            return 'private'
        else:
            return 'agriculture'
    
    def update_channel_from_csv(self):
        """Update channel preferences based on CSV preferred channel"""
        channel_map = {
            'mobile': {'mobile': 0.6, 'online': 0.2, 'branch': 0.1, 'atm': 0.05, 'call_center': 0.05},
            'branch': {'branch': 0.6, 'mobile': 0.15, 'online': 0.1, 'atm': 0.1, 'call_center': 0.05},
            'whatsapp': {'mobile': 0.5, 'online': 0.2, 'branch': 0.15, 'call_center': 0.1, 'atm': 0.05},
            'online': {'online': 0.5, 'mobile': 0.3, 'branch': 0.1, 'atm': 0.05, 'call_center': 0.05}
        }
        
        # Get preferences for the CSV channel, with fallback
        new_preferences = channel_map.get(
            self.csv_preferred_channel, 
            {'branch': 0.4, 'online': 0.2, 'mobile': 0.2, 'call_center': 0.1, 'atm': 0.1}
        )
        
        self.channel_preferences = new_preferences
        self.primary_channel = self.csv_preferred_channel
    
    def calculate_product_appetite(self) -> float:
        """Calculate appetite for new products based on profile"""
        base_appetite = 0.5
        
        # Age factor
        if 25 <= self.age <= 45:
            base_appetite += 0.2
        elif self.age < 25:
            base_appetite += 0.1
        
        # Income factor
        if self.income > 3000:
            base_appetite += 0.2
        elif self.income > 2000:
            base_appetite += 0.1
        
        # Digital engagement factor
        base_appetite += self.digital_engagement_score * 0.2
        
        return min(1.0, base_appetite)
    
    def calculate_service_expectations(self) -> float:
        """Calculate service expectation level"""
        # Higher income and digital engagement = higher expectations
        income_factor = min(1.0, self.income / 5000)
        digital_factor = self.digital_engagement_score
        age_factor = 1.0 if self.age < 40 else 0.8
        
        return (income_factor + digital_factor + age_factor) / 3
    
    def initialize_retail_products(self):
        """Initialize typical retail banking products"""
        # Basic account (everyone has one)
        self.current_products = ['checking_account']
        
        # Add products based on profile
        if self.income > 1500:
            if random.random() < 0.6:
                self.current_products.append('savings_account')
        
        if self.income > 2500 and self.age > 25:
            if random.random() < 0.4:
                self.current_products.append('personal_loan')
        
        if self.digital_engagement_score > 0.6:
            if random.random() < 0.7:
                self.current_products.append('mobile_banking')
        
        if self.age > 30 and self.income > 2000:
            if random.random() < 0.3:
                self.current_products.append('mortgage')
    
    def step(self):
        """Retail client step with specific behaviors"""
        # Call parent step for basic behaviors
        super().step()
        
        # RETAIL-SPECIFIC BEHAVIORS
        
        # 1. Check for life events
        if self.model.current_step >= self.next_life_event_check:
            self.check_life_events()
            self.next_life_event_check = self.model.current_step + random.randint(20, 50)
        
        # 2. Evaluate digital services
        if random.random() < 0.05:  # 5% chance each step
            self.evaluate_digital_services()
        
        # 3. Product discovery
        if random.random() < self.product_appetite * 0.02:
            self.explore_new_products()
        
        # 4. Peer influence (retail clients are more socially influenced)
        if random.random() < 0.1:
            self.check_peer_recommendations()
    
    def evaluate_product_portfolio(self):
        """Retail-specific product evaluation"""
        # Check if needs are being met
        unmet_needs = self.identify_unmet_needs()
        
        for need in unmet_needs:
            if self.should_adopt_product(need):
                self.adopt_product(need)
        
        # Consider dropping underused products
        for product in self.current_products[:]:  # Copy to avoid modification during iteration
            if self.should_drop_product(product):
                self.drop_product(product)
    
    def identify_unmet_needs(self) -> List[str]:
        """Identify financial needs not currently met"""
        unmet = []
        
        # Savings need
        if 'savings_account' not in self.current_products and self.income > 1500:
            if self.age > 25 or self.income > 2000:
                unmet.append('savings_account')
        
        # Credit need
        if 'credit_card' not in self.current_products and self.income > 2000:
            if self.digital_engagement_score > 0.5:
                unmet.append('credit_card')
        
        # Investment need
        if 'investment_account' not in self.current_products and self.income > 3500:
            if self.risk_tolerance > 0.5 and self.age > 30:
                unmet.append('investment_account')
        
        # Insurance need
        if 'life_insurance' not in self.current_products and self.age > 35:
            if self.income > 2500:
                unmet.append('life_insurance')
        
        return unmet
    
    def should_adopt_product(self, product: str) -> bool:
        """Decide whether to adopt a new product"""
        # Base probability
        adoption_prob = self.product_appetite * 0.3
        
        # Adjust based on satisfaction
        adoption_prob *= self.satisfaction_level
        
        # Adjust based on digital engagement for digital products
        if product in ['mobile_banking', 'online_banking', 'digital_wallet']:
            adoption_prob *= self.digital_engagement_score
        
        # Trust factor
        adoption_prob *= self.trust_level
        
        return random.random() < adoption_prob
    
    def should_drop_product(self, product: str) -> bool:
        """Decide whether to drop a product"""
        # Never drop basic checking account
        if product == 'checking_account':
            return False
        
        # Low satisfaction increases drop probability
        drop_prob = (1 - self.satisfaction_level) * 0.05
        
        # High fees increase drop probability
        if product in ['credit_card', 'investment_account']:
            drop_prob *= self.price_sensitivity
        
        return random.random() < drop_prob
    
    def adopt_product(self, product: str):
        """Adopt a new product"""
        self.current_products.append(product)
        self.product_history.append({
            'product': product,
            'action': 'adopted',
            'step': self.model.current_step
        })
        
        # Positive experience
        self.add_experience('product_adoption', self.primary_channel, 0.7, f'Adopted {product}')
    
    def drop_product(self, product: str):
        """Drop a product"""
        if product in self.current_products:
            self.current_products.remove(product)
            self.product_history.append({
                'product': product,
                'action': 'dropped',
                'step': self.model.current_step
            })
            
            # Negative impact on satisfaction
            self.satisfaction_level *= 0.95
    
    def check_life_events(self):
        """Check for major life events that affect banking needs"""
        event_probability = {
            'marriage': 0.01 if 25 <= self.age <= 35 else 0.001,
            'new_job': 0.02 if self.age < 45 else 0.005,
            'retirement': 0.05 if self.age > 55 else 0,
            'home_purchase': 0.02 if 30 <= self.age <= 50 and self.income > 2500 else 0.001
        }
        
        for event, prob in event_probability.items():
            if random.random() < prob:
                self.process_life_event(event)
    
    def process_life_event(self, event: str):
        """Process a life event and adjust needs"""
        self.life_events.append({
            'event': event,
            'step': self.model.current_step
        })
        
        if event == 'marriage':
            self.product_appetite += 0.1
            if 'joint_account' not in self.current_products:
                self.current_products.append('joint_account')
        
        elif event == 'new_job':
            self.income *= random.uniform(1.1, 1.3)
            self.product_appetite += 0.05
        
        elif event == 'home_purchase':
            if 'mortgage' not in self.current_products:
                self.current_products.append('mortgage')
            self.satisfaction_level += 0.1
        
        elif event == 'retirement':
            self.risk_tolerance *= 0.7
            if 'retirement_account' not in self.current_products:
                self.current_products.append('retirement_account')
    
    def evaluate_digital_services(self):
        """Evaluate and potentially adopt digital services"""
        if self.digital_engagement_score > 0.5:
            if 'mobile_banking' not in self.current_products:
                if random.random() < self.digital_engagement_score * 0.3:
                    self.adopt_product('mobile_banking')
                    self.channel_preferences['mobile'] += 0.1
                    self.channel_preferences['branch'] -= 0.1
    
    def explore_new_products(self):
        """Actively explore new product offerings"""
        # Simulate product discovery through various channels
        discovery_channel = random.choices(
            list(self.channel_preferences.keys()),
            weights=list(self.channel_preferences.values())
        )[0]
        
        # Quality of discovery experience
        quality = random.uniform(0.4, 0.9)
        self.add_experience('product_discovery', discovery_channel, quality, 'Explored new products')
    
    def check_peer_recommendations(self):
        """Check for product recommendations from social network"""
        if self.social_network:
            for peer in self.social_network:
                if hasattr(peer, 'current_products'):
                    # See what products peers have that I don't
                    peer_products = set(peer.current_products)
                    my_products = set(self.current_products)
                    recommendations = peer_products - my_products
                    
                    for product in recommendations:
                        if random.random() < self.influence_susceptibility * 0.1:
                            if self.should_adopt_product(product):
                                self.adopt_product(product)
                                break
    
    def get_export_data(self) -> Dict[str, Any]:
        """Export retail-specific data for analysis"""
        base_data = super().get_export_data()
        
        retail_data = {
            'original_client_id': self.original_client_id,
            'csv_preferred_channel': self.csv_preferred_channel,
            'digital_engagement_score': self.digital_engagement_score,
            'product_appetite': self.product_appetite,
            'service_expectations': self.service_expectations,
            'life_events_count': len(self.life_events),
            'products_list': ','.join(self.current_products)
        }
        
        return {**base_data, **retail_data}