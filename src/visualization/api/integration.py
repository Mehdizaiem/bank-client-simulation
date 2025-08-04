"""
Integration layer for connecting Dash app with REST API
"""
import threading
import time
from typing import Optional, Dict, Any
from api.server import create_api_server
from api.client import APIClient
import logging


class APIIntegration:
    """Integration manager for API and Dash app."""
    
    def __init__(self, api_port: int = 5000, dash_port: int = 8050):
        """Initialize API integration."""
        self.api_port = api_port
        self.dash_port = dash_port
        self.api_server = None
        self.api_client = None
        self.api_thread = None
        self.logger = logging.getLogger(__name__)
    
    def start_api_server(self) -> bool:
        """Start the API server in a separate thread."""
        try:
            self.api_server = create_api_server()
            
            def run_server():
                self.api_server.run(
                    host='0.0.0.0', 
                    port=self.api_port, 
                    debug=False,  # Disable debug in threaded mode
                    use_reloader=False
                )
            
            self.api_thread = threading.Thread(target=run_server, daemon=True)
            self.api_thread.start()
            
            # Wait a moment for server to start
            time.sleep(2)
            
            # Initialize API client
            self.api_client = APIClient(f"http://localhost:{self.api_port}")
            
            # Test connection
            if self.api_client.is_api_available():
                self.logger.info(f"API server started successfully on port {self.api_port}")
                return True
            else:
                self.logger.error("API server failed to start or is not responding")
                return False
                
        except Exception as e:
            self.logger.error(f"Error starting API server: {e}")
            return False
    
    def stop_api_server(self):
        """Stop the API server."""