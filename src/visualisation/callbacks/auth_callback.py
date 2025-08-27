"""
callbacks/auth_callback.py – Auth0 UI callbacks - SIMPLIFIED FIX
Drop this into src/visualisation/callbacks/auth_callback.py
"""

from dash import Input, Output, State, ctx, no_update, html, dcc, ALL
from datetime import datetime
from config.colors import COLORS
from services.auth_service import get_session_manager


def register_auth_callbacks(app):
    """Register authentication UI callbacks."""

    # Open modal
    @app.callback(
        Output("auth-modals-container", "children"),
        Input("login-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def show_login_modal(n_clicks):
        if n_clicks and n_clicks > 0:
            return create_oauth_login_modal()
        return []

    # Close modal
    @app.callback(
        Output("auth-modals-container", "children", allow_duplicate=True),
        Input("close-login-modal", "n_clicks"),
        prevent_initial_call=True,
    )
    def close_login_modal(n_clicks):
        if n_clicks and n_clicks > 0:
            return []
        return no_update

    # Update header + auth state when session-token changes
    @app.callback(
        [
            Output("auth-state", "data"),
            Output("header-user-section", "children"),
        ],
        Input("session-token", "data"),
    )
    def update_auth_state(session_token):
        sm = get_session_manager()

        if session_token:
            user = sm.get_current_user(session_token)
            if user:
                auth_state = {"authenticated": True, "user": user, "last_check": datetime.utcnow().isoformat()}
                header = create_authenticated_header(user)
                return auth_state, header
        
        # Not authenticated - return default header
        auth_state = {"authenticated": False, "user": None}
        return auth_state, create_default_header()

    # Handle OAuth redirects
    @app.callback(
        Output("redirector", "children"),
        [
            Input({"type": "oauth-btn", "provider": ALL}, "n_clicks"),
        ],
        prevent_initial_call=True,
    )
    def oauth_redirect(oauth_clicks):
        if not ctx.triggered:
            return no_update
            
        trig = ctx.triggered_id
        if isinstance(trig, dict) and trig.get("type") == "oauth-btn":
            if oauth_clicks and any(oauth_clicks):
                provider = trig.get("provider")
                connection_map = {
                    "google": "google-oauth2",
                    "github": "github",
                    "linkedin": "linkedin",
                }
                connection = connection_map.get(provider)
                href = f"/auth/login?connection={connection}" if connection else "/auth/login"
                return dcc.Location(href=href, id="oauth-redirect")
        
        return no_update

    # Toggle profile dropdown
    @app.callback(
        Output("profile-dropdown", "style"),
        [Input("profile-trigger", "n_clicks")],
        [State("profile-dropdown", "style")],
        prevent_initial_call=True,
    )
    def toggle_profile_dropdown(n_clicks, current_style):
        if n_clicks:
            # Toggle between display: none and display: block
            if current_style and current_style.get("display") == "none":
                return {**current_style, "display": "block"}
            else:
                return {**current_style, "display": "none"}
        return no_update

    # Close dropdown when clicking elsewhere (optional, uses clientside callback)
    app.clientside_callback(
        """
        function(n_clicks) {
            // Close dropdown when clicking outside
            document.addEventListener('click', function(event) {
                const trigger = document.getElementById('profile-trigger');
                const dropdown = document.getElementById('profile-dropdown');
                if (trigger && dropdown && !trigger.contains(event.target) && !dropdown.contains(event.target)) {
                    dropdown.style.display = 'none';
                }
            });
            return window.dash_clientside.no_update;
        }
        """,
        Output("profile-dropdown", "style", allow_duplicate=True),
        Input("profile-trigger", "n_clicks"),
        prevent_initial_call=True,
    )


# ---------- UI helpers ----------

def create_oauth_login_modal():
    return html.Div([
        html.Div([
            html.Div([
                html.Button("×",
                    id="close-login-modal",
                    n_clicks=0,
                    style={
                        "position": "absolute", "top": "15px", "right": "15px",
                        "border": "none", "backgroundColor": "transparent",
                        "fontSize": "2rem", "cursor": "pointer", "color": COLORS["dark"],
                        "fontWeight": "bold", "width": "30px", "height": "30px",
                        "borderRadius": "50%", "display": "flex", "alignItems": "center",
                        "justifyContent": "center",
                    }
                ),
                html.H2("Welcome to BankSim", style={
                    "fontSize": "2rem", "fontWeight": "700", "color": COLORS["dark"],
                    "marginBottom": "10px", "textAlign": "center",
                }),
                html.P("Sign in to access your simulation dashboard", style={
                    "color": COLORS["secondary"], "textAlign": "center",
                    "marginBottom": "30px", "fontSize": "1rem",
                }),

                html.Div([
                    html.Button([
                        html.Span("G", style={"marginRight": "12px", "fontWeight": "bold"}), 
                        html.Span("Continue with Google")
                    ],
                        id={"type": "oauth-btn", "provider": "google"}, 
                        n_clicks=0,
                        style=btn_style("#db4437")),
                    html.Button([
                        html.Span("H", style={"marginRight": "12px", "fontWeight": "bold"}), 
                        html.Span("Continue with GitHub")
                    ],
                        id={"type": "oauth-btn", "provider": "github"}, 
                        n_clicks=0,
                        style=btn_style("#333333")),
                    html.Button([
                        html.Span("L", style={"marginRight": "12px", "fontWeight": "bold"}), 
                        html.Span("Continue with LinkedIn")
                    ],
                        id={"type": "oauth-btn", "provider": "linkedin"}, 
                        n_clicks=0,
                        style=btn_style("#0077b5")),
                ]),

                html.P([
                    "By signing in, you agree to our ",
                    html.A("Terms", href="#", style={"color": COLORS["primary"]}),
                    " and ",
                    html.A("Privacy Policy", href="#", style={"color": COLORS["primary"]})
                ],
                    style={"fontSize": "0.85rem", "color": COLORS["secondary"], "textAlign": "center"}),
            ], style={
                "backgroundColor": "white", "padding": "40px", "borderRadius": "16px",
                "boxShadow": "0 20px 40px rgba(0,0,0,0.15)", "position": "relative",
                "maxWidth": "400px", "width": "90%",
            })
        ], style={
            "position": "fixed", "top": "0", "left": "0", "width": "100%", "height": "100%",
            "backgroundColor": "rgba(0,0,0,0.6)", "display": "flex", "alignItems": "center",
            "justifyContent": "center", "zIndex": "9999",
        })
    ])


def btn_style(bg):
    return {
        "width": "100%", "padding": "15px 20px", "marginBottom": "12px",
        "backgroundColor": bg, "color": "white", "border": "none", "borderRadius": "8px",
        "cursor": "pointer", "fontSize": "1rem", "fontWeight": "500",
        "display": "flex", "alignItems": "center", "justifyContent": "center",
    }


def create_authenticated_header(user):
    first_name = user.get("first_name", "User")
    provider = user.get("provider", "oauth")
    profile_image = user.get("profile_image_url", "")
    email = user.get("email", "")

    return html.Div([
        html.Div([
            dcc.Input(
                id="global-search",
                placeholder="Search simulations, scenarios...",
                style={
                    "padding": "10px 15px", "border": f'1px solid {COLORS["hover"]}',
                    "borderRadius": "25px", "width": "300px", "fontSize": "0.9rem", "outline": "none",
                },
            )
        ], style={"marginRight": "20px"}),

        html.Div([
            html.Span(f"Connected via {provider.title()}", style={
                "fontSize": "0.8rem", "color": COLORS["success"], "marginRight": "15px"}),

            # Profile dropdown container
            html.Div([
                # Profile image/avatar that triggers dropdown
                html.Div([
                    # If profile image exists, use it, otherwise show initials
                    html.Img(
                        src=profile_image,
                        style={
                            "width": "40px", 
                            "height": "40px", 
                            "borderRadius": "50%",
                            "cursor": "pointer",
                            "border": f"2px solid {COLORS['primary']}",
                            "objectFit": "cover",
                        }
                    ) if profile_image else html.Div(
                        first_name[0].upper(), 
                        style={
                            "width": "40px", 
                            "height": "40px", 
                            "borderRadius": "50%",
                            "backgroundColor": COLORS["primary"], 
                            "color": "white",
                            "display": "flex", 
                            "alignItems": "center", 
                            "justifyContent": "center",
                            "fontWeight": "600", 
                            "cursor": "pointer",
                            "fontSize": "1.1rem",
                        }
                    ),
                ], id="profile-trigger", n_clicks=0),
                
                # Dropdown menu (initially hidden)
                html.Div([
                    html.Div([
                        # User info section
                        html.Div([
                            html.Div(first_name, style={"fontWeight": "600", "fontSize": "0.95rem"}),
                            html.Div(email, style={"fontSize": "0.8rem", "color": COLORS["secondary"]}),
                        ], style={"padding": "10px 15px", "borderBottom": f"1px solid {COLORS['hover']}"}),
                        
                        # Menu items
                        html.A([
                            html.I(className="fas fa-user", style={"marginRight": "8px", "width": "16px"}),
                            "View Profile"
                        ], href="/profile", style={
                            "display": "block",
                            "padding": "10px 15px",
                            "color": COLORS["dark"],
                            "textDecoration": "none",
                            "fontSize": "0.9rem",
                            "transition": "background-color 0.2s",
                        }, className="dropdown-item"),
                        
                        html.A([
                            html.I(className="fas fa-cog", style={"marginRight": "8px", "width": "16px"}),
                            "Settings"
                        ], href="/settings", style={
                            "display": "block",
                            "padding": "10px 15px",
                            "color": COLORS["dark"],
                            "textDecoration": "none",
                            "fontSize": "0.9rem",
                            "transition": "background-color 0.2s",
                        }, className="dropdown-item"),
                        
                        html.Div(style={"height": "1px", "backgroundColor": COLORS["hover"], "margin": "5px 0"}),
                        
                        html.A([
                            html.I(className="fas fa-sign-out-alt", style={"marginRight": "8px", "width": "16px"}),
                            "Sign Out"
                        ], href="/logout", style={
                            "display": "block",
                            "padding": "10px 15px",
                            "color": COLORS["danger"],
                            "textDecoration": "none",
                            "fontSize": "0.9rem",
                            "fontWeight": "500",
                            "transition": "background-color 0.2s",
                        }, className="dropdown-item"),
                    ], style={
                        "backgroundColor": "white",
                        "borderRadius": "8px",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.15)",
                        "minWidth": "200px",
                    })
                ], id="profile-dropdown", style={
                    "position": "absolute",
                    "top": "45px",
                    "right": "0",
                    "display": "none",  # Initially hidden
                    "zIndex": "1000",
                }),
            ], style={"position": "relative"}),  # Container needs relative positioning
            
        ], style={"display": "flex", "alignItems": "center"}),
    ], style={"display": "flex", "alignItems": "center"})


def create_default_header():
    return html.Div([
        html.Div([
            dcc.Input(
                id="global-search",
                placeholder="Search simulations, scenarios...",
                style={
                    "padding": "10px 15px", "border": f'1px solid {COLORS["hover"]}',
                    "borderRadius": "25px", "width": "300px", "fontSize": "0.9rem", "outline": "none",
                },
            )
        ], style={"marginRight": "20px"}),

        html.Button(
            "Sign In",
            id="login-button",
            n_clicks=0,
            style={
                "padding": "10px 20px", "backgroundColor": COLORS["primary"], "color": "white",
                "border": "none", "borderRadius": "25px", "cursor": "pointer",
                "fontSize": "0.9rem", "fontWeight": "600",
            },
        ),

        html.Div("N", style={
            "width": "35px", "height": "35px", "borderRadius": "50%", "backgroundColor": COLORS["secondary"],
            "color": "white", "display": "flex", "alignItems": "center", "justifyContent": "center",
            "marginLeft": "15px",
        }),
    ], style={"display": "flex", "alignItems": "center"})