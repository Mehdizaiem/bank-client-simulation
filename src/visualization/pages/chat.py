"""
AI Chat page for Bank Client Simulation Platform
"""
from dash import html, dcc
from config.colors import COLORS
from config.settings import CHAT_CONFIG, DASHBOARD_CONFIG


def create_simulation_chat_content():
    """Create the complete simulation chat page content."""
    return html.Div([
        html.H2("AI Simulation Assistant", style={
            'fontSize': '2rem', 
            'fontWeight': '700', 
            'color': COLORS['dark'], 
            'marginBottom': '20px'
        }),
        create_simulation_capabilities_panel(),
        create_quick_actions_panel(),
        create_simulation_suggested_questions(),
        create_simulation_chat_messages_container(),
        create_simulation_chat_input()
    ], style={'maxWidth': '1000px'})


def create_simulation_capabilities_panel():
    """Create AI capabilities panel for simulation context."""
    return html.Div([
        html.H3("AI Assistant Capabilities", style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'color': COLORS['dark'],
            'marginBottom': '15px'
        }),
        html.Div([
            # Simulation & Modeling
            html.Div([
                html.Div("🎯", style={'fontSize': '2rem', 'marginBottom': '10px'}),
                html.H4("Scenario Simulation", style={'color': COLORS['primary'], 'marginBottom': '8px'}),
                html.Ul([
                    html.Li("Branch network optimization"),
                    html.Li("Economic shock modeling"),
                    html.Li("Competition analysis"),
                    html.Li("Product launch simulations")
                ], style={'fontSize': '0.9rem', 'paddingLeft': '20px'})
            ], style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                'flex': '1'
            }),
            
            # Data Analysis
            html.Div([
                html.Div("📊", style={'fontSize': '2rem', 'marginBottom': '10px'}),
                html.H4("Behavioral Analysis", style={'color': COLORS['secondary'], 'marginBottom': '8px'}),
                html.Ul([
                    html.Li("Client churn prediction"),
                    html.Li("Channel preference patterns"),
                    html.Li("Regional behavior insights"),
                    html.Li("Risk profile analysis")
                ], style={'fontSize': '0.9rem', 'paddingLeft': '20px'})
            ], style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                'flex': '1'
            }),
            
            # Strategic Insights
            html.Div([
                html.Div("💡", style={'fontSize': '2rem', 'marginBottom': '10px'}),
                html.H4("Strategic Insights", style={'color': COLORS['accent'], 'marginBottom': '8px'}),
                html.Ul([
                    html.Li("Market opportunity identification"),
                    html.Li("Resource allocation optimization"),
                    html.Li("Competitive positioning"),
                    html.Li("Performance benchmarking")
                ], style={'fontSize': '0.9rem', 'paddingLeft': '20px'})
            ], style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                'flex': '1'
            })
        ], style={'display': 'flex', 'gap': '20px'})
    ], style={'marginBottom': '25px'})


def create_quick_actions_panel():
    """Create quick actions panel for common simulation tasks."""
    return html.Div([
        html.H3("Quick Actions", style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'color': COLORS['dark'],
            'marginBottom': '15px'
        }),
        html.Div([
            html.Button("🏪 Branch Impact Calculator", id="quick-branch-calc", style={
                'padding': '15px 20px', 'backgroundColor': COLORS['primary'], 'color': 'white',
                'border': 'none', 'borderRadius': '8px', 'fontWeight': '600',
                'cursor': 'pointer', 'margin': '5px', 'minWidth': '200px'
            }),
            html.Button("💱 Economic Scenario Tester", id="quick-economic-test", style={
                'padding': '15px 20px', 'backgroundColor': COLORS['secondary'], 'color': 'white',
                'border': 'none', 'borderRadius': '8px', 'fontWeight': '600',
                'cursor': 'pointer', 'margin': '5px', 'minWidth': '200px'
            }),
            html.Button("📊 Client Behavior Analyzer", id="quick-behavior-analyze", style={
                'padding': '15px 20px', 'backgroundColor': COLORS['accent'], 'color': 'white',
                'border': 'none', 'borderRadius': '8px', 'fontWeight': '600',
                'cursor': 'pointer', 'margin': '5px', 'minWidth': '200px'
            }),
            html.Button("🎯 Market Opportunity Finder", id="quick-opportunity-find", style={
                'padding': '15px 20px', 'backgroundColor': COLORS['success'], 'color': 'white',
                'border': 'none', 'borderRadius': '8px', 'fontWeight': '600',
                'cursor': 'pointer', 'margin': '5px', 'minWidth': '200px'
            })
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '10px'})
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 12px rgba(0,0,0,0.1)',
        'marginBottom': '20px'
    })


