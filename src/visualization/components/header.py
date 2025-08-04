from dash import html, dcc
from config.colors import COLORS

def create_search_bar():
    return html.Div([
        dcc.Input(
            placeholder="Search...",
            style={
                'width': '250px',
                'marginRight': '15px',
                'padding': '8px 12px',
                'border': f'1px solid {COLORS["hover"]}',
                'borderRadius': '6px',
                'fontSize': '0.9rem'
            }
        )
    ])

def create_user_profile():
    return html.Div([
        html.Div("🔔", style={
            'fontSize': '1.3rem',
            'cursor': 'pointer',
            'padding': '8px',
            'borderRadius': '8px',
            'backgroundColor': 'white',
            'border': f'1px solid {COLORS["hover"]}',
            'marginRight': '10px'
        }),
        html.Div([
            html.Div("N", id="user-avatar-button", n_clicks=0, style={
                'width': '40px',
                'height': '40px',
                'borderRadius': '50%',
                'backgroundColor': COLORS['primary'],
                'color': 'white',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center',
                'fontWeight': '600',
                'fontSize': '1.2rem',
                'cursor': 'pointer',
                'transition': 'all 0.3s ease',
                'position': 'relative'
            }),
            # Dropdown
            html.Div([
                html.Div([
                    html.Div("N", style={
                        'width': '30px', 'height': '30px', 'borderRadius': '50%',
                        'backgroundColor': COLORS['primary'], 'color': 'white',
                        'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                        'fontWeight': '600', 'marginRight': '10px'
                    }),
                    html.Div([
                        html.Div("nom et prenom", style={'fontWeight': '600', 'fontSize': '0.9rem', 'color': COLORS['dark']}),
                        html.Div("nom et prenom@bankdash.com", style={'fontSize': '0.8rem', 'color': COLORS['dark'], 'opacity': '0.7'})
                    ])
                ], style={'display': 'flex', 'alignItems': 'center', 'padding': '15px',
                          'borderBottom': f'1px solid {COLORS["hover"]}'}),
                html.Div([
                    html.Span("🔗", style={'fontSize': '1.1rem', 'marginRight': '12px'}),
                    html.Span("Connect", style={'fontSize': '0.9rem'})
                ], id="connect-option", n_clicks=0, style={
                    'padding': '10px 15px', 'cursor': 'pointer', 'color': COLORS['dark'],
                    'display': 'flex', 'alignItems': 'center', 'borderBottom': f'1px solid {COLORS["hover"]}'
                }),
                html.Div([
                    html.Span("⚙️", style={'fontSize': '1.1rem', 'marginRight': '12px'}),
                    html.Span("Manage Account", style={'fontSize': '0.9rem'})
                ], id="manage-account-option", n_clicks=0, style={
                    'padding': '10px 15px', 'cursor': 'pointer', 'color': COLORS['dark'],
                    'display': 'flex', 'alignItems': 'center', 'borderBottom': f'1px solid {COLORS["hover"]}'
                }),
                html.Div([
                    html.Span("📊", style={'fontSize': '1.1rem', 'marginRight': '12px'}),
                    html.Span("View Profile", style={'fontSize': '0.9rem'})
                ], id="view-profile-option", n_clicks=0, style={
                    'padding': '10px 15px', 'cursor': 'pointer', 'color': COLORS['dark'],
                    'display': 'flex', 'alignItems': 'center', 'borderBottom': f'1px solid {COLORS["hover"]}'
                }),
                html.Div([
                    html.Span("🚪", style={'fontSize': '1.1rem', 'marginRight': '12px'}),
                    html.Span("Sign Out", style={'fontSize': '0.9rem'})
                ], id="sign-out-option", n_clicks=0, style={
                    'padding': '10px 15px', 'cursor': 'pointer', 'color': COLORS['danger'],
                    'display': 'flex', 'alignItems': 'center'
                })
            ], id="user-dropdown-menu", style={
                'position': 'absolute',
                'top': '50px',
                'right': '0',
                'width': '250px',
                'backgroundColor': 'white',
                'borderRadius': '10px',
                'boxShadow': '0 10px 30px rgba(0,0,0,0.15)',
                'border': f'1px solid {COLORS["hover"]}',
                'zIndex': '1000',
                'display': 'none'
            })
        ], style={'position': 'relative', 'display': 'inline-block'})
    ], style={'display': 'flex', 'alignItems': 'center'})

def create_header_content():
    return html.Div([
        html.H1("Dashboard Overview", id="page-title", style={
            'margin': '0',
            'fontSize': '1.8rem',
            'fontWeight': '700',
            'color': COLORS['dark']
        }),
        html.Div([
            create_search_bar(),
            create_user_profile()
        ], style={'display': 'flex', 'alignItems': 'center'})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'})

def create_top_header():
    """Create the complete top header with empty modals ready for dynamic content."""
    return html.Div([
        create_header_content(),
        # Modal containers, children set by callback!
        html.Div(id="connect-card", style={
            'position': 'fixed', 'top': '100px', 'right': '50px',
            'width': '350px', 'backgroundColor': 'white', 'borderRadius': '15px',
            'boxShadow': '0 15px 40px rgba(0,0,0,0.15)', 'border': f'1px solid {COLORS["hover"]}',
            'padding': '25px', 'zIndex': '1001', 'display': 'none'
        }),
        html.Div(id="manage-account-card", style={
            'position': 'fixed', 'top': '100px', 'right': '50px',
            'width': '300px', 'backgroundColor': 'white', 'borderRadius': '15px',
            'boxShadow': '0 15px 40px rgba(0,0,0,0.15)', 'border': f'1px solid {COLORS["hover"]}',
            'padding': '25px', 'zIndex': '1001', 'display': 'none'
        }),
        html.Button("dummy", id="back-to-main-btn", style={"display": "none"})  # Error fix
    ], style={
        'padding': '20px 30px',
        'backgroundColor': 'white',
        'borderBottom': f'1px solid {COLORS["hover"]}',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
        'position': 'relative'
    })
