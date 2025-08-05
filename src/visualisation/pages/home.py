"""
Homepage for Bank Client Simulation Platform
"""
from dash import html, dcc
from components.cards import create_metric_card
from components.charts import create_simulation_charts
from services.data_service import DataService
from config.colors import COLORS


def create_simulation_homepage_content():
    """Create the simulation homepage content."""
    return html.Div([
        create_welcome_section(),
        create_simulation_control_panel(),
        create_simulation_metrics(),
        create_scenario_testing_section(),
        create_simulation_charts()  # Using the new charts component
    ])


def create_welcome_section():
    """Create the simulation platform welcome section."""
    return html.Div([
        html.H2("Bank Client Simulation Platform", style={
            'fontSize': '2rem', 
            'fontWeight': '700', 
            'color': COLORS['dark'], 
            'marginBottom': '10px'
        }),
        html.P("AI-powered simulation of retail and corporate client behavior across Tunisia", style={
            'fontSize': '1.1rem', 
            'color': COLORS['dark'], 
            'opacity': '0.7', 
            'marginBottom': '30px'
        }),
        html.Div([
            html.Span("🤖 AI Agent Status: ", style={'fontWeight': 'bold'}),
            html.Span("Active", style={'color': COLORS['success'], 'fontWeight': 'bold'}),
            html.Span(" | ", style={'margin': '0 15px'}),
            html.Span("⚡ Simulation Engine: ", style={'fontWeight': 'bold'}),
            html.Span("Running", style={'color': COLORS['success'], 'fontWeight': 'bold'}),
            html.Span(" | ", style={'margin': '0 15px'}),
            html.Span("📊 Last Update: ", style={'fontWeight': 'bold'}),
            html.Span("2 minutes ago", style={'color': COLORS['primary']})
        ], style={'marginBottom': '20px', 'fontSize': '0.95rem'})
    ])


def create_simulation_control_panel():
    """Create simulation control panel."""
    return html.Div([
        html.H3("Simulation Controls", style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'color': COLORS['dark'],
            'marginBottom': '15px'
        }),
        html.Div([
            # Client Type Filter
            html.Div([
                html.Label("Client Segment:", style={
                    'marginRight': '8px', 
                    'fontWeight': 'bold'
                }),
                dcc.Dropdown(
                    id='sim-client-filter',
                    options=[
                        {'label': 'All Segments', 'value': 'all'},
                        {'label': 'Retail Clients', 'value': 'retail'},
                        {'label': 'Corporate Clients', 'value': 'corporate'},
                        {'label': 'SME', 'value': 'sme'},
                        {'label': 'High Net Worth', 'value': 'hnw'}
                    ],
                    value='all',
                    clearable=False,
                    style={'width': '160px', 'display': 'inline-block'}
                ),
            ], style={'display': 'inline-block', 'marginRight': '24px'}),
            
            # Geographic Filter
            html.Div([
                html.Label("Region:", style={
                    'marginRight': '8px', 
                    'fontWeight': 'bold'
                }),
                dcc.Dropdown(
                    id='sim-region-filter',
                    options=[
                        {'label': 'All Tunisia', 'value': 'all'},
                        {'label': 'Greater Tunis', 'value': 'tunis'},
                        {'label': 'Northern Tunisia', 'value': 'north'},
                        {'label': 'Central Tunisia', 'value': 'central'},
                        {'label': 'Southern Tunisia', 'value': 'south'}
                    ],
                    value='all',
                    clearable=False,
                    style={'width': '140px', 'display': 'inline-block'}
                ),
            ], style={'display': 'inline-block', 'marginRight': '24px'}),
            
            # Simulation Actions
            html.Button("🚀 Run New Simulation", id="sim-run-btn", n_clicks=0, style={
                'padding': '10px 20px', 
                'backgroundColor': COLORS['primary'], 
                'color': 'white', 
                'border': 'none',
                'borderRadius': '6px', 
                'fontWeight': '600', 
                'marginRight': '10px',
                'cursor': 'pointer'
            }),
            html.Button("⏸️ Pause", id="sim-pause-btn", n_clicks=0, style={
                'padding': '10px 20px', 
                'backgroundColor': COLORS['warning'], 
                'color': 'white', 
                'border': 'none',
                'borderRadius': '6px', 
                'fontWeight': '600', 
                'marginRight': '10px',
                'cursor': 'pointer'
            }),
            html.Button("📤 Export Results", id="sim-export-btn", n_clicks=0, style={
                'padding': '10px 20px', 
                'backgroundColor': COLORS['success'], 
                'color': 'white', 
                'border': 'none',
                'borderRadius': '6px', 
                'fontWeight': '600', 
                'cursor': 'pointer'
            })
        ], style={'display': 'flex', 'alignItems': 'center', 'flexWrap': 'wrap', 'gap': '10px'})
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 12px rgba(0,0,0,0.1)',
        'marginBottom': '20px'
    })


