"""
Chat controller handling AI chat functionality
"""
from dash import Input, Output, State, html
from services.ai_service import AIService
from config.colors import COLORS
from config.settings import CHAT_CONFIG


def register_callbacks(app):
    """Register all chat-related callbacks."""
    
    @app.callback(
        Output('chat-messages', 'children'),
        Input('send-chat-button', 'n_clicks'),
        State('chat-input', 'value'),
        prevent_initial_call=True
    )
    def handle_chat_message(n_clicks, user_message):
        """Handle chat message and generate AI response."""
        if not user_message or not user_message.strip():
            return [create_initial_message()]
        
        # Get AI response
        ai_response = AIService.process_user_message(user_message)
        
        # Create message components
        initial_msg = create_initial_message()
        user_msg = create_user_message(user_message)
        ai_msg = create_ai_message(ai_response)
        
        return [initial_msg, user_msg, ai_msg]
    
    @app.callback(
        Output('chat-input', 'value'),
        Input('send-chat-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def clear_chat_input(n_clicks):
        """Clear chat input after sending."""
        return ""


def create_initial_message():
    """Create the initial AI welcome message."""
    return html.Div([
        html.Div(CHAT_CONFIG['ai_icon'], style={
            'fontSize': '1.5rem', 
            'marginRight': '10px'
        }),
        html.Div(
            AIService.get_welcome_message(),
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


def create_user_message(message):
    """Create a user message component."""
    return html.Div([
        html.Div([
            html.Div(CHAT_CONFIG['user_icon'], style={
                'fontSize': '1.5rem', 
                'marginRight': '10px'
            }),
            html.Div(message, style={
                'backgroundColor': COLORS['primary'], 
                'color': 'white', 
                'padding': '12px', 
                'borderRadius': '15px', 
                'flex': '1', 
                'maxWidth': '70%'
            })
        ], style={
            'display': 'flex', 
            'alignItems': 'flex-start', 
            'justifyContent': 'flex-end', 
            'marginBottom': '15px'
        })
    ])


def create_ai_message(message):
    """Create an AI response message component."""
    return html.Div([
        html.Div(CHAT_CONFIG['ai_icon'], style={
            'fontSize': '1.5rem', 
            'marginRight': '10px'
        }),
        html.Div(message, style={
            'backgroundColor': COLORS['light'], 
            'padding': '12px', 
            'borderRadius': '15px', 
            'flex': '1', 
            'maxWidth': '70%',
            'border': f'1px solid {COLORS["hover"]}'
        })
    ], style={
        'display': 'flex', 
        'alignItems': 'flex-start', 
        'marginBottom': '15px'
    })