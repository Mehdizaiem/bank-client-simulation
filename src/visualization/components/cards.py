"""
Reusable card components for metrics and information display
"""
from dash import html
from config.colors import COLORS


def create_metric_card(icon, title, value, change, color):
    """Create a metric card with icon, title, value, and change indicator."""
    return html.Div([
        html.Div([
            html.Div(icon, style={'fontSize': '2rem', 'marginBottom': '10px'}),
            html.H3(value, style={
                'fontSize': '1.8rem', 
                'fontWeight': '700', 
                'color': color, 
                'margin': '0', 
                'marginBottom': '5px'
            }),
            html.P(title, style={
                'fontSize': '1rem', 
                'fontWeight': '600', 
                'color': COLORS['dark'], 
                'margin': '0', 
                'marginBottom': '8px'
            }),
            html.P(change, style={
                'fontSize': '0.85rem', 
                'color': COLORS['success'], 
                'margin': '0'
            })
        ])
    ], style={
        'backgroundColor': 'white', 
        'padding': '25px', 
        'borderRadius': '15px',
        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)', 
        'border': f'1px solid {COLORS["hover"]}',
        'textAlign': 'center', 
        'transition': 'transform 0.3s ease', 
        'cursor': 'pointer'
    })


def create_info_card(title, content, color=None):
    """Create a general information card."""
    border_color = color or COLORS['primary']
    
    return html.Div([
        html.H4(title, style={
            'marginBottom': '10px', 
            'color': border_color
        }),
        html.Div(content),
    ], style={
        'backgroundColor': '#fff', 
        'padding': '20px', 
        'borderRadius': '14px', 
        'marginBottom': '22px',
        'boxShadow': '0 2px 12px #e5e7eb', 
        'borderLeft': f'5px solid {border_color}'
    })


def create_status_card(title, status, status_color):
    """Create a status card with colored indicator."""
    return html.Div([
        html.H4(title, style={
            'fontSize': '0.85rem', 
            'fontWeight': '600', 
            'color': COLORS['dark'], 
            'marginBottom': '10px'
        }),
        html.Div([
            html.Div("●", style={
                'color': status_color, 
                'fontSize': '1.2rem', 
                'marginRight': '8px'
            }),
            html.Span(status, style={
                'fontSize': '0.9rem', 
                'color': COLORS['dark']
            })
        ], style={
            'display': 'flex', 
            'alignItems': 'center'
        })
    ])