"""
Sidebar navigation component
"""
from dash import html
from config.colors import COLORS
from config.settings import NAVIGATION_ITEMS


def create_nav_button(icon, label, page_id):
    """Create a navigation button."""
    return html.Button([
        html.Span(
            icon, 
            style={
                'fontSize': '1.3rem', 
                'marginRight': '15px', 
                'width': '25px', 
                'textAlign': 'center'
            }
        ),
        html.Span(
            label, 
            style={
                'fontSize': '0.95rem', 
                'fontWeight': '500'
            }
        )
    ],
    id=f"nav-{page_id}",
    n_clicks=0,
    style={
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
        'fontFamily': 'Inter, sans-serif'
    })


def create_sidebar_header():
    """Create the sidebar header with logo and title."""
    return html.Div([
        html.Div("🏦", style={
            'fontSize': '2.5rem',
            'background': f'linear-gradient(135deg, {COLORS["primary"]}, {COLORS["secondary"]})',
            'WebkitBackgroundClip': 'text',
            'WebkitTextFillColor': 'transparent',
            'textAlign': 'center',
            'marginBottom': '10px'
        }),
        html.H3("Bank Simulation", style={
            'color': COLORS['dark'],
            'margin': '0',
            'fontSize': '1.3rem',
            'fontWeight': '700',
            'textAlign': 'center'
        }),
        html.P("AI-Powered Analytics", style={
            'color': COLORS['dark'],
            'margin': '5px 0 0 0',
            'fontSize': '0.85rem',
            'opacity': '0.7',
            'textAlign': 'center'
        })
    ], style={
        'padding': '25px 20px', 
        'borderBottom': f'1px solid {COLORS["hover"]}', 
        'marginBottom': '20px'
    })


def create_navigation_menu():
    """Create the navigation menu with all buttons."""
    nav_buttons = []
    for item in NAVIGATION_ITEMS:
        nav_buttons.append(
            create_nav_button(item['icon'], item['label'], item['page_id'])
        )
    
    return html.Div(nav_buttons, id="navigation-menu")


def create_system_status():
    """Create the system status panel at the bottom of sidebar."""
    return html.Div([
        html.Div("System Status", style={
            'fontSize': '0.85rem', 
            'fontWeight': '600', 
            'color': COLORS['dark'], 
            'marginBottom': '10px'
        }),
        html.Div([
            html.Div("●", style={
                'color': COLORS['success'], 
                'fontSize': '1.2rem', 
                'marginRight': '8px'
            }),
            html.Span("Online", style={
                'fontSize': '0.9rem', 
                'color': COLORS['dark']
            })
        ], style={
            'display': 'flex', 
            'alignItems': 'center', 
            'marginBottom': '8px'
        }),
        html.Div([
            html.Span("Agents: ", style={
                'fontSize': '0.8rem', 
                'color': COLORS['dark']
            }),
            html.Span("1,247", style={
                'fontSize': '0.8rem', 
                'fontWeight': '600', 
                'color': COLORS['primary']
            })
        ], style={'marginBottom': '5px'}),
        html.Div([
            html.Span("Last Update: ", style={
                'fontSize': '0.8rem', 
                'color': COLORS['dark']
            }),
            html.Span("2min ago", style={
                'fontSize': '0.8rem', 
                'color': COLORS['dark']
            })
        ])
    ], style={
        'position': 'absolute', 
        'bottom': '20px', 
        'left': '20px', 
        'right': '20px',
        'padding': '15px', 
        'backgroundColor': 'white', 
        'borderRadius': '10px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)', 
        'border': f'1px solid {COLORS["hover"]}'
    })


def create_sidebar_navigation():
    """Create the complete sidebar navigation."""
    return html.Div([
        create_sidebar_header(),
        create_navigation_menu(),
        create_system_status()
    ], style={
        'position': 'fixed', 
        'left': '0', 
        'top': '0', 
        'width': '280px', 
        'height': '100vh',
        'backgroundColor': COLORS['sidebar'], 
        'borderRight': f'1px solid {COLORS["hover"]}',
        'zIndex': '1000', 
        'boxShadow': '2px 0 10px rgba(0,0,0,0.1)'
    })