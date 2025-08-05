"""
Geographic simulation analysis page for Bank Client Simulation
"""
from dash import html, dcc
from config.colors import COLORS
from components.charts import create_geographic_charts


def create_geographic_simulation_content():
    """Create the geographic simulation page content."""
    return html.Div([
        create_geographic_simulation_header(),
        create_branch_strategy_panel(),
        create_tunisia_map_section(),
        create_geographic_insights_panel(),
        create_geographic_charts()  # Using the new charts component
    ])


def create_geographic_simulation_header():
    """Create the geographic simulation header."""
    return html.Div([
        html.H2("Geographic Simulation & Branch Strategy", style={
            'fontSize': '2rem', 
            'fontWeight': '700', 
            'color': COLORS['dark'], 
            'marginBottom': '10px'
        }),
        html.P("Simulate branch network changes and geographic expansion strategies across Tunisia", style={
            'fontSize': '1.1rem', 
            'color': COLORS['dark'], 
            'opacity': '0.7', 
            'marginBottom': '20px'
        })
    ])


def create_branch_strategy_panel():
    """Create branch strategy simulation panel."""
    return html.Div([
        html.H3("Branch Network Simulator", style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'color': COLORS['dark'],
            'marginBottom': '15px'
        }),
        html.Div([
            # Branch Action Type
            html.Div([
                html.Label("Strategy Type:", style={
                    'marginRight': '8px', 
                    'fontWeight': 'bold'
                }),
                dcc.Dropdown(
                    id='branch-strategy-type',
                    options=[
                        {'label': '🏪 Open New Branch', 'value': 'open'},
                        {'label': '🚪 Close Branch', 'value': 'close'},
                        {'label': '📍 Relocate Branch', 'value': 'relocate'},
                        {'label': '🏧 Add ATM Network', 'value': 'atm'},
                        {'label': '📱 Digital-Only Zone', 'value': 'digital'}
                    ],
                    value='open',
                    clearable=False,
                    style={'width': '180px', 'display': 'inline-block'}
                ),
            ], style={'display': 'inline-block', 'marginRight': '20px'}),
            
            # Target Location
            html.Div([
                html.Label("Governorate:", style={
                    'marginRight': '8px', 
                    'fontWeight': 'bold'
                }),
                dcc.Dropdown(
                    id='target-governorate',
                    options=[
                        {'label': 'Tunis', 'value': 'tunis'},
                        {'label': 'Ariana', 'value': 'ariana'},
                        {'label': 'Ben Arous', 'value': 'ben_arous'},
                        {'label': 'Manouba', 'value': 'manouba'},
                        {'label': 'Sfax', 'value': 'sfax'},
                        {'label': 'Sousse', 'value': 'sousse'},
                        {'label': 'Nabeul', 'value': 'nabeul'},
                        {'label': 'Bizerte', 'value': 'bizerte'},
                        {'label': 'Kairouan', 'value': 'kairouan'},
                        {'label': 'Gabès', 'value': 'gabes'},
                        {'label': 'Médenine', 'value': 'medenine'},
                        {'label': 'Monastir', 'value': 'monastir'}
                    ],
                    value='tunis',
                    clearable=False,
                    style={'width': '140px', 'display': 'inline-block'}
                ),
            ], style={'display': 'inline-block', 'marginRight': '20px'}),
            
            # Branch Type
            html.Div([
                html.Label("Branch Type:", style={
                    'marginRight': '8px', 
                    'fontWeight': 'bold'
                }),
                dcc.Dropdown(
                    id='branch-type',
                    options=[
                        {'label': 'Full Service', 'value': 'full'},
                        {'label': 'Express Branch', 'value': 'express'},
                        {'label': 'Corporate Center', 'value': 'corporate'},
                        {'label': 'Digital Hub', 'value': 'digital'}
                    ],
                    value='full',
                    clearable=False,
                    style={'width': '140px', 'display': 'inline-block'}
                ),
            ], style={'display': 'inline-block', 'marginRight': '20px'}),
            
            html.Button("🎯 Simulate Impact", id="branch-sim-btn", n_clicks=0, style={
                'padding': '12px 24px', 
                'backgroundColor': COLORS['secondary'], 
                'color': 'white', 
                'border': 'none',
                'borderRadius': '6px', 
                'fontWeight': '600', 
                'cursor': 'pointer'
            })
        ], style={'display': 'flex', 'alignItems': 'center', 'flexWrap': 'wrap', 'gap': '15px'})
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 12px rgba(0,0,0,0.1)',
        'marginBottom': '20px'
    })


def create_tunisia_map_section():
    """Create interactive Tunisia map section."""
    return html.Div([
        html.H3("Interactive Tunisia Map", style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'color': COLORS['dark'],
            'marginBottom': '15px'
        }),
        html.Div([
            # Map controls
            html.Div([
                html.Label("Map View:", style={'fontWeight': 'bold', 'marginBottom': '10px', 'display': 'block'}),
                dcc.RadioItems(
                    id='map-view-type',
                    options=[
                        {'label': ' Client Density', 'value': 'clients'},
                        {'label': ' Branch Coverage', 'value': 'branches'},
                        {'label': ' Market Penetration', 'value': 'penetration'},
                        {'label': ' Growth Potential', 'value': 'potential'}
                    ],
                    value='clients',
                    labelStyle={'display': 'block', 'marginBottom': '8px'},
                    style={'marginBottom': '15px'}
                ),
                html.Label("Overlay:", style={'fontWeight': 'bold', 'marginBottom': '10px', 'display': 'block'}),
                dcc.Checklist(
                    id='map-overlays',
                    options=[
                        {'label': ' Competitor Branches', 'value': 'competitors'},
                        {'label': ' Population Centers', 'value': 'population'},
                        {'label': ' Economic Zones', 'value': 'economic'},
                        {'label': ' Transport Hubs', 'value': 'transport'}
                    ],
                    value=['population'],
                    labelStyle={'display': 'block', 'marginBottom': '5px'}
                )
            ], style={'width': '200px', 'marginRight': '20px'}),
            
            # Interactive map
            html.Div([
                dcc.Graph(id="tunisia-interactive-map", style={'height': '500px'})
            ], style={'flex': '1'})
        ], style={'display': 'flex'})
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 12px rgba(0,0,0,0.1)',
        'marginBottom': '20px'
    })


