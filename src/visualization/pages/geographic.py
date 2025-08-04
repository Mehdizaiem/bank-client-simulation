"""
Geographic analysis page layout and components
"""
from dash import html, dcc
from config.colors import COLORS


def create_geographic_header():
    """Create the geographic analysis page header."""
    return html.H2("Geographic Analysis Dashboard", style={
        'fontSize': '2rem', 
        'fontWeight': '700', 
        'color': COLORS['dark'], 
        'marginBottom': '20px'
    })


def create_geographic_control_panel():
    """Create control panel for geographic analysis."""
    return html.Div([
        # Region filter
        html.Div([
            html.Label("Region:", style={
                'marginRight': '8px', 
                'fontWeight': 'bold'
            }),
            dcc.Dropdown(
                id='geographic-region-filter',
                options=[
                    {'label': 'All Regions', 'value': 'all'},
                    {'label': 'Northern Tunisia', 'value': 'north'},
                    {'label': 'Central Tunisia', 'value': 'central'},
                    {'label': 'Southern Tunisia', 'value': 'south'}
                ],
                value='all',
                clearable=False,
                style={'width': '140px', 'display': 'inline-block'}
            ),
        ], style={'display': 'inline-block', 'marginRight': '24px'}),
        
        # Metric type dropdown
        html.Div([
            html.Label("Metric:", style={
                'marginRight': '8px', 
                'fontWeight': 'bold'
            }),
            dcc.Dropdown(
                id='geographic-metric-filter',
                options=[
                    {'label': 'Client Count', 'value': 'clients'},
                    {'label': 'Branch Count', 'value': 'branches'},
                    {'label': 'Revenue', 'value': 'revenue'},
                    {'label': 'Market Share', 'value': 'market_share'}
                ],
                value='clients',
                clearable=False,
                style={'width': '140px', 'display': 'inline-block'}
            ),
        ], style={'display': 'inline-block', 'marginRight': '24px'}),
        
        # Export buttons
        html.Button("Export Map", id="geographic-export-btn", n_clicks=0, style={
            'padding': '10px 20px', 
            'backgroundColor': COLORS['secondary'], 
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


def create_geographic_charts():
    """Create the geographic charts section."""
    return html.Div([
        html.Div([
            dcc.Graph(id="tunisia-map")
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
            dcc.Graph(id="branch-distribution-chart")
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


def create_governorate_stats():
    """Create governorate statistics section."""
    return html.Div([
        html.H3("Governorate Performance", style={
            'fontSize': '1.5rem',
            'fontWeight': '600',
            'color': COLORS['dark'],
            'marginBottom': '15px'
        }),
        html.Div([
            # Top performers
            html.Div([
                html.H4("Top Performing Regions", style={'color': COLORS['success'], 'marginBottom': '10px'}),
                html.Div([
                    html.Div("🥇 Tunis - 3,200 clients", style={'padding': '8px', 'marginBottom': '5px'}),
                    html.Div("🥈 Sfax - 2,100 clients", style={'padding': '8px', 'marginBottom': '5px'}),
                    html.Div("🥉 Sousse - 1,850 clients", style={'padding': '8px', 'marginBottom': '5px'})
                ])
            ], style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                'margin': '10px',
                'flex': '1'
            }),
            
            # Growth opportunities
            html.Div([
                html.H4("Growth Opportunities", style={'color': COLORS['warning'], 'marginBottom': '10px'}),
                html.Div([
                    html.Div("📈 Kairouan - Emerging market", style={'padding': '8px', 'marginBottom': '5px'}),
                    html.Div("🎯 Bizerte - Untapped potential", style={'padding': '8px', 'marginBottom': '5px'}),
                    html.Div("🚀 Ariana - Rapid growth area", style={'padding': '8px', 'marginBottom': '5px'})
                ])
            ], style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                'margin': '10px',
                'flex': '1'
            })
        ], style={'display': 'flex', 'gap': '20px'})
    ], style={'marginTop': '30px'})


def create_geographic_content():
    """Create the complete geographic analysis page content."""
    return html.Div([
        create_geographic_header(),
        create_geographic_control_panel(),
        create_geographic_charts(),
        create_governorate_stats()
    ])