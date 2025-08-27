"""
app.py – Auth0-integrated version (Dash on Flask) - FIXED
Drop this into src/visualisation/app.py
"""

import os
import sys
from urllib.parse import urlencode, urlparse, parse_qs

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # load .env from repo root if needed

import dash
from dash import html, dcc, Input, Output, no_update
from flask import session, request, redirect
from authlib.integrations.flask_client import OAuth

# Make local imports work when running this file directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ----- Imports from your project -----
try:
    # Components / pages
    from components.sidebar import create_sidebar_navigation
    from components.header import create_top_header
    from pages.home import create_simulation_homepage_content
    from pages.economic import create_economic_simulation_content
    from pages.geographic import create_geographic_simulation_content
    from pages.chat import create_simulation_chat_content
    from pages.profile import create_profile_page_content
    from pages.settings import create_simulation_settings_content

    # Config
    from config.colors import COLORS
    from config.settings import DASHBOARD_CONFIG

    # Callbacks
    from callbacks.navigation import register_navigation_callbacks
    from callbacks.chat import register_chat_callbacks
    from callbacks.ui_interactions import register_ui_interactions
    from callbacks.auth_callback import register_auth_callbacks

    # Local session manager
    from services.auth_service import get_session_manager
except Exception as e:
    print("Import error: ", e)
    raise

# ----- App config -----
HOST = os.getenv("DASHBOARD_HOST", "0.0.0.0")
PORT = int(os.getenv("DASHBOARD_PORT", "8050"))
DEBUG = os.getenv("DASHBOARD_DEBUG", "true").lower() == "true"

app = dash.Dash(__name__, suppress_callback_exceptions=True, title="Bank Client Simulation Platform")
server = app.server

# Flask secret for encrypted session cookies
server.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

# ----- Auth0 wiring -----
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")               # e.g. your-tenant.auth0.com
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8050")

oauth = OAuth(server)
auth0 = oauth.register(
    "auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid profile email",
    },
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
    """Handle Auth0 redirect -> exchange code -> fetch userinfo -> create local session -> return to Dash."""
    try:
        # Exchange authorization code for tokens
        token = oauth.auth0.authorize_access_token()
        
        # The token response should include the access_token
        # Use it to fetch userinfo from the userinfo endpoint
        resp = oauth.auth0.get(
            f"https://{AUTH0_DOMAIN}/userinfo",
            token={"access_token": token.get("access_token"), "token_type": "Bearer"}
        )
        userinfo = resp.json()

        # Extract user data
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
        session["local_token"] = res["local_token"]  # stash in Flask session for convenience

        # bounce back to the Dash app; a client callback will set dcc.Store
        return redirect(f"/?{urlencode({'logged_in': '1'})}")
        
    except Exception as e:
        print(f"Auth callback error: {e}")
        import traceback
        traceback.print_exc()
        # On error, redirect to home with error message
        return redirect(f"/?{urlencode({'error': 'auth_failed'})}")

@server.route("/logout")
def auth_logout():
    """Clear local session and redirect through Auth0 logout."""
    # Clear the Flask session
    session.clear()
    
    # Clear the session manager
    sm = get_session_manager()
    # Clear all sessions (in production, you'd want to clear only the current user's session)
    sm.active_sessions.clear()
    
    # Redirect to Auth0 logout endpoint
    logout_url = (
        f"https://{AUTH0_DOMAIN}/v2/logout?"
        + urlencode({
            "returnTo": APP_BASE_URL,
            "client_id": AUTH0_CLIENT_ID,
        })
    )
    return redirect(logout_url)

# ---- Dash Layout ----
app.layout = html.Div([
    # Location & stores
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="session-token", storage_type="session"),
    dcc.Store(id="auth-state", data={"authenticated": False, "user": None}),
    dcc.Store(id="page-store", data="home"),

    # Sidebar
    create_sidebar_navigation(),

    # Main content
    html.Div([
        create_top_header(),
        # Initialize with home content to avoid empty page
        html.Div(
            id="page-content", 
            children=create_simulation_homepage_content(),  # Default content
            style={"padding": "30px"}
        ),
    ], style={
        "marginLeft": f'{DASHBOARD_CONFIG["sidebar_width"]}px',
        "backgroundColor": COLORS["light"],
        "minHeight": "100vh",
    }),

    # Dedicated redirect mount (kept separate from modals)
    html.Div(id="redirector"),
    # Auth modal container
    html.Div(id="auth-modals-container"),
])

# A superset of all components that appear dynamically in callbacks.
# This is NOT rendered; it's only used for callback graph validation.
app.validation_layout = html.Div([
    # core pieces
    dcc.Location(id="url"),
    dcc.Store(id="session-token"),
    dcc.Store(id="auth-state"),
    dcc.Store(id="page-store"),

    # things your callbacks reference but may not exist initially
    html.Div(id="header-user-section"),
    html.H1(id="page-title"),
    html.Div(id="page-content"),
    html.Div(id="redirector"),
    html.Div(id="auth-modals-container"),
    html.Button(id="login-button"),
    html.Button(id="close-login-modal"),
    
    # Profile dropdown elements
    html.Div(id="profile-trigger"),
    html.Div(id="profile-dropdown"),

    # pattern-matching ids used by the OAuth modal
    html.Button(id={"type": "oauth-btn", "provider": "google"}),
    html.Button(id={"type": "oauth-btn", "provider": "github"}),
    html.Button(id={"type": "oauth-btn", "provider": "linkedin"}),
])


# ---- Callbacks that glue URL <-> local store ----
@app.callback(
    Output("session-token", "data", allow_duplicate=True),
    Input("url", "href"),
    prevent_initial_call=True,
)
def set_session_from_url(href: str):
    if not href:
        return no_update
    qs = parse_qs(urlparse(href).query)
    if qs.get("logged_in", ["0"])[0] != "1":
        return no_update

    # Prefer Flask session if present
    token = session.get("local_token")
    if token:
        return token

    # Fallback to latest in SessionManager
    sm = get_session_manager()
    if sm.active_sessions:
        latest = list(sm.active_sessions.values())[-1]
        return latest["local_token"]
    return no_update

# ---- Register app-specific callbacks ----
register_auth_callbacks(app)        # Auth UI only (header + modal + redirects)
register_navigation_callbacks(app)  # Owns page-content + (optionally) page-title
register_chat_callbacks(app)
register_ui_interactions(app)

# (If you have chart callbacks)
try:
    from components.charts import register_all_chart_callbacks
    register_all_chart_callbacks(app)
except Exception:
    pass

# ---- Main ----
if __name__ == "__main__":
    print("Auth0 Domain:", AUTH0_DOMAIN)
    print("App running at:", APP_BASE_URL)
    app.run(debug=DEBUG, host=HOST, port=PORT)