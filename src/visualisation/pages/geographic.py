"""
Single Simulation Geographic Analysis Page
Icon-polished version using Font Awesome
"""
from dash import html, dcc
from config.colors import COLORS

def create_geographic_simulation_content():
    """Create single simulation page with comprehensive results"""
    return html.Div([
        create_page_header(),
        create_simulation_configuration_section(),
        create_comprehensive_results_section()
    ])

def create_page_header():
    """Simple page header"""
    return html.Div([
        html.H1([
            html.I(className="fas fa-chart-line", style={'marginRight': '10px', 'color': COLORS['primary']}),
            "Banking Simulation Analysis"
        ], style={
            'fontSize': '2.2rem',
            'fontWeight': '700',
            'color': COLORS['dark'],
            'textAlign': 'center',
            'marginBottom': '10px',
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center'
        }),
        html.P([
            html.I(className="fas fa-tools", style={'marginRight': '8px', 'color': COLORS['secondary']}),
            "Configure and run comprehensive banking simulation with complete analysis"
        ], style={
            'fontSize': '1.1rem',
            'color': COLORS['secondary'],
            'textAlign': 'center',
            'marginBottom': '30px',
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center'
        })
    ])

def create_simulation_configuration_section():
    """Single simulation configuration section"""
    return html.Div([
        html.H2([
            html.I(className="fas fa-sliders-h", style={'marginRight': '10px', 'color': COLORS['primary']}),
            "Simulation Configuration"
        ], style=create_section_header_style()),
        
        html.Div([
            # Main configuration
            html.Div([
                html.H4([
                    html.I(className="fas fa-cogs", style={'marginRight': '8px', 'color': COLORS['secondary']}),
                    "Simulation Parameters"
                ], style={'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center'}),

                html.Div([
                    html.Div([
                        html.Label([
                            html.I(className="fas fa-users", style={'marginRight': '6px'}),
                            "Number of Agents:"
                        ], style=create_label_style()),
                        dcc.Input(
                            id='sim-num-agents',
                            type='number',
                            value=800,
                            min=100,
                            max=2000,
                            step=100,
                            style=create_input_style()
                        )
                    ], style={'flex': '1', 'marginRight': '20px'}),
                    
                    html.Div([
                        html.Label([
                            html.I(className="fas fa-balance-scale", style={'marginRight': '6px'}),
                            "Retail Client Ratio:"
                        ], style=create_label_style()),
                        dcc.Slider(
                            id='sim-retail-ratio',
                            min=0.5,
                            max=0.9,
                            step=0.05,
                            value=0.75,
                            marks={0.5: '50%', 0.6: '60%', 0.7: '70%', 0.8: '80%', 0.9: '90%'},
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], style={'flex': '1', 'marginRight': '20px'}),
                    
                    html.Div([
                        html.Label([
                            html.I(className="fas fa-hourglass-half", style={'marginRight': '6px'}),
                            "Simulation Steps:"
                        ], style=create_label_style()),
                        dcc.Input(
                            id='sim-time-steps',
                            type='number',
                            value=100,
                            min=50,
                            max=500,
                            step=50,
                            style=create_input_style()
                        )
                    ], style={'flex': '1'})
                ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px', 'flexWrap': 'wrap'}),

                html.Div([
                    html.Div([
                        html.Label([
                            html.I(className="fas fa-project-diagram", style={'marginRight': '6px'}),
                            "Market Scenario:"
                        ], style=create_label_style()),
                        dcc.Dropdown(
                            id='sim-scenario',
                            options=[
                                {'label': 'Normal Market Conditions', 'value': 'normal'},
                                {'label': 'Digital Transformation Focus', 'value': 'digital'},
                                {'label': 'Economic Downturn', 'value': 'downturn'},
                                {'label': 'Marketing Campaign Active', 'value': 'marketing'},
                                {'label': 'Service Quality Initiative', 'value': 'service'}
                            ],
                            value='normal',
                            clearable=False,
                            style={'marginBottom': '15px'}
                        )
                    ], style={'flex': '1', 'marginRight': '20px'}),
                    
                    html.Div([
                        html.Label([
                            html.I(className="fas fa-map-marker-alt", style={'marginRight': '6px'}),
                            "Target Region (Optional):"
                        ], style=create_label_style()),
                        dcc.Dropdown(
                            id='sim-target-region',
                            options=[
                                {'label': 'All Regions', 'value': ''},
                                {'label': 'Tunis', 'value': 'tunis'},
                                {'label': 'Sfax', 'value': 'sfax'},
                                {'label': 'Sousse', 'value': 'sousse'},
                                {'label': 'Ariana', 'value': 'ariana'},
                                {'label': 'Bizerte', 'value': 'bizerte'},
                                {'label': 'Kairouan', 'value': 'kairouan'}
                            ],
                            value='',
                            placeholder="Select specific region or leave for all"
                        )
                    ], style={'flex': '1', 'marginRight': '20px'}),
                    
                    html.Div([
                        html.Label([
                            html.I(className="fas fa-user-tag", style={'marginRight': '6px'}),
                            "Target Segment (Optional):"
                        ], style=create_label_style()),
                        dcc.Dropdown(
                            id='sim-target-segment',
                            options=[
                                {'label': 'All Segments', 'value': ''},
                                {'label': 'Premium', 'value': 'premium'},
                                {'label': 'Corporate', 'value': 'corporate'},
                                {'label': 'Standard', 'value': 'standard'},
                                {'label': 'Basic', 'value': 'basic'}
                            ],
                            value='',
                            placeholder="Select specific segment or leave for all"
                        )
                    ], style={'flex': '1'})
                ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '25px', 'flexWrap': 'wrap'})
            ], style={'flex': '2', 'marginRight': '30px'}),
            
            # Simulation status and action
            html.Div([
                html.H4([
                    html.I(className="fas fa-play-circle", style={'marginRight': '8px', 'color': COLORS['primary']}),
                    "Simulation Control"
                ], style={'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center'}),
                
                html.Button([
                    html.I(className="fas fa-rocket", style={'marginRight': '8px'}),
                    "Run Complete Simulation"
                ],
                    id="run-complete-simulation-btn",
                    n_clicks=0,
                    style={
                        'width': '100%',
                        'padding': '15px',
                        'backgroundColor': COLORS['primary'],
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '8px',
                        'fontSize': '1.1rem',
                        'fontWeight': '600',
                        'cursor': 'pointer',
                        'marginBottom': '20px'
                    }
                ),
                
                html.Div(
                    id="simulation-execution-status",
                    children=[
                        html.P([
                            html.I(className="fas fa-info-circle", style={'marginRight': '6px'}),
                            "Ready to run simulation"
                        ], style={'textAlign': 'center', 'color': COLORS['secondary']})
                    ],
                    style={'minHeight': '100px', 'padding': '15px', 'backgroundColor': '#f8fafc', 'borderRadius': '8px'}
                )
            ], style={'flex': '1'})
        ], style={'display': 'flex', 'flexWrap': 'wrap'})
        
    ], style=create_section_style())

def create_comprehensive_results_section():
    """Comprehensive results section showing all simulation outputs"""
    return html.Div([
        html.H2([
            html.I(className="fas fa-chart-bar", style={'marginRight': '10px', 'color': COLORS['primary']}),
            "Simulation Results & Analysis"
        ], style=create_section_header_style()),
        
        # Executive Summary KPIs (appears first)
        html.Div([
            html.H3([
                html.I(className="fas fa-clipboard-list", style={'marginRight': '8px'}),
                "Executive Summary"
            ], style={'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center'}),
            html.Div(id="executive-kpi-cards", children=[
                html.P([
                    html.I(className="fas fa-tachometer-alt", style={'marginRight': '6px'}),
                    "Run simulation to see executive KPIs"
                ], style={'textAlign': 'center', 'padding': '40px', 'color': COLORS['secondary']})
            ])
        ], style=create_subsection_style()),
        
        # Core Metrics Over Time (Time Series Charts)
        html.Div([
            html.H3([
                html.I(className="fas fa-history", style={'marginRight': '8px'}),
                "Performance Metrics Over Time"
            ], style={'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center'}),
            html.Div([
                html.Div([
                    dcc.Graph(id="satisfaction-timeline", style={'height': '300px'})
                ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                html.Div([
                    dcc.Graph(id="churn-retention-timeline", style={'height': '300px'})
                ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'})
            ]),
            html.Div([
                html.Div([
                    dcc.Graph(id="digital-adoption-timeline", style={'height': '300px'})
                ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                html.Div([
                    dcc.Graph(id="business-metrics-timeline", style={'height': '300px'})
                ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'})
            ])
        ], style=create_subsection_style()),
        
        # Channel Insights (text)
        html.Div([
            html.H3([
                html.I(className="fas fa-network-wired", style={'marginRight': '8px'}),
                "Channel Insights"
            ], style={'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center'}),
            html.Div(id="channel-insights-text")
        ], style=create_subsection_style()),
        
        # Regional Analysis
        html.Div([
            html.H3([
                html.I(className="fas fa-map", style={'marginRight': '8px'}),
                "Regional Performance Analysis"
            ], style={'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center'}),
            html.Div([
                html.Div([
                    dcc.Graph(id="regional-performance-chart", style={'height': '400px'})
                ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                html.Div([
                    html.H4([
                        html.I(className="fas fa-trophy", style={'marginRight': '6px'}),
                        "Top Performing Regions"
                    ], style={'marginBottom': '15px', 'display': 'flex', 'alignItems': 'center'}),
                    html.Div(id="regional-rankings")
                ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px', 'verticalAlign': 'top'})
            ])
        ], style=create_subsection_style()),
        
        # ROI and Financial Analysis
        html.Div([
            html.H3([
                html.I(className="fas fa-coins", style={'marginRight': '8px'}),
                "Financial Impact Analysis"
            ], style={'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center'}),
            html.Div([
                html.Div([
                    html.H4([
                        html.I(className="fas fa-chart-line", style={'marginRight': '6px'}),
                        "ROI Projections"
                    ], style={'marginBottom': '15px', 'display': 'flex', 'alignItems': 'center'}),
                    html.Div(id="roi-analysis-display")
                ], style={'width': '50%', 'display': 'inline-block', 'paddingRight': '10px', 'verticalAlign': 'top'}),
                html.Div([
                    html.H4([
                        html.I(className="fas fa-balance-scale", style={'marginRight': '6px'}),
                        "Cost-Benefit Analysis"
                    ], style={'marginBottom': '15px', 'display': 'flex', 'alignItems': 'center'}),
                    html.Div(id="cost-benefit-display")
                ], style={'width': '50%', 'display': 'inline-block', 'paddingLeft': '10px', 'verticalAlign': 'top'})
            ])
        ], style=create_subsection_style()),
        
        # Client Segmentation Analysis
        html.Div([
            html.H3([
                html.I(className="fas fa-users-cog", style={'marginRight': '8px'}),
                "Client Segmentation Analysis"
            ], style={'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center'}),
            html.Div([
                html.Div([
                    dcc.Graph(id="client-segmentation-chart", style={'height': '350px'})
                ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                html.Div([
                    dcc.Graph(id="satisfaction-by-segment-chart", style={'height': '350px'})
                ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'})
            ])
        ], style=create_subsection_style()),
        
        # Alerts and Recommendations
        html.Div([
            html.H3([
                html.I(className="fas fa-bell", style={'marginRight': '8px'}),
                "Strategic Alerts & Recommendations"
            ], style={'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center'}),
            html.Div([
                html.Div([
                    html.H4([
                        html.I(className="fas fa-exclamation-triangle", style={'marginRight': '6px', 'color': COLORS['warning']}),
                        "System Alerts"
                    ], style={'color': COLORS['warning'], 'marginBottom': '15px', 'display': 'flex', 'alignItems': 'center'}),
                    html.Div(id="simulation-alerts")
                ], style={'width': '50%', 'display': 'inline-block', 'paddingRight': '10px', 'verticalAlign': 'top'}),
                html.Div([
                    html.H4([
                        html.I(className="fas fa-lightbulb", style={'marginRight': '6px', 'color': COLORS['primary']}),
                        "Strategic Recommendations"
                    ], style={'color': COLORS['primary'], 'marginBottom': '15px', 'display': 'flex', 'alignItems': 'center'}),
                    html.Div(id="strategic-recommendations")
                ], style={'width': '50%', 'display': 'inline-block', 'paddingLeft': '10px', 'verticalAlign': 'top'})
            ])
        ], style=create_subsection_style()),
        
        # Summary Statistics Table
        html.Div([
            html.H3([
                html.I(className="fas fa-table", style={'marginRight': '8px'}),
                "Detailed Summary Statistics"
            ], style={'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center'}),
            html.Div(id="summary-statistics-table")
        ], style=create_subsection_style())
        
    ], style=create_section_style())

# Helper functions for styling

def create_section_header_style():
    """Section header style"""
    return {
        'fontSize': '1.6rem',
        'fontWeight': '600',
        'color': COLORS['dark'],
        'borderBottom': f'3px solid {COLORS["primary"]}',
        'paddingBottom': '10px',
        'marginBottom': '25px',
        'display': 'flex',
        'alignItems': 'center'
    }

def create_section_style():
    """Main section style"""
    return {
        'backgroundColor': 'white',
        'padding': '30px',
        'borderRadius': '12px',
        'boxShadow': '0 4px 15px rgba(0,0,0,0.08)',
        'marginBottom': '30px'
    }

def create_subsection_style():
    """Subsection style"""
    return {
        'padding': '25px',
        'backgroundColor': '#f8fafc',
        'borderRadius': '10px',
        'marginBottom': '25px',
        'border': f'1px solid {COLORS["primary"]}20'
    }

def create_label_style():
    """Input label style"""
    return {
        'fontWeight': 'bold',
        'marginBottom': '8px',
        'display': 'block',
        'color': COLORS['dark']
    }

def create_input_style():
    """Input field style"""
    return {
        'width': '100%',
        'padding': '10px',
        'borderRadius': '6px',
        'border': '2px solid #e5e7eb',
        'fontSize': '1rem'
    }
