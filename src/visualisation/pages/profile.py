"""
Dynamic User Profile Page that updates based on authentication
"""
from dash import html, Input, Output
from components.cards import create_metric_card
from config.colors import COLORS
import datetime


def create_profile_page_content():
    """Create the complete profile page content that updates dynamically"""
    return html.Div([
        html.Div(id="dynamic-profile-content", children=[
            create_default_profile()  # Default content
        ])
    ])


def create_default_profile():
    """Default profile when not authenticated"""
    return html.Div([
        html.Div([
            html.H2("Welcome to BankSim", style={
                'fontSize': '2rem',
                'fontWeight': '700',
                'color': COLORS['dark'],
                'textAlign': 'center',
                'marginBottom': '20px'
            }),
            html.P("Please sign in to view your profile", style={
                'fontSize': '1.1rem',
                'color': COLORS['secondary'],
                'textAlign': 'center',
                'marginBottom': '30px'
            }),
            html.Div([
                html.Button("Sign In", id="profile-signin-btn", style={
                    'padding': '12px 30px',
                    'backgroundColor': COLORS['primary'],
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '8px',
                    'fontSize': '1rem',
                    'fontWeight': '600',
                    'cursor': 'pointer'
                })
            ], style={'textAlign': 'center'})
        ], style={
            'backgroundColor': 'white',
            'padding': '60px 40px',
            'borderRadius': '15px',
            'boxShadow': '0 4px 20px rgba(0,0,0,0.1)',
            'textAlign': 'center',
            'marginTop': '50px'
        })
    ])


def create_authenticated_profile(user_data):
    """Create profile content for authenticated user"""
    
    # Extract user information with safe defaults
    user_id = user_data.get('id', 'unknown')
    email = user_data.get('email', 'Not provided')
    first_name = user_data.get('first_name', 'User')
    last_name = user_data.get('last_name', '')
    full_name = f"{first_name} {last_name}".strip()
    profile_image = user_data.get('profile_image_url', '')
    provider = user_data.get('provider', 'oauth').title()
    
    # Generate initials for avatar
    initials = get_user_initials(first_name, last_name)
    
    return html.Div([
        create_dynamic_profile_header(full_name, email, initials, profile_image, provider),
        create_dynamic_profile_stats(provider),
        
        # Profile Content Grid
        html.Div([
            # Left Column
            html.Div([
                create_dynamic_personal_info_section(user_data),
                create_dynamic_security_section(provider)
            ], style={'flex': '1', 'marginRight': '20px'}),
            
            # Right Column
            html.Div([
                create_activity_section(),
                create_preferences_section()
            ], style={'flex': '1'})
        ], style={'display': 'flex', 'gap': '20px', 'marginTop': '30px'}),
        
        create_profile_action_buttons()
    ])


def create_dynamic_profile_header(full_name, email, initials, profile_image, provider):
    """Create dynamic profile header based on user data"""
    
    # Avatar - use profile image if available, otherwise initials
    if profile_image:
        avatar = html.Img(
            src=profile_image,
            style={
                'width': '120px', 'height': '120px', 'borderRadius': '50%',
                'marginRight': '30px', 'objectFit': 'cover',
                'boxShadow': '0 10px 30px rgba(30, 64, 175, 0.3)',
                'border': f'4px solid {COLORS["primary"]}'
            }
        )
    else:
        avatar = html.Div(initials, style={
            'width': '120px', 'height': '120px', 'borderRadius': '50%',
            'backgroundColor': COLORS['primary'], 'color': 'white',
            'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
            'fontWeight': '700', 'fontSize': '3rem', 'marginRight': '30px',
            'boxShadow': '0 10px 30px rgba(30, 64, 175, 0.3)'
        })
    
    return html.Div([
        html.Div([
            avatar,
            html.Div([
                html.H1(full_name or "Welcome!", style={
                    'fontSize': '2.5rem', 'fontWeight': '700', 
                    'color': COLORS['dark'], 'margin': '0 0 10px 0'
                }),
                html.P(f"Banking Simulation User", style={
                    'fontSize': '1.2rem', 'color': COLORS['primary'], 
                    'fontWeight': '500', 'margin': '0 0 10px 0'
                }),
                html.P(f"✉️ {email}", style={
                    'fontSize': '1rem', 'color': COLORS['dark'], 
                    'opacity': '0.8', 'margin': '0 0 15px 0'
                }),
                html.Div([
                    html.Span(f"🔗 Connected via {provider}", style={
                        'backgroundColor': COLORS['success'], 'color': 'white', 
                        'padding': '5px 12px', 'borderRadius': '20px', 
                        'fontSize': '0.9rem', 'fontWeight': '600', 'marginRight': '10px'
                    }),
                    html.Span(f"👤 Profile Active", style={
                        'backgroundColor': COLORS['light'], 'color': COLORS['dark'], 
                        'padding': '5px 12px', 'borderRadius': '20px', 
                        'fontSize': '0.9rem', 'border': f'1px solid {COLORS["hover"]}'
                    })
                ])
            ])
        ], style={'display': 'flex', 'alignItems': 'center'})
    ], style={
        'backgroundColor': 'white', 'padding': '40px', 'borderRadius': '15px',
        'boxShadow': '0 4px 20px rgba(0,0,0,0.1)', 'marginBottom': '30px'
    })


