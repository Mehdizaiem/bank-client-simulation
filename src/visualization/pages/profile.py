"""
User profile page layout and components
"""
from dash import html
from components.cards import create_metric_card
from config.colors import COLORS


def create_profile_header():
    """Create the profile header with avatar and basic info."""
    return html.Div([
        html.Div([
            html.Div("N", style={
                'width': '120px', 'height': '120px', 'borderRadius': '50%',
                'backgroundColor': COLORS['primary'], 'color': 'white',
                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                'fontWeight': '700', 'fontSize': '3rem', 'marginRight': '30px',
                'boxShadow': '0 10px 30px rgba(30, 64, 175, 0.3)'
            }),
            html.Div([
                html.H1("nom et prenom Ben Ahmed", style={
                    'fontSize': '2.5rem', 'fontWeight': '700', 'color': COLORS['dark'], 'margin': '0 0 10px 0'
                }),
                html.P("Senior Banking Analyst", style={
                    'fontSize': '1.2rem', 'color': COLORS['primary'], 'fontWeight': '500', 'margin': '0 0 10px 0'
                }),
                html.P("📧 nom et prenom@bankdash.com | 📞 +216 12 345 678", style={
                    'fontSize': '1rem', 'color': COLORS['dark'], 'opacity': '0.8', 'margin': '0'
                }),
                html.Div([
                    html.Span("🌟 Premium Member", style={
                        'backgroundColor': COLORS['success'], 'color': 'white', 'padding': '5px 12px',
                        'borderRadius': '20px', 'fontSize': '0.9rem', 'fontWeight': '600', 'marginRight': '10px'
                    }),
                    html.Span("🔗 3 Connected Accounts", style={
                        'backgroundColor': COLORS['light'], 'color': COLORS['dark'], 'padding': '5px 12px',
                        'borderRadius': '20px', 'fontSize': '0.9rem', 'border': f'1px solid {COLORS["hover"]}'
                    })
                ], style={'marginTop': '15px'})
            ])
        ], style={'display': 'flex', 'alignItems': 'center'})
    ], style={
        'backgroundColor': 'white', 'padding': '40px', 'borderRadius': '15px',
        'boxShadow': '0 4px 20px rgba(0,0,0,0.1)', 'marginBottom': '30px'
    })


def create_profile_stats():
    """Create profile statistics cards."""
    return html.Div([
        create_metric_card("📈", "Account Age", "2.5 Years", "Since Jan 2022", COLORS['primary']),
        create_metric_card("💰", "Total Transactions", "1,247", "+23 this month", COLORS['success']),
        create_metric_card("🔒", "Security Score", "98%", "Excellent", COLORS['secondary']),
        create_metric_card("⭐", "Loyalty Points", "15,670", "+450 this month", COLORS['accent']),
    ], style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
        'gap': '20px',
        'marginBottom': '30px'
    })


def create_personal_info_section():
    """Create personal information section."""
    return html.Div([
        html.H3("Personal Information", style={
            'fontSize': '1.5rem', 'fontWeight': '700', 'color': COLORS['dark'], 'marginBottom': '20px'
        }),
        
        html.Div([
            html.Div([
                html.Strong("Full Name: "),
                html.Span("nom et prenom")
            ], style={'marginBottom': '15px', 'fontSize': '1rem'}),
            
            html.Div([
                html.Strong("Email: "),
                html.Span("nom et prenom@bankdash.com")
            ], style={'marginBottom': '15px', 'fontSize': '1rem'}),
            
            html.Div([
                html.Strong("Phone: "),
                html.Span("+216 12 345 678")
            ], style={'marginBottom': '15px', 'fontSize': '1rem'}),
            
            html.Div([
                html.Strong("Location: "),
                html.Span("Tunis, Tunisia")
            ], style={'marginBottom': '15px', 'fontSize': '1rem'}),
            
            html.Div([
                html.Strong("Department: "),
                html.Span("Risk Analysis")
            ], style={'marginBottom': '15px', 'fontSize': '1rem'}),
            
            html.Div([
                html.Strong("Employee ID: "),
                html.Span("BA-2022-0154")
            ], style={'marginBottom': '15px', 'fontSize': '1rem'})
        ])
    ], style={
        'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '12px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)', 'marginBottom': '20px'
    })


def create_security_section():
    """Create account security section."""
    return html.Div([
        html.H3("Account Security", style={
            'fontSize': '1.5rem', 'fontWeight': '700', 'color': COLORS['dark'], 'marginBottom': '20px'
        }),
        
        html.Div([
            html.Div([
                html.Div([
                    html.Span("🔐", style={'fontSize': '1.2rem', 'marginRight': '10px'}),
                    html.Span("Two-Factor Authentication", style={'fontWeight': '600'})
                ], style={'marginBottom': '5px'}),
                html.Div("Enabled", style={'color': COLORS['success'], 'fontSize': '0.9rem'})
            ], style={'marginBottom': '15px'}),
            
            html.Div([
                html.Div([
                    html.Span("🔑", style={'fontSize': '1.2rem', 'marginRight': '10px'}),
                    html.Span("Password Strength", style={'fontWeight': '600'})
                ], style={'marginBottom': '5px'}),
                html.Div("Strong", style={'color': COLORS['success'], 'fontSize': '0.9rem'})
            ], style={'marginBottom': '15px'}),
            
            html.Div([
                html.Div([
                    html.Span("📱", style={'fontSize': '1.2rem', 'marginRight': '10px'}),
                    html.Span("Last Login", style={'fontWeight': '600'})
                ], style={'marginBottom': '5px'}),
                html.Div("Today, 09:24 AM", style={'color': COLORS['dark'], 'opacity': '0.7', 'fontSize': '0.9rem'})
            ])
        ])
    ], style={
        'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '12px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
    })


