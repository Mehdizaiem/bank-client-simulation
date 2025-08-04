"""
API client for making requests to the REST API endpoints
"""
import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime


class APIClient:
    """Client for interacting with the Bank Dashboard API."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """Initialize API client with base URL."""
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to API endpoint."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'message': f"API request failed: {str(e)}",
                'timestamp': datetime.now().isoformat()
            }
    
    # ==================== DATA METHODS ====================
    
    def get_client_growth(self) -> Dict[str, Any]:
        """Get client growth data."""
        return self._make_request('GET', '/api/clients/growth')
    
    def get_client_segmentation(self) -> Dict[str, Any]:
        """Get client segmentation data."""
        return self._make_request('GET', '/api/clients/segmentation')
    
    def get_monthly_revenue(self) -> Dict[str, Any]:
        """Get monthly revenue data."""
        return self._make_request('GET', '/api/revenue/monthly')
    
    def get_geographic_distribution(self) -> Dict[str, Any]:
        """Get geographic distribution data."""
        return self._make_request('GET', '/api/geography/distribution')
    
    # ==================== ECONOMIC METHODS ====================
    
    def get_economic_indicators(self) -> Dict[str, Any]:
        """Get economic indicators."""
        return self._make_request('GET', '/api/economic/indicators')
    
    def get_economic_trends(self) -> Dict[str, Any]:
        """Get economic trends over time."""
        return self._make_request('GET', '/api/economic/trends')
    
    # ==================== AI CHAT METHODS ====================
    
    def send_chat_message(self, message: str) -> Dict[str, Any]:
        """Send message to AI chat."""
        return self._make_request('POST', '/api/chat/message', {'message': message})
    
    def get_chat_suggestions(self) -> Dict[str, Any]:
        """Get suggested chat questions."""
        return self._make_request('GET', '/api/chat/suggestions')
    
    # ==================== METRICS METHODS ====================
    
    def get_key_metrics(self) -> Dict[str, Any]:
        """Get key dashboard metrics."""
        return self._make_request('GET', '/api/metrics/key')
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary."""
        return self._make_request('GET', '/api/metrics/summary')
    
    # ==================== EXPORT METHODS ====================
    
    def export_csv_data(self, data_type: str) -> Dict[str, Any]:
        """Export data as CSV."""
        return self._make_request('GET', f'/api/export/csv/{data_type}')
    
    # ==================== UTILITY METHODS ====================
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health status."""
        return self._make_request('GET', '/api/health')
    
    def is_api_available(self) -> bool:
        """Check if API is available."""
        try:
            response = self.health_check()
            return response.get('status') == 'healthy'
        except Exception:
            return False


# ==================== CONVENIENCE FUNCTIONS ====================

def create_api_client(base_url: str = "http://localhost:5000") -> APIClient:
    """Create and return an API client instance."""
    return APIClient(base_url)


def test_api_connection(base_url: str = "http://localhost:5000") -> bool:
    """Test API connection."""
    client = create_api_client(base_url)
    return client.is_api_available()


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    # Example usage of the API client
    client = create_api_client()
    
    # Test API connection
    if client.is_api_available():
        print("✅ API is available")
        
        # Get client growth data
        growth_data = client.get_client_growth()
        print(f"Client Growth: {growth_data}")
        
        # Send chat message
        chat_response = client.send_chat_message("What are the current trends?")
        print(f"Chat Response: {chat_response}")
        
        # Get key metrics
        metrics = client.get_key_metrics()
        print(f"Key Metrics: {metrics}")
        
    else:
        print("❌ API is not available")