import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.graph_objs as go
import plotly.express as px
import random

COLORS = {
    'primary': '#1e40af',      # Professional blue
    'secondary': '#0f766e',    # Teal
    'accent': '#7c3aed',       # Purple
    'success': '#059669',      # Green
    'warning': '#d97706',      # Orange
    'danger': '#dc2626',       # Red
    'light': '#f8fafc',        # Light gray
    'dark': '#1e293b',         # Dark gray
    'sidebar': '#f1f5f9',      # Sidebar background
    'hover': '#e2e8f0'         # Hover color
}

def create_nav_button(icon, label, page_id):
    """Create a navigation button."""
    return html.Button([
        html.Span(icon, style={'fontSize': '1.3rem', 'marginRight': '15px', 'width': '25px', 'textAlign': 'center'}),
        html.Span(label, style={'fontSize': '0.95rem', 'fontWeight': '500'})
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

def create_sidebar_navigation():
    """Create modern sidebar with navigation buttons."""
    return html.Div([
        html.Div([
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
        ], style={'padding': '25px 20px', 'borderBottom': f'1px solid {COLORS["hover"]}', 'marginBottom': '20px'}),
        html.Div([
            create_nav_button("🏠", "Home", "home"),
            create_nav_button("📊", "Economic Analysis", "economic"),
            create_nav_button("🗺️", "Geographic Analysis", "geographic"),
            create_nav_button("💬", "AI Chat", "chat"),
            create_nav_button("⚙️", "Settings", "settings"),
        ], id="navigation-menu"),
        html.Div([
            html.Div("System Status", style={'fontSize': '0.85rem', 'fontWeight': '600', 'color': COLORS['dark'], 'marginBottom': '10px'}),
            html.Div([
                html.Div("●", style={'color': COLORS['success'], 'fontSize': '1.2rem', 'marginRight': '8px'}),
                html.Span("Online", style={'fontSize': '0.9rem', 'color': COLORS['dark']})
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '8px'}),
            html.Div([
                html.Span("Agents: ", style={'fontSize': '0.8rem', 'color': COLORS['dark']}),
                html.Span("1,247", style={'fontSize': '0.8rem', 'fontWeight': '600', 'color': COLORS['primary']})
            ], style={'marginBottom': '5px'}),
            html.Div([
                html.Span("Last Update: ", style={'fontSize': '0.8rem', 'color': COLORS['dark']}),
                html.Span("2min ago", style={'fontSize': '0.8rem', 'color': COLORS['dark']})
            ])
        ], style={
            'position': 'absolute', 'bottom': '20px', 'left': '20px', 'right': '20px',
            'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '10px',
            'boxShadow': '0 2px 10px rgba(0,0,0,0.1)', 'border': f'1px solid {COLORS["hover"]}'
        })
    ], style={
        'position': 'fixed', 'left': '0', 'top': '0', 'width': '280px', 'height': '100vh',
        'backgroundColor': COLORS['sidebar'], 'borderRight': f'1px solid {COLORS["hover"]}',
        'zIndex': '1000', 'boxShadow': '2px 0 10px rgba(0,0,0,0.1)'
    })

def create_top_header():
    return html.Div([
        html.Div([
            html.H1("Dashboard Overview", id="page-title", style={
                'margin': '0', 'fontSize': '1.8rem', 'fontWeight': '700', 'color': COLORS['dark']
            }),
            html.Div([
                html.Div([dcc.Input(placeholder="Search...", style={
                    'width': '250px', 'marginRight': '15px', 'padding': '8px 12px',
                    'border': f'1px solid {COLORS["hover"]}', 'borderRadius': '6px', 'fontSize': '0.9rem'
                })]),
                html.Div([
                    html.Div("🔔", style={
                        'fontSize': '1.3rem', 'cursor': 'pointer', 'padding': '8px', 'borderRadius': '8px',
                        'backgroundColor': 'white', 'border': f'1px solid {COLORS["hover"]}', 'marginRight': '10px'
                    }),
                    html.Div("N", style={
                        'width': '35px', 'height': '35px', 'borderRadius': '50%', 'backgroundColor': COLORS['primary'],
                        'color': 'white', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                        'fontWeight': '600', 'fontSize': '1rem'
                    })
                ], style={'display': 'flex', 'alignItems': 'center'})
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'})
    ], style={'padding': '20px 30px', 'backgroundColor': 'white', 'borderBottom': f'1px solid {COLORS["hover"]}', 'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'})

def create_homepage_content():
    return html.Div([
        # Welcome Section
        html.Div([
            html.H2("Welcome to Bank Client Simulation", style={'fontSize': '2rem', 'fontWeight': '700', 'color': COLORS['dark'], 'marginBottom': '10px'}),
            html.P("Monitor real-time client behavior and market dynamics across Tunisia", style={'fontSize': '1.1rem', 'color': COLORS['dark'], 'opacity': '0.7', 'marginBottom': '30px'})
        ]),
        # Home page chart/action buttons row
        html.Div([
            # Filter dropdown
            html.Div([
                html.Label("Filter by Segment:", style={'marginRight': '8px', 'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='home-segment-filter',
                    options=[
                        {'label': 'All', 'value': 'all'},
                        {'label': 'Retail', 'value': 'retail'},
                        {'label': 'Corporate', 'value': 'corporate'},
                        {'label': 'SME', 'value': 'sme'},
                        {'label': 'Private', 'value': 'private'}
                    ],
                    value='all',
                    clearable=False,
                    style={'width': '140px', 'display': 'inline-block'}
                ),
            ], style={'display': 'inline-block', 'marginRight': '24px'}),
            # Sort dropdown
            html.Div([
                html.Label("Sort by:", style={'marginRight': '8px', 'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='home-sort',
                    options=[
                        {'label': 'Alphabetical', 'value': 'alpha'},
                        {'label': 'Clients Desc', 'value': 'clients_desc'},
                        {'label': 'Clients Asc', 'value': 'clients_asc'}
                    ],
                    value='alpha',
                    clearable=False,
                    style={'width': '140px', 'display': 'inline-block'}
                ),
            ], style={'display': 'inline-block', 'marginRight': '24px'}),
            # Export buttons
            html.Button("Export CSV", id="home-export-csv", n_clicks=0, style={
                'padding': '10px 20px', 'backgroundColor': COLORS['primary'], 'color': 'white', 'border': 'none',
                'borderRadius': '6px', 'fontWeight': '600', 'marginRight': '8px', 'cursor': 'pointer'
            }),
            html.Button("Export PNG", id="home-export-png", n_clicks=0, style={
                'padding': '10px 20px', 'backgroundColor': COLORS['success'], 'color': 'white', 'border': 'none',
                'borderRadius': '6px', 'fontWeight': '600', 'marginRight': '8px', 'cursor': 'pointer'
            }),
            html.Button("Export PDF", id="home-export-pdf", n_clicks=0, style={
                'padding': '10px 20px', 'backgroundColor': COLORS['accent'], 'color': 'white', 'border': 'none',
                'borderRadius': '6px', 'fontWeight': '600', 'cursor': 'pointer'
            }),
            dcc.Download(id="home-csv-download")
        ], style={'marginBottom': '16px', 'display': 'flex', 'alignItems': 'center'}),

        # Key Metrics Cards
        html.Div([
            create_metric_card("👥", "Total Clients", "12,847", "+5.2% this month", COLORS['primary']),
            create_metric_card("📈", "Market Share", "34.2%", "+2.1% this quarter", COLORS['success']),
            create_metric_card("🏢", "Active Branches", "156", "3 new branches", COLORS['secondary']),
            create_metric_card("💰", "Revenue", "€2.4M", "+8.7% vs last month", COLORS['accent']),
        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
            'gap': '20px',
            'marginBottom': '30px'
        }),

        # Four charts in a 2x2 grid
        # Four charts in a 2x2 grid (2 charts per row)
    html.Div([
        # Row 1: Line chart + Bar chart
        html.Div([
            html.Div(dcc.Graph(id="homepage-line-chart"), style={
                'width': '100%', 'padding': '8px', 'backgroundColor': '#fff', 'borderRadius': '12px', 'boxShadow': '0 2px 12px #e5e7eb'
            }),
            html.Div(dcc.Graph(id="homepage-bar-chart"), style={
                'width': '100%', 'padding': '8px', 'backgroundColor': '#fff', 'borderRadius': '12px', 'boxShadow': '0 2px 12px #e5e7eb'
            })
        ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}),

        # Row 2: Pie chart + Map chart
        html.Div([
            html.Div(dcc.Graph(id="homepage-pie-chart"), style={
                'width': '100%', 'padding': '8px', 'backgroundColor': '#fff', 'borderRadius': '12px', 'boxShadow': '0 2px 12px #e5e7eb'
            }),
            html.Div(dcc.Graph(id="homepage-map-chart"), style={
                'width': '100%', 'padding': '8px', 'backgroundColor': '#fff', 'borderRadius': '12px', 'boxShadow': '0 2px 12px #e5e7eb'
            })
        ], style={'display': 'flex', 'gap': '20px'})
            ], style={'width': '100%'})
        
    ])


def update_homepage_charts(current_page):
    # Only show data if on Home page
    if current_page != 'home':
        return {}, {}

    # Example: Client Growth Trend (line)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    clients = [11500, 12000, 12250, 12500, 12800, 12847]
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=months,
        y=clients,
        mode='lines+markers',
        name='Total Clients',
        line=dict(color=COLORS['primary'], width=4)
    ))
    fig1.update_layout(
        title="Client Growth Over Time",
        xaxis_title="Month",
        yaxis_title="Number of Clients",
        template='plotly_white',
        height=340
    )

    # Example: Churn Rate Pie
    fig2 = go.Figure(go.Pie(
        labels=["Retained", "Churned"],
        values=[95, 5],
        marker_colors=[COLORS['success'], COLORS['danger']],
        hole=0.4
    ))
    fig2.update_layout(
        title="Client Retention vs Churn",
        height=340,
        showlegend=True
    )

    return fig1, fig2


def create_metric_card(icon, title, value, change, color):
    return html.Div([
        html.Div([
            html.Div(icon, style={'fontSize': '2rem', 'marginBottom': '10px'}),
            html.H3(value, style={'fontSize': '1.8rem', 'fontWeight': '700', 'color': color, 'margin': '0', 'marginBottom': '5px'}),
            html.P(title, style={'fontSize': '1rem', 'fontWeight': '600', 'color': COLORS['dark'], 'margin': '0', 'marginBottom': '8px'}),
            html.P(change, style={'fontSize': '0.85rem', 'color': COLORS['success'], 'margin': '0'})
        ])
    ], style={
        'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '15px',
        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)', 'border': f'1px solid {COLORS["hover"]}',
        'textAlign': 'center', 'transition': 'transform 0.3s ease', 'cursor': 'pointer'
    })

def create_economic_content():
    return html.Div([
        html.H2("Economic Analysis Dashboard", style={'fontSize': '2rem', 'fontWeight': '700', 'color': COLORS['dark'], 'marginBottom': '20px'}),
        # Home page chart/action buttons row
        html.Div([
            # Filter dropdown
            html.Div([
                html.Label("Filter by Segment:", style={'marginRight': '8px', 'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='home-segment-filter',
                    options=[
                        {'label': 'All', 'value': 'all'},
                        {'label': 'Retail', 'value': 'retail'},
                        {'label': 'Corporate', 'value': 'corporate'},
                        {'label': 'SME', 'value': 'sme'},
                        {'label': 'Private', 'value': 'private'}
                    ],
                    value='all',
                    clearable=False,
                    style={'width': '140px', 'display': 'inline-block'}
                ),
            ], style={'display': 'inline-block', 'marginRight': '24px'}),
            # Sort dropdown
            html.Div([
                html.Label("Sort by:", style={'marginRight': '8px', 'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='home-sort',
                    options=[
                        {'label': 'Alphabetical', 'value': 'alpha'},
                        {'label': 'Clients Desc', 'value': 'clients_desc'},
                        {'label': 'Clients Asc', 'value': 'clients_asc'}
                    ],
                    value='alpha',
                    clearable=False,
                    style={'width': '140px', 'display': 'inline-block'}
                ),
            ], style={'display': 'inline-block', 'marginRight': '24px'}),
            # Export buttons
            html.Button("Export CSV", id="home-export-csv", n_clicks=0, style={
                'padding': '10px 20px', 'backgroundColor': COLORS['primary'], 'color': 'white', 'border': 'none',
                'borderRadius': '6px', 'fontWeight': '600', 'marginRight': '8px', 'cursor': 'pointer'
            }),
            html.Button("Export PNG", id="home-export-png", n_clicks=0, style={
                'padding': '10px 20px', 'backgroundColor': COLORS['success'], 'color': 'white', 'border': 'none',
                'borderRadius': '6px', 'fontWeight': '600', 'marginRight': '8px', 'cursor': 'pointer'
            }),
            html.Button("Export PDF", id="home-export-pdf", n_clicks=0, style={
                'padding': '10px 20px', 'backgroundColor': COLORS['accent'], 'color': 'white', 'border': 'none',
                'borderRadius': '6px', 'fontWeight': '600', 'cursor': 'pointer'
            }),
            dcc.Download(id="home-csv-download")
        ], style={'marginBottom': '16px', 'display': 'flex', 'alignItems': 'center'}),

        html.Div([
            html.Div([dcc.Graph(id="economic-trends-chart")], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(id="market-indicators-chart")], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
        ])
    ])

def create_geographic_content():
    return html.Div([
        html.H2("Geographic Analysis Dashboard", style={'fontSize': '2rem', 'fontWeight': '700', 'color': COLORS['dark'], 'marginBottom': '20px'}),
        # Home page chart/action buttons row
        html.Div([
            # Filter dropdown
            html.Div([
                html.Label("Filter by Segment:", style={'marginRight': '8px', 'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='home-segment-filter',
                    options=[
                        {'label': 'All', 'value': 'all'},
                        {'label': 'Retail', 'value': 'retail'},
                        {'label': 'Corporate', 'value': 'corporate'},
                        {'label': 'SME', 'value': 'sme'},
                        {'label': 'Private', 'value': 'private'}
                    ],
                    value='all',
                    clearable=False,
                    style={'width': '140px', 'display': 'inline-block'}
                ),
            ], style={'display': 'inline-block', 'marginRight': '24px'}),
            # Sort dropdown
            html.Div([
                html.Label("Sort by:", style={'marginRight': '8px', 'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='home-sort',
                    options=[
                        {'label': 'Alphabetical', 'value': 'alpha'},
                        {'label': 'Clients Desc', 'value': 'clients_desc'},
                        {'label': 'Clients Asc', 'value': 'clients_asc'}
                    ],
                    value='alpha',
                    clearable=False,
                    style={'width': '140px', 'display': 'inline-block'}
                ),
            ], style={'display': 'inline-block', 'marginRight': '24px'}),
            # Export buttons
            html.Button("Export CSV", id="home-export-csv", n_clicks=0, style={
                'padding': '10px 20px', 'backgroundColor': COLORS['primary'], 'color': 'white', 'border': 'none',
                'borderRadius': '6px', 'fontWeight': '600', 'marginRight': '8px', 'cursor': 'pointer'
            }),
            html.Button("Export PNG", id="home-export-png", n_clicks=0, style={
                'padding': '10px 20px', 'backgroundColor': COLORS['success'], 'color': 'white', 'border': 'none',
                'borderRadius': '6px', 'fontWeight': '600', 'marginRight': '8px', 'cursor': 'pointer'
            }),
            html.Button("Export PDF", id="home-export-pdf", n_clicks=0, style={
                'padding': '10px 20px', 'backgroundColor': COLORS['accent'], 'color': 'white', 'border': 'none',
                'borderRadius': '6px', 'fontWeight': '600', 'cursor': 'pointer'
            }),
            dcc.Download(id="home-csv-download")
        ], style={'marginBottom': '16px', 'display': 'flex', 'alignItems': 'center'}),

        html.Div([
            html.Div([dcc.Graph(id="tunisia-map")], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(id="branch-distribution-chart")], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
        ])
    ])

def create_chat_content():
    return html.Div([
        html.H2("AI Assistant Chat", style={'fontSize': '2rem', 'fontWeight': '700', 'color': COLORS['dark'], 'marginBottom': '20px'}),
        html.Div([
            html.Div([
                html.Div("🤖", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
                html.Div("Hello! I'm your AI banking assistant. How can I help you analyze client behavior today?",
                        style={'backgroundColor': COLORS['light'], 'padding': '12px', 'borderRadius': '15px', 'flex': '1'})
            ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '15px'})
        ], id="chat-messages", style={
            'height': '400px', 'overflowY': 'auto', 'padding': '20px', 'backgroundColor': 'white',
            'border': f'1px solid {COLORS["hover"]}', 'borderRadius': '15px', 'marginBottom': '20px'
        }),
        html.Div([
            dcc.Input(id="chat-input", placeholder="Ask me about client trends, market analysis, or any banking insights...", style={
                'flex': '1', 'marginRight': '10px', 'padding': '12px', 'border': f'1px solid {COLORS["hover"]}', 'borderRadius': '6px', 'fontSize': '1rem', 'width': '70%'
            }),
            html.Button("Send", id="send-chat-button", n_clicks=0, style={
                'padding': '12px 24px', 'background': f'linear-gradient(135deg, {COLORS["primary"]}, {COLORS["secondary"]})', 'color': 'white',
                'border': 'none', 'borderRadius': '6px', 'cursor': 'pointer', 'fontWeight': '600'
            })
        ], style={'display': 'flex', 'alignItems': 'center'})
    ], style={'maxWidth': '800px'})

def create_settings_content():
    return html.Div([
        html.H2("Dashboard Settings", style={
            'fontSize': '2rem', 'fontWeight': '700', 'color': COLORS['dark'], 'marginBottom': '20px'
        }),

        html.Div([
            # Theme card
            html.Div([
                html.H4("Theme & Personalization", style={'marginBottom': '10px', 'color': COLORS['primary']}),
                dcc.RadioItems(
                    id='setting-theme',
                    options=[
                        {'label': ' Light', 'value': 'light'},
                        {'label': ' Dark', 'value': 'dark'},
                        {'label': ' Corporate', 'value': 'corporate'},
                    ],
                    value='light',
                    labelStyle={'display': 'inline-block', 'marginRight': '18px', 'fontSize': '1rem'}
                ),
                html.Div("Select your preferred dashboard theme.", style={'fontSize': '0.92rem', 'opacity': '0.75'})
            ], style={
                'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '14px', 'marginBottom': '22px',
                'boxShadow': '0 2px 12px #e5e7eb', 'borderLeft': f'5px solid {COLORS["primary"]}'
            }),

            # Notification and language settings
            html.Div([
                html.H4("Notifications & Preferences", style={'marginBottom': '10px', 'color': COLORS['accent']}),
                dcc.Checklist(
                    options=[
                        {"label": " Email Notifications", "value": "email"},
                        {"label": " Push Notifications", "value": "push"},
                        {"label": " SMS Alerts", "value": "sms"},
                    ],
                    value=["push"],
                    id="setting-notifications",
                    style={'marginBottom': '12px'}
                ),
                html.Label("Interface Language", style={'marginRight': '10px', 'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='setting-language',
                    options=[
                        {'label': 'English', 'value': 'en'},
                        {'label': 'French', 'value': 'fr'},
                        {'label': 'Arabic', 'value': 'ar'},
                    ],
                    value='en',
                    clearable=False,
                    style={'width': '200px', 'display': 'inline-block', 'marginBottom': '16px'}
                ),
                html.Label("Default Refresh Rate", style={'marginRight': '10px', 'fontWeight': 'bold'}),
                dcc.Slider(
                    id='setting-refresh-interval',
                    min=5, max=60, step=5, value=15,
                    marks={i: f"{i}s" for i in range(5, 65, 10)},
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode="drag"
                )
            ], style={
                'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '14px', 'boxShadow': '0 2px 12px #e5e7eb',
                'borderLeft': f'5px solid {COLORS["accent"]}'
            }),

            html.Div([
                html.Button("Save Changes", id="settings-save-btn", n_clicks=0, style={
                    'padding': '10px 28px', 'backgroundColor': COLORS['success'],
                    'color': 'white', 'border': 'none', 'borderRadius': '6px', 'fontWeight': '700',
                    'marginTop': '22px', 'marginRight': '12px', 'fontSize': '1.07rem'
                }),
                html.Button("Reset All", id="settings-reset-btn", n_clicks=0, style={
                    'padding': '10px 28px', 'backgroundColor': COLORS['danger'],
                    'color': 'white', 'border': 'none', 'borderRadius': '6px', 'fontWeight': '700',
                    'marginTop': '22px', 'fontSize': '1.07rem'
                }),
                html.Div(id="settings-status", style={'marginTop': '20px', 'fontWeight': '600', 'color': COLORS['success']})
            ])
        ], style={'maxWidth': '600px', 'margin': '0 auto'})
    ])



# -------------------- DASH APP SETUP ------------------------

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Store(id='current-page-store', data='home'),
    create_sidebar_navigation(),
    html.Div([
        create_top_header(),
        html.Div(id="page-content", children=[create_homepage_content()], style={
            'padding': '20px', 'backgroundColor': '#ffffff',
            'minHeight': 'calc(100vh - 80px)', 'overflowY': 'auto'
        })
    ], style={'marginLeft': '280px', 'transition': 'margin-left 0.3s ease'})
], style={'fontFamily': 'Inter, sans-serif', 'backgroundColor': COLORS['light']})

# -------------------- CALLBACKS -----------------------------
@app.callback(
    [Output('homepage-line-chart', 'figure'),
     Output('homepage-bar-chart', 'figure'),
     Output('homepage-pie-chart', 'figure'),
     Output('homepage-map-chart', 'figure')],
    Input('current-page-store', 'data'),
    prevent_initial_call=False
)
def update_homepage_charts(current_page):
    if current_page != 'home':
        return {}, {}, {}, {}

    # 1. Line Chart (Client Growth)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    clients = [11500, 12000, 12250, 12500, 12800, 12847]
    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(
        x=months, y=clients, mode='lines+markers', name='Clients',
        line=dict(color=COLORS['primary'], width=4)
    ))
    line_fig.update_layout(
        title="Client Growth Over Time",
        xaxis_title="Month",
        yaxis_title="Number of Clients",
        template='plotly_white',
        height=320
    )

    # 2. Bar Chart (Monthly Revenue)
    revenue = [200, 250, 260, 270, 310, 340]
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(
        x=months, y=revenue, name='Revenue (€K)', marker_color=COLORS['accent']
    ))
    bar_fig.update_layout(
        title="Monthly Revenue (€K)",
        xaxis_title="Month",
        yaxis_title="Revenue (€K)",
        template='plotly_white',
        height=320
    )

    # 3. Pie Chart (Client Segmentation)
    segments = ["Retail", "Corporate", "SME", "Private"]
    sizes = [62, 20, 10, 8]
    pie_fig = go.Figure(go.Pie(
        labels=segments, values=sizes, hole=0.45,
        marker=dict(colors=[COLORS['primary'], COLORS['accent'], COLORS['secondary'], COLORS['success']])
    ))
    pie_fig.update_layout(
        title="Client Segmentation",
        height=320,
        showlegend=True
    )

    # 4. Map (Tunisia, fake data)
    governorates = ["Tunis", "Sfax", "Sousse", "Kairouan", "Bizerte", "Ariana"]
    counts = [3200, 2100, 1850, 1300, 1400, 1600]
    # Use px.choropleth if you have geojson; for simplicity, let's use a bar chart for regions as "map"
    map_fig = px.bar(
        x=governorates, y=counts, title="Clients by Governorate",
        color=counts, color_continuous_scale='Blues'
    )
    map_fig.update_layout(
        template='plotly_white',
        height=320,
        showlegend=False
    )

    return line_fig, bar_fig, pie_fig, map_fig
import pandas as pd

@app.callback(
    Output("home-csv-download", "data"),
    Input("home-export-csv", "n_clicks"),
    prevent_initial_call=True
)
def download_csv(n_clicks):
    # Example export data (you can customize)
    df = pd.DataFrame({
        "Month": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        "Clients": [11500, 12000, 12250, 12500, 12800, 12847],
        "Revenue": [200, 250, 260, 270, 310, 340]
    })
    return dcc.send_data_frame(df.to_csv, "dashboard_data.csv")

# PNG/PDF export handled by plotly modebar (download as PNG) - just enable the modebar on your dcc.Graph
# For PDF, more advanced (use orca or browser "Print to PDF")

# For filter/sort: just read the dropdown values in your chart callbacks and modify the data accordingly!


@app.callback(
    [Output('page-content', 'children'), Output('page-title', 'children'), Output('current-page-store', 'data')],
    [Input('nav-home', 'n_clicks'),
     Input('nav-economic', 'n_clicks'),
     Input('nav-geographic', 'n_clicks'),
     Input('nav-chat', 'n_clicks'),
     Input('nav-settings', 'n_clicks')],
    prevent_initial_call=False
)
def handle_navigation(home, economic, geo, chat, settings):
    ctx = callback_context
    # On initial load or if all buttons never clicked, show homepage
    if not ctx.triggered or all(x is None for x in [home, economic, geo, chat, settings]):
        return create_homepage_content(), "Dashboard Overview", "home"
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == "nav-home":
        return create_homepage_content(), "Dashboard Overview", "home"
    elif button_id == "nav-economic":
        return create_economic_content(), "Economic Analysis", "economic"
    elif button_id == "nav-geographic":
        return create_geographic_content(), "Geographic Analysis", "geographic"
    elif button_id == "nav-chat":
        return create_chat_content(), "AI Assistant Chat", "chat"
    elif button_id == "nav-settings":
        return create_settings_content(), "Settings", "settings"
    # fallback (should not be reached)
    return create_homepage_content(), "Dashboard Overview", "home"


@app.callback(
    [Output('nav-home', 'style'), Output('nav-economic', 'style'), Output('nav-geographic', 'style'),
     Output('nav-chat', 'style'), Output('nav-settings', 'style')],
    Input('current-page-store', 'data')
)
def update_nav_styles(current_page):
    base_style = {
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
    }
    active_style = {**base_style, 'backgroundColor': COLORS['primary'], 'color': 'white', 'transform': 'translateX(5px)', 'boxShadow': f'0 4px 15px {COLORS["primary"]}40'}
    return (
        active_style if current_page == "home" else base_style,
        active_style if current_page == "economic" else base_style,
        active_style if current_page == "geographic" else base_style,
        active_style if current_page == "chat" else base_style,
        active_style if current_page == "settings" else base_style
    )

# Economic Analysis Charts
@app.callback(
    [Output('economic-trends-chart', 'figure'), Output('market-indicators-chart', 'figure')],
    Input('current-page-store', 'data'),
    prevent_initial_call=False
)
def update_economic_charts(current_page):
    if current_page != 'economic':
        return {}, {}
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    economic_data = [100, 102, 104, 103, 105, 107]
    trends_fig = go.Figure()
    trends_fig.add_trace(go.Scatter(
        x=months, y=economic_data, mode='lines+markers', name='Economic Index',
        line=dict(color=COLORS['primary'], width=3), marker=dict(size=8)
    ))
    trends_fig.update_layout(
        title="Economic Trends Over Time", xaxis_title="Month", yaxis_title="Economic Index",
        template='plotly_white', height=400
    )
    indicators = ['GDP Growth', 'Inflation', 'Unemployment', 'Consumer Confidence']
    values = [random.uniform(1, 8) for _ in indicators]
    indicators_fig = px.bar(
        x=indicators, y=values, title="Key Market Indicators", color=values, color_continuous_scale='Viridis'
    )
    indicators_fig.update_layout(template='plotly_white', height=400, showlegend=False)
    return trends_fig, indicators_fig

# Geographic Analysis Charts
@app.callback(
    [Output('tunisia-map', 'figure'), Output('branch-distribution-chart', 'figure')],
    Input('current-page-store', 'data'),
    prevent_initial_call=False
)
def update_geographic_charts(current_page):
    if current_page != 'geographic':
        return {}, {}
    all_governorates = ['Tunis', 'Sfax', 'Sousse', 'Kairouan', 'Bizerte', 'Ariana']
    client_counts = [random.randint(1000, 5000) for _ in all_governorates]
    map_fig = px.bar(
        x=all_governorates, y=client_counts, title="Client Distribution Across Tunisia",
        color=client_counts, color_continuous_scale='Blues'
    )
    map_fig.update_layout(template='plotly_white', height=400, showlegend=False)
    branch_types = ['Main Branch', 'Sub Branch', 'ATM Only', 'Digital Point']
    branch_counts = [random.randint(5, 25) for _ in branch_types]
    branch_fig = px.pie(
        values=branch_counts, names=branch_types, title="Branch Type Distribution",
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['success']]
    )
    branch_fig.update_layout(template='plotly_white', height=400)
    return map_fig, branch_fig

# Chat functionality
@app.callback(
    Output('chat-messages', 'children'),
    Input('send-chat-button', 'n_clicks'),
    State('chat-input', 'value'),
    prevent_initial_call=True
)
def handle_chat_message(n_clicks, user_message):
    if not user_message or not user_message.strip():
        return [
            html.Div([
                html.Div("🤖", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
                html.Div("Hello! I'm your AI banking assistant. How can I help you analyze client behavior today?",
                        style={'backgroundColor': COLORS['light'], 'padding': '12px', 'borderRadius': '15px', 'flex': '1'})
            ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '15px'})
        ]
    ai_responses = {
        'market': "Based on current data, the market shows a 3.2% growth trend with strong performance in the Tunis region.",
        'client': "Client satisfaction has increased by 12% this quarter, primarily due to improved digital services.",
        'branch': "We have 156 active branches across Tunisia, with highest concentration in urban areas.",
        'revenue': "Revenue projections show continued growth, with digital channels contributing 34% of total income.",
        'default': "I can help you analyze client trends, market data, branch performance, and financial metrics. What specific area interests you?"
    }
    response_key = 'default'
    user_lower = user_message.lower()
    if any(word in user_lower for word in ['market', 'trend', 'growth']):
        response_key = 'market'
    elif any(word in user_lower for word in ['client', 'customer', 'satisfaction']):
        response_key = 'client'
    elif any(word in user_lower for word in ['branch', 'location', 'office']):
        response_key = 'branch'
    elif any(word in user_lower for word in ['revenue', 'profit', 'money', 'financial']):
        response_key = 'revenue'
    ai_response = ai_responses[response_key]
    return [
        html.Div([
            html.Div("🤖", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
            html.Div("Hello! I'm your AI banking assistant. How can I help you analyze client behavior today?",
                    style={'backgroundColor': COLORS['light'], 'padding': '12px', 'borderRadius': '15px', 'flex': '1'})
        ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '15px'}),
        html.Div([
            html.Div([
                html.Div("👤", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
                html.Div(user_message, style={
                    'backgroundColor': COLORS['primary'], 'color': 'white', 'padding': '12px', 'borderRadius': '15px', 'flex': '1', 'maxWidth': '70%'
                })
            ], style={'display': 'flex', 'alignItems': 'flex-start', 'justifyContent': 'flex-end', 'marginBottom': '15px'})
        ]),
        html.Div([
            html.Div("🤖", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
            html.Div(ai_response, style={
                'backgroundColor': COLORS['light'], 'padding': '12px', 'borderRadius': '15px', 'flex': '1', 'maxWidth': '70%',
                'border': f'1px solid {COLORS["hover"]}'
            })
        ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '15px'})
    ]

# Clear chat input after sending
@app.callback(
    Output('chat-input', 'value'),
    Input('send-chat-button', 'n_clicks'),
    prevent_initial_call=True
)
def clear_chat_input(n_clicks):
    return ""

# -------------------- APP RUN ------------------------

if __name__ == "__main__":
    print("🏦 MODERN BANK DASHBOARD - SELF CONTAINED VERSION")
    print("=" * 60)
    print("🚀 Starting Modern Bank Dashboard...")
    print("🌐 Dashboard URL: http://localhost:8050")
    print("🎯 Features: Multi-page navigation, AI Chat, Economic & Geographic Analysis")
    print("📊 Modern sidebar design with beautiful UI!")
    print("-" * 60)
    app.run(debug=True, host='0.0.0.0', port=8050)