def create_geographic_insights_panel():
    """Create geographic analysis insights."""
    return html.Div([
        html.H3("Geographic Intelligence", style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'color': COLORS['dark'],
            'marginBottom': '15px'
        }),
        html.Div([
            # Top performing regions
            html.Div([
                html.H4("🥇 Top Performing Regions", style={'color': COLORS['success'], 'marginBottom': '15px'}),
                html.Div([
                    html.Div([
                        html.Strong("Greater Tunis"),
                        html.Div("• 35,420 clients (+8.2%)", style={'fontSize': '0.9rem', 'color': COLORS['dark']}),
                        html.Div("• 89% digital adoption", style={'fontSize': '0.9rem', 'color': COLORS['success']}),
                        html.Div("• €2.1M avg. revenue/branch", style={'fontSize': '0.9rem', 'color': COLORS['primary']})
                    ], style={'marginBottom': '15px', 'padding': '10px', 'backgroundColor': COLORS['light'], 'borderRadius': '6px'}),
                    
                    html.Div([
                        html.Strong("Sfax"),
                        html.Div("• 18,950 clients (+12.1%)", style={'fontSize': '0.9rem', 'color': COLORS['dark']}),
                        html.Div("• 76% digital adoption", style={'fontSize': '0.9rem', 'color': COLORS['success']}),
                        html.Div("• €1.8M avg. revenue/branch", style={'fontSize': '0.9rem', 'color': COLORS['primary']})
                    ], style={'marginBottom': '15px', 'padding': '10px', 'backgroundColor': COLORS['light'], 'borderRadius': '6px'}),
                    
                    html.Div([
                        html.Strong("Sousse"),
                        html.Div("• 14,230 clients (+6.7%)", style={'fontSize': '0.9rem', 'color': COLORS['dark']}),
                        html.Div("• 82% digital adoption", style={'fontSize': '0.9rem', 'color': COLORS['success']}),
                        html.Div("• €1.6M avg. revenue/branch", style={'fontSize': '0.9rem', 'color': COLORS['primary']})
                    ], style={'padding': '10px', 'backgroundColor': COLORS['light'], 'borderRadius': '6px'})
                ])
            ], style={'flex': '1', 'marginRight': '20px'}),
            
            # Expansion opportunities
            html.Div([
                html.H4("🎯 Expansion Opportunities", style={'color': COLORS['warning'], 'marginBottom': '15px'}),
                html.Div([
                    html.Div([
                        html.Strong("Ariana"),
                        html.Div("• High growth potential", style={'fontSize': '0.9rem', 'color': COLORS['warning']}),
                        html.Div("• Low competition", style={'fontSize': '0.9rem', 'color': COLORS['success']}),
                        html.Div("• Young demographics", style={'fontSize': '0.9rem', 'color': COLORS['primary']}),
                        html.Div("• ROI: 18 months", style={'fontSize': '0.9rem', 'fontWeight': 'bold'})
                    ], style={'marginBottom': '15px', 'padding': '10px', 'backgroundColor': COLORS['light'], 'borderRadius': '6px'}),
                    
                    html.Div([
                        html.Strong("Bizerte"),
                        html.Div("• Emerging market", style={'fontSize': '0.9rem', 'color': COLORS['warning']}),
                        html.Div("• Industrial growth", style={'fontSize': '0.9rem', 'color': COLORS['success']}),
                        html.Div("• Corporate potential", style={'fontSize': '0.9rem', 'color': COLORS['primary']}),
                        html.Div("• ROI: 24 months", style={'fontSize': '0.9rem', 'fontWeight': 'bold'})
                    ], style={'marginBottom': '15px', 'padding': '10px', 'backgroundColor': COLORS['light'], 'borderRadius': '6px'}),
                    
                    html.Div([
                        html.Strong("Kairouan"),
                        html.Div("• Underserved region", style={'fontSize': '0.9rem', 'color': COLORS['danger']}),
                        html.Div("• Government initiatives", style={'fontSize': '0.9rem', 'color': COLORS['success']}),
                        html.Div("• Digital-first strategy", style={'fontSize': '0.9rem', 'color': COLORS['primary']}),
                        html.Div("• ROI: 30 months", style={'fontSize': '0.9rem', 'fontWeight': 'bold'})
                    ], style={'padding': '10px', 'backgroundColor': COLORS['light'], 'borderRadius': '6px'})
                ])
            ], style={'flex': '1'})
        ], style={'display': 'flex', 'gap': '20px'})
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 12px rgba(0,0,0,0.1)',
        'marginBottom': '20px'
    })


# Legacy function for compatibility
def create_geographic_content():
    """Legacy function name for compatibility."""
    return create_geographic_simulation_content()