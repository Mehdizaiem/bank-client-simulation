"""
Chat callbacks for the Bank Client Simulation Platform
"""
import dash
from dash import html, Input, Output, State, callback_context
from config.colors import COLORS
from services.ai_service import AIService


def register_chat_callbacks(app):
    """Register all chat-related callbacks."""
    
    @app.callback(
        Output('chat-messages', 'children'),
        [Input('send-chat-button', 'n_clicks'),
         Input({'type': 'simulation-suggestion-btn', 'index': dash.dependencies.ALL}, 'n_clicks'),
         Input('quick-branch-calc', 'n_clicks'),
         Input('quick-economic-test', 'n_clicks'),
         Input('quick-behavior-analyze', 'n_clicks'),
         Input('quick-opportunity-find', 'n_clicks')],
        [State('chat-input', 'value'),
         State('chat-messages', 'children')]
    )
    def update_chat_messages(send_clicks, suggestion_clicks, branch_clicks, economic_clicks, 
                            behavior_clicks, opportunity_clicks, message, current_messages):
        """Update chat messages with AI responses."""
        ctx = callback_context
        
        if not ctx.triggered:
            return current_messages
        
        trigger_id = ctx.triggered[0]['prop_id']
        
        # Determine the message to process
        user_message = None
        
        if 'send-chat-button' in trigger_id and message:
            user_message = message
        elif 'simulation-suggestion-btn' in trigger_id:
            # Extract suggestion from button
            suggestions = AIService.get_simulation_suggestions()
            button_index = eval(trigger_id.split('.')[0])['index']
            user_message = suggestions[button_index] if button_index < len(suggestions) else "Help me with simulations"
        elif 'quick-branch-calc' in trigger_id:
            user_message = AIService.process_quick_action('branch_calc')
        elif 'quick-economic-test' in trigger_id:
            user_message = AIService.process_quick_action('economic_test')
        elif 'quick-behavior-analyze' in trigger_id:
            user_message = AIService.process_quick_action('behavior_analyze')
        elif 'quick-opportunity-find' in trigger_id:
            user_message = AIService.process_quick_action('opportunity_find')
        
        if not user_message:
            return current_messages
        
        # Process the message and get AI response
        ai_response = AIService.process_user_message(user_message)
        
        # Create new message elements
        user_message_element = create_chat_message("👤", "You", user_message, True)
        ai_message_element = create_chat_message("🤖", "AI Assistant", ai_response, False)
        
        # Add new messages to existing ones
        updated_messages = current_messages + [user_message_element, ai_message_element]
        
        return updated_messages

    @app.callback(
        Output('chat-input', 'value'),
        [Input('send-chat-button', 'n_clicks')],
        [State('chat-input', 'value')]
    )
    def clear_chat_input(n_clicks, message):
        """Clear chat input after sending message."""
        if n_clicks and message:
            return ""
        return message


def create_chat_message(icon, sender, message, is_user):
    """Create a chat message element."""
    message_style = {
        'backgroundColor': COLORS['primary'] if is_user else COLORS['light'],
        'color': 'white' if is_user else COLORS['dark'],
        'padding': '12px',
        'borderRadius': '15px',
        'lineHeight': '1.4'
    }
    
    if is_user:
        message_style['marginLeft'] = '30px'
    
    return html.Div([
        html.Div(icon, style={'fontSize': '1.5rem', 'marginRight': '10px'}),
        html.Div([
            html.Div(sender, style={
                'fontWeight': 'bold', 
                'fontSize': '1.1rem', 
                'marginBottom': '8px'
            }),
            html.Div(message, style=message_style)
        ], style={'flex': '1'})
    ], style={
        'display': 'flex', 
        'alignItems': 'flex-start', 
        'marginBottom': '15px'
    })