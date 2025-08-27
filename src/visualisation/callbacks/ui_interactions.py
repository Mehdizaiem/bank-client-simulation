"""
UI Interactions Callbacks
Créez ce fichier : callbacks/ui_interactions.py
"""

from dash import Input, Output, State, callback, no_update
import dash


def register_ui_interactions(app):
    """Register UI interaction callbacks"""
    
    @app.callback(
        Output('user-dropdown-menu', 'style'),
        [Input('user-avatar-button', 'n_clicks')],
        [State('user-dropdown-menu', 'style')],
        prevent_initial_call=True
    )
    def toggle_user_dropdown(n_clicks, current_style):
        """Toggle user dropdown menu"""
        if n_clicks:
            current_display = current_style.get('display', 'none')
            new_display = 'block' if current_display == 'none' else 'none'
            return {**current_style, 'display': new_display}
        return no_update
    
    @app.callback(
        Output('notifications-dropdown', 'style', allow_duplicate=True),
        [Input('notifications-btn', 'n_clicks')],
        [State('notifications-dropdown', 'style')],
        prevent_initial_call=True
    )
    def toggle_notifications_dropdown(n_clicks, current_style):
        """Toggle notifications dropdown"""
        if n_clicks:
            current_display = current_style.get('display', 'none')
            new_display = 'block' if current_display == 'none' else 'none'
            return {**current_style, 'display': new_display}
        return no_update
    
    print("UI interaction callbacks registered successfully")