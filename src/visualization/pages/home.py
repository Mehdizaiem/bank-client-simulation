"""
Homepage layout and components
"""
from dash import html, dcc
from components.cards import create_metric_card
from services.data_service import DataService
from config.colors import COLORS


def create_welcome_section():
    """Create the welcome section."""
    return html.Div([
        html.H2("Welcome to Bank Client Simulation", style={
            'fontSize': '2rem', 
            'fontWeight': '700', 
            'color': COLORS['dark'], 
            'marginBottom': '10px'
        }),
        html.P("Monitor real-time client behavior and market dynamics across Tunisia", style={
            'fontSize': '1.1rem', 
            'color': COLORS['dark'], 
            'opacity': '0.7', 
            'marginBottom': '30px'
        })
    ])


def create_control_panel():
    """Create the control panel with filters and export buttons."""
    return html.Div([
        # Filter dropdown
        html.Div([
            html.Label("Filter by Segment:", style={
                'marginRight': '8px', 
                'fontWeight': 'bold'
            }),
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
            html.Label("Sort by:", style={
                'marginRight': '8px', 
                'fontWeight': 'bold'
            }),
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
            'padding': '10px 20px', 
            'backgroundColor': COLORS['primary'], 
            'color': 'white', 
            'border': 'none',
            'borderRadius': '6px', 
            'fontWeight': '600', 
            'marginRight': '8px', 
            'cursor': 'pointer'
        }),
        html.Button("Export PNG", id="home-export-png", n_clicks=0, style={
            'padding': '10px 20px', 
            'backgroundColor': COLORS['success'], 
            'color': 'white', 
            'border': 'none',
            'borderRadius': '6px', 
            'fontWeight': '600', 
            'marginRight': '8px', 
            'cursor': 'pointer'
        }),
        html.Button("Export PDF", id="home-export-pdf", n_clicks=0, style={
            'padding': '10px 20px', 
            'backgroundColor': COLORS['accent'], 
            'color': 'white', 
            'border': 'none',
            'borderRadius': '6px', 
            'fontWeight': '600', 
            'cursor': 'pointer'
        }),
        dcc.Download(id="home-csv-download")
    ], style={
        'marginBottom': '16px', 
        'display': 'flex', 
        'alignItems': 'center'
    })


def create_metrics_section():
    """Create the key metrics cards section."""
    metrics = DataService.get_key_metrics()
    colors = [COLORS['primary'], COLORS['success'], COLORS['secondary'], COLORS['accent']]
    
    cards = []
    for i, (key, metric) in enumerate(metrics.items()):
        cards.append(
            create_metric_card(
                metric['icon'],
                metric['title'],
                metric['value'],
                metric['change'],
                colors[i]
            )
        )
    
    return html.Div(cards, style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
        'gap': '20px',
        'marginBottom': '30px'
    })


def create_charts_section():
    """Create the charts grid section."""
    return html.Div([
        # Row 1: Line chart + Bar chart
        html.Div([
            html.Div(
                dcc.Graph(id="homepage-line-chart"), 
                style={
                    'width': '100%', 
                    'padding': '8px', 
                    'backgroundColor': '#fff', 
                    'borderRadius': '12px', 
                    'boxShadow': '0 2px 12px #e5e7eb'
                }
            ),
            html.Div(
                dcc.Graph(id="homepage-bar-chart"), 
                style={
                    'width': '100%', 
                    'padding': '8px', 
                    'backgroundColor': '#fff', 
                    'borderRadius': '12px', 
                    'boxShadow': '0 2px 12px #e5e7eb'
                }
            )
        ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}),

        # Row 2: Pie chart + Map chart
        html.Div([
            html.Div(
                dcc.Graph(id="homepage-pie-chart"), 
                style={
                    'width': '100%', 
                    'padding': '8px', 
                    'backgroundColor': '#fff', 
                    'borderRadius': '12px', 
                    'boxShadow': '0 2px 12px #e5e7eb'
                }
            ),
            html.Div(
                dcc.Graph(id="homepage-map-chart"), 
                style={
                    'width': '100%', 
                    'padding': '8px', 
                    'backgroundColor': '#fff', 
                    'borderRadius': '12px', 
                    'boxShadow': '0 2px 12px #e5e7eb'
                }
            )
        ], style={'display': 'flex', 'gap': '20px'})
    ], style={'width': '100%'})


def create_homepage_content():
    """Create the complete homepage content."""
    return html.Div([
        create_welcome_section(),
        create_control_panel(),
        create_metrics_section(),
        create_charts_section()
    ])