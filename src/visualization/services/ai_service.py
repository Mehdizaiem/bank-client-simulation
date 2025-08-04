"""
AI service for handling chat responses and AI-powered features
"""
from typing import Dict
from config.settings import CHAT_CONFIG


class AIService:
    """Service class for AI-powered features and chat responses."""
    
    # Predefined responses for different query types
    AI_RESPONSES = {
        'market': "Based on current data, the market shows a 3.2% growth trend with strong performance in the Tunis region.",
        'client': "Client satisfaction has increased by 12% this quarter, primarily due to improved digital services.",
        'branch': "We have 156 active branches across Tunisia, with highest concentration in urban areas.",
        'revenue': "Revenue projections show continued growth, with digital channels contributing 34% of total income.",
        'trend': "Current trends indicate a shift towards digital banking, with mobile transactions up 45% this year.",
        'risk': "Risk assessment shows stable portfolio performance with controlled exposure in key sectors.",
        'loan': "Loan approval rates have improved by 8% with enhanced AI-driven credit scoring systems.",
        'default': "I can help you analyze client trends, market data, branch performance, and financial metrics. What specific area interests you?"
    }
    
    @staticmethod
    def get_welcome_message() -> str:
        """Get the AI welcome message."""
        return CHAT_CONFIG['welcome_message']
    
    @staticmethod
    def process_user_message(message: str) -> str:
        """Process user message and return appropriate AI response."""
        if not message or not message.strip():
            return AIService.AI_RESPONSES['default']
        
        message_lower = message.lower()
        
        # Determine response category based on keywords
        response_key = AIService._categorize_message(message_lower)
        
        return AIService.AI_RESPONSES.get(response_key, AIService.AI_RESPONSES['default'])
    
    @staticmethod
    def _categorize_message(message: str) -> str:
        """Categorize user message to determine appropriate response."""
        keyword_mapping = {
            'market': ['market', 'trend', 'growth', 'economy', 'economic'],
            'client': ['client', 'customer', 'satisfaction', 'service', 'feedback'],
            'branch': ['branch', 'location', 'office', 'atm', 'physical'],
            'revenue': ['revenue', 'profit', 'money', 'financial', 'income', 'earning'],
            'trend': ['trend', 'trending', 'analysis', 'pattern', 'behavior'],
            'risk': ['risk', 'exposure', 'threat', 'security', 'compliance'],
            'loan': ['loan', 'credit', 'lending', 'mortgage', 'financing']
        }
        
        for category, keywords in keyword_mapping.items():
            if any(keyword in message for keyword in keywords):
                return category
        
        return 'default'
    
    @staticmethod
    def get_suggested_questions() -> list:
        """Get list of suggested questions for users."""
        return [
            "What are the current market trends?",
            "How is client satisfaction performing?",
            "Show me branch distribution analysis",
            "What's our revenue growth this quarter?",
            "Analyze risk exposure in our portfolio",
            "How are loan approval rates trending?"
        ]
    
    @staticmethod
    def generate_insights(data_type: str) -> Dict[str, str]:
        """Generate AI-powered insights based on data type."""
        insights = {
            'home': {
                'title': 'Key Insights',
                'content': 'Client growth is accelerating with digital adoption driving 34% of new acquisitions.'
            },
            'economic': {
                'title': 'Economic Analysis',
                'content': 'Economic indicators show stable growth with positive outlook for banking sector.'
            },
            'geographic': {
                'title': 'Geographic Trends',
                'content': 'Urban areas show 23% higher engagement rates compared to rural regions.'
            }
        }
        
        return insights.get(data_type, insights['home'])