def create_simulation_metrics():
    """Create simulation metrics cards."""
    metrics = DataService.get_simulation_metrics()
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


def create_scenario_testing_section():
    """Create scenario testing interface."""
    return html.Div([
        html.H3("Scenario Testing", style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'color': COLORS['dark'],
            'marginBottom': '15px'
        }),
        html.Div([
            # Quick Scenarios
            html.Div([
                html.H4("Quick Scenarios", style={'marginBottom': '10px', 'color': COLORS['primary']}),
                html.Button("🏪 Branch Closure Impact", className="scenario-btn", style={
                    'display': 'block', 'width': '100%', 'padding': '10px', 'marginBottom': '8px',
                    'backgroundColor': 'transparent', 'border': f'1px solid {COLORS["hover"]}',
                    'borderRadius': '6px', 'cursor': 'pointer', 'textAlign': 'left'
                }),
                html.Button("💳 New Product Launch", className="scenario-btn", style={
                    'display': 'block', 'width': '100%', 'padding': '10px', 'marginBottom': '8px',
                    'backgroundColor': 'transparent', 'border': f'1px solid {COLORS["hover"]}',
                    'borderRadius': '6px', 'cursor': 'pointer', 'textAlign': 'left'
                }),
                html.Button("🏛️ Competitor Entry", className="scenario-btn", style={
                    'display': 'block', 'width': '100%', 'padding': '10px', 'marginBottom': '8px',
                    'backgroundColor': 'transparent', 'border': f'1px solid {COLORS["hover"]}',
                    'borderRadius': '6px', 'cursor': 'pointer', 'textAlign': 'left'
                }),
                html.Button("📱 Digital Campaign", className="scenario-btn", style={
                    'display': 'block', 'width': '100%', 'padding': '10px', 'marginBottom': '8px',
                    'backgroundColor': 'transparent', 'border': f'1px solid {COLORS["hover"]}',
                    'borderRadius': '6px', 'cursor': 'pointer', 'textAlign': 'left'
                })
            ], style={'flex': '1', 'marginRight': '20px'}),
            
            # Custom Scenario Builder
            html.Div([
                html.H4("Custom Scenario", style={'marginBottom': '10px', 'color': COLORS['secondary']}),
                dcc.Textarea(
                    id='custom-scenario-input',
                    placeholder='Describe your scenario: e.g., "What if we reduce fees by 20% in Sfax region?"',
                    style={
                        'width': '100%', 'height': '80px', 'padding': '10px',
                        'border': f'1px solid {COLORS["hover"]}', 'borderRadius': '6px',
                        'fontSize': '0.9rem', 'resize': 'vertical'
                    }
                ),
                html.Button("🧪 Test Custom Scenario", id="custom-scenario-btn", style={
                    'marginTop': '10px', 'padding': '10px 20px',
                    'backgroundColor': COLORS['accent'], 'color': 'white',
                    'border': 'none', 'borderRadius': '6px', 'fontWeight': '600',
                    'cursor': 'pointer'
                })
            ], style={'flex': '1'})
        ], style={'display': 'flex', 'gap': '20px'})
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 12px rgba(0,0,0,0.1)',
        'marginBottom': '30px'
    })


# Legacy function for compatibility
def create_homepage_content():
    """Legacy function name for compatibility."""
    return create_simulation_homepage_content()