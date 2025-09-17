"""
app.py - Updated with proper CSS loading and theme support
Replace src/visualisation/app.py with this version
"""

import os
import sys
import requests
from flask import Response
from urllib.parse import quote
from urllib.parse import urlencode, urlparse, parse_qs

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import dash
from dash import html, dcc, Input, Output, no_update
from flask import session, request, redirect
from authlib.integrations.flask_client import OAuth

THIS_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(THIS_DIR, '../..'))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Core imports
try:
    from components.sidebar import create_sidebar_navigation
    from components.header import create_top_header
    from pages.home import create_simulation_homepage_content

    
    from config.colors import COLORS
    from config.config_settings import DASHBOARD_CONFIG
    
    # Import callback registration functions
    from callbacks.navigation import register_navigation_callbacks
    from callbacks.auth_callback import register_auth_callbacks
    from callbacks.data_callbacks import register_data_callbacks
    from callbacks.simulation_callbacks import register_simulation_callbacks
    from callbacks.geographic_callbacks import register_geographic_callbacks
    from callbacks.profile_callbacks import register_profile_callbacks    
    from services.auth_service import get_session_manager
    
except Exception as e:
    print(f"Import error: {e}")
    raise

# App configuration
HOST = os.getenv("DASHBOARD_HOST", "0.0.0.0")
PORT = int(os.getenv("DASHBOARD_PORT", "8050"))
DEBUG = os.getenv("DASHBOARD_DEBUG", "true").lower() == "true"
external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
]
# Initialize Dash app - CSS will be loaded automatically from assets folder
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=True, 
    external_stylesheets=external_stylesheets,
    title="Bank Client Simulation Platform"
)
server = app.server
server.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

# Auth0 configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8050")

# Setup OAuth if credentials are available
if AUTH0_DOMAIN and AUTH0_CLIENT_ID and AUTH0_CLIENT_SECRET:
    oauth = OAuth(server)
    auth0 = oauth.register(
        "auth0",
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
        client_kwargs={"scope": "openid profile email"},
    )

    @server.route("/auth/login")
    def auth_login():
        connection = request.args.get("connection")
        redirect_uri = f"{APP_BASE_URL}/auth/callback"
        if connection:
            return oauth.auth0.authorize_redirect(redirect_uri=redirect_uri, connection=connection)
        return oauth.auth0.authorize_redirect(redirect_uri=redirect_uri, prompt="login")

    @server.route("/auth/callback")
    def auth_callback():
        try:
            token = oauth.auth0.authorize_access_token()
            resp = oauth.auth0.get(
                f"https://{AUTH0_DOMAIN}/userinfo",
                token={"access_token": token.get("access_token"), "token_type": "Bearer"}
            )
            userinfo = resp.json()

            provider = (userinfo.get("sub", "").split("|")[0]) or "oauth"
            name = userinfo.get("name") or "User"
            first = userinfo.get("given_name") or name.split(" ")[0]
            last = userinfo.get("family_name") or (" ".join(name.split(" ")[1:]) if " " in name else "")

            user_data = {
                "id": userinfo.get("sub"),
                "email": userinfo.get("email"),
                "first_name": first,
                "last_name": last,
                "profile_image_url": userinfo.get("picture", ""),
                "provider": provider,
            }

            sm = get_session_manager()
            res = sm.authenticate_user(user_data)
            session["local_token"] = res["local_token"]
            
            session["user_id"] = userinfo.get("sub")

            return redirect(f"/?{urlencode({'logged_in': '1'})}")
            
        except Exception as e:
            print(f"Auth callback error: {e}")
            return redirect(f"/?{urlencode({'error': 'auth_failed'})}")

    @server.route("/logout")
    def auth_logout():
        """Manual logout only"""
        
        local_token = session.get("local_token")
        user_id = session.get("user_id")
        
        session.clear()
        
        sm = get_session_manager()
        if local_token:
            sm.logout_by_token(local_token)
        elif user_id:
            sm.logout_user(user_id)
        
        print("Manual logout completed")
        
        logout_url = (
            f"https://{AUTH0_DOMAIN}/v2/logout?"
            + urlencode({
                "returnTo": APP_BASE_URL,
                "client_id": AUTH0_CLIENT_ID,
            })
        )
        return redirect(logout_url)
    @server.route("/_img")
    def img_proxy():
        """Image proxy to avoid CORS issues with external images"""
        url = request.args.get("u", "")
        if not url:
            return Response(status=404)

        try:
            # Fetch the external image
            r = requests.get(url, timeout=5, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if r.status_code != 200 or not r.content:
                print(f"Image proxy failed: HTTP {r.status_code} for {url}")
                return Response(status=404)

            # Pass through the content-type if present
            content_type = r.headers.get("Content-Type", "image/jpeg")
            print(f"Image proxy success: Serving {len(r.content)} bytes as {content_type}")
            
            return Response(
                r.content, 
                status=200, 
                content_type=content_type,
                headers={
                    'Cache-Control': 'public, max-age=3600',  # Cache for 1 hour
                }
            )
            
        except requests.exceptions.RequestException as e:
            print(f"Image proxy error: {e}")
            return Response(status=404)
        except Exception as e:
            print(f"Image proxy unexpected error: {e}")
            return Response(status=404)
    
else:
    print("Warning: Auth0 credentials not configured. Authentication disabled.")

# App layout (CSS will be loaded from assets/layout.css automatically)
app.layout = html.Div([
    
    # Core components
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="session-token", storage_type="session"),
    dcc.Store(id="auth-state", data={"authenticated": False, "user": None}),
    dcc.Store(id="page-store", data="home"),
    dcc.Store(id="data-refresh-token", data=0),
    
    # Main layout
    create_sidebar_navigation(),
    html.Div([
        create_top_header(),
        html.Div(
            id="page-content", 
            children=create_simulation_homepage_content(),
            style={"padding": "30px"}
        ),
    ], style={
        "marginLeft": f'{DASHBOARD_CONFIG["sidebar_width"]}px',
        "backgroundColor": "var(--bg-color)",
        "minHeight": "100vh",
        "transition": "all 0.3s ease"
    }),

    # Modal containers
    html.Div(id="redirector"),
    html.Div(id="auth-modals-container"),
    
    # Hidden dummy outputs for theme callbacks
    html.Div(id='theme-dummy', style={'display': 'none'}),
    html.Div(id='auto-save-dummy', style={'display': 'none'}),
    html.Div(id='settings-load-dummy', style={'display': 'none'}),
    html.Div(id='session-debug-info', style={'display': 'none'})
])

