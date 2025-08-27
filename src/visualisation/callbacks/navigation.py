"""
callbacks/navigation.py - Updated to handle profile and settings routes
Drop this into src/visualisation/callbacks/navigation.py
"""

import dash
from dash import Input, Output, State, html, no_update
from pages.home import create_simulation_homepage_content
from pages.economic import create_economic_simulation_content
from pages.geographic import create_geographic_simulation_content
from pages.chat import create_simulation_chat_content
from pages.profile import create_profile_page_content
from pages.settings import create_simulation_settings_content


def register_navigation_callbacks(app):
    """Register navigation callbacks for the dashboard"""
    
    @app.callback(
        [Output("page-content", "children"),
         Output("page-title", "children"),
         Output("page-store", "data")],
        [Input("url", "pathname"),
         Input("nav-home", "n_clicks"),
         Input("nav-economic", "n_clicks"),
         Input("nav-geographic", "n_clicks"),
         Input("nav-chat", "n_clicks"),
         Input("nav-settings", "n_clicks"),
         Input("nav-profile", "n_clicks")],
        [State("page-store", "data")]
    )
    def update_page_content(pathname, home_clicks, econ_clicks, geo_clicks, 
                           chat_clicks, settings_clicks, profile_clicks, current_page):
        """Update page content based on navigation"""
        
        # Handle URL-based navigation first (for direct links)
        if pathname:
            if pathname == "/profile":
                return create_profile_page_content(), "Profile", "profile"
            elif pathname == "/settings":
                return create_simulation_settings_content(), "Settings", "settings"
            elif pathname == "/economic":
                return create_economic_simulation_content(), "Economic Simulation", "economic"
            elif pathname == "/geographic":
                return create_geographic_simulation_content(), "Geographic Analysis", "geographic"
            elif pathname == "/chat":
                return create_simulation_chat_content(), "AI Assistant", "chat"
            elif pathname == "/" or pathname == "/home":
                return create_simulation_homepage_content(), "Dashboard Overview", "home"
        
        # Handle sidebar navigation clicks
        ctx = dash.callback_context
        if not ctx.triggered:
            return create_simulation_homepage_content(), "Dashboard Overview", "home"
        
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if button_id == "nav-home":
            return create_simulation_homepage_content(), "Dashboard Overview", "home"
        elif button_id == "nav-economic":
            return create_economic_simulation_content(), "Economic Simulation", "economic"
        elif button_id == "nav-geographic":
            return create_geographic_simulation_content(), "Geographic Analysis", "geographic"
        elif button_id == "nav-chat":
            return create_simulation_chat_content(), "AI Assistant", "chat"
        elif button_id == "nav-settings":
            return create_simulation_settings_content(), "Settings", "settings"
        elif button_id == "nav-profile":
            return create_profile_page_content(), "Profile", "profile"
        
        # Default to home
        return create_simulation_homepage_content(), "Dashboard Overview", "home"