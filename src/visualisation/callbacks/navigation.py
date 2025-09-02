"""
callbacks/navigation.py - Simplified navigation callback handlers
"""
from dash import Input, Output, callback_context, no_update
from pages.home import create_simulation_homepage_content
from pages.geographic import create_geographic_simulation_content
from pages.profile import create_profile_page_content

def register_navigation_callbacks(app):
    """Register simplified navigation-related callbacks."""
    
    @app.callback(
        Output('page-content', 'children'),
        Output('page-store', 'data'),
        [
            Input('nav-home', 'n_clicks'),
            Input('nav-geographic', 'n_clicks'),
            Input('nav-profile', 'n_clicks'),
            Input('url', 'pathname')
        ]
    )
    def update_page_content(*args):
        """Update page content based on navigation clicks."""
        ctx = callback_context
        
        if not ctx.triggered:
            return create_simulation_homepage_content(), 'home'
        
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Navigation button clicks
        if trigger_id == 'nav-home':
            return create_simulation_homepage_content(), 'home'
        elif trigger_id == 'nav-geographic':
            return create_geographic_simulation_content(), 'geographic'
        elif trigger_id == 'nav-profile':
            return create_profile_page_content(), 'profile'
      
        # URL pathname changes
        elif trigger_id == 'url':
            pathname = args[-1] or '/'
            if pathname == '/':
                return create_simulation_homepage_content(), 'home'
            elif pathname == '/geographic':
                return create_geographic_simulation_content(), 'geographic'
            elif pathname == '/profile':
                return create_profile_page_content(), 'profile'
           
        
        # Default to home
        return create_simulation_homepage_content(), 'home'

    @app.callback(
        Output('url', 'pathname'),
        [
            Input('nav-home', 'n_clicks'),
            Input('nav-geographic', 'n_clicks'),
            Input('nav-profile', 'n_clicks'),
        ],
        prevent_initial_call=True
    )
    def update_url(*args):
        """Update URL based on navigation clicks."""
        ctx = callback_context
        
        if not ctx.triggered:
            return no_update
        
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        url_map = {
            'nav-home': '/',
            'nav-geographic': '/geographic',
            'nav-profile': '/profile',
        }
        
        return url_map.get(trigger_id, '/')

    @app.callback(
        Output('nav-home', 'style'),
        Output('nav-geographic', 'style'),
        Output('nav-profile', 'style'),
        Input('page-store', 'data')
    )
    def update_nav_button_styles(current_page):
        """Update navigation button styles based on current page."""
        from components.sidebar import get_nav_button_style, get_active_nav_button_style
        
        default_style = get_nav_button_style()
        active_style = get_active_nav_button_style()
        
        styles = {
            'home': default_style,
            'geographic': default_style,
            'profile': default_style,
        }
        
        # Set active style for current page
        if current_page in styles:
            styles[current_page] = active_style
        
        return (
            styles['home'],
            styles['geographic'],
            styles['profile'],
        )