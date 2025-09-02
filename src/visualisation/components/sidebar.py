# sidebar.py
from dash import html
from config.colors import COLORS

PRIMARY = COLORS.get('primary', '#3B82F6')

def create_sidebar_navigation():
    return html.Div([
        # Brand
        html.Div([
            html.Div([
                html.Div([
                    html.I(className="fas fa-university")
                ], style={
                    'width': 56, 'height': 56, 'borderRadius': 14,
                    'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                    'backgroundColor': 'rgba(59,130,246,.10)', 'color': PRIMARY, 'fontSize': 22
                }),
                html.Div([
                    html.H2("Bank Simulation", style={
                        'fontSize': '1.12rem', 'margin': '0 0 4px 0', 'color': COLORS['dark'], 'fontWeight': 800
                    }),
                    html.P("AI-Powered Analytics", style={
                        'fontSize': '.82rem', 'margin': 0, 'color': COLORS['secondary']
                    })
                ], style={'display': 'flex', 'flexDirection': 'column'})
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': 14})
        ], style={'padding': '22px 18px', 'borderBottom': '1px solid #eef2f7', 'backgroundColor': 'white'}),

        # Nav (no Settings)
        html.Nav([
            _nav_button("nav-home",       "fas fa-home",         "Home"),
            _nav_button("nav-geographic", "fas fa-globe-africa", "Geographic Analysis"),
            html.Hr(style={'margin': '14px 18px', 'border': '1px solid #eef2f7'}),
            _nav_button("nav-profile",    "fas fa-user",         "Profile"),
        ], style={'padding': '10px 0', 'backgroundColor': 'white'})
    ], style={
        'width': 300, 'height': '100vh', 'position': 'fixed', 'left': 0, 'top': 0,
        'backgroundColor': 'white',
        'borderRight': f'3px solid {PRIMARY}',               # blue border
        'boxShadow': '12px 0 30px rgba(2,6,23,.10)',         # stronger presence
        'overflowY': 'auto', 'zIndex': 2000
    })


def _nav_button(button_id: str, icon_class: str, label: str):
    return html.Button([
        html.Div([
            html.I(className=icon_class)
        ], style={
            'width': 36, 'height': 36, 'minWidth': 36,
            'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
            'borderRadius': 10, 'marginRight': 14,
            'backgroundColor': 'rgba(59,130,246,.08)', 'color': PRIMARY, 'fontSize': 18
        }),
        html.Span(label, style={'flex': 1})
    ], id=button_id, n_clicks=0, className="nav-button", style=get_nav_button_style())


def get_nav_button_style():
    return {
        'padding': '14px 16px', 'margin': '0 14px 10px 14px', 'borderRadius': 12,
        'cursor': 'pointer', 'transition': 'all .16s ease',
        'display': 'flex', 'alignItems': 'center', 'width': 'calc(100% - 28px)',
        'backgroundColor': 'white', 'border': '1px solid #e9eef7',
        'color': COLORS['dark'], 'textAlign': 'left',
        'fontSize': '1.02rem', 'fontWeight': 600
    }


def get_active_nav_button_style():
    active = get_nav_button_style().copy()
    active.update({
        'backgroundColor': PRIMARY,
        'color': 'white',
        'borderColor': PRIMARY,
        'boxShadow': '0 8px 20px rgba(59,130,246,.28)'
    })
    return active
