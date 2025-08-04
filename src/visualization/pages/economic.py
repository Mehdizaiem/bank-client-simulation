"""
Economic analysis page layout and components
"""
from dash import html, dcc
from config.colors import COLORS


def create_economic_header():
    """Create the economic analysis page header."""
    return html.H2("Economic Analysis Dashboard", style={
        'fontSize': '2rem', 
        'fontWeight': '700', 
        'color': COLORS['dark'], 
        'marginBottom': '20px'
    })


def create_economic_control_panel():
    """Create control panel for economic analysis."""
    return html.Div([
        # Filter dropdown
        html.Div([
            html.Label("Time Period:", style={
                'marginRight': '8px', 
                'fontWeight': 'bold'
            }),
            dcc.Dropdown(
                id='economic-time-filter',
                options=[
                    {'label': 'Last 6 Months', 'value': '6m'},
                    {'label': 'Last Year', 'value': '1y'},
                    {'label': 'Last 2 Years', 'value': '2y'},
                    {'label': 'All Time', 'value': 'all'}
                ],
                value='6m',
                clearable=False,
                style={'width': '140px', 'display': 'inline-block'}
            ),
        ], style={'display': 'inline-block', 'marginRight': '24px'}),
        
        # Indicator type dropdown
        html.Div([
            html.Label("Indicators:", style={
                'marginRight': '8px', 
                'fontWeight': 'bold'
            }),
            dcc.Dropdown(
                id='economic-indicator-filter',
                options=[
                    {'label': 'All Indicators', 'value': 'all'},
                    {'label': 'Growth Metrics', 'value': 'growth'},
                    {'label': 'Risk Metrics', 'value': 'risk'},
                    {'label': 'Market Metrics', 'value': 'market'}
                ],
                value='all',
                clearable=False,
                style={'width': '140px', 'display': 'inline-block'}
            ),
        ], style={'display': 'inline-block', 'marginRight': '24px'}),
        
        # Export buttons
        html.Button("Export Analysis", id="economic-export-btn", n_clicks=0, style={
            'padding': '10px 20px', 
            'backgroundColor': COLORS['primary'], 
            'color': 'white', 
            'border': 'none',
            'borderRadius': '6px', 
            'fontWeight': '600', 
            'cursor': 'pointer'
        })
    ], style={
        'marginBottom': '20px', 
        'display': 'flex', 
        'alignItems': 'center'
    })


def create_economic_charts():
    """Create the economic charts section."""
    return html.Div([
        html.Div([
            dcc.Graph(id="economic-trends-chart")
        ], style={
            'width': '48%', 
            'display': 'inline-block',
            'backgroundColor': 'white',
            'borderRadius': '12px',
            'boxShadow': '0 2px 12px rgba(0,0,0,0.1)',
            'padding': '15px',
            'margin': '10px'
        }),
        html.Div([
            dcc.Graph(id="market-indicators-chart")
        ], style={
            'width': '48%', 
            'display': 'inline-block', 
            'marginLeft': '4%',
            'backgroundColor': 'white',
            'borderRadius': '12px',
            'boxShadow': '0 2px 12px rgba(0,0,0,0.1)',
            'padding': '15px',
            'margin': '10px'
        })
    ])


def create_economic_insights():
    """Create economic insights section."""
    return html.Div([
        html.H3("Key Economic Insights", style={
            'fontSize': '1.5rem',
            'fontWeight': '600',
            'color': COLORS['dark'],
            'marginBottom': '15px'
        }),
        html.Div([
            html.Div([
                html.H4("Market Growth", style={'color': COLORS['success']}),
                html.P("Economic indicators show positive growth trajectory with stable fundamentals.")
            ], style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                'margin': '10px',
                'borderLeft': f'4px solid {COLORS["success"]}'
            }),
            html.Div([
                html.H4("Risk Assessment", style={'color': COLORS['warning']}),
                html.P("Moderate risk levels detected in certain sectors, monitoring recommended.")
            ], style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                'margin': '10px',
                'borderLeft': f'4px solid {COLORS["warning"]}'
            })
        ], style={'display': 'flex', 'gap': '20px'})
    ], style={'marginTop': '30px'})


def create_economic_content():
    """Create the complete economic analysis page content."""
    return html.Div([
        create_economic_header(),
        create_economic_control_panel(),
        create_economic_charts(),
        create_economic_insights()
    ])