# Complete validation layout (keep existing one but add the missing elements)
app.validation_layout = html.Div([
    # All your existing validation layout components...
    # Core
    dcc.Location(id="url"),
    dcc.Store(id="session-token"),
    dcc.Store(id="auth-state"),
    dcc.Store(id="page-store"),
    dcc.Store(id="data-refresh-token"),
    
    # Layout
    html.Div(id="header-user-section"),
    html.Div(id="page-content"),
    html.Div(id="redirector"),
    html.Div(id="auth-modals-container"),
    
    # Auth
    html.Button(id="login-button"),
    html.Button(id="close-login-modal"),
    html.Div(id="profile-trigger"),
    html.Div(id="profile-dropdown"),
    html.Button(id={"type": "oauth-btn", "provider": "google"}),
    html.Button(id={"type": "oauth-btn", "provider": "github"}),
    html.Button(id={"type": "oauth-btn", "provider": "linkedin"}),
    
    # Profile components - CONDITIONALLY INCLUDE
    html.Div(id="dynamic-profile-content"),
    html.Button(id="profile-signin-btn"),
    html.Button(id="profile-refresh-btn"),  # This will only exist on profile page
    html.Button(id="profile-export-btn"),
    html.Button(id="profile-signout-btn"),
    
    # Homepage
    html.Div(id="data-source-info"),
    html.Div(id="coverage-info"),
    html.Div(id="simulation-status-display"),
    html.Div(id="simulation-results-container"),
    html.Div(id="retail-ratio-display"),
    
    # Charts
    dcc.Graph(id="governorate-distribution-chart"),
    dcc.Graph(id="client-type-pie-chart"),
    dcc.Graph(id="satisfaction-tiers-chart"),
    dcc.Graph(id="channel-usage-chart"),
    dcc.Graph(id="age-demographics-chart"),
    dcc.Graph(id="value-tiers-chart"),
    
    # Controls
    dcc.Input(id="agent-count-input"),
    dcc.Slider(id="retail-ratio-slider"),
    dcc.Input(id="time-steps-input"),
    dcc.Input(id="seed-input"),
    dcc.RadioItems(id="scenario-selector"),
    html.Button(id="run-simulation-btn"),
    html.Button(id="load-results-btn"),
    html.Button(id="reset-simulation-btn"),
    
    # Export
    html.Button(id="export-pdf-btn"),
    html.Button(id="export-excel-btn"), 
    html.Button(id="export-json-btn"),
    html.Div(id="export-status"),
    dcc.Download(id="download-pdf"),
    dcc.Download(id="download-excel"),
    dcc.Download(id="download-json"),
    
    # Settings - Theme components (THESE ARE REQUIRED)
    dcc.RadioItems(id="theme-selector"),
    dcc.Slider(id="font-size-slider"),
    dcc.Dropdown(id="accent-color-dropdown"),
    html.Button(id="save-settings-btn"),
    html.Button(id="reset-settings-btn"),
    html.Div(id="settings-status"),
    html.Div(id='theme-dummy'),
    html.Div(id='auto-save-dummy'),
    html.Div(id='settings-load-dummy'),
    html.Div(id='font-preview'),
    html.Div(id='session-debug-info'),
    
    # Geographic simulation (keep existing)
    dcc.Input(id="sim-num-agents"),
    dcc.Slider(id="sim-retail-ratio"),
    dcc.Input(id="sim-time-steps"),
    dcc.Dropdown(id="sim-scenario"),
    dcc.Dropdown(id="sim-target-region"),
    dcc.Dropdown(id="sim-target-segment"),
    html.Button(id="run-complete-simulation-btn"),
    html.Div(id="simulation-execution-status"),
    html.Div(id="executive-kpi-cards"),
    
    # Geographic results (keep existing)
    dcc.Graph(id="satisfaction-timeline"),
    dcc.Graph(id="churn-retention-timeline"),
    dcc.Graph(id="digital-adoption-timeline"),
    dcc.Graph(id="business-metrics-timeline"),
    html.Div(id="channel-insights-text"),
    dcc.Graph(id="regional-performance-chart"),
    html.Div(id="regional-rankings"),
    html.Div(id="roi-analysis-display"),
    html.Div(id="cost-benefit-display"),
    dcc.Graph(id="client-segmentation-chart"),
    dcc.Graph(id="satisfaction-by-segment-chart"),
    html.Div(id="simulation-alerts"),
    html.Div(id="strategic-recommendations"),
    html.Div(id="summary-statistics-table")
])

