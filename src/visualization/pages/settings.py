"""
Settings page layout and components
"""
from dash import html, dcc
from config.colors import COLORS
from components.cards import create_info_card


def create_settings_header():
    """Create the settings page header."""
    return html.H2("Dashboard Settings", style={
        'fontSize': '2rem', 
        'fontWeight': '700', 
        'color': COLORS['dark'], 
        'marginBottom': '20px'
    })


def create_theme_settings():
    """Create theme and personalization settings."""
    theme_content = [
        dcc.RadioItems(
            id='setting-theme',
            options=[
                {'label': ' Light', 'value': 'light'},
                {'label': ' Dark', 'value': 'dark'},
                {'label': ' Corporate', 'value': 'corporate'},
            ],
            value='light',
            labelStyle={
                'display': 'inline-block', 
                'marginRight': '18px', 
                'fontSize': '1rem'
            }
        ),
        html.Div("Select your preferred dashboard theme.", style={
            'fontSize': '0.92rem', 
            'opacity': '0.75',
            'marginTop': '10px'
        })
    ]
    
    return create_info_card("Theme & Personalization", theme_content, COLORS['primary'])


def create_notification_settings():
    """Create notification and preference settings."""
    notification_content = [
        dcc.Checklist(
            options=[
                {"label": " Email Notifications", "value": "email"},
                {"label": " Push Notifications", "value": "push"},
                {"label": " SMS Alerts", "value": "sms"},
            ],
            value=["push"],
            id="setting-notifications",
            style={'marginBottom': '12px'}
        ),
        html.Div([
            html.Label("Interface Language", style={
                'marginRight': '10px', 
                'fontWeight': 'bold'
            }),
            dcc.Dropdown(
                id='setting-language',
                options=[
                    {'label': 'English', 'value': 'en'},
                    {'label': 'French', 'value': 'fr'},
                    {'label': 'Arabic', 'value': 'ar'},
                ],
                value='en',
                clearable=False,
                style={'width': '200px', 'display': 'inline-block', 'marginBottom': '16px'}
            ),
        ]),
        html.Div([
            html.Label("Default Refresh Rate", style={
                'marginRight': '10px', 
                'fontWeight': 'bold',
                'display': 'block',
                'marginBottom': '10px'
            }),
            dcc.Slider(
                id='setting-refresh-interval',
                min=5, max=60, step=5, value=15,
                marks={i: f"{i}s" for i in range(5, 65, 10)},
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode="drag"
            )
        ], style={'marginTop': '15px'})
    ]
    
    return create_info_card("Notifications & Preferences", notification_content, COLORS['accent'])


def create_data_settings():
    """Create data and export settings."""
    data_content = [
        html.Div([
            html.Label("Default Export Format", style={
                'marginRight': '10px', 
                'fontWeight': 'bold'
            }),
            dcc.Dropdown(
                id='setting-export-format',
                options=[
                    {'label': 'CSV', 'value': 'csv'},
                    {'label': 'Excel', 'value': 'xlsx'},
                    {'label': 'JSON', 'value': 'json'},
                ],
                value='csv',
                clearable=False,
                style={'width': '150px', 'display': 'inline-block', 'marginBottom': '16px'}
            ),
        ]),
        html.Div([
            html.Label("Chart Animation", style={'marginRight': '10px', 'fontWeight': 'bold'}),
            dcc.RadioItems(
                id='setting-chart-animation',
                options=[
                    {'label': ' Enabled', 'value': 'enabled'},
                    {'label': ' Disabled', 'value': 'disabled'}
                ],
                value='enabled',
                labelStyle={'display': 'inline-block', 'marginRight': '15px'}
            )
        ], style={'marginTop': '15px'})
    ]
    
    return create_info_card("Data & Display", data_content, COLORS['secondary'])


def create_settings_actions():
    """Create settings action buttons."""
    return html.Div([
        html.Button("Save Changes", id="settings-save-btn", n_clicks=0, style={
            'padding': '12px 28px', 
            'backgroundColor': COLORS['success'],
            'color': 'white', 
            'border': 'none', 
            'borderRadius': '8px', 
            'fontWeight': '700',
            'marginRight': '12px', 
            'fontSize': '1.07rem',
            'cursor': 'pointer'
        }),
        html.Button("Reset All", id="settings-reset-btn", n_clicks=0, style={
            'padding': '12px 28px', 
            'backgroundColor': COLORS['danger'],
            'color': 'white', 
            'border': 'none', 
            'borderRadius': '8px', 
            'fontWeight': '700',
            'fontSize': '1.07rem',
            'cursor': 'pointer'
        }),
        html.Div(id="settings-status", style={
            'marginTop': '20px', 
            'fontWeight': '600', 
            'color': COLORS['success']
        })
    ], style={'marginTop': '30px'})


def create_settings_content():
    """Create the complete settings page content."""
    return html.Div([
        create_settings_header(),
        html.Div([
            create_theme_settings(),
            create_notification_settings(),
            create_data_settings(),
            create_settings_actions()
        ], style={'maxWidth': '800px', 'margin': '0 auto'})
    ])