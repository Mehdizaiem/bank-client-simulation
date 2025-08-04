"""
Standalone API server that can run independently of the Dash application
"""
from flask import Flask
from flask_cors import CORS
import logging
from datetime import datetime
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.routes import api_app
from config.settings import APP_CONFIG


def create_api_server(config=None):
    """Create and configure the API server."""
    
    # Use the existing api_app from routes.py
    app = api_app
    
    # Apply additional configuration if provided
    if config:
        app.config.update(config)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    app.logger = logging.getLogger(__name__)
    
    # Log startup information
    @app.before_first_request
    def log_startup():
        app.logger.info("Bank Dashboard API Server starting up...")
        app.logger.info(f"Server started at: {datetime.now().isoformat()}")
    
    return app


def run_api_server(host='0.0.0.0', port=5000, debug=True):
    """Run the API server."""
    app = create_api_server()
    
    print("🏦 BANK DASHBOARD API SERVER")
    print("=" * 50)
    print(f"🚀 Starting API Server...")
    print(f"🌐 API URL: http://{host}:{port}")
    print(f"📊 Available endpoints:")
    print("   - GET  /api/health")
    print("   - GET  /api/clients/growth")
    print("   - GET  /api/clients/segmentation") 
    print("   - GET  /api/revenue/monthly")
    print("   - GET  /api/geography/distribution")
    print("   - GET  /api/economic/indicators")
    print("   - GET  /api/economic/trends")
    print("   - POST /api/chat/message")
    print("   - GET  /api/chat/suggestions")
    print("   - GET  /api/metrics/key")
    print("   - GET  /api/metrics/summary")
    print("   - GET  /api/export/csv/<data_type>")
    print("-" * 50)
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n🛑 API Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting API server: {e}")


if __name__ == '__main__':
    # Run the standalone API server
    run_api_server(
        host=APP_CONFIG.get('host', '0.0.0.0'),
        port=5000,  # Different port from Dash app
        debug=APP_CONFIG.get('debug', True)
    )