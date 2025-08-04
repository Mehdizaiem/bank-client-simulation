"""
Main application file for Bank Client Simulation Dashboard
Run this file to start the dashboard server
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.visualization.dashboard import create_dashboard
from src.visualization.utils.config import DashboardConfig
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dashboard.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main function to run the dashboard"""
    try:
        # Load configuration
        config_file = "simulation_config.yaml"
        if os.path.exists(config_file):
            config = DashboardConfig.from_file(config_file)
            logger.info(f"Loaded configuration from {config_file}")
        else:
            config = DashboardConfig.from_env()
            logger.info("Using environment-based configuration")
        
        # Create and run dashboard
        dashboard = create_dashboard(config)
        
        logger.info("="*50)
        logger.info("🏦 BANK CLIENT SIMULATION DASHBOARD")
        logger.info("="*50)
        logger.info(f"🌐 Server running on: http://{config.host}:{config.port}")
        logger.info(f"🔧 Debug mode: {config.debug}")
        logger.info(f"⏱️  Update interval: {config.update_interval}ms")
        logger.info("="*50)
        logger.info("Press Ctrl+C to stop the server")
        logger.info("="*50)
        
        # Run the server
        dashboard.run_server(
            debug=config.debug,
            host=config.host,
            port=config.port
        )
        
    except KeyboardInterrupt:
        logger.info("\n👋 Dashboard server stopped by user")
    except Exception as e:
        logger.error(f"❌ Error starting dashboard: {e}")
        raise

if __name__ == "__main__":
    main()