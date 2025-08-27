"""
Settings page for Bank Client Simulation Platform
"""
from dash import html, dcc
from config.colors import COLORS
from components.cards import create_info_card


def create_simulation_settings_content():
    """Create the complete simulation settings content."""
    return html.Div([
        create_simulation_settings_header(),
        create_system_status_panel(),
        html.Div([
            html.Div([
                create_simulation_engine_settings(),
                create_ai_model_settings()
            ], style={'width': '48%', 'marginRight': '4%'}),
            html.Div([
                create_geographic_settings(),
                create_data_privacy_settings()
            ], style={'width': '48%'})
        ], style={'display': 'flex', 'marginBottom': '20px'}),
        create_performance_settings(),
        create_simulation_settings_actions()
    ])


def create_simulation_settings_header():
    """Create the simulation settings header."""
    return html.H2("Simulation Platform Settings", style={
        'fontSize': '2rem', 
        'fontWeight': '700', 
        'color': COLORS['dark'], 
        'marginBottom': '20px'
    })


def create_system_status_panel():
    """Create system status monitoring panel."""
    return html.Div([
        html.H3("System Status", style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'color': COLORS['dark'],
            'marginBottom': '15px'
        }),
        html.Div([
            html.Div([
                html.Div("🟢", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
                html.Div([
                    html.Strong("Simulation Engine"),
                    html.Div("Running - 50,247 active agents", style={'fontSize': '0.9rem', 'color': COLORS['success']})
                ])
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            
            html.Div([
                html.Div("🟢", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
                html.Div([
                    html.Strong("AI Models"),
                    html.Div("CTGAN & GPT-4 operational", style={'fontSize': '0.9rem', 'color': COLORS['success']})
                ])
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            
            html.Div([
                html.Div("🟡", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
                html.Div([
                    html.Strong("Data Pipeline"),
                    html.Div("Minor delays in economic data feed", style={'fontSize': '0.9rem', 'color': COLORS['warning']})
                ])
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            
            html.Div([
                html.Div("🟢", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
                html.Div([
                    html.Strong("Database"),
                    html.Div("98.7% uptime this month", style={'fontSize': '0.9rem', 'color': COLORS['success']})
                ])
            ], style={'display': 'flex', 'alignItems': 'center'})
        ])
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 12px rgba(0,0,0,0.1)',
        'marginBottom': '20px'
    })


def create_simulation_engine_settings():
    """Create simulation engine configuration settings."""
    engine_content = [
        html.Div([
            html.Label("Simulation Engine Mode:", style={
                'marginRight': '10px', 
                'fontWeight': 'bold',
                'display': 'block',
                'marginBottom': '10px'
            }),
            dcc.RadioItems(
                id='simulation-engine-mode',
                options=[
                    {'label': ' Real-time Simulation', 'value': 'realtime'},
                    {'label': ' Batch Processing', 'value': 'batch'},
                    {'label': ' Hybrid Mode', 'value': 'hybrid'}
                ],
                value='realtime',
                labelStyle={'display': 'block', 'marginBottom': '8px'}
            )
        ], style={'marginBottom': '20px'}),
        
        html.Div([
            html.Label("Agent Population Size:", style={
                'marginRight': '10px', 
                'fontWeight': 'bold',
                'display': 'block',
                'marginBottom': '10px'
            }),
            dcc.Slider(
                id='agent-population-size',
                min=1000, max=100000, step=5000, value=50000,
                marks={
                    1000: '1K',
                    25000: '25K', 
                    50000: '50K',
                    75000: '75K',
                    100000: '100K'
                },
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={'marginBottom': '20px'}),
        
        html.Div([
            html.Label("Simulation Update Frequency:", style={
                'marginRight': '10px', 
                'fontWeight': 'bold'
            }),
            dcc.Dropdown(
                id='simulation-update-frequency',
                options=[
                    {'label': 'Every 30 seconds', 'value': 30},
                    {'label': 'Every minute', 'value': 60},
                    {'label': 'Every 5 minutes', 'value': 300},
                    {'label': 'Every 15 minutes', 'value': 900}
                ],
                value=60,
                clearable=False,
                style={'width': '200px', 'display': 'inline-block'}
            )
        ])
    ]
    
    return create_info_card("Simulation Engine Configuration", engine_content, COLORS['primary'])


def create_ai_model_settings():
    """Create AI model and behavior settings."""
    ai_content = [
        html.Div([
            html.Label("AI Model Selection:", style={
                'marginRight': '10px', 
                'fontWeight': 'bold'
            }),
            dcc.Dropdown(
                id='ai-model-selection',
                options=[
                    {'label': 'CTGAN (Tabular Data)', 'value': 'ctgan'},
                    {'label': 'TVAE (Variational Autoencoder)', 'value': 'tvae'},
                    {'label': 'GPT-4 (Behavioral Enrichment)', 'value': 'gpt4'},
                    {'label': 'Arabic LLM (Local Context)', 'value': 'arabic_llm'}
                ],
                value='ctgan',
                clearable=False,
                style={'width': '250px', 'display': 'inline-block', 'marginBottom': '16px'}
            ),
        ]),
        
        html.Div([
            html.Label("Behavioral Learning Mode:", style={
                'marginRight': '10px', 
                'fontWeight': 'bold',
                'display': 'block',
                'marginBottom': '10px'
            }),
            dcc.RadioItems(
                id='behavioral-learning-mode',
                options=[
                    {'label': ' Reinforcement Learning', 'value': 'rl'},
                    {'label': ' Rule-Based Logic', 'value': 'rules'},
                    {'label': ' Hybrid Approach', 'value': 'hybrid'}
                ],
                value='hybrid',
                labelStyle={'display': 'block', 'marginBottom': '8px'}
            )
        ], style={'marginTop': '15px'}),
        
        html.Div([
            html.Label("Agent Memory Duration (days):", style={
                'marginRight': '10px', 
                'fontWeight': 'bold',
                'display': 'block',
                'marginBottom': '10px'
            }),
            dcc.Slider(
                id='agent-memory-duration',
                min=7, max=365, step=7, value=90,
                marks={7: '1W', 30: '1M', 90: '3M', 180: '6M', 365: '1Y'},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={'marginTop': '15px'})
    ]
    
    return create_info_card("AI Model & Behavior Configuration", ai_content, COLORS['secondary'])


def create_geographic_settings():
    """Create geographic and regional settings."""
    geo_content = [
        html.Div([
            html.Label("Default Geographic Scope:", style={
                'marginRight': '10px', 
                'fontWeight': 'bold'
            }),
            dcc.Dropdown(
                id='default-geographic-scope',
                options=[
                    {'label': 'All Tunisia', 'value': 'all_tunisia'},
                    {'label': 'Greater Tunis Only', 'value': 'greater_tunis'},
                    {'label': 'Northern Regions', 'value': 'north'},
                    {'label': 'Coastal Cities', 'value': 'coastal'},
                    {'label': 'Custom Selection', 'value': 'custom'}
                ],
                value='all_tunisia',
                clearable=False,
                style={'width': '200px', 'display': 'inline-block', 'marginBottom': '16px'}
            ),
        ]),
        
        html.Div([
            html.Label("Governorates to Include:", style={
                'marginRight': '10px', 
                'fontWeight': 'bold',
                'display': 'block',
                'marginBottom': '10px'
            }),
            dcc.Checklist(
                id='included-governorates',
                options=[
                    {'label': ' Tunis', 'value': 'tunis'},
                    {'label': ' Ariana', 'value': 'ariana'},
                    {'label': ' Ben Arous', 'value': 'ben_arous'},
                    {'label': ' Sfax', 'value': 'sfax'},
                    {'label': ' Sousse', 'value': 'sousse'},
                    {'label': ' Nabeul', 'value': 'nabeul'},
                    {'label': ' Bizerte', 'value': 'bizerte'},
                    {'label': ' Kairouan', 'value': 'kairouan'}
                ],
                value=['tunis', 'ariana', 'sfax', 'sousse'],
                labelStyle={'display': 'inline-block', 'marginRight': '15px', 'marginBottom': '5px'}
            )
        ], style={'marginTop': '15px'}),
        
        html.Div([
            html.Label("Map Visualization Provider:", style={
                'marginRight': '10px', 
                'fontWeight': 'bold'
            }),
            dcc.Dropdown(
                id='map-provider',
                options=[
                    {'label': 'OpenStreetMap', 'value': 'osm'},
                    {'label': 'Mapbox', 'value': 'mapbox'},
                    {'label': 'Satellite View', 'value': 'satellite'}
                ],
                value='osm',
                clearable=False,
                style={'width': '180px', 'display': 'inline-block'}
            )
        ], style={'marginTop': '15px'})
    ]
    
    return create_info_card("Geographic Configuration", geo_content, COLORS['accent'])


def create_data_privacy_settings():
    """Create data privacy and compliance settings."""
    privacy_content = [
        html.Div([
            html.Label("Data Privacy Compliance:", style={
                'marginRight': '10px', 
                'fontWeight': 'bold',
                'display': 'block',
                'marginBottom': '10px'
            }),
            dcc.Checklist(
                id='privacy-compliance',
                options=[
                    {'label': ' GDPR Compliance', 'value': 'gdpr'},
                    {'label': ' Tunisia CNIL Compliance', 'value': 'cnil'},
                    {'label': ' Data Anonymization', 'value': 'anonymization'},
                    {'label': ' Synthetic Data Only', 'value': 'synthetic_only'}
                ],
                value=['gdpr', 'cnil', 'anonymization'],
                labelStyle={'display': 'block', 'marginBottom': '8px'}
            )
        ], style={'marginBottom': '20px'}),
        
        html.Div([
            html.Label("Data Retention Period:", style={
                'marginRight': '10px', 
                'fontWeight': 'bold'
            }),
            dcc.Dropdown(
                id='data-retention-period',
                options=[
                    {'label': '30 days', 'value': 30},
                    {'label': '90 days', 'value': 90},
                    {'label': '1 year', 'value': 365},
                    {'label': '2 years', 'value': 730},
                    {'label': 'Indefinite (Compliance Required)', 'value': -1}
                ],
                value=365,
                clearable=False,
                style={'width': '250px', 'display': 'inline-block', 'marginBottom': '16px'}
            )
        ]),
        
        html.Div([
            html.Label("Export Data Format:", style={
                'marginRight': '10px', 
                'fontWeight': 'bold'
            }),
            dcc.Dropdown(
                id='export-data-format',
                options=[
                    {'label': 'CSV (Anonymized)', 'value': 'csv_anon'},
                    {'label': 'JSON (Structured)', 'value': 'json'},
                    {'label': 'Excel (Dashboard)', 'value': 'xlsx'},
                    {'label': 'PDF (Reports Only)', 'value': 'pdf'}
                ],
                value='csv_anon',
                clearable=False,
                style={'width': '200px', 'display': 'inline-block'}
            )
        ])
    ]
    
    return create_info_card("Data Privacy & Compliance", privacy_content, COLORS['warning'])


def create_performance_settings():
    """Create performance and optimization settings."""
    performance_content = [
        html.Div([
            html.Label("Processing Priority:", style={
                'marginRight': '10px', 
                'fontWeight': 'bold',
                'display': 'block',
                'marginBottom': '10px'
            }),
            dcc.RadioItems(
                id='processing-priority',
                options=[
                    {'label': ' Speed (Lower Accuracy)', 'value': 'speed'},
                    {'label': ' Balanced', 'value': 'balanced'},
                    {'label': ' Accuracy (Slower Processing)', 'value': 'accuracy'}
                ],
                value='balanced',
                labelStyle={'display': 'block', 'marginBottom': '8px'}
            )
        ], style={'marginBottom': '20px'}),
        
        html.Div([
            html.Label("Cache Management:", style={
                'marginRight': '10px', 
                'fontWeight': 'bold',
                'display': 'block',
                'marginBottom': '10px'
            }),
            dcc.Checklist(
                id='cache-management',
                options=[
                    {'label': ' Enable Result Caching', 'value': 'enable_cache'},
                    {'label': ' Auto-clear Old Results', 'value': 'auto_clear'},
                    {'label': ' Compress Stored Data', 'value': 'compress'}
                ],
                value=['enable_cache', 'auto_clear'],
                labelStyle={'display': 'block', 'marginBottom': '5px'}
            )
        ]),
        
        html.Div([
            html.Label("Maximum Concurrent Simulations:", style={
                'marginRight': '10px', 
                'fontWeight': 'bold',
                'display': 'block',
                'marginBottom': '10px'
            }),
            dcc.Slider(
                id='max-concurrent-sims',
                min=1, max=10, step=1, value=3,
                marks={i: f"{i}" for i in range(1, 11)},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={'marginTop': '15px'})
    ]
    
    return create_info_card("Performance & Optimization", performance_content, COLORS['success'])


def create_simulation_settings_actions():
    """Create simulation settings action buttons."""
    return html.Div([
        html.Button("💾 Save Configuration", id="sim-settings-save-btn", n_clicks=0, style={
            'padding': '14px 28px', 
            'backgroundColor': COLORS['success'],
            'color': 'white', 
            'border': 'none', 
            'borderRadius': '8px', 
            'fontWeight': '700',
            'marginRight': '12px', 
            'fontSize': '1.07rem',
            'cursor': 'pointer'
        }),
        html.Button("🔄 Reset to Defaults", id="sim-settings-reset-btn", n_clicks=0, style={
            'padding': '14px 28px', 
            'backgroundColor': COLORS['danger'],
            'color': 'white', 
            'border': 'none', 
            'borderRadius': '8px', 
            'fontWeight': '700',
            'marginRight': '12px',
            'fontSize': '1.07rem',
            'cursor': 'pointer'
        }),
        html.Button("🧪 Test Configuration", id="sim-settings-test-btn", n_clicks=0, style={
            'padding': '14px 28px', 
            'backgroundColor': COLORS['primary'],
            'color': 'white', 
            'border': 'none', 
            'borderRadius': '8px', 
            'fontWeight': '700',
            'fontSize': '1.07rem',
            'cursor': 'pointer'
        }),
        html.Div(id="sim-settings-status", style={
            'marginTop': '20px', 
            'fontWeight': '600', 
            'color': COLORS['success']
        })
    ], style={'marginTop': '30px', 'textAlign': 'center'})


# Legacy function for compatibility
def create_settings_content():
    """Legacy function name for compatibility."""
    return create_simulation_settings_content()