def create_activity_section():
    """Create recent activity section."""
    return html.Div([
        html.H3("Recent Activity", style={
            'fontSize': '1.5rem', 'fontWeight': '700', 'color': COLORS['dark'], 'marginBottom': '20px'
        }),
        
        html.Div([
            # Activity items
            html.Div([
                html.Div("📊", style={'fontSize': '1.5rem', 'marginRight': '15px'}),
                html.Div([
                    html.Div("Generated Q4 Risk Report", style={'fontWeight': '600', 'marginBottom': '5px'}),
                    html.Div("2 hours ago", style={'fontSize': '0.85rem', 'opacity': '0.7'})
                ])
            ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '20px'}),
            
            html.Div([
                html.Div("🔄", style={'fontSize': '1.5rem', 'marginRight': '15px'}),
                html.Div([
                    html.Div("Updated profile information", style={'fontWeight': '600', 'marginBottom': '5px'}),
                    html.Div("1 day ago", style={'fontSize': '0.85rem', 'opacity': '0.7'})
                ])
            ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '20px'}),
            
            html.Div([
                html.Div("🔐", style={'fontSize': '1.5rem', 'marginRight': '15px'}),
                html.Div([
                    html.Div("Password changed successfully", style={'fontWeight': '600', 'marginBottom': '5px'}),
                    html.Div("3 days ago", style={'fontSize': '0.85rem', 'opacity': '0.7'})
                ])
            ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '20px'}),
            
            html.Div([
                html.Div("🔗", style={'fontSize': '1.5rem', 'marginRight': '15px'}),
                html.Div([
                    html.Div("Connected GitHub account", style={'fontWeight': '600', 'marginBottom': '5px'}),
                    html.Div("1 week ago", style={'fontSize': '0.85rem', 'opacity': '0.7'})
                ])
            ], style={'display': 'flex', 'alignItems': 'flex-start'})
        ])
    ], style={
        'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '12px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)', 'marginBottom': '20px'
    })


def create_preferences_section():
    """Create preferences section."""
    return html.Div([
        html.H3("Preferences", style={
            'fontSize': '1.5rem', 'fontWeight': '700', 'color': COLORS['dark'], 'marginBottom': '20px'
        }),
        
        html.Div([
            html.Div([
                html.Strong("Language: "),
                html.Span("English")
            ], style={'marginBottom': '15px', 'fontSize': '1rem'}),
            
            html.Div([
                html.Strong("Timezone: "),
                html.Span("GMT+1 (Tunis)")
            ], style={'marginBottom': '15px', 'fontSize': '1rem'}),
            
            html.Div([
                html.Strong("Theme: "),
                html.Span("Light Mode")
            ], style={'marginBottom': '15px', 'fontSize': '1rem'}),
            
            html.Div([
                html.Strong("Notifications: "),
                html.Span("Email + Push")
            ], style={'marginBottom': '15px', 'fontSize': '1rem'}),
            
            html.Div([
                html.Strong("Dashboard Refresh: "),
                html.Span("Every 15 seconds")
            ], style={'fontSize': '1rem'})
        ])
    ], style={
        'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '12px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
    })


def create_action_buttons():
    """Create action buttons for the profile page."""
    return html.Div([
        html.Button([
            html.Span("✏️", style={'marginRight': '8px'}),
            html.Span("Edit Profile")
        ], id="profile-edit-btn", n_clicks=0, style={
            'padding': '12px 24px', 'backgroundColor': COLORS['primary'], 'color': 'white',
            'border': 'none', 'borderRadius': '8px', 'fontSize': '1rem', 'fontWeight': '600',
            'cursor': 'pointer', 'marginRight': '15px', 'transition': 'all 0.3s ease'
        }),
        
        html.Button([
            html.Span("📤", style={'marginRight': '8px'}),
            html.Span("Export Data")
        ], id="profile-export-btn", n_clicks=0, style={
            'padding': '12px 24px', 'backgroundColor': COLORS['secondary'], 'color': 'white',
            'border': 'none', 'borderRadius': '8px', 'fontSize': '1rem', 'fontWeight': '600',
            'cursor': 'pointer', 'marginRight': '15px', 'transition': 'all 0.3s ease'
        }),
        
        html.Button([
            html.Span("🔒", style={'marginRight': '8px'}),
            html.Span("Privacy Settings")
        ], id="profile-privacy-btn", n_clicks=0, style={
            'padding': '12px 24px', 'backgroundColor': 'white', 'color': COLORS['dark'],
            'border': f'2px solid {COLORS["hover"]}', 'borderRadius': '8px', 'fontSize': '1rem', 
            'fontWeight': '600', 'cursor': 'pointer', 'transition': 'all 0.3s ease'
        })
    ], style={'textAlign': 'center', 'marginTop': '40px'})


def create_profile_page_content():
    """Create the complete profile page content."""
    return html.Div([
        create_profile_header(),
        create_profile_stats(),
        
        # Profile Content Grid
        html.Div([
            # Left Column
            html.Div([
                create_personal_info_section(),
                create_security_section()
            ], style={'flex': '1', 'marginRight': '20px'}),
            
            # Right Column
            html.Div([
                create_activity_section(),
                create_preferences_section()
            ], style={'flex': '1'})
        ], style={'display': 'flex', 'gap': '20px'}),
        
        create_action_buttons()
    ])