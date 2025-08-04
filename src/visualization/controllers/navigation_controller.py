"""
Navigation controller handling page routing and navigation callbacks
"""
from dash import Input, Output, callback_context
from pages.home import create_homepage_content
from pages.economic import create_economic_content
from pages.geographic import create_geographic_content
from pages.chat import create_chat_content
from pages.settings import create_settings_content
from pages.profile import create_profile_page_content  # Add this import
from config.colors import COLORS


def register_callbacks(app):
    """Register all navigation-related callbacks."""
    
    @app.callback(
        [Output('page-content', 'children'), 
         Output('page-title', 'children'), 
         Output('current-page-store', 'data')],
        [Input('nav-home', 'n_clicks'),
         Input('nav-economic', 'n_clicks'),
         Input('nav-geographic', 'n_clicks'),
         Input('nav-chat', 'n_clicks'),
         Input('nav-settings', 'n_clicks')],
        prevent_initial_call=False
    )
    def handle_navigation(home, economic, geo, chat, settings):
        """Handle navigation between pages."""
        ctx = callback_context
        
        # On initial load or if all buttons never clicked, show homepage
        if not ctx.triggered or all(x is None for x in [home, economic, geo, chat, settings]):
            return create_homepage_content(), "Dashboard Overview", "home"
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        navigation_map = {
            "nav-home": (create_homepage_content(), "Dashboard Overview", "home"),
            "nav-economic": (create_economic_content(), "Economic Analysis", "economic"),
            "nav-geographic": (create_geographic_content(), "Geographic Analysis", "geographic"),
            "nav-chat": (create_chat_content(), "AI Assistant Chat", "chat"),
            "nav-settings": (create_settings_content(), "Settings", "settings"),
            "nav-profile": (create_profile_page_content(), "User Profile", "profile")  # Add profile page
        }
        
        return navigation_map.get(button_id, navigation_map["nav-home"])
    
    @app.callback(
        [Output('nav-home', 'style'), 
         Output('nav-economic', 'style'), 
         Output('nav-geographic', 'style'),
         Output('nav-chat', 'style'), 
         Output('nav-settings', 'style')],
        Input('current-page-store', 'data')
    )
    def update_nav_styles(current_page):
        """Update navigation button styles based on current page."""
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
            'fontFamily': 'Inter, sans-serif'
        }
        
        active_style = {
            **base_style, 
            'backgroundColor': COLORS['primary'], 
            'color': 'white', 
            'transform': 'translateX(5px)', 
            'boxShadow': f'0 4px 15px {COLORS["primary"]}40'
        }
        
        styles = {
            "home": active_style if current_page == "home" else base_style,
            "economic": active_style if current_page == "economic" else base_style,
            "geographic": active_style if current_page == "geographic" else base_style,
            "chat": active_style if current_page == "chat" else base_style,
            "settings": active_style if current_page == "settings" else base_style
        }
        
        return (
            styles["home"],
            styles["economic"], 
            styles["geographic"],
            styles["chat"],
            styles["settings"]
        )