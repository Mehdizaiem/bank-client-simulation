"""
Fixed Home Page - Guaranteed 2 Charts Per Row
Replace the chart section in pages/home.py
"""
import json
import pandas as pd
from pathlib import Path
from dash import html, dcc
from config.colors import COLORS

def create_real_data_charts_section():
    """Create charts section with guaranteed 2 charts per row using inline styles"""
    return html.Div([
        html.H3(
            children=[
                html.I(className="fas fa-chart-pie", style={'marginRight': '8px', 'color': COLORS['primary']}),
                "Portfolio Analytics"
            ],
            style={
                'fontSize': 'clamp(1.2rem, 3vw, 1.4rem)',
                'fontWeight': '600',
                'color': COLORS['dark'],
                'marginBottom': '20px',
                'display': 'flex',
                'alignItems': 'center'
            }
        ),

        # Row 1: Geographic Distribution + Client Segment Mix
        html.Div([
            create_chart_container(
                "governorate-distribution-chart",
                "Geographic Distribution",
                "Client distribution across Tunisia governorates"
            ),
            create_chart_container(
                "client-type-pie-chart",
                "Client Segment Mix",
                "Retail vs Corporate client distribution"
            )
        ], style={
            'display': 'flex',
            'gap': '20px',
            'marginBottom': '20px',
            'width': '100%',
            'flexWrap': 'wrap'
        }),

        # Row 2: Satisfaction Distribution + Channel Preferences
        html.Div([
            create_chart_container(
                "satisfaction-tiers-chart", 
                "Satisfaction Distribution",
                "Customer satisfaction level breakdown"
            ),
            create_chart_container(
                "channel-usage-chart",
                "Channel Preferences", 
                "Digital vs traditional channel usage"
            )
        ], style={
            'display': 'flex',
            'gap': '20px',
            'marginBottom': '20px',
            'width': '100%',
            'flexWrap': 'wrap'
        }),

        # Row 3: Age Demographics + Value Segmentation
        html.Div([
            create_chart_container(
                "age-demographics-chart",
                "Age Demographics", 
                "Age group distribution with digital adoption"
            ),
            create_chart_container(
                "value-tiers-chart",
                "Value Segmentation",
                "Premium, standard, and basic client tiers"
            )
        ], style={
            'display': 'flex',
            'gap': '20px',
            'marginBottom': '20px',
            'width': '100%',
            'flexWrap': 'wrap'
        })
    ])

def create_chart_container(chart_id, title, subtitle):
    """Create a chart container with forced 50% width"""
    return html.Div([
        html.Div([
            html.H4(title, style={
                'fontSize': 'clamp(1rem, 2.5vw, 1.1rem)',
                'fontWeight': '600',
                'color': COLORS['dark'],
                'marginBottom': '5px'
            }),
            html.P(subtitle, style={
                'fontSize': 'clamp(0.75rem, 2vw, 0.85rem)',
                'color': COLORS['secondary'],
                'marginBottom': '15px',
                'lineHeight': '1.4'
            })
        ]),
        dcc.Graph(
            id=chart_id, 
            config={'displayModeBar': False, 'responsive': True},
            style={'height': '350px', 'width': '100%'}
        )
    ], style={
        'flex': '1',
        'minWidth': '300px',
        'maxWidth': 'calc(50% - 10px)',
        'width': 'calc(50% - 10px)',
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 12px rgba(0,0,0,0.08)',
        'transition': 'all 0.3s ease',
        'boxSizing': 'border-box'
    })

