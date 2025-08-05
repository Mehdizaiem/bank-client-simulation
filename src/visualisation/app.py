"""
Bank Client Simulation Platform - Main Application
Run this file to start the Dash application
"""

import dash
from dash import html, dcc, Input, Output, State, callback_context
import sys
import os
from dotenv import load_dotenv
load_dotenv()

# Get configuration
HOST = os.getenv('DASHBOARD_HOST', '0.0.0.0')
PORT = int(os.getenv('DASHBOARD_PORT', '8050'))
DEBUG = os.getenv('DASHBOARD_DEBUG', 'true').lower() == 'true'
# Add the current directory to Python path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import components and services
    from components.sidebar import create_sidebar_navigation
    from components.header import create_top_header
    from pages.home import create_simulation_homepage_content
    from pages.economic import create_economic_simulation_content
    from pages.geographic import create_geographic_simulation_content
    from pages.chat import create_simulation_chat_content
    from pages.profile import create_profile_page_content
    from pages.settings import create_simulation_settings_content
    from config.colors import COLORS
    from config.settings import DASHBOARD_CONFIG
    
    # Import callbacks and UI interactions
    from callbacks.navigation import register_navigation_callbacks
    from callbacks.chat import register_chat_callbacks
    from callbacks.ui_interactions import register_ui_callbacks
    from components.charts import register_all_chart_callbacks
    
    print("✅ All imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all files are in the correct directories and try again.")
    sys.exit(1)

# Initialize the Dash app with custom CSS
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Bank Client Simulation Platform"

# Add custom CSS to prevent chart stretching and improve layout
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            /* Chart styling improvements */
            .js-plotly-plot {
                width: 100% !important;
                height: 300px !important;
            }
            .plot-container {
                width: 100% !important;
                height: 300px !important;
            }
            .main-svg {
                width: 100% !important;
                height: 300px !important;
            }
            
            /* Responsive design */
            @media (max-width: 768px) {
                .js-plotly-plot {
                    height: 250px !important;
                }
                .plot-container {
                    height: 250px !important;
                }
                .main-svg {
                    height: 250px !important;
                }
            }
            
            /* Chart container improvements */
            .chart-row {
                display: flex !important;
                gap: 20px !important;
                margin-bottom: 30px !important;
                align-items: stretch !important;
            }
            
            .chart-container {
                flex: 1 !important;
                min-width: 0 !important;
                display: flex !important;
                flex-direction: column !important;
            }
            
            /* Page layout improvements */
            body {
                margin: 0;
                padding: 0;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            
            /* Scrollbar styling */
            ::-webkit-scrollbar {
                width: 6px;
            }
            ::-webkit-scrollbar-track {
                background: #f1f1f1;
            }
            ::-webkit-scrollbar-thumb {
                background: #c1c1c1;
                border-radius: 3px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #a8a8a8;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define the main app layout
app.layout = html.Div([
    # Store for page state
    dcc.Store(id='page-store', data='home'),
    
    # Sidebar
    create_sidebar_navigation(),
    
    # Main content area
    html.Div([
        create_top_header(),
        html.Div(id='page-content', style={'padding': '30px'})
    ], style={
        'marginLeft': f'{DASHBOARD_CONFIG["sidebar_width"]}px',
        'backgroundColor': COLORS['light'],
        'minHeight': '100vh'
    })
])

# Register all callbacks
register_navigation_callbacks(app)
register_chat_callbacks(app)
register_ui_callbacks(app)
register_all_chart_callbacks(app)

# Run the app
if __name__ == '__main__':
    print("🏦 Starting Bank Client Simulation Platform...")
    print("🌐 Open your browser and go to: http://localhost:8050")
    print("🚀 Platform Features:")
    print("   • AI-powered client behavior simulation")
    print("   • Economic scenario modeling")
    print("   • Geographic analysis for Tunisia")
    print("   • Interactive chat assistant")
    print("   • Real-time dashboard analytics")
    
    app.run(debug=DEBUG, host=HOST, port=PORT)