def create_simulation_suggested_questions():
    """Create simulation-specific suggested questions."""
    suggestions = [
        "🎯 Run a branch closure simulation for Kairouan",
        "💱 What happens if the dinar devalues by 15%?",
        "📱 Simulate launching a mobile-only banking service",
        "🏛️ How would a competitor entering Sfax affect us?",
        "📊 Show me client churn patterns in northern Tunisia",
        "💳 Test impact of reducing fees by 20%",
        "🏪 Where should we open our next branch?",
        "📈 Analyze corporate client behavior trends"
    ]
    
    suggestion_buttons = []
    for i, suggestion in enumerate(suggestions):
        suggestion_buttons.append(
            html.Button(
                suggestion,
                id={'type': 'simulation-suggestion-btn', 'index': i},
                n_clicks=0,
                style={
                    'padding': '10px 16px',
                    'margin': '4px',
                    'backgroundColor': 'white',
                    'border': f'1px solid {COLORS["primary"]}',
                    'borderRadius': '25px',
                    'cursor': 'pointer',
                    'fontSize': '0.85rem',
                    'color': COLORS['primary'],
                    'transition': 'all 0.3s ease',
                    'fontWeight': '500'
                }
            )
        )
    
    return html.Div([
        html.P("💡 Try these simulation questions:", style={
            'fontSize': '1rem', 
            'color': COLORS['dark'], 
            'marginBottom': '15px',
            'fontWeight': '600'
        }),
        html.Div(suggestion_buttons, style={
            'display': 'flex', 
            'flexWrap': 'wrap', 
            'gap': '8px'
        })
    ], style={'marginBottom': '25px'})


def create_simulation_chat_messages_container():
    """Create the chat messages container for simulation context."""
    return html.Div([
        create_simulation_chat_welcome()
    ], 
    id="chat-messages", 
    style={
        'height': f'{DASHBOARD_CONFIG["chat_height"]}px', 
        'overflowY': 'auto', 
        'padding': '20px', 
        'backgroundColor': 'white',
        'border': f'1px solid {COLORS["hover"]}', 
        'borderRadius': '15px', 
        'marginBottom': '20px'
    })


def create_simulation_chat_welcome():
    """Create the AI simulation assistant welcome message."""
    return html.Div([
        html.Div("🤖", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
        html.Div([
            html.Div("AI Simulation Assistant", style={
                'fontWeight': 'bold', 'fontSize': '1.1rem', 'marginBottom': '8px'
            }),
            html.Div(
                "Welcome! I'm your AI assistant for the Bank Client Simulation Platform. I can help you run scenarios, interpret simulation results, analyze client behavior patterns, and provide strategic insights for your Tunisian banking operations.",
                style={
                    'backgroundColor': COLORS['light'], 
                    'padding': '12px', 
                    'borderRadius': '15px', 
                    'lineHeight': '1.4'
                }
            )
        ], style={'flex': '1'})
    ], style={
        'display': 'flex', 
        'alignItems': 'flex-start', 
        'marginBottom': '15px'
    })


def create_simulation_chat_input():
    """Create the simulation-focused chat input section."""
    return html.Div([
        dcc.Input(
            id="chat-input", 
            placeholder="Ask about simulations, client behavior, branch strategies, or economic scenarios...", 
            style={
                'flex': '1', 
                'marginRight': '10px', 
                'padding': '12px', 
                'border': f'1px solid {COLORS["hover"]}', 
                'borderRadius': '6px', 
                'fontSize': '1rem', 
                'width': '70%'
            }
        ),
        html.Button("Send", id="send-chat-button", n_clicks=0, style={
            'padding': '12px 24px', 
            'background': f'linear-gradient(135deg, {COLORS["primary"]}, {COLORS["secondary"]})', 
            'color': 'white',
            'border': 'none', 
            'borderRadius': '6px', 
            'cursor': 'pointer', 
            'fontWeight': '600'
        })
    ], style={'display': 'flex', 'alignItems': 'center'})


# Legacy function for compatibility
def create_chat_content():
    """Legacy function name for compatibility."""
    return create_simulation_chat_content()