def create_simulation_control_panel():
    """Create compact simulation control panel"""
    return html.Div([
        html.H3(
            children=[
                html.I(className="fas fa-sliders-h", style={'marginRight': '8px', 'color': COLORS['primary']}),
                "Simulation Controls"
            ],
            style={
                'fontSize': 'clamp(1.2rem, 3vw, 1.4rem)',
                'fontWeight': '600',
                'color': COLORS['dark'],
                'marginBottom': '20px',
                'textAlign': 'center',
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center'
            }
        ),
        
        # Single row for all simulation controls using flexbox
        html.Div([
            # Agent Configuration
            html.Div([
                html.H4(
                    children=[html.I(className="fas fa-users", style={'marginRight': '6px'}), "Agent Setup"],
                    style=create_column_header_style()
                ),
                html.Div([
                    html.Label("Agents:", style=create_compact_label_style()),
                    dcc.Input(
                        id='agent-count-input',
                        type='number',
                        value=1000,
                        min=100,
                        max=2000,
                        step=100,
                        style=create_compact_input_style()
                    )
                ], style={'marginBottom': '15px'}),
                
                html.Div([
                    html.Label("Retail/Corporate:", style=create_compact_label_style()),
                    html.Div(id="retail-ratio-display", style={'fontSize': '0.85rem', 'marginBottom': '5px', 'color': COLORS['primary']}),
                    dcc.Slider(
                        id='retail-ratio-slider',
                        min=0.5,
                        max=0.9,
                        step=0.1,
                        value=0.8,
                        marks={0.5: '50%', 0.7: '70%', 0.9: '90%'},
                        tooltip={"placement": "bottom", "always_visible": False}
                    )
                ])
            ], style={'flex': '1', 'padding': '15px', 'textAlign': 'center'}),
            
            # Parameters
            html.Div([
                html.H4(
                    children=[html.I(className="fas fa-cogs", style={'marginRight': '6px'}), "Parameters"],
                    style=create_column_header_style()
                ),
                html.Div([
                    html.Label("Steps:", style=create_compact_label_style()),
                    dcc.Input(
                        id='time-steps-input',
                        type='number',
                        value=100,
                        min=10,
                        max=500,
                        step=10,
                        style=create_compact_input_style()
                    )
                ], style={'marginBottom': '15px'}),
                
                html.Div([
                    html.Label("Seed (optional):", style=create_compact_label_style()),
                    dcc.Input(
                        id='seed-input',
                        type='number',
                        value=None,
                        placeholder="Random",
                        min=0,
                        max=999999,
                        style=create_compact_input_style()
                    )
                ])
            ], style={'flex': '1', 'padding': '15px', 'textAlign': 'center'}),
            
            # Scenario
            html.Div([
                html.H4(
                    children=[html.I(className="fas fa-project-diagram", style={'marginRight': '6px'}), "Scenario"],
                    style=create_column_header_style()
                ),
                dcc.RadioItems(
                    id='scenario-selector',
                    options=[
                        {'label': [html.I(className="fas fa-balance-scale", style={'marginRight': '6px'}), "Normal"], 'value': 'normal'},
                        {'label': [html.I(className="fas fa-laptop", style={'marginRight': '6px'}), "Digital"], 'value': 'digital'},
                        {'label': [html.I(className="fas fa-chart-line", style={'marginRight': '6px'}), "Downturn"], 'value': 'downturn'},
                        {'label': [html.I(className="fas fa-bullhorn", style={'marginRight': '6px'}), "Marketing"], 'value': 'marketing'},
                        {'label': [html.I(className="fas fa-concierge-bell", style={'marginRight': '6px'}), "Service"], 'value': 'service'}
                    ],
                    value='normal',
                    labelStyle={'display': 'block', 'marginBottom': '5px', 'fontSize': '0.85rem'},
                    style={'textAlign': 'left'}
                )
            ], style={'flex': '1', 'padding': '15px'}),
            
            # Actions
            html.Div([
                html.H4(
                    children=[html.I(className="fas fa-mouse-pointer", style={'marginRight': '6px'}), "Actions"],
                    style=create_column_header_style()
                ),
                html.Div([
                    html.Button([
                        html.I(className="fas fa-rocket", style={'marginRight': '6px'}),
                        "Run"
                    ], id="run-simulation-btn", n_clicks=0, style=create_sim_button_style(COLORS['success'])),
                    
                    html.Button([
                        html.I(className="fas fa-folder-open", style={'marginRight': '6px'}),
                        "Load"
                    ], id="load-results-btn", n_clicks=0, style=create_sim_button_style(COLORS['primary'])),
                    
                    html.Button([
                        html.I(className="fas fa-redo", style={'marginRight': '6px'}),
                        "Reset"
                    ], id="reset-simulation-btn", n_clicks=0, style=create_sim_button_style(COLORS['secondary']))
                ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '8px'})
            ], style={'flex': '1', 'padding': '15px'})
            
        ], style={
            'display': 'flex',
            'width': '100%',
            'backgroundColor': '#f8fafc',
            'borderRadius': '8px',
            'border': '1px solid #e5e7eb',
            'flexWrap': 'wrap',
            'gap': '10px'
        })
        
    ], style={
        'backgroundColor': 'white',
        'padding': '25px',
        'borderRadius': '12px',
        'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
        'marginBottom': '25px',
        'width': '100%',
        'maxWidth': '100%'
    })

# Helper functions for styling
def create_column_header_style():
    return {
        'fontSize': '1rem',
        'fontWeight': '600',
        'color': COLORS['dark'],
        'marginBottom': '15px',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'gap': '6px'
    }

def create_compact_input_style():
    return {
        'width': '100%',
        'maxWidth': '120px',
        'padding': '6px 8px',
        'borderRadius': '4px',
        'border': f'1px solid {COLORS["secondary"]}',
        'fontSize': '0.9rem'
    }

