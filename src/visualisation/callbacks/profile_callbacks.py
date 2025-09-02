"""
Simple Profile Callbacks - No Theme System
Replace callbacks/profile_callbacks.py with this version
"""
from dash import Input, Output, State, callback, no_update, html
from pages.profile import create_authenticated_profile, create_default_profile


def register_profile_callbacks(app):
    """Register basic profile page callbacks"""
    
    @app.callback(
        Output('dynamic-profile-content', 'children'),
        [Input('session-token', 'data'),
         Input('auth-state', 'data'),
         Input('url', 'pathname')],
        prevent_initial_call=False
    )
    def update_profile_content(session_token, auth_state, pathname):
        """Update profile content based on authentication"""
        
        print(f"Profile callback: pathname={pathname}, session_token={bool(session_token)}, auth_state={bool(auth_state)}")
        
        # Check session token first
        if session_token:
            try:
                from services.auth_service import get_session_manager
                sm = get_session_manager()
                user = sm.get_current_user(session_token)
                if user:
                    print(f"Profile: User authenticated - {user.get('first_name', 'Unknown')}")
                    return create_authenticated_profile(user)
            except Exception as e:
                print(f"Profile: Session check failed - {e}")
        
        # Check auth_state as fallback
        if auth_state and isinstance(auth_state, dict):
            if auth_state.get('authenticated') and auth_state.get('user'):
                print(f"Profile: User authenticated via auth state")
                return create_authenticated_profile(auth_state['user'])
        
        # Try Flask session as last resort
        try:
            from flask import session
            local_token = session.get("local_token")
            if local_token:
                from services.auth_service import get_session_manager
                sm = get_session_manager()
                user = sm.get_current_user(local_token)
                if user:
                    print(f"Profile: User authenticated via Flask session")
                    return create_authenticated_profile(user)
        except Exception as e:
            print(f"Profile: Flask session check failed - {e}")
        
        print("Profile: No authentication found, showing login prompt")
        return create_default_profile()
    
    @app.callback(
        Output('auth-modals-container', 'children', allow_duplicate=True),
        Input('profile-signin-btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def show_signin_from_profile(n_clicks):
        """Show sign-in modal when clicked from profile page"""
        if n_clicks and n_clicks > 0:
            try:
                from callbacks.auth_callback import create_oauth_login_modal
                return create_oauth_login_modal()
            except ImportError:
                return html.Div([
                    html.H3("Please sign in"),
                    html.P("Click the Sign In button in the header to authenticate.")
                ])
        return no_update
    
    @app.callback(
        Output('url', 'pathname', allow_duplicate=True),
        Input('profile-signout-btn', 'n_clicks'),
        State('session-token', 'data'),
        prevent_initial_call=True
    )
    def handle_manual_signout(n_clicks, session_token):
        """Handle manual sign out from profile page"""
        if n_clicks and n_clicks > 0:
            print("Manual signout initiated from profile page")
            
            try:
                if session_token:
                    from services.auth_service import get_session_manager
                    sm = get_session_manager()
                    sm.logout_by_token(session_token)
                    print("Session cleared from session manager")
                
                from flask import session
                session.clear()
                print("Flask session cleared")
                
            except Exception as e:
                print(f"Logout error: {e}")
            
            return '/logout'
        return no_update
    
    print("Basic profile callbacks registered successfully")