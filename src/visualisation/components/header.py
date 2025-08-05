"""
Header component for bank simulation platform
"""
from dash import html, dcc
from config.colors import COLORS


def create_top_header():
    """Create the top header with title and user info."""
    return html.Header([
        html.Div([
            # Page title area
            html.Div([
                html.H1(id="page-title", children="Dashboard Overview", style={
                    'fontSize': '1.8rem',
                    'fontWeight': '700',
                    'color': COLORS['dark'],
                    'margin': '0'
                })
            ], style={'flex': '1'}),
            
            # Search and user area
            html.Div([
                # Search bar
                html.Div([
                    dcc.Input(
                        placeholder="Search simulations, scenarios...",
                        style={
                            'padding': '10px 15px',
                            'border': f'1px solid {COLORS["hover"]}',
                            'borderRadius': '25px',
                            'width': '300px',
                            'fontSize': '0.9rem',
                            'outline': 'none'
                        }
                    )
                ], style={'marginRight': '20px'}),
                
                # Notifications
                html.Button([
                    html.Span("🔔", style={'fontSize': '1.2rem'})
                ], style={
                    'padding': '10px',
                    'border': 'none',
                    'backgroundColor': 'transparent',
                    'borderRadius': '50%',
                    'cursor': 'pointer',
                    'marginRight': '15px'
                }),
                
                    # User avatar and dropdown
                html.Div([
                    html.Button([
                        html.Div("N", style={
                            'width': '40px',
                            'height': '40px',
                            'borderRadius': '50%',
                            'backgroundColor': COLORS['primary'],
                            'color': 'white',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'fontWeight': '600',
                            'fontSize': '1.1rem'
                        })
                    ], id="user-avatar-button", n_clicks=0, style={
                        'border': 'none',
                        'backgroundColor': 'transparent',
                        'cursor': 'pointer',
                        'padding': '0'
                    }),
                    
                    # Dropdown menu
                    html.Div([
                        html.Div([
                            html.Button("👤 View Profile", 
                                      id="view-profile-option", 
                                      n_clicks=0, 
                                      style=get_dropdown_item_style()),
                            html.Button("🔗 Connect Account", 
                                      id="connect-option", 
                                      n_clicks=0, 
                                      style=get_dropdown_item_style()),
                            html.Button("⚙️ Manage Account", 
                                      id="manage-account-option", 
                                      n_clicks=0, 
                                      style=get_dropdown_item_style()),
                            html.Hr(style={'margin': '10px 0', 'border': f'1px solid {COLORS["hover"]}'}),
                            html.Button("🚪 Sign Out", 
                                      id="sign-out-option", 
                                      n_clicks=0, 
                                      style=get_dropdown_item_style())
                        ])
                    ], id="user-dropdown-menu", style={
                        'position': 'absolute',
                        'top': '50px',
                        'right': '0',
                        'backgroundColor': 'white',
                        'border': f'1px solid {COLORS["hover"]}',
                        'borderRadius': '10px',
                        'boxShadow': '0 4px 20px rgba(0,0,0,0.1)',
                        'padding': '10px',
                        'minWidth': '200px',
                        'display': 'none',
                        'zIndex': '1001'
                    })
                ], style={'position': 'relative'})
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'space-between',
            'padding': '15px 25px'
        }),
        
        # Profile cards and modals
        html.Div(id="connect-card", style={'display': 'none'}),
        html.Div(id="manage-account-card", style={'display': 'none'}),
        html.Div(id="profile-modal", style={'display': 'none'})
    ], style={
        'backgroundColor': 'white',
        'borderBottom': f'1px solid {COLORS["hover"]}',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'position': 'relative',
        'zIndex': '999'
    })


def create_connect_modal():
    """Create connect accounts modal content."""
    return html.Div([
        html.Div([
            html.Div([
                html.H3("Connect Your Accounts", style={
                    'fontSize': '1.5rem',
                    'fontWeight': '700',
                    'color': COLORS['dark'],
                    'marginBottom': '20px',
                    'textAlign': 'center'
                }),
                html.Button("✕", id={'type': 'close-modal', 'modal': 'connect'}, n_clicks=0, style={
                    'position': 'absolute',
                    'top': '15px',
                    'right': '15px',
                    'border': 'none',
                    'backgroundColor': 'transparent',
                    'fontSize': '1.5rem',
                    'cursor': 'pointer',
                    'color': COLORS['dark'],
                    'fontWeight': 'bold',
                    'width': '30px',
                    'height': '30px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'borderRadius': '50%',
                    'transition': 'background-color 0.2s ease'
                }),
                
                # Social Login Options
                html.Div([
                    html.Button([
                        html.Span("🔗 ", style={'marginRight': '10px'}),
                        html.Span("Connect with Google")
                    ], style={
                        'width': '100%',
                        'padding': '12px 20px',
                        'marginBottom': '10px',
                        'backgroundColor': '#db4437',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '6px',
                        'cursor': 'pointer',
                        'fontSize': '1rem',
                        'fontWeight': '600'
                    }),
                    
                    html.Button([
                        html.Span("🔗 ", style={'marginRight': '10px'}),
                        html.Span("Connect with GitHub")
                    ], style={
                        'width': '100%',
                        'padding': '12px 20px',
                        'marginBottom': '10px',
                        'backgroundColor': '#333',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '6px',
                        'cursor': 'pointer',
                        'fontSize': '1rem',
                        'fontWeight': '600'
                    }),
                    
                    html.Button([
                        html.Span("🔗 ", style={'marginRight': '10px'}),
                        html.Span("Connect with LinkedIn")
                    ], style={
                        'width': '100%',
                        'padding': '12px 20px',
                        'marginBottom': '20px',
                        'backgroundColor': '#0077b5',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '6px',
                        'cursor': 'pointer',
                        'fontSize': '1rem',
                        'fontWeight': '600'
                    }),
                    
                    html.Hr(style={'margin': '20px 0'}),
                    
                    # Email Connection
                    html.H4("Or connect with email:", style={
                        'fontSize': '1.1rem',
                        'marginBottom': '15px',
                        'color': COLORS['dark']
                    }),
                    
                    dcc.Input(
                        id="connect-email",
                        type="email",
                        placeholder="Enter your email address",
                        style={
                            'width': '100%',
                            'padding': '10px',
                            'marginBottom': '10px',
                            'border': f'1px solid {COLORS["hover"]}',
                            'borderRadius': '6px',
                            'fontSize': '1rem'
                        }
                    ),
                    
                    html.Button("Send Connection Link", style={
                        'width': '100%',
                        'padding': '12px 20px',
                        'backgroundColor': COLORS['primary'],
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '6px',
                        'cursor': 'pointer',
                        'fontSize': '1rem',
                        'fontWeight': '600'
                    })
                ])
            ], style={
                'backgroundColor': 'white',
                'padding': '30px',
                'borderRadius': '12px',
                'boxShadow': '0 10px 30px rgba(0,0,0,0.2)',
                'position': 'relative',
                'maxWidth': '400px',
                'width': '90%'
            })
        ], style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'backgroundColor': 'rgba(0,0,0,0.5)',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'zIndex': '2000'
        })
    ])


def create_profile_modal():
    """Create profile view/edit modal content."""
    return html.Div([
        html.Div([
            html.Div([
                html.H3("User Profile", style={
                    'fontSize': '1.5rem',
                    'fontWeight': '700',
                    'color': COLORS['dark'],
                    'marginBottom': '20px',
                    'textAlign': 'center'
                }),
                html.Button("✕", id={'type': 'close-modal', 'modal': 'profile'}, n_clicks=0, style={
                    'position': 'absolute',
                    'top': '15px',
                    'right': '15px',
                    'border': 'none',
                    'backgroundColor': 'transparent',
                    'fontSize': '1.5rem',
                    'cursor': 'pointer',
                    'color': COLORS['dark'],
                    'fontWeight': 'bold',
                    'width': '30px',
                    'height': '30px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'borderRadius': '50%',
                    'transition': 'background-color 0.2s ease'
                }),
                
                # Profile Info
                html.Div([
                    html.Div("N", style={
                        'width': '80px',
                        'height': '80px',
                        'borderRadius': '50%',
                        'backgroundColor': COLORS['primary'],
                        'color': 'white',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'fontWeight': '700',
                        'fontSize': '2rem',
                        'margin': '0 auto 20px'
                    }),
                    
                    html.Div([
                        html.Label("Full Name:", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                        dcc.Input(
                            id="profile-name",
                            value="Nessrine Ben Ahmed",
                            style={
                                'width': '100%',
                                'padding': '8px',
                                'marginBottom': '15px',
                                'border': f'1px solid {COLORS["hover"]}',
                                'borderRadius': '4px'
                            }
                        ),
                        
                        html.Label("Email:", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                        dcc.Input(
                            id="profile-email",
                            value="nessrine@bankdash.com",
                            type="email",
                            style={
                                'width': '100%',
                                'padding': '8px',
                                'marginBottom': '15px',
                                'border': f'1px solid {COLORS["hover"]}',
                                'borderRadius': '4px'
                            }
                        ),
                        
                        html.Label("Department:", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                        dcc.Input(
                            id="profile-department",
                            value="Risk Analysis",
                            style={
                                'width': '100%',
                                'padding': '8px',
                                'marginBottom': '15px',
                                'border': f'1px solid {COLORS["hover"]}',
                                'borderRadius': '4px'
                            }
                        ),
                        
                        html.Label("Location:", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                        dcc.Input(
                            id="profile-location",
                            value="Tunis, Tunisia",
                            style={
                                'width': '100%',
                                'padding': '8px',
                                'marginBottom': '20px',
                                'border': f'1px solid {COLORS["hover"]}',
                                'borderRadius': '4px'
                            }
                        ),
                        
                        html.Div([
                            html.Button("Save Changes", id="save-profile-btn", n_clicks=0, style={
                                'padding': '10px 20px',
                                'backgroundColor': COLORS['success'],
                                'color': 'white',
                                'border': 'none',
                                'borderRadius': '6px',
                                'cursor': 'pointer',
                                'marginRight': '10px',
                                'fontWeight': '600'
                            }),
                            html.Button("Cancel", id={'type': 'close-modal', 'modal': 'profile'}, n_clicks=0, style={
                                'padding': '10px 20px',
                                'backgroundColor': COLORS['danger'],
                                'color': 'white',
                                'border': 'none',
                                'borderRadius': '6px',
                                'cursor': 'pointer',
                                'fontWeight': '600'
                            })
                        ], style={'textAlign': 'center'})
                    ])
                ])
            ], style={
                'backgroundColor': 'white',
                'padding': '30px',
                'borderRadius': '12px',
                'boxShadow': '0 10px 30px rgba(0,0,0,0.2)',
                'position': 'relative',
                'maxWidth': '500px',
                'width': '90%'
            })
        ], style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'backgroundColor': 'rgba(0,0,0,0.5)',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'zIndex': '2000'
        })
    ])


def create_manage_account_modal():
    """Create manage account modal content."""
    return html.Div([
        html.Div([
            html.Div([
                html.H3("Manage Account", style={
                    'fontSize': '1.5rem',
                    'fontWeight': '700',
                    'color': COLORS['dark'],
                    'marginBottom': '20px',
                    'textAlign': 'center'
                }),
                html.Button("✕", id={'type': 'close-modal', 'modal': 'manage'}, n_clicks=0, style={
                    'position': 'absolute',
                    'top': '15px',
                    'right': '15px',
                    'border': 'none',
                    'backgroundColor': 'transparent',
                    'fontSize': '1.5rem',
                    'cursor': 'pointer',
                    'color': COLORS['dark'],
                    'fontWeight': 'bold',
                    'width': '30px',
                    'height': '30px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'borderRadius': '50%',
                    'transition': 'background-color 0.2s ease'
                }),
                
                # Account Management Options
                html.Div([
                    html.Div([
                        html.H4("Security Settings", style={'color': COLORS['primary'], 'marginBottom': '15px'}),
                        html.Button("🔐 Change Password", style={
                            'width': '100%',
                            'padding': '10px',
                            'marginBottom': '10px',
                            'backgroundColor': 'white',
                            'border': f'2px solid {COLORS["primary"]}',
                            'borderRadius': '6px',
                            'cursor': 'pointer',
                            'color': COLORS['primary'],
                            'fontWeight': '600'
                        }),
                        html.Button("📱 Setup 2FA", style={
                            'width': '100%',
                            'padding': '10px',
                            'marginBottom': '20px',
                            'backgroundColor': 'white',
                            'border': f'2px solid {COLORS["success"]}',
                            'borderRadius': '6px',
                            'cursor': 'pointer',
                            'color': COLORS['success'],
                            'fontWeight': '600'
                        }),
                    ]),
                    
                    html.Div([
                        html.H4("Preferences", style={'color': COLORS['secondary'], 'marginBottom': '15px'}),
                        html.Button("🌙 Theme Settings", style={
                            'width': '100%',
                            'padding': '10px',
                            'marginBottom': '10px',
                            'backgroundColor': 'white',
                            'border': f'2px solid {COLORS["secondary"]}',
                            'borderRadius': '6px',
                            'cursor': 'pointer',
                            'color': COLORS['secondary'],
                            'fontWeight': '600'
                        }),
                        html.Button("🔔 Notifications", style={
                            'width': '100%',
                            'padding': '10px',
                            'marginBottom': '20px',
                            'backgroundColor': 'white',
                            'border': f'2px solid {COLORS["warning"]}',
                            'borderRadius': '6px',
                            'cursor': 'pointer',
                            'color': COLORS['warning'],
                            'fontWeight': '600'
                        }),
                    ]),
                    
                    html.Div([
                        html.H4("Data & Privacy", style={'color': COLORS['danger'], 'marginBottom': '15px'}),
                        html.Button("📥 Download Data", style={
                            'width': '100%',
                            'padding': '10px',
                            'marginBottom': '10px',
                            'backgroundColor': 'white',
                            'border': f'2px solid {COLORS["accent"]}',
                            'borderRadius': '6px',
                            'cursor': 'pointer',
                            'color': COLORS['accent'],
                            'fontWeight': '600'
                        }),
                        html.Button("🗑️ Delete Account", style={
                            'width': '100%',
                            'padding': '10px',
                            'backgroundColor': COLORS['danger'],
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '6px',
                            'cursor': 'pointer',
                            'fontWeight': '600'
                        }),
                    ])
                ])
            ], style={
                'backgroundColor': 'white',
                'padding': '30px',
                'borderRadius': '12px',
                'boxShadow': '0 10px 30px rgba(0,0,0,0.2)',
                'position': 'relative',
                'maxWidth': '450px',
                'width': '90%'
            })
        ], style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'backgroundColor': 'rgba(0,0,0,0.5)',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'zIndex': '2000'
        })
    ])


def get_dropdown_item_style():
    """Get dropdown item style."""
    return {
        'display': 'block',
        'width': '100%',
        'padding': '10px 15px',
        'border': 'none',
        'backgroundColor': 'transparent',
        'textAlign': 'left',
        'cursor': 'pointer',
        'borderRadius': '6px',
        'fontSize': '0.9rem',
        'transition': 'background-color 0.2s ease',
        'color': COLORS['dark'],
        'fontFamily': 'inherit'
    }