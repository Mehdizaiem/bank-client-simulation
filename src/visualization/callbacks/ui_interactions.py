"""
UI interaction callbacks for the Bank Client Simulation Platform
"""
import dash
from dash import html, Input, Output, State
from config.colors import COLORS


def register_ui_callbacks(app):
    """Register all UI interaction callbacks."""
    
    # User dropdown functionality
    @app.callback(
        Output('user-dropdown-menu', 'style'),
        [Input('user-avatar-button', 'n_clicks')],
        [State('user-dropdown-menu', 'style')]
    )
    def toggle_user_dropdown(n_clicks, current_style):
        """Toggle user dropdown menu visibility."""
        print(f"DEBUG: Avatar clicked {n_clicks} times")
        if n_clicks and n_clicks > 0:
            if current_style.get('display') == 'none':
                print("DEBUG: Showing dropdown")
                current_style['display'] = 'block'
            else:
                print("DEBUG: Hiding dropdown")
                current_style['display'] = 'none'
        return current_style

    # Modal callbacks
    @app.callback(
        [Output('connect-card', 'children'),
         Output('connect-card', 'style')],
        [Input('connect-option', 'n_clicks')],
        prevent_initial_call=True
    )
    def handle_connect_modal(open_clicks):
        """Handle connect accounts modal."""
        print(f"DEBUG: Connect button clicked {open_clicks} times")
        if open_clicks and open_clicks > 0:
            from components.header import create_connect_modal
            return create_connect_modal(), {'display': 'block'}
        return [], {'display': 'none'}

    @app.callback(
        [Output('profile-modal', 'children'),
         Output('profile-modal', 'style')],
        [Input('view-profile-option', 'n_clicks')],
        prevent_initial_call=True
    )
    def handle_profile_modal(open_clicks):
        """Handle profile modal."""
        print(f"DEBUG: Profile button clicked {open_clicks} times")
        if open_clicks and open_clicks > 0:
            from components.header import create_profile_modal
            return create_profile_modal(), {'display': 'block'}
        return [], {'display': 'none'}

    @app.callback(
        [Output('manage-account-card', 'children'),
         Output('manage-account-card', 'style')],
        [Input('manage-account-option', 'n_clicks')],
        prevent_initial_call=True
    )
    def handle_manage_modal(open_clicks):
        """Handle manage account modal."""
        print(f"DEBUG: Manage button clicked {open_clicks} times")
        if open_clicks and open_clicks > 0:
            from components.header import create_manage_account_modal
            return create_manage_account_modal(), {'display': 'block'}
        return [], {'display': 'none'}

    # Close modal callbacks using clientside callback for immediate response
    app.clientside_callback(
        """
        function(n_clicks) {
            if (n_clicks > 0) {
                console.log('Closing connect modal');
                return {'display': 'none'};
            }
            return window.dash_clientside.no_update;
        }
        """,
        Output('connect-card', 'style', allow_duplicate=True),
        Input({'type': 'close-modal', 'modal': 'connect'}, 'n_clicks'),
        prevent_initial_call=True
    )

    app.clientside_callback(
        """
        function(n_clicks) {
            if (n_clicks > 0) {
                console.log('Closing profile modal');
                return {'display': 'none'};
            }
            return window.dash_clientside.no_update;
        }
        """,
        Output('profile-modal', 'style', allow_duplicate=True),
        Input({'type': 'close-modal', 'modal': 'profile'}, 'n_clicks'),
        prevent_initial_call=True
    )

    app.clientside_callback(
        """
        function(n_clicks) {
            if (n_clicks > 0) {
                console.log('Closing manage modal');
                return {'display': 'none'};
            }
            return window.dash_clientside.no_update;
        }
        """,
        Output('manage-account-card', 'style', allow_duplicate=True),
        Input({'type': 'close-modal', 'modal': 'manage'}, 'n_clicks'),
        prevent_initial_call=True
    )

    # Sign out functionality
    @app.callback(
        Output('page-content', 'children', allow_duplicate=True),
        [Input('sign-out-option', 'n_clicks')],
        prevent_initial_call=True
    )
    def handle_sign_out(n_clicks):
        """Handle sign out functionality."""
        print(f"DEBUG: Sign out clicked {n_clicks} times")
        if n_clicks and n_clicks > 0:
            return create_sign_out_page()
        
        return dash.no_update


def create_sign_out_page():
    """Create the sign out confirmation page."""
    return html.Div([
        html.Div([
            html.H2("👋 You have been signed out", style={
                'textAlign': 'center',
                'color': COLORS['primary'],
                'marginBottom': '20px'
            }),
            html.P("Thank you for using the Bank Client Simulation Platform!", style={
                'textAlign': 'center',
                'fontSize': '1.1rem',
                'marginBottom': '30px'
            }),
            html.Button("Sign In Again", style={
                'padding': '12px 24px',
                'backgroundColor': COLORS['primary'],
                'color': 'white',
                'border': 'none',
                'borderRadius': '6px',
                'cursor': 'pointer',
                'fontSize': '1rem',
                'fontWeight': '600',
                'display': 'block',
                'margin': '0 auto'
            })
        ], style={
            'backgroundColor': 'white',
            'padding': '50px',
            'borderRadius': '12px',
            'boxShadow': '0 4px 20px rgba(0,0,0,0.1)',
            'textAlign': 'center',
            'maxWidth': '500px',
            'margin': '100px auto'
        })
    ])