def create_compact_label_style():
    return {
        'fontWeight': 'bold',
        'display': 'block',
        'marginBottom': '5px',
        'fontSize': '0.85rem',
        'color': COLORS['dark']
    }

def create_sim_button_style(bg_color):
    return {
        'width': '100%',
        'padding': '8px 12px',
        'backgroundColor': bg_color,
        'color': 'white',
        'border': 'none',
        'borderRadius': '6px',
        'fontWeight': '600',
        'cursor': 'pointer',
        'fontSize': '0.9rem',
        'transition': 'all 0.3s ease'
    }

# Keep the rest of the home.py functions unchanged...
def load_data():
    """Load data from various sources"""
    data = {
        'bundle': None,
        'retail_training': None,
        'corporate_training': None,
        'agents_enhanced': None,
        'simulation_results': None
    }
    
    try:
        bundle_path = Path('output/dashboard_exports/dashboard_bundle_enhanced.json')
        if bundle_path.exists():
            with open(bundle_path, 'r') as f:
                data['bundle'] = json.load(f)
    except:
        pass
    
    try:
        retail_path = Path('retail_training_data_20250807_154910.csv')
        if retail_path.exists():
            data['retail_training'] = pd.read_csv(retail_path)
    except:
        pass
    
    return data

def get_current_kpis(data):
    """Extract current KPIs from loaded data"""
    if data['bundle'] and 'quick_stats' in data['bundle']:
        stats = data['bundle']['quick_stats']['headline_numbers']
        return {
            'total_clients': stats.get('total_clients', 0),
            'active_clients': stats.get('active_clients', 0), 
            'satisfaction_score': stats.get('satisfaction_score', 0),
            'digital_adoption': stats.get('digital_adoption', 0),
            'retention_rate': stats.get('retention_rate', 0)
        }
    
    return {
        'total_clients': 1000,
        'active_clients': 1000,
        'satisfaction_score': 62.6,
        'digital_adoption': 47.0,
        'retention_rate': 100.0
    }

def create_simulation_homepage_content():
    """Create the main homepage content"""
    return html.Div([
        create_header_section(),
        create_real_data_charts_section(),
        create_simulation_control_panel(),
        html.Div(id="simulation-status-display", style={'marginBottom': '20px'}),
        create_simulation_results_section()
    ], style={
        'width': '100%',
        'maxWidth': '100%',
        'overflow': 'hidden'
    })

def create_header_section():
    """Create the header section"""
    return html.Div([
        html.H2("Bank Client Simulation Platform - Tunisia", style={
            'fontSize': 'clamp(1.5rem, 4vw, 2.2rem)',
            'fontWeight': '700', 
            'color': COLORS['dark'], 
            'marginBottom': '10px'
        }),
        html.P("Agent-based simulation of retail and corporate banking clients across Tunisia", style={
            'fontSize': 'clamp(0.9rem, 2vw, 1.1rem)', 
            'color': COLORS['dark'], 
            'opacity': '0.7', 
            'marginBottom': '25px'
        }),
        html.Div([
            html.Div([
                html.I(className="fas fa-database", style={'color': COLORS['primary'], 'marginRight': '6px'}),
                html.Span("Data Source: ", style={'fontWeight': 'bold'}),
                html.Span(id="data-source-info", children="Loading...", style={'color': COLORS['primary']})
            ], style={'display': 'inline-block', 'marginRight': '30px', 'marginBottom': '10px'}),
            
            html.Div([
                html.I(className="fas fa-map-marker-alt", style={'color': COLORS['success'], 'marginRight': '6px'}),
                html.Span("Coverage: ", style={'fontWeight': 'bold'}),
                html.Span(id="coverage-info", children="12 Governorates", style={'color': COLORS['success']})
            ], style={'display': 'inline-block', 'marginRight': '30px', 'marginBottom': '10px'}),
            
            html.Div([
                html.I(className="fas fa-bolt", style={'color': COLORS['secondary'], 'marginRight': '6px'}),
                html.Span("Engine: ", style={'fontWeight': 'bold'}),
                html.Span("Mesa 3.x Agent-Based Model", style={'color': COLORS['secondary']})
            ], style={'display': 'inline-block', 'marginBottom': '10px'})
        ], style={
            'marginBottom': '20px', 
            'fontSize': '0.95rem',
            'display': 'flex',
            'flexWrap': 'wrap',
            'gap': '10px'
        })
    ])

def create_simulation_results_section():
    """Create the simulation results display section"""
    return html.Div(id="simulation-results-container", children=[
        # Populated by callbacks when simulation runs
    ], style={'marginTop': '25px'})

# Export for compatibility
def create_homepage_content():
    """Legacy function name for compatibility"""
    return create_simulation_homepage_content()
