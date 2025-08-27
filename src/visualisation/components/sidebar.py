"""
Sidebar navigation component for bank simulation platform
"""
from dash import html
from config.colors import COLORS


def create_sidebar_navigation():
    """Create the main sidebar navigation."""
    return html.Div([
        # Logo and title
        html.Div([
            html.Div("🏦", style={
                'fontSize': '2.5rem', 
                'marginBottom': '10px',
                'textAlign': 'center'
            }),
            html.H2("Bank Simulation", style={
                'fontSize': '1.3rem',
                'fontWeight': '700',
                'color': COLORS['dark'],
                'textAlign': 'center',
                'marginBottom': '5px'
            }),
            html.P("AI-Powered Analytics", style={
                'fontSize': '0.8rem',
                'color': COLORS['dark'],
                'opacity': '0.7',
                'textAlign': 'center',
                'margin': '0'
            })
        ], style={
            'padding': '20px 15px',
            'borderBottom': f'1px solid {COLORS["hover"]}'
        }),
        
        # Navigation menu
        html.Nav([
            html.Button([
                html.Span("🏠", style={'marginRight': '12px', 'fontSize': '1.2rem'}),
                html.Span("Home")
            ], id="nav-home", n_clicks=0, style=get_nav_button_style()),
            
            html.Button([
                html.Span("💱", style={'marginRight': '12px', 'fontSize': '1.2rem'}),
                html.Span("Economic Analysis")
            ], id="nav-economic", n_clicks=0, style=get_nav_button_style()),
            
            html.Button([
                html.Span("🗺️", style={'marginRight': '12px', 'fontSize': '1.2rem'}),
                html.Span("Geographic Analysis")
            ], id="nav-geographic", n_clicks=0, style=get_nav_button_style()),
            
            html.Button([
                html.Span("🤖", style={'marginRight': '12px', 'fontSize': '1.2rem'}),
                html.Span("AI Chat")
            ], id="nav-chat", n_clicks=0, style=get_nav_button_style()),
            
            # Advanced sections
            html.Hr(style={'margin': '20px 15px', 'border': f'1px solid {COLORS["hover"]}'}),
            
            html.Button([
                html.Span("🧮", style={'marginRight': '12px', 'fontSize': '1.2rem'}),
                html.Span("Advanced Simulation")
            ], id="nav-advanced-sim", n_clicks=0, style=get_nav_button_style()),
            
            html.Button([
                html.Span("🧠", style={'marginRight': '12px', 'fontSize': '1.2rem'}),
                html.Span("AI Configuration")
            ], id="nav-ai-config", n_clicks=0, style=get_nav_button_style()),
            
            html.Button([
                html.Span("📊", style={'marginRight': '12px', 'fontSize': '1.2rem'}),
                html.Span("Real-time Monitoring")
            ], id="nav-monitoring", n_clicks=0, style=get_nav_button_style()),
            
            # Settings and profile
            html.Hr(style={'margin': '20px 15px', 'border': f'1px solid {COLORS["hover"]}'}),
            
            html.Button([
                html.Span("⚙️", style={'marginRight': '12px', 'fontSize': '1.2rem'}),
                html.Span("Settings")
            ], id="nav-settings", n_clicks=0, style=get_nav_button_style()),
            
            html.Button([
                html.Span("👤", style={'marginRight': '12px', 'fontSize': '1.2rem'}),
                html.Span("Profile")
            ], id="nav-profile", n_clicks=0, style=get_nav_button_style())
        ], style={'padding': '10px 0'}),
        
        # System status
        html.Div([
            html.H4("System Status", style={
                'fontSize': '0.9rem',
                'fontWeight': '600',
                'color': COLORS['dark'],
                'marginBottom': '10px'
            }),
            html.Div([
                html.Div("🟢", style={'marginRight': '8px'}),
                html.Span("Online", style={'fontSize': '0.8rem'})
            ], style={'marginBottom': '5px'}),
            html.Div([
                html.Strong("Agents: "),
                html.Span("1,247", style={'fontSize': '0.8rem'})
            ], style={'marginBottom': '5px'}),
            html.Div([
                html.Strong("Last Update: "),
                html.Span("2min ago", style={'fontSize': '0.8rem'})
            ])
        ], style={
            'position': 'absolute',
            'bottom': '20px',
            'left': '15px',
            'right': '15px',
            'padding': '15px',
            'backgroundColor': COLORS['light'],
            'borderRadius': '8px',
            'fontSize': '0.8rem'
        })
    ], style={
        'width': f'{280}px',
        'height': '100vh',
        'position': 'fixed',
        'left': '0',
        'top': '0',
        'backgroundColor': 'white',
        'borderRight': f'1px solid {COLORS["hover"]}',
        'overflowY': 'auto',
        'zIndex': '1000'
    })


def get_nav_button_style():
    """Get the navigation button style."""
    return {
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
        'fontFamily': 'Inter, sans-serif',
        'fontSize': '0.9rem',
        'fontWeight': '500'
    }


def get_active_nav_button_style():
    """Get the active navigation button style."""
    active_style = get_nav_button_style().copy()
    active_style.update({
        'backgroundColor': COLORS['primary'],
        'color': 'white',
        'fontWeight': '600'
    })
    return active_style