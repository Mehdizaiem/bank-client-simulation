"""
AI service for handling simulation chat responses and AI-powered banking features
"""
from typing import Dict
from config.settings import CHAT_CONFIG


class AIService:
    """Service class for AI-powered simulation features and chat responses."""
    
    # Simulation-specific responses for banking context
    SIMULATION_RESPONSES = {
        # Branch and Geographic
        'branch_closure': "Simulating branch closure in {location}: Expected 15% client migration to nearest branch, 8% potential churn to competitors. Digital adoption would increase by 25% among affected clients.",
        'branch_opening': "New branch simulation for {location}: ROI projection 18-24 months, estimated 2,500 new clients in first year, 12% market share increase in catchment area.",
        'branch_relocation': "Branch relocation impact: 92% client retention expected, improved accessibility could increase foot traffic by 30%.",
        
        # Economic Scenarios
        'currency_devaluation': "Currency devaluation simulation: 20% increase in USD-linked product demand, 15% rise in savings withdrawals, corporate clients showing hedging behavior.",
        'inflation_impact': "Inflation scenario: Retail clients reducing luxury spending by 35%, increased demand for inflation-protected products, loan applications down 12%.",
        'interest_rate': "Interest rate change impact: {direction} in deposits by {percentage}%, mortgage applications {trend}, SME lending affected significantly.",
        
        # Client Behavior
        'client_churn': "Churn analysis shows: Price-sensitive clients (25%) most at risk, relationship duration negatively correlates with churn probability. Retention strategies recommended for high-value segments.",
        'digital_adoption': "Digital adoption simulation: Mobile banking usage up 45%, branch visits down 30%, cost-per-transaction reduced by €2.50 on average.",
        'product_launch': "New product simulation: {product} expected uptake 12-15% among target demographic, revenue impact €450K annually, requires 6-month marketing investment.",
        
        # Market and Competition
        'competitor_entry': "Competitor entry simulation: 8-12% market share erosion expected, price pressure on standard products, differentiation through service quality becomes critical.",
        'market_expansion': "Market expansion to {region}: Untapped potential 3,200 clients, cultural adaptation required, local partnership recommended.",
        'pricing_strategy': "Pricing simulation: {percentage}% fee reduction increases client acquisition by {factor}x but reduces margin by {margin}%. Net positive after 14 months.",
        
        # Regional Analysis
        'regional_performance': "Regional analysis - {region}: {performance} performing, {insights}. Demographic trends favor {opportunities}.",
        'governorate_trends': "Governorate analysis: Tunis leads in digital adoption (89%), Sfax strong in SME banking, southern regions underserved but growing.",
        
        # Risk and Compliance
        'risk_assessment': "Portfolio risk simulation: Current exposure within acceptable limits, stress testing shows resilience to 15% economic downturn.",
        'regulatory_impact': "Regulatory change simulation: Compliance costs increase €120K annually, operational adjustments required in 3 months.",
        
        # General simulation queries
        'simulation_help': "I can run simulations for: Branch strategies, Economic scenarios, Client behavior modeling, Competition analysis, Regional expansion, Product launches, and Risk assessments. What would you like to explore?",
        'default': "I'm your AI assistant for bank client simulation. I can help model branch strategies, economic scenarios, client behavior, and market dynamics across Tunisia. What simulation would you like to run?"
    }
    
    @staticmethod
    def get_welcome_message() -> str:
        """Get the AI simulation welcome message."""
        return ("Welcome! I'm your AI Simulation Assistant for the Bank Client Platform. "
                "I can help you run scenarios, interpret simulation results, analyze client behavior patterns, "
                "and provide strategic insights for your Tunisian banking operations.")
    
    @staticmethod
    def process_user_message(message: str) -> str:
        """Process user message and return appropriate AI simulation response."""
        if not message or not message.strip():
            return AIService.SIMULATION_RESPONSES['default']
        
        message_lower = message.lower()
        
        # Extract entities and parameters from message
        entities = AIService._extract_entities(message_lower)
        
        # Determine response category based on simulation keywords
        response_key = AIService._categorize_simulation_message(message_lower)
        
        # Get base response and customize with entities
        response = AIService.SIMULATION_RESPONSES.get(response_key, AIService.SIMULATION_RESPONSES['default'])
        
        # Customize response with extracted entities
        return AIService._customize_response(response, entities)
    
    @staticmethod
    def _categorize_simulation_message(message: str) -> str:
        """Categorize user message for simulation context."""
        simulation_keywords = {
            # Branch operations
            'branch_closure': ['close', 'closure', 'shut', 'fermer', 'fermeture'],
            'branch_opening': ['open', 'new branch', 'ouvrir', 'nouvelle agence'],
            'branch_relocation': ['relocate', 'move', 'déplacer', 'relocaliser'],
            
            # Economic scenarios
            'currency_devaluation': ['devaluation', 'dinar', 'currency', 'dévaluation', 'devise'],
            'inflation_impact': ['inflation', 'price', 'cost', 'inflation'],
            'interest_rate': ['interest rate', 'taux', 'rate', 'pourcentage'],
            
            # Client behavior
            'client_churn': ['churn', 'attrition', 'leaving', 'quitter', 'partir'],
            'digital_adoption': ['digital', 'mobile', 'app', 'numérique', 'application'],
            'product_launch': ['launch', 'new product', 'lancement', 'nouveau produit'],
            
            # Competition and market
            'competitor_entry': ['competitor', 'competition', 'concurrence', 'concurrent'],
            'market_expansion': ['expansion', 'expand', 'growth', 'croissance', 'développement'],
            'pricing_strategy': ['price', 'fee', 'cost', 'prix', 'tarif', 'coût'],
            
            # Regional
            'regional_performance': ['region', 'regional', 'area', 'région', 'zone'],
            'governorate_trends': ['governorate', 'gouvernorat', 'tunis', 'sfax', 'sousse'],
            
            # Risk and compliance
            'risk_assessment': ['risk', 'exposure', 'threat', 'risque', 'exposition'],
            'regulatory_impact': ['regulation', 'compliance', 'law', 'réglementation', 'conformité'],
            
            # General
            'simulation_help': ['help', 'aide', 'comment', 'how', 'what can'],
        }
        
        for category, keywords in simulation_keywords.items():
            if any(keyword in message for keyword in keywords):
                return category
        
        return 'default'
    
    @staticmethod
    def _extract_entities(message: str) -> Dict[str, str]:
        """Extract entities like location, percentage, product names from message."""
        entities = {}
        
        # Extract governorates
        governorates = ['tunis', 'sfax', 'sousse', 'kairouan', 'bizerte', 'ariana', 'nabeul', 'gabès']
        for gov in governorates:
            if gov in message:
                entities['location'] = gov.title()
                entities['region'] = gov.title()
                break
        
        # Extract percentages
        import re
        percentage_match = re.search(r'(\d+)%', message)
        if percentage_match:
            entities['percentage'] = percentage_match.group(1)
        
        # Extract numbers
        number_match = re.search(r'(\d+)', message)
        if number_match:
            entities['number'] = number_match.group(1)
        
        # Extract products
        products = ['credit', 'loan', 'mortgage', 'savings', 'current account', 'mobile banking']
        for product in products:
            if product in message:
                entities['product'] = product
                break
        
        return entities
    
    @staticmethod
    def _customize_response(response: str, entities: Dict[str, str]) -> str:
        """Customize response with extracted entities."""
        # Simple template replacement
        for key, value in entities.items():
            placeholder = f"{{{key}}}"
            if placeholder in response:
                response = response.replace(placeholder, value)
        
        # Add location-specific insights
        if 'location' in entities:
            location = entities['location']
            if location == 'Tunis':
                response += " Note: Tunis market shows high digital adoption and competitive landscape."
            elif location == 'Sfax':
                response += " Note: Sfax has strong SME presence and industrial client base."
            elif location == 'Sousse':
                response += " Note: Sousse benefits from tourism and coastal economic activity."
        
        return response
    
    @staticmethod
    def get_simulation_suggestions() -> list:
        """Get list of simulation-specific suggested questions."""
        return [
            "🎯 Run a branch closure simulation for Kairouan",
            "💱 What happens if the dinar devalues by 15%?",
            "📱 Simulate launching a mobile-only banking service",
            "🏛️ How would a competitor entering Sfax affect us?",
            "📊 Show me client churn patterns in northern Tunisia",
            "💳 Test impact of reducing fees by 20%",
            "🏪 Where should we open our next branch?",
            "📈 Analyze corporate client behavior trends"
        ]
    
    @staticmethod
    def generate_simulation_insights(simulation_type: str) -> Dict[str, str]:
        """Generate AI-powered insights based on simulation type."""
        insights = {
            'branch_strategy': {
                'title': '🏪 Branch Strategy Insights',
                'content': 'Optimal branch placement in emerging suburbs shows 23% higher ROI than city center locations. Digital-first branches reduce operational costs by 40%.'
            },
            'economic_scenario': {
                'title': '💱 Economic Impact Analysis',
                'content': 'Currency volatility creates opportunities in forex services. Recommend increasing USD product portfolio by 30% to capture demand.'
            },
            'client_behavior': {
                'title': '👥 Client Behavior Patterns',
                'content': 'Young professionals (25-35) drive 67% of digital adoption. Rural clients prefer branch relationships but accept digital for routine transactions.'
            },
            'market_competition': {
                'title': '🏛️ Competitive Intelligence',
                'content': 'Fintech disruption strongest in urban areas. Traditional banks maintain advantage in corporate and government sectors.'
            }
        }
        
        return insights.get(simulation_type, insights['branch_strategy'])
    
    @staticmethod
    def process_quick_action(action_type: str) -> str:
        """Process quick action requests from the interface."""
        quick_responses = {
            'branch_calc': "Branch Impact Calculator: Select target location and strategy type. I'll analyze client migration patterns, revenue impact, and ROI projections.",
            'economic_test': "Economic Scenario Tester: Choose economic event type and severity. I'll model client responses and portfolio effects across all segments.",
            'behavior_analyze': "Client Behavior Analyzer: Analyzing current patterns... Digital adoption varies by region: Tunis (89%), Sfax (76%), rural areas (45%).",
            'opportunity_find': "Market Opportunity Finder: Scanning for underserved areas... High potential in Ariana (young demographics), Bizerte (industrial growth)."
        }
        
        return quick_responses.get(action_type, "I'm ready to help with your simulation request. Please provide more specific details about what you'd like to analyze.")
    
    # Legacy methods for compatibility
    @staticmethod
    def get_suggested_questions() -> list:
        """Get list of suggested questions for users (legacy)."""
        return [
            "What are the current market trends?",
            "How is client satisfaction performing?", 
            "Show me branch distribution analysis",
            "What's our revenue growth this quarter?",
            "Analyze risk exposure in our portfolio",
            "How are loan approval rates trending?"
        ]