def create_dynamic_profile_stats(provider):
    """Create profile statistics that update based on authentication"""
    # Calculate days since typical account creation
    days_active = 45  # Simulated
    
    return html.Div([
        create_metric_card("🔗", "Authentication", provider, "OAuth Provider", COLORS['primary']),
        create_metric_card("📅", "Days Active", f"{days_active}", "In current session", COLORS['success']),
        create_metric_card("🔒", "Security Level", "High", "OAuth Secured", COLORS['secondary']),
        create_metric_card("⚡", "Session Status", "Active", "Currently signed in", COLORS['accent']),
    ], style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
        'gap': '20px',
        'marginBottom': '30px'
    })


def create_dynamic_personal_info_section(user_data):
    """Create personal information section with real user data"""
    
    user_id = user_data.get('id', 'Not available')
    email = user_data.get('email', 'Not provided')
    first_name = user_data.get('first_name', 'Not provided')
    last_name = user_data.get('last_name', 'Not provided')
    provider = user_data.get('provider', 'oauth').title()
    
    # Extract additional info from user ID if possible
    location = "Tunisia"  # Default
    if 'auth0' in user_id.lower():
        account_type = "Auth0 Managed"
    elif 'google' in user_id.lower():
        account_type = "Google Account"
    elif 'github' in user_id.lower():
        account_type = "GitHub Account"
    else:
        account_type = "OAuth Account"
    
    return html.Div([
        html.H3("Personal Information", style={
            'fontSize': '1.5rem', 'fontWeight': '700', 
            'color': COLORS['dark'], 'marginBottom': '20px'
        }),
        
        create_info_row("Full Name", f"{first_name} {last_name}".strip() or "Not provided"),
        create_info_row("Email Address", email),
        create_info_row("User ID", user_id[:20] + "..." if len(user_id) > 20 else user_id),
        create_info_row("Account Provider", provider),
        create_info_row("Account Type", account_type),
        create_info_row("Location", location),
        create_info_row("Time Zone", "GMT+1 (Tunis)"),
        create_info_row("Member Since", datetime.datetime.now().strftime("%B %Y"))
        
    ], style={
        'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '12px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)', 'marginBottom': '20px'
    })


def create_dynamic_security_section(provider):
    """Create security section based on authentication method"""
    
    security_features = []
    
    if provider.lower() == 'google':
        security_features = [
            ("🔐", "Google OAuth", "Active", COLORS['success']),
            ("🛡️", "Two-Factor Available", "Through Google", COLORS['success']),
            ("📱", "Device Security", "Google Managed", COLORS['primary'])
        ]
    elif provider.lower() == 'github':
        security_features = [
            ("🔐", "GitHub OAuth", "Active", COLORS['success']),
            ("🛡️", "Two-Factor Available", "Through GitHub", COLORS['success']),
            ("🔑", "SSH Keys", "GitHub Managed", COLORS['primary'])
        ]
    else:
        security_features = [
            ("🔐", "OAuth Authentication", "Active", COLORS['success']),
            ("🛡️", "Secure Connection", "Encrypted", COLORS['success']),
            ("📱", "Session Management", "Active", COLORS['primary'])
        ]
    
    return html.Div([
        html.H3("Account Security", style={
            'fontSize': '1.5rem', 'fontWeight': '700', 
            'color': COLORS['dark'], 'marginBottom': '20px'
        }),
        
        html.Div([
            create_security_row(icon, feature, status, color) 
            for icon, feature, status, color in security_features
        ])
        
    ], style={
        'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '12px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
    })


