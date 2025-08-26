"""
Card components for bank simulation platform
"""
from dash import html
from config.colors import COLORS


def create_metric_card(icon, title, value, change, color):
    """Create a metric card component."""
    return html.Div([
        html.Div([
            html.Div(icon, style={
                'fontSize': '2.5rem',
                'marginBottom': '15px',
                'textAlign': 'center'
            }),
            html.H4(title, style={
                'fontSize': '1rem',
                'fontWeight': '600',
                'color': COLORS['dark'],
                'marginBottom': '10px',
                'textAlign': 'center'
            }),
            html.H2(value, style={
                'fontSize': '2rem',
                'fontWeight': '700',
                'color': color,
                'marginBottom': '8px',
                'textAlign': 'center'
            }),
            html.P(change, style={
                'fontSize': '0.85rem',
                'color': COLORS['success'] if '+' in str(change) else COLORS['dark'],
                'textAlign': 'center',
                'margin': '0'
            })
        ])
    ], style={
        'backgroundColor': 'white',
        'padding': '25px 20px',
        'borderRadius': '15px',
        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
        'transition': 'transform 0.3s ease, box-shadow 0.3s ease',
        'cursor': 'pointer',
        'border': f'1px solid {COLORS["hover"]}'
    })


def create_info_card(title, content, color):
    """Create an information card with title and content."""
    return html.Div([
        html.H3(title, style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'color': color,
            'marginBottom': '20px',
            'borderBottom': f'2px solid {color}',
            'paddingBottom': '10px'
        }),
        html.Div(content)
    ], style={
        'backgroundColor': 'white',
        'padding': '25px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
        'marginBottom': '20px',
        'border': f'1px solid {COLORS["hover"]}'
    })


def create_stat_card(label, value, icon, trend=None):
    """Create a statistics card."""
    return html.Div([
        html.Div([
            html.Div([
                html.Span(icon, style={'fontSize': '1.5rem', 'marginRight': '10px'}),
                html.Div([
                    html.Div(label, style={
                        'fontSize': '0.9rem',
                        'color': COLORS['dark'],
                        'opacity': '0.8',
                        'marginBottom': '5px'
                    }),
                    html.Div(value, style={
                        'fontSize': '1.8rem',
                        'fontWeight': '700',
                        'color': COLORS['dark']
                    })
                ])
            ], style={'display': 'flex', 'alignItems': 'center'}),
            
            html.Div(trend, style={
                'fontSize': '0.8rem',
                'color': COLORS['success'] if trend and '+' in str(trend) else COLORS['danger'],
                'marginTop': '10px'
            }) if trend else html.Div()
        ])
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
        'border': f'1px solid {COLORS["hover"]}'
    })


def create_status_card(title, status, details, color):
    """Create a status card with color coding."""
    return html.Div([
        html.Div([
            html.H4(title, style={
                'fontSize': '1.1rem',
                'fontWeight': '600',
                'color': COLORS['dark'],
                'marginBottom': '10px'
            }),
            html.Div([
                html.Span("●", style={
                    'color': color,
                    'fontSize': '1.2rem',
                    'marginRight': '8px'
                }),
                html.Span(status, style={
                    'fontSize': '1rem',
                    'fontWeight': '600',
                    'color': color
                })
            ], style={'marginBottom': '10px'}),
            html.P(details, style={
                'fontSize': '0.9rem',
                'color': COLORS['dark'],
                'opacity': '0.8',
                'margin': '0',
                'lineHeight': '1.4'
            })
        ])
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
        'border': f'1px solid {COLORS["hover"]}',
        'borderLeft': f'4px solid {color}'
    })


def create_progress_card(title, current, total, color):
    """Create a progress card with progress bar."""
    percentage = (current / total) * 100 if total > 0 else 0
    
    return html.Div([
        html.H4(title, style={
            'fontSize': '1.1rem',
            'fontWeight': '600',
            'color': COLORS['dark'],
            'marginBottom': '15px'
        }),
        html.Div([
            html.Div(f"{current:,} / {total:,}", style={
                'fontSize': '1.2rem',
                'fontWeight': '600',
                'color': color,
                'marginBottom': '10px'
            }),
            html.Div([
                html.Div(style={
                    'width': f'{percentage}%',
                    'height': '8px',
                    'backgroundColor': color,
                    'borderRadius': '4px',
                    'transition': 'width 0.3s ease'
                })
            ], style={
                'width': '100%',
                'height': '8px',
                'backgroundColor': COLORS['light'],
                'borderRadius': '4px',
                'overflow': 'hidden'
            }),
            html.Div(f"{percentage:.1f}%", style={
                'fontSize': '0.9rem',
                'color': COLORS['dark'],
                'marginTop': '8px',
                'textAlign': 'right'
            })
        ])
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
        'border': f'1px solid {COLORS["hover"]}'
    })