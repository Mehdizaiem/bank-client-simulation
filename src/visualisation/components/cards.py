"""
Card components for bank simulation platform (polished)
"""
from dash import html
from config.colors import COLORS

def create_metric_card(icon, title, value, change, color):
    """Metric card with hover elevation (uses .card styles from CSS)."""
    is_up = ('+' in str(change)) if change is not None else False
    delta_cls = "card__delta--up" if is_up else "card__delta--down"
    return html.Div([
        html.Div([
            html.Div(icon, style={'fontSize': '2rem', 'marginBottom': 12, 'textAlign': 'center'}),
            html.Div(title, className="card__title", style={'fontSize': '1rem', 'textAlign': 'center', 'marginBottom': 8}),
            html.Div(value, className="card__value", style={'color': color, 'textAlign': 'center'}),
            html.Div(change, className=f"card__muted card__delta {delta_cls}",
                     style={'fontSize': '.88rem', 'textAlign': 'center', 'marginTop': 6}) if change else html.Div()
        ])
    ], className="card card--metric", style={'padding': '20px'})

def create_info_card(title, content, color):
    """Information card with titled divider."""
    return html.Div([
        html.Div(title, className="card__title",
                 style={'fontSize': '1.15rem', 'color': color, 'marginBottom': 12,
                        'paddingBottom': 8, 'borderBottom': f'2px solid {color}'}),
        html.Div(content, className="card__body")
    ], className="card", style={'padding': 22, 'marginBottom': 16})

def create_stat_card(label, value, icon, trend=None):
    """Simple stat card (icon + numbers)."""
    return html.Div([
        html.Div([
            html.Div([
                html.Span(icon, style={'fontSize': '1.25rem', 'marginRight': 10}),
                html.Div([
                    html.Div(label, className="card__muted",
                             style={'fontSize': '.9rem', 'marginBottom': 4, 'color': COLORS['dark'], 'opacity': .8}),
                    html.Div(value, style={'fontSize': '1.6rem', 'fontWeight': 700, 'color': COLORS['dark']})
                ])
            ], style={'display': 'flex', 'alignItems': 'center'}),
            html.Div(trend, className=("card__delta card__delta--up" if trend and '+' in str(trend)
                                       else "card__delta card__delta--down") if trend else "",
                     style={'fontSize': '.85rem', 'marginTop': 10}) if trend else html.Div()
        ])
    ], className="card", style={'padding': 18})

def create_status_card(title, status, details, color):
    """Status card with FA dot."""
    return html.Div([
        html.Div([
            html.Div(title, className="card__title", style={'fontSize': '1.05rem', 'marginBottom': 10}),
            html.Div([
                html.I(className="fas fa-circle", style={'color': color, 'fontSize': '.7rem', 'marginRight': 8}),
                html.Span(status, style={'fontWeight': 600, 'color': color})
            ], style={'marginBottom': 10, 'display': 'flex', 'alignItems': 'center'}),
            html.Div(details, className="card__muted",
                     style={'fontSize': '.92rem', 'color': COLORS['dark'], 'opacity': .85, 'lineHeight': 1.45})
        ])
    ], className="card", style={'padding': 18, 'borderLeft': f'4px solid {color}'})

def create_progress_card(title, current, total, color):
    """Progress card with bar."""
    pct = (current / total * 100) if total else 0
    return html.Div([
        html.Div(title, className="card__title", style={'fontSize': '1.05rem', 'marginBottom': 12}),
        html.Div(f"{current:,} / {total:,}", style={'fontWeight': 600, 'color': color, 'marginBottom': 10}),
        html.Div([
            html.Div(style={'width': f'{pct:.2f}%', 'height': 8, 'backgroundColor': color,
                            'borderRadius': 4, 'transition': 'width .25s ease'})
        ], style={'width': '100%', 'height': 8, 'backgroundColor': COLORS['light'], 'borderRadius': 4, 'overflow': 'hidden'}),
        html.Div(f"{pct:.1f}%", className="card__muted", style={'marginTop': 8, 'textAlign': 'right'})
    ], className="card", style={'padding': 18})
