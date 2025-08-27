"""
Economic simulation analysis page for Bank Client Simulation
"""
from dash import html, dcc
from config.colors import COLORS
from components.charts import create_economic_charts


def create_economic_simulation_content():
    """Create the economic simulation page content."""
    return html.Div([
        create_economic_simulation_header(),
        create_economic_scenario_panel(),
        create_economic_indicators_panel(),
        create_economic_charts(),  # Using the new charts component
        create_economic_insights_panel()
    ])


def create_economic_simulation_header():
    """Create the economic simulation analysis header."""
    return html.Div([
        html.H2("Economic Impact Simulation", style={
            'fontSize': '2rem', 
            'fontWeight': '700', 
            'color': COLORS['dark'], 
            'marginBottom': '10px'
        }),
        html.P("Model client responses to macroeconomic changes and policy shifts in Tunisia", style={
            'fontSize': '1.1rem', 
            'color': COLORS['dark'], 
            'opacity': '0.7', 
            'marginBottom': '20px'
        })
    ])


def create_economic_scenario_panel():
    """Create economic scenario simulation panel."""
    return html.Div([
        html.H3("Economic Scenario Builder", style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'color': COLORS['dark'],
            'marginBottom': '15px'
        }),
        html.Div([
            # Economic Shock Type
            html.Div([
                html.Label("Economic Event:", style={
                    'marginRight': '8px', 
                    'fontWeight': 'bold'
                }),
                dcc.Dropdown(
                    id='economic-event-type',
                    options=[
                        {'label': 'Currency Devaluation', 'value': 'currency'},
                        {'label': 'Interest Rate Change', 'value': 'interest'},
                        {'label': 'Inflation Spike', 'value': 'inflation'},
                        {'label': 'GDP Growth Change', 'value': 'gdp'},
                        {'label': 'Political Uncertainty', 'value': 'political'},
                        {'label': 'Oil Price Shock', 'value': 'oil'}
                    ],
                    value='currency',
                    clearable=False,
                    style={'width': '180px', 'display': 'inline-block'}
                ),
            ], style={'display': 'inline-block', 'marginRight': '20px'}),

            # Severity
            html.Div([
                html.Label("Impact Severity:", style={
                    'marginRight': '8px', 
                    'fontWeight': 'bold'
                }),
                dcc.Slider(
                    id='economic-severity',
                    min=1, max=10, step=1, value=5,
                    marks={i: f"{i}" for i in range(1, 11)},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style={'width': '200px', 'display': 'inline-block', 'marginRight': '20px'}),

            # Time Horizon
            html.Div([
                html.Label("Time Horizon:", style={
                    'marginRight': '8px', 
                    'fontWeight': 'bold'
                }),
                dcc.Dropdown(
                    id='economic-time-horizon',
                    options=[
                        {'label': '3 Months', 'value': '3m'},
                        {'label': '6 Months', 'value': '6m'},
                        {'label': '1 Year', 'value': '1y'},
                        {'label': '2 Years', 'value': '2y'}
                    ],
                    value='6m',
                    clearable=False,
                    style={'width': '120px', 'display': 'inline-block'}
                ),
            ], style={'display': 'inline-block', 'marginRight': '20px'}),

            # Run Button
            html.Button("🧮 Run Economic Simulation", id="economic-sim-btn", n_clicks=0, style={
                'padding': '12px 24px', 
                'backgroundColor': COLORS['primary'], 
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


def create_economic_indicators_panel():
    """Create economic indicators monitoring panel."""
    return html.Div([
        html.H3("Current Economic Indicators", style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'color': COLORS['dark'],
            'marginBottom': '15px'
        }),
        html.Div([
            # Real indicators from Tunisia
            html.Div([
                html.Div("🏛️", style={'fontSize': '2rem', 'marginBottom': '10px'}),
                html.H4("Central Bank Rate", style={'color': COLORS['primary'], 'marginBottom': '5px'}),
                html.Div("8.0%", style={'fontSize': '1.5rem', 'fontWeight': 'bold'}),
                html.Div("Stable", style={'color': COLORS['success'], 'fontSize': '0.9rem'})
            ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 
                     'borderRadius': '10px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)', 'flex': '1'}),
            
            html.Div([
                html.Div("💱", style={'fontSize': '2rem', 'marginBottom': '10px'}),
                html.H4("USD/TND Rate", style={'color': COLORS['warning'], 'marginBottom': '5px'}),
                html.Div("3.18", style={'fontSize': '1.5rem', 'fontWeight': 'bold'}),
                html.Div("-0.5% today", style={'color': COLORS['danger'], 'fontSize': '0.9rem'})
            ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 
                     'borderRadius': '10px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)', 'flex': '1'}),
            
            html.Div([
                html.Div("📈", style={'fontSize': '2rem', 'marginBottom': '10px'}),
                html.H4("Inflation Rate", style={'color': COLORS['danger'], 'marginBottom': '5px'}),
                html.Div("7.3%", style={'fontSize': '1.5rem', 'fontWeight': 'bold'}),
                html.Div("+0.2% this month", style={'color': COLORS['danger'], 'fontSize': '0.9rem'})
            ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 
                     'borderRadius': '10px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)', 'flex': '1'}),
            
            html.Div([
                html.Div("🏭", style={'fontSize': '2rem', 'marginBottom': '10px'}),
                html.H4("GDP Growth", style={'color': COLORS['success'], 'marginBottom': '5px'}),
                html.Div("2.1%", style={'fontSize': '1.5rem', 'fontWeight': 'bold'}),
                html.Div("Q3 2025", style={'color': COLORS['success'], 'fontSize': '0.9rem'})
            ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 
                     'borderRadius': '10px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)', 'flex': '1'})
        ], style={'display': 'flex', 'gap': '15px'})
    ], style={'marginBottom': '20px'})


def create_economic_insights_panel():
    """Create AI-generated economic insights panel."""
    return html.Div([
        html.H3("AI Economic Insights", style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'color': COLORS['dark'],
            'marginBottom': '15px'
        }),
        html.Div([
            html.Div([
                html.H4("🚨 Risk Alert", style={'color': COLORS['danger'], 'marginBottom': '10px'}),
                html.P("High inflation scenario may trigger 15% increase in savings withdrawals among retail clients, particularly in Tunis and Sfax regions."),
                html.P("Recommended action: Prepare liquidity management strategies and consider promotional deposit rates.", 
                       style={'fontSize': '0.9rem', 'fontStyle': 'italic'})
            ], style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                'borderLeft': f'4px solid {COLORS["danger"]}',
                'flex': '1'
            }),
            
            html.Div([
                html.H4("💡 Opportunity", style={'color': COLORS['success'], 'marginBottom': '10px'}),
                html.P("Currency devaluation scenario shows increased demand for USD-linked products, especially among corporate clients."),
                html.P("Recommended action: Accelerate foreign currency product offerings and hedging solutions.", 
                       style={'fontSize': '0.9rem', 'fontStyle': 'italic'})
            ], style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                'borderLeft': f'4px solid {COLORS["success"]}',
                'flex': '1'
            })
        ], style={'display': 'flex', 'gap': '20px'})
    ], style={'marginTop': '20px'})


# Legacy function for compatibility
def create_economic_content():
    """Legacy function name for compatibility."""
    return create_economic_simulation_content()