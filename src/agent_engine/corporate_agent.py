"""
Corporate Client Agent implementation
Uses actual data from hamza_corporate_agents.csv
"""
from src.agent_engine.base_agent import BaseClientAgent
import random
from typing import Dict, Any, List

class CorporateClientAgent(BaseClientAgent):
    """Corporate banking client with business-specific behaviors"""
    
    def __init__(self, model, client_data: Dict[str, Any]):
        """
        Initialize corporate client from CSV data
        
        Args:
            model: Reference to BankSimulationModel
            client_data: Dictionary from hamza_corporate_agents.csv
        """
        # Convert corporate data to base agent format
        base_data = {
            'client_type': 'corporate',
            'age': 40,  # Corporate entities don't have age - use default
            'income': client_data.get('annual_revenue', 500000) / 12,  # Monthly from annual
            'governorate': client_data.get('headquarters_governorate', 'Tunis'),
            'education_level': 'university',  # Assume corporate decision makers are educated
            'employment_sector': client_data.get('business_sector', 'services'),
            'risk_tolerance': self.calculate_corporate_risk_tolerance(client_data)
        }
        
        # Initialize base class
        super().__init__(model, base_data)
        
        # CORPORATE-SPECIFIC ATTRIBUTES FROM CSV
        self.original_client_id = client_data.get('client_id', f'C_{self.unique_id}')
        self.company_name = client_data.get('company_name', f'Company_{self.unique_id}')
        self.business_sector = client_data.get('business_sector', 'services')
        self.company_size = client_data.get('company_size', 'small')
        self.annual_revenue = client_data.get('annual_revenue', 500000)
        self.digital_maturity_score = client_data.get('digital_maturity_score', 0.5)
        
        # CORPORATE BEHAVIORAL ATTRIBUTES
        self.business_complexity = self.calculate_business_complexity()
        self.growth_orientation = self.calculate_growth_orientation()
        self.cash_flow_stability = random.uniform(0.4, 0.9)
        self.international_operations = self.annual_revenue > 1000000 and random.random() < 0.3
        
        # CORPORATE BANKING NEEDS
        self.financing_needs = self.calculate_financing_needs()
        self.transaction_volume = self.calculate_transaction_volume()
        self.seasonal_pattern = self.determine_seasonal_pattern()
        
        # DECISION MAKING
        self.decision_makers = random.randint(1, 5 if self.company_size == 'large' else 2)
        self.decision_speed = 'fast' if self.company_size == 'small' else 'slow'
        
        # RELATIONSHIP MANAGEMENT
        self.relationship_manager_assigned = self.company_size in ['medium', 'large']
        self.relationship_quality = 0.6 if self.relationship_manager_assigned else 0.4
        
        # Initialize corporate products
        self.initialize_corporate_products()
        
        # Business events tracking
        self.business_events = []
        self.next_business_review = random.randint(5, 15)
    
    def calculate_corporate_risk_tolerance(self, data: Dict) -> float:
        """Calculate risk tolerance based on company profile"""
        base_risk = 0.5
        
        # Sector adjustments
        sector_risk = {
            'technology': 0.7,
            'retail': 0.5,
            'manufacturing': 0.4,
            'services': 0.5,
            'agriculture': 0.3,
            'construction': 0.6
        }
        base_risk = sector_risk.get(data.get('business_sector', 'services'), 0.5)
        
        # Size adjustments
        size_factor = {
            'micro': 0.8,
            'small': 1.0,
            'medium': 0.9,
            'large': 0.7
        }
        base_risk *= size_factor.get(data.get('company_size', 'small'), 1.0)
        
        # Digital maturity increases risk tolerance slightly
        base_risk += data.get('digital_maturity_score', 0.5) * 0.1
        
        return min(1.0, max(0.1, base_risk))
    
    def calculate_business_complexity(self) -> float:
        """Calculate business complexity score"""
        complexity = 0.3
        
        # Size increases complexity
        size_complexity = {
            'micro': 0.2,
            'small': 0.4,
            'medium': 0.6,
            'large': 0.8
        }
        complexity = size_complexity.get(self.company_size, 0.4)
        
        # Sector complexity
        if self.business_sector in ['manufacturing', 'technology']:
            complexity += 0.2
        
        # Revenue adds complexity
        if self.annual_revenue > 1000000:
            complexity += 0.2
        elif self.annual_revenue > 500000:
            complexity += 0.1
        
        return min(1.0, complexity)
    
    def calculate_growth_orientation(self) -> float:
        """Calculate how growth-oriented the company is"""
        growth = 0.5
        
        # Sector growth orientation
        if self.business_sector == 'technology':
            growth = 0.8
        elif self.business_sector in ['services', 'retail']:
            growth = 0.6
        elif self.business_sector in ['manufacturing', 'agriculture']:
            growth = 0.4
        
        # Small companies often more growth-oriented
        if self.company_size == 'small':
            growth += 0.1
        
        # Digital maturity indicates growth orientation
        growth += self.digital_maturity_score * 0.2
        
        return min(1.0, growth)
    
    def calculate_financing_needs(self) -> Dict[str, float]:
        """Calculate various financing needs"""
        needs = {
            'working_capital': 0.5,
            'equipment_financing': 0.3,
            'expansion_capital': 0.2,
            'trade_finance': 0.1
        }
        
        # Adjust based on sector
        if self.business_sector == 'manufacturing':
            needs['equipment_financing'] += 0.3
            needs['working_capital'] += 0.2
        elif self.business_sector == 'retail':
            needs['working_capital'] += 0.4
            needs['trade_finance'] += 0.2
        elif self.business_sector == 'technology':
            needs['expansion_capital'] += 0.3
        
        # Adjust based on size
        if self.company_size in ['medium', 'large']:
            needs['trade_finance'] += 0.2
            needs['expansion_capital'] += 0.1
        
        return needs
    
    def calculate_transaction_volume(self) -> str:
        """Calculate expected transaction volume"""
        if self.annual_revenue > 5000000:
            return 'very_high'
        elif self.annual_revenue > 1000000:
            return 'high'
        elif self.annual_revenue > 500000:
            return 'medium'
        else:
            return 'low'
    
    def determine_seasonal_pattern(self) -> str:
        """Determine if business has seasonal patterns"""
        seasonal_sectors = {
            'agriculture': 'high_seasonal',
            'retail': 'moderate_seasonal',
            'services': 'low_seasonal',
            'manufacturing': 'low_seasonal',
            'technology': 'none'
        }
        return seasonal_sectors.get(self.business_sector, 'low_seasonal')
    
    def initialize_corporate_products(self):
        """Initialize typical corporate banking products"""
        # All corporates have business checking
        self.current_products = ['business_checking']
        
        # Add products based on profile
        if self.transaction_volume in ['medium', 'high', 'very_high']:
            self.current_products.append('cash_management')
        
        if self.annual_revenue > 500000:
            if random.random() < 0.7:
                self.current_products.append('business_credit_line')
        
        if self.international_operations:
            self.current_products.append('trade_finance')
            self.current_products.append('fx_services')
        
        if self.digital_maturity_score > 0.6:
            self.current_products.append('online_banking_corporate')
        
        if self.company_size in ['medium', 'large']:
            if random.random() < 0.5:
                self.current_products.append('payroll_services')
    
    def step(self):
        """Corporate client step with business-specific behaviors"""
        # Call parent step for basic behaviors
        super().step()
        
        # CORPORATE-SPECIFIC BEHAVIORS
        
        # 1. Business review cycle
        if self.model.current_step >= self.next_business_review:
            self.conduct_business_review()
            self.next_business_review = self.model.current_step + random.randint(10, 30)
        
        # 2. Cash flow management
        if random.random() < 0.1:  # 10% chance each step
            self.manage_cash_flow()
        
        # 3. Evaluate financing options
        if random.random() < self.growth_orientation * 0.05:
            self.evaluate_financing_options()
        
        # 4. Digital transformation considerations
        if random.random() < 0.02:
            self.consider_digital_upgrades()
        
        # 5. Relationship management interaction
        if self.relationship_manager_assigned and random.random() < 0.05:
            self.interact_with_relationship_manager()
    
    def evaluate_product_portfolio(self):
        """Corporate-specific product evaluation"""
        # Evaluate business needs
        current_needs = self.assess_current_business_needs()
        
        for need, urgency in current_needs.items():
            if urgency > 0.6:
                product = self.map_need_to_product(need)
                if product and product not in self.current_products:
                    if self.should_adopt_corporate_product(product, urgency):
                        self.adopt_product(product)
        
        # Review existing products for relevance
        for product in self.current_products[:]:
            if self.should_drop_corporate_product(product):
                self.drop_product(product)
    
    def assess_current_business_needs(self) -> Dict[str, float]:
        """Assess current business banking needs"""
        needs = {}
        
        # Working capital needs
        if self.cash_flow_stability < 0.5:
            needs['working_capital'] = 0.8
        
        # Growth financing
        if self.growth_orientation > 0.7:
            needs['expansion_financing'] = 0.7
        
        # Digital services
        if self.digital_maturity_score > 0.6 and 'online_banking_corporate' not in self.current_products:
            needs['digital_banking'] = 0.8
        
        # International services
        if self.international_operations:
            needs['international_banking'] = 0.9
        
        return needs
    
    def map_need_to_product(self, need: str) -> str:
        """Map business need to specific product"""
        mapping = {
            'working_capital': 'business_credit_line',
            'expansion_financing': 'term_loan',
            'digital_banking': 'online_banking_corporate',
            'international_banking': 'trade_finance'
        }
        return mapping.get(need)
    
    def should_adopt_corporate_product(self, product: str, urgency: float) -> bool:
        """Decide whether to adopt a new corporate product"""
        # Base probability influenced by urgency
        adoption_prob = urgency * 0.5
        
        # Relationship quality matters for corporate decisions
        adoption_prob *= (0.5 + self.relationship_quality * 0.5)
        
        # Digital readiness for digital products
        if 'online' in product or 'digital' in product:
            adoption_prob *= self.digital_maturity_score
        
        # Size affects decision speed
        if self.company_size == 'large':
            adoption_prob *= 0.7  # Slower decisions
        elif self.company_size == 'small':
            adoption_prob *= 1.2  # Faster decisions
        
        return random.random() < adoption_prob
    
    def should_drop_corporate_product(self, product: str) -> bool:
        """Decide whether to drop a corporate product"""
        # Never drop core business checking
        if product == 'business_checking':
            return False
        
        # Low satisfaction increases drop probability
        drop_prob = (1 - self.satisfaction_level) * 0.03  # Lower than retail
        
        # Poor relationship quality increases drop probability
        if self.relationship_manager_assigned:
            drop_prob *= (1 - self.relationship_quality)
        
        return random.random() < drop_prob
    
    def conduct_business_review(self):
        """Conduct periodic business review"""
        self.business_events.append({
            'event': 'business_review',
            'step': self.model.current_step
        })
        
        # Review may lead to changes
        if random.random() < 0.3:
            # Growth scenario
            self.annual_revenue *= random.uniform(1.05, 1.15)
            self.growth_orientation = min(1.0, self.growth_orientation + 0.1)
        elif random.random() < 0.1:
            # Contraction scenario
            self.annual_revenue *= random.uniform(0.85, 0.95)
            self.cash_flow_stability *= 0.9
    
    def manage_cash_flow(self):
        """Manage cash flow and liquidity"""
        # Simulate cash flow event
        if self.seasonal_pattern == 'high_seasonal':
            # More volatile cash flow
            self.cash_flow_stability += random.uniform(-0.2, 0.2)
        else:
            self.cash_flow_stability += random.uniform(-0.05, 0.05)
        
        self.cash_flow_stability = max(0.1, min(1.0, self.cash_flow_stability))
        
        # Poor cash flow may trigger financing needs
        if self.cash_flow_stability < 0.3:
            self.financing_needs['working_capital'] = min(1.0, self.financing_needs['working_capital'] + 0.2)
    
    def evaluate_financing_options(self):
        """Evaluate financing options for growth"""
        max_need = max(self.financing_needs.values())
        
        if max_need > 0.6:
            # High financing need - consider loan products
            experience_quality = 0.7 if self.relationship_manager_assigned else 0.5
            self.add_experience('financing_consultation', 'branch', experience_quality, 
                              'Discussed financing options')
    
    def consider_digital_upgrades(self):
        """Consider upgrading digital banking capabilities"""
        if self.digital_maturity_score < 0.8:
            # Gradual digital transformation
            self.digital_maturity_score += 0.02
            
            # May adopt digital products
            if self.digital_maturity_score > 0.6 and 'online_banking_corporate' not in self.current_products:
                if random.random() < 0.3:
                    self.adopt_product('online_banking_corporate')
    
    def interact_with_relationship_manager(self):
        """Interact with relationship manager"""
        # Quality of interaction
        interaction_quality = random.uniform(0.5, 1.0) if self.relationship_quality > 0.6 else random.uniform(0.3, 0.7)
        
        self.add_experience('rm_interaction', 'branch', interaction_quality, 
                          'Relationship manager meeting')
        
        # Update relationship quality
        self.relationship_quality = 0.9 * self.relationship_quality + 0.1 * interaction_quality
    
    def get_export_data(self) -> Dict[str, Any]:
        """Export corporate-specific data for analysis"""
        base_data = super().get_export_data()
        
        corporate_data = {
            'original_client_id': self.original_client_id,
            'company_name': self.company_name,
            'business_sector': self.business_sector,
            'company_size': self.company_size,
            'annual_revenue': self.annual_revenue,
            'digital_maturity_score': self.digital_maturity_score,
            'business_complexity': self.business_complexity,
            'growth_orientation': self.growth_orientation,
            'cash_flow_stability': self.cash_flow_stability,
            'transaction_volume': self.transaction_volume,
            'relationship_quality': self.relationship_quality,
            'has_rm': self.relationship_manager_assigned,
            'products_list': ','.join(self.current_products)
        }
        
        return {**base_data, **corporate_data}