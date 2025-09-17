"""
callbacks/auth_callback.py – Fixed auth callbacks with proper error handling
Replace your entire auth_callback.py with this version
"""

from dash import Input, Output, State, ctx, no_update, html, dcc, ALL
from datetime import datetime
from config.colors import COLORS
from services.auth_service import get_session_manager
from dash.exceptions import PreventUpdate
from urllib.parse import quote

def normalize_google_picture(url: str, size: int = 64) -> str:
    """Normalize Google profile picture URLs for better loading"""
    if not url:
        return ""
    
    url = str(url).strip()
    
    # Force https
    if url.startswith("http://"):
        url = "https://" + url[len("http://"):]
    
    # Google images commonly look like:
    # https://lh3.googleusercontent.com/a/....=s96-c
    # We want to normalize them to a specific size
    if "googleusercontent.com" in url:
        # Remove any existing '=sXX-c' suffix
        if "=s" in url and "-c" in url and url.rfind("=s") < url.rfind("-c"):
            base = url[:url.rfind("=s")]
        else:
            base = url
        
        # Add proper size parameter
        if "?" in base:
            url = f"{base}&sz={size}"
        else:
            url = f"{base}?sz={size}"
    
    return url

def register_auth_callbacks(app):
    """Register authentication UI callbacks with comprehensive error handling."""

    # Open modal
    @app.callback(
        Output("auth-modals-container", "children"),
        Input("login-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def show_login_modal(n_clicks):
        try:
            if n_clicks and n_clicks > 0:
                return create_oauth_login_modal()
            return []
        except Exception as e:
            print(f"Login modal error: {e}")
            return []

    # Close modal
    @app.callback(
        Output("auth-modals-container", "children", allow_duplicate=True),
        Input("close-login-modal", "n_clicks"),
        prevent_initial_call=True,
    )
    def close_login_modal(n_clicks):
        try:
            if n_clicks and n_clicks > 0:
                return []
            return no_update
        except Exception as e:
            print(f"Close modal error: {e}")
            return []

    # Update header + auth state when session-token changes
    @app.callback(
        [
            Output("auth-state", "data"),
            Output("header-user-section", "children"),
        ],
        Input("session-token", "data"),
        prevent_initial_call=False,  # Allow initial call to set default state
    )
    def update_auth_state(session_token):
        try:
            sm = get_session_manager()

            if session_token:
                user = sm.get_current_user(session_token)
                if user:
                    print(f"✅ Updating header for authenticated user: {user.get('first_name', 'User')}")
                    auth_state = {
                        "authenticated": True, 
                        "user": user, 
                        "last_check": datetime.utcnow().isoformat()
                    }
                    header = create_authenticated_header(user)
                    return auth_state, header
            
            # Not authenticated - return default header
            print("📝 Setting default header (not authenticated)")
            auth_state = {"authenticated": False, "user": None}
            return auth_state, create_default_header()
            
        except Exception as e:
            print(f"❌ Auth state callback error: {e}")
            # Return safe defaults
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
        try:
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
        except Exception as e:
            print(f"OAuth redirect error: {e}")
            return no_update

    # Toggle profile dropdown (only if profile elements exist)
    @app.callback(
        Output("profile-dropdown", "style"),
        [Input("profile-trigger", "n_clicks")],
        [State("profile-dropdown", "style")],
        prevent_initial_call=True,
    )
    def toggle_profile_dropdown(n_clicks, current_style):
        try:
            if n_clicks:
                # Toggle between display: none and display: block
                if current_style and current_style.get("display") == "none":
                    return {**current_style, "display": "block"}
                else:
                    return {**current_style, "display": "none"}
            return no_update
        except Exception as e:
            print(f"Profile dropdown toggle error: {e}")
            return no_update

   # Add this clientside callback to your auth_callback.py to debug image loading

    app.clientside_callback(
        """
        function(n_clicks) {
            // Debug profile image loading
            setTimeout(function() {
                const profileImg = document.querySelector('img[data-fallback="true"]');
                const debugDiv = document.getElementById('debug-image-url');
                
                if (profileImg) {
                    console.log('Profile image found:', profileImg.src);
                    
                    // Test if image loads
                    const testImg = new Image();
                    testImg.onload = function() {
                        console.log('✅ Image loaded successfully:', profileImg.src);
                    };
                    testImg.onerror = function() {
                        console.log('❌ Image failed to load:', profileImg.src);
                        console.log('Error details:', this);
                    };
                    testImg.src = profileImg.src;
                    
                    // Show debug info on hover
                    if (debugDiv) {
                        profileImg.addEventListener('mouseenter', function() {
                            debugDiv.style.display = 'block';
                        });
                        profileImg.addEventListener('mouseleave', function() {
                            debugDiv.style.display = 'none';
                        });
                    }
                } else {
                    console.log('No profile image found - using initials fallback');
                }
            }, 1000);
            
            return window.dash_clientside.no_update;
        }
        """,
        Output("profile-trigger", "style", allow_duplicate=True),
        Input("profile-trigger", "n_clicks"),
        prevent_initial_call=True,
    )

# ---------- UI Helper Functions ----------

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


# Add this enhanced debugging to your auth_callback.py

def create_authenticated_header(user):
    """Create authenticated header with working Google profile images via proxy"""
    first_name = user.get("first_name", "User")
    provider = user.get("provider", "oauth")
    profile_image = user.get("profile_image_url", "")
    email = user.get("email", "")

    # Debug output
    print("=" * 50)
    print("PROFILE IMAGE DEBUG:")
    print(f"Raw profile_image_url: '{profile_image}'")
    
    # Process the profile image through proxy
    avatar_element = None
    
    if profile_image:
        try:
            # Normalize the Google image URL
            normalized_url = normalize_google_picture(profile_image, size=64)
            print(f"Normalized URL: '{normalized_url}'")
            
            if normalized_url:
                # Create proxied URL to avoid CORS issues
                proxied_url = f"/_img?u={quote(normalized_url, safe='')}"
                print(f"Proxied URL: '{proxied_url}'")
                
                avatar_element = html.Img(
                    src=proxied_url,
                    alt=f"{first_name} profile picture",
                    style={
                        "width": "40px",
                        "height": "40px",
                        "borderRadius": "50%",
                        "cursor": "pointer",
                        "border": f"2px solid {COLORS['primary']}",
                        "objectFit": "cover",
                        "display": "block",
                        "backgroundColor": "#f3f4f6",  # Light background while loading
                    },
                    title=f"{first_name} - Google Profile Image"
                )
                print("✅ Created Google profile image element")
            else:
                print("❌ URL normalization failed")
        except Exception as e:
            print(f"❌ Profile image processing error: {e}")
    
    # Fallback to initials if no image or processing failed
    if avatar_element is None:
        print("Using initials fallback")
        avatar_element = html.Div(
            first_name[0].upper() if first_name else "U",
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
                "border": f"2px solid {COLORS['primary']}",
            },
            title=f"Initials: {first_name[0]} - No profile image available"
        )
    
    print("=" * 50)

    return html.Div([
        html.Div([
            dcc.Input(
                id="global-search",
                placeholder="Search simulations, scenarios...",
                style={
                    "padding": "10px 15px", 
                    "border": f'1px solid {COLORS["hover"]}',
                    "borderRadius": "25px", 
                    "width": "300px", 
                    "fontSize": "0.9rem", 
                    "outline": "none",
                },
            )
        ], style={"marginRight": "20px"}),

        html.Div([
            html.Span(f"Connected via {provider.title()}", style={
                "fontSize": "0.8rem", 
                "color": COLORS["success"], 
                "marginRight": "15px"
            }),

            # Profile dropdown container
            html.Div([
                # Profile image/avatar that triggers dropdown
                html.Div([
                    avatar_element  # This is either the Google image or initials fallback
                ], id="profile-trigger", n_clicks=0),
                
                # Dropdown menu (keep existing)
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
                        }),
                        
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
                        }),
                        
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
                        }),
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
                    "display": "none",
                    "zIndex": "1000",
                }),
            ], style={"position": "relative"}),
            
        ], style={"display": "flex", "alignItems": "center"}),
    ], style={"display": "flex", "alignItems": "center"})

