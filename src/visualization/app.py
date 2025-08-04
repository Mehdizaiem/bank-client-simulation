"""
Main application entry point for the Bank Dashboard
"""
import dash
from dash import html, dcc

from components.sidebar import create_sidebar_navigation
from components.header import create_top_header
from pages.home import create_homepage_content
from config.colors import COLORS

# Import controllers
try:
    from controllers import (
        navigation_controller,
        chart_controller,
        chat_controller,
        export_controller,
        profile_controller
    )
    CONTROLLERS_LOADED = True
except ImportError as e:
    print(f"Warning: Could not import controllers: {e}")
    print("Make sure all controller files are present and properly structured.")
    CONTROLLERS_LOADED = False

# Initialize Dash app with suppress_callback_exceptions=True
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Bank Dashboard"

# Main layout
app.layout = html.Div([
    dcc.Store(id='current-page-store', data='home'),
    create_sidebar_navigation(),
    html.Div([
        create_top_header(),
        html.Div(
            id="page-content", 
            children=[create_homepage_content()], 
            style={
                'padding': '20px', 
                'backgroundColor': '#ffffff',
                'minHeight': 'calc(100vh - 80px)', 
                'overflowY': 'auto'
            }
        )
    ], style={'marginLeft': '280px', 'transition': 'margin-left 0.3s ease'})
], style={'fontFamily': 'Inter, sans-serif', 'backgroundColor': COLORS['light']})

# Register all controllers if they were loaded successfully
if CONTROLLERS_LOADED:
    try:
        navigation_controller.register_callbacks(app)
        chart_controller.register_callbacks(app)
        chat_controller.register_callbacks(app)
        export_controller.register_callbacks(app)
        profile_controller.register_callbacks(app)
        print("✅ All controllers registered successfully")
    except Exception as e:
        print(f"❌ Error registering controllers: {e}")
        print("The app will still run but some functionality may not work.")
else:
    print("⚠️  Running without controllers - limited functionality")

if __name__ == "__main__":
    print("🏦 MODERN BANK DASHBOARD - MODULAR VERSION")
    print("=" * 60)
    print("🚀 Starting Modern Bank Dashboard...")
    print("🌐 Dashboard URL: http://localhost:8050")
    print("🎯 Features: Multi-page navigation, AI Chat, Economic & Geographic Analysis")
    print("📊 Modern sidebar design with beautiful UI!")
    
    if CONTROLLERS_LOADED:
        print("✅ Full functionality enabled")
    else:
        print("⚠️  Limited functionality - some features may not work")
        print("   Make sure all files are in the correct directory structure")
    
    print("-" * 60)
    app.run(debug=True, host='0.0.0.0', port=8050)