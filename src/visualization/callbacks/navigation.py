"""
Navigation callbacks for the Bank Client Simulation Platform
"""
from dash import Input, Output, callback_context
from config.colors import COLORS
from pages.home import create_simulation_homepage_content
from pages.economic import create_economic_simulation_content
from pages.geographic import create_geographic_simulation_content
from pages.chat import create_simulation_chat_content
from pages.profile import create_profile_page_content
from pages.settings import create_simulation_settings_content


def register_navigation_callbacks(app):
    """Register all navigation-related callbacks."""
    
    @app.callback(
        [Output('page-content', 'children'),
         Output('page-title', 'children')],
        [Input('nav-home', 'n_clicks'),
         Input('nav-economic', 'n_clicks'),
         Input('nav-geographic', 'n_clicks'),
         Input('nav-chat', 'n_clicks'),
         Input('nav-profile', 'n_clicks'),
         Input('nav-settings', 'n_clicks')],
        prevent_initial_call=False
    )
    def update_page_content(home_clicks, economic_clicks, geographic_clicks, 
                           chat_clicks, profile_clicks, settings_clicks):
        """Update page content based on navigation clicks."""
        ctx = callback_context
        
        if not ctx.triggered:
            return create_simulation_homepage_content(), "Dashboard Overview"
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        page_map = {
            'nav-home': (create_simulation_homepage_content(), "Dashboard Overview"),
            'nav-economic': (create_economic_simulation_content(), "Economic Analysis"),
            'nav-geographic': (create_geographic_simulation_content(), "Geographic Analysis"),
            'nav-chat': (create_simulation_chat_content(), "AI Chat Assistant"),
            'nav-profile': (create_profile_page_content(), "User Profile"),
            'nav-settings': (create_simulation_settings_content(), "Settings")
        }
        
        return page_map.get(button_id, (create_simulation_homepage_content(), "Dashboard Overview"))

    @app.callback(
        [Output('nav-home', 'style'),
         Output('nav-economic', 'style'),
         Output('nav-geographic', 'style'),
         Output('nav-chat', 'style'),
         Output('nav-profile', 'style'),
         Output('nav-settings', 'style')],
        [Input('nav-home', 'n_clicks'),
         Input('nav-economic', 'n_clicks'),
         Input('nav-geographic', 'n_clicks'),
         Input('nav-chat', 'n_clicks'),
         Input('nav-profile', 'n_clicks'),
         Input('nav-settings', 'n_clicks')]
    )
    def update_nav_styles(home_clicks, economic_clicks, geographic_clicks, 
                         chat_clicks, profile_clicks, settings_clicks):
        """Update navigation button styles based on active page."""
        ctx = callback_context
        
        base_style = {
            'padding': '15px 20px',
            'margin': '0 15px 8px 15px',
            'borderRadius': '12px',
            'cursor': 'pointer',
            'transition': 'all 0.3s ease',
            'color': COLORS['dark'],
            'display': 'flex',
            'alignItems': 'center',
            'backgroundColor': 'transparent',
            'border': 'none',
            'width': 'calc(100% - 30px)',
            'textAlign': 'left',
            'fontFamily': 'Inter, sans-serif',
            'fontSize': '0.9rem',
            'fontWeight': '500'
        }
        
        active_style = base_style.copy()
        active_style.update({
            'backgroundColor': COLORS['primary'],
            'color': 'white',
            'fontWeight': '600'
        })
        
        styles = [base_style] * 6  # Default style for all buttons
        
        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            button_map = {
                'nav-home': 0,
                'nav-economic': 1,
                'nav-geographic': 2,
                'nav-chat': 3,
                'nav-profile': 4,
                'nav-settings': 5
            }
            
            if button_id in button_map:
                styles[button_map[button_id]] = active_style
        else:
            styles[0] = active_style  # Default to home active
        
        return styles