# Enhanced session token callback
@app.callback(
    Output("session-token", "data", allow_duplicate=True),
    [Input("url", "href")],
    prevent_initial_call=True,
)
def set_session_from_url(href):
    """Simplified session token management"""
    try:
        # First check Flask session
        existing_token = session.get("local_token")
        if existing_token:
            # Verify token is still valid
            sm = get_session_manager()
            user = sm.get_current_user(existing_token)
            if user:
                return existing_token
        
        # Check for login success in URL
        if href:
            qs = parse_qs(urlparse(href).query)
            if qs.get("logged_in", ["0"])[0] == "1":
                token = session.get("local_token")
                if token:
                    return token
        
        return no_update
        
    except Exception as e:
        print(f"Session token error: {e}")
        return no_update
@app.callback(
    Output("session-debug-info", "children"),
    [Input("session-token", "data")],
    prevent_initial_call=True
)
def maintain_session_simple(token):
    """Simple session maintenance with debugging"""
    try:
        if token:
            sm = get_session_manager()
            user = sm.get_current_user(token)
            if user:
                # Sync Flask session
                session["local_token"] = token
                session["user_id"] = user.get("id")
                print(f"✅ Session synced for {user.get('first_name', 'User')}")
                
                # Debug profile image
                profile_image = user.get("profile_image_url", "")
                print(f"🖼️ Profile image in session: '{profile_image}'")
            else:
                print("❌ Token exists but no user found")
        else:
            print("📝 No session token")
        return ""
    except Exception as e:
        print(f"❌ Session maintenance error: {e}")
        return ""
"""@app.callback(
    Output("session-debug-info", "children"),
    [Input("session-token", "data"),
     Input("url", "pathname")],
    prevent_initial_call=True
)
def maintain_session_debug(token, pathname):
    Debug session state and maintain it during navigation
    try:
        if token:
            sm = get_session_manager()
            user = sm.get_current_user(token)
            if user:
                # Store in Flask session as backup
                session["local_token"] = token
                session["user_id"] = user.get("id")
                print(f"Session maintained for {user.get('first_name', 'User')} on {pathname}")
        return ""
    except Exception as e:
        print(f"Session maintenance error: {e}")
        return "" 
        """
# Register all callbacks
print("Registering callbacks...")
register_auth_callbacks(app)
register_navigation_callbacks(app)  
register_data_callbacks(app)
register_simulation_callbacks(app)
register_geographic_callbacks(app)
register_profile_callbacks(app)

print("All callbacks registered successfully")

if __name__ == "__main__":
    print("=== BankSim Dashboard Starting ===")
    print(f"Auth0 Domain: {AUTH0_DOMAIN}")
    print(f"App running at: {APP_BASE_URL}")
    print("Features enabled:")
    print("  ✅ Working dark/light theme toggle")
    print("  ✅ Real-time font size changes")
    print("  ✅ Button color customization") 
    print("  ✅ Persistent sessions (no auto-logout)")
    print("  ✅ Manual logout only")
    print("  ✅ Responsive charts (2 per row)")
    print("  ✅ Fixed theme system")
    app.run(debug=DEBUG, host=HOST, port=PORT)