def create_default_header():
    """Create default header for non-authenticated users"""
    return html.Div([
        html.Div([
            dcc.Input(
                id="global-search",
                placeholder="Search simulations, scenarios...",
                style={
                    "padding": "10px 15px", 
                    "border": f'1px solid {COLORS["hover"]}',
                    "borderRadius": "25px", 
                    "width": "300px", 
                    "fontSize": "0.9rem", 
                    "outline": "none",
                },
            )
        ], style={"marginRight": "20px"}),

        html.Button(
            "Sign In",
            id="login-button",
            n_clicks=0,
            style={
                "padding": "10px 20px", 
                "backgroundColor": COLORS["primary"], 
                "color": "white",
                "border": "none", 
                "borderRadius": "25px", 
                "cursor": "pointer",
                "fontSize": "0.9rem", 
                "fontWeight": "600",
                "marginRight": "10px",
            },
        ),

        html.Div("N", style={
            "width": "35px", 
            "height": "35px", 
            "borderRadius": "50%", 
            "backgroundColor": COLORS["secondary"],
            "color": "white", 
            "display": "flex", 
            "alignItems": "center", 
            "justifyContent": "center",
            "fontWeight": "600",
            "fontSize": "0.9rem",
        }),
    ], style={"display": "flex", "alignItems": "center"})