def create_activity_section():
    """Create recent activity section"""
    return html.Div([
        html.H3("Recent Activity", style={
            'fontSize': '1.5rem', 'fontWeight': '700', 
            'color': COLORS['dark'], 'marginBottom': '20px'
        }),
        
        create_activity_item("🔐", "Signed in successfully", "Just now"),
        create_activity_item("📊", "Viewed dashboard", "2 minutes ago"), 
        create_activity_item("🎮", "Started simulation", "5 minutes ago"),
        create_activity_item("⚙️", "Updated preferences", "1 hour ago")
        
    ], style={
        'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '12px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)', 'marginBottom': '20px'
    })


def create_preferences_section():
    """Create user preferences section"""
    return html.Div([
        html.H3("Preferences", style={
            'fontSize': '1.5rem', 'fontWeight': '700', 
            'color': COLORS['dark'], 'marginBottom': '20px'
        }),
        
        create_info_row("Language", "English"),
        create_info_row("Theme", "Light Mode (Auto-detect available)"),
        create_info_row("Timezone", "GMT+1 (Tunis)"),
        create_info_row("Notifications", "Browser notifications"),
        create_info_row("Data Export", "JSON format preferred"),
        
    ], style={
        'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '12px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
    })


def create_profile_action_buttons():
    """Create action buttons for the profile page"""
    return html.Div([
        html.Button([
            html.Span("🔄", style={'marginRight': '8px'}),
            html.Span("Refresh Profile")
        ], id="profile-refresh-btn", n_clicks=0, style=create_button_style(COLORS['primary'])),
        
        html.Button([
            html.Span("📤", style={'marginRight': '8px'}),
            html.Span("Export Data")
        ], id="profile-export-btn", n_clicks=0, style=create_button_style(COLORS['secondary'])),
        
        html.Button([
            html.Span("🚪", style={'marginRight': '8px'}),
            html.Span("Sign Out")
        ], id="profile-signout-btn", n_clicks=0, style=create_button_style('#ef4444'))
        
    ], style={'textAlign': 'center', 'marginTop': '40px', 'display': 'flex', 'gap': '15px', 'justifyContent': 'center', 'flexWrap': 'wrap'})


# Helper functions
def get_user_initials(first_name, last_name):
    """Get user initials from name"""
    first = first_name[0].upper() if first_name else "U"
    last = last_name[0].upper() if last_name else ""
    return first + last if last else first


def create_info_row(label, value):
    """Create an information row"""
    return html.Div([
        html.Strong(f"{label}: "),
        html.Span(value)
    ], style={'marginBottom': '15px', 'fontSize': '1rem'})


def create_security_row(icon, feature, status, color):
    """Create a security feature row"""
    return html.Div([
        html.Div([
            html.Span(icon, style={'fontSize': '1.2rem', 'marginRight': '10px'}),
            html.Span(feature, style={'fontWeight': '600'})
        ], style={'marginBottom': '5px'}),
        html.Div(status, style={'color': color, 'fontSize': '0.9rem'})
    ], style={'marginBottom': '15px'})


def create_activity_item(icon, action, time):
    """Create an activity item"""
    return html.Div([
        html.Div(icon, style={'fontSize': '1.5rem', 'marginRight': '15px'}),
        html.Div([
            html.Div(action, style={'fontWeight': '600', 'marginBottom': '5px'}),
            html.Div(time, style={'fontSize': '0.85rem', 'opacity': '0.7'})
        ])
    ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '15px'})


def create_button_style(bg_color):
    """Create consistent button styling"""
    return {
        'padding': '12px 24px', 'backgroundColor': bg_color, 'color': 'white',
        'border': 'none', 'borderRadius': '8px', 'fontSize': '1rem', 'fontWeight': '600',
        'cursor': 'pointer', 'transition': 'all 0.3s ease', 'minWidth': '150px'
    }


# Callback to update profile based on authentication
def register_profile_callback(app):
    """Register callback to update profile content based on auth state"""
    @app.callback(
        Output('dynamic-profile-content', 'children'),
        Input('auth-state', 'data')
    )
    def update_profile_content(auth_state):
        if not auth_state:
            return create_default_profile()
            
        if auth_state.get('authenticated') and auth_state.get('user'):
            return create_authenticated_profile(auth_state['user'])
        else:
            return create_default_profile()