"""
Chat page layout and components
"""
from dash import html, dcc
from config.colors import COLORS
from config.settings import CHAT_CONFIG, DASHBOARD_CONFIG


def create_initial_message():
    """Create the initial AI welcome message."""
    return html.Div([
        html.Div("🤖", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
        html.Div(
            CHAT_CONFIG['welcome_message'],
            style={
                'backgroundColor': COLORS['light'], 
                'padding': '12px', 
                'borderRadius': '15px', 
                'flex': '1'
            }
        )
    ], style={
        'display': 'flex', 
        'alignItems': 'flex-start', 
        'marginBottom': '15px'
    })


def create_chat_messages_container():
    """Create the chat messages container."""
    return html.Div([
        create_initial_message()
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


def create_chat_input_section():
    """Create the chat input and send button section."""
    return html.Div([
        dcc.Input(
            id="chat-input", 
            placeholder="Ask me about client trends, market analysis, or any banking insights...", 
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


def create_suggested_questions():
    """Create suggested questions section."""
    suggestions = [
        "What are the current market trends?",
        "How is client satisfaction performing?",
        "Show me branch distribution analysis",
        "What's our revenue growth this quarter?"
    ]
    
    suggestion_buttons = []
    for suggestion in suggestions:
        suggestion_buttons.append(
            html.Button(
                suggestion,
                className="suggestion-btn",
                style={
                    'padding': '8px 16px',
                    'margin': '4px',
                    'backgroundColor': 'transparent',
                    'border': f'1px solid {COLORS["hover"]}',
                    'borderRadius': '20px',
                    'cursor': 'pointer',
                    'fontSize': '0.85rem',
                    'color': COLORS['dark'],
                    'transition': 'all 0.3s ease'
                }
            )
        )
    
    return html.Div([
        html.P("Suggested questions:", style={
            'fontSize': '0.9rem', 
            'color': COLORS['dark'], 
            'marginBottom': '10px',
            'opacity': '0.7'
        }),
        html.Div(suggestion_buttons, style={
            'display': 'flex', 
            'flexWrap': 'wrap', 
            'gap': '5px'
        })
    ], style={'marginBottom': '20px'})


def create_chat_content():
    """Create the complete chat page content."""
    return html.Div([
        html.H2("AI Assistant Chat", style={
            'fontSize': '2rem', 
            'fontWeight': '700', 
            'color': COLORS['dark'], 
            'marginBottom': '20px'
        }),
        create_suggested_questions(),
        create_chat_messages_container(),
        create_chat_input_section()
    ], style={'maxWidth': '800px'})