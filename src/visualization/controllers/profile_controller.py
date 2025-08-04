"""
Profile controller - Fixed final version that works with dynamic content
"""
from dash import Input, Output, State, callback_context, html, dcc, no_update, ALL
import dash
from config.colors import COLORS


def register_callbacks(app):
    print("🔧 Registering profile controller callbacks...")

    # Toggle dropdown
    @app.callback(
        Output('user-dropdown-menu', 'style'),
        Input('user-avatar-button', 'n_clicks'),
        State('user-dropdown-menu', 'style'),
        prevent_initial_call=True
    )
    def toggle_dropdown(n_clicks, current_style):
        if n_clicks:
            print(f"🎯 Avatar clicked {n_clicks} times")
            new_style = current_style.copy() if current_style else {}
            if current_style.get('display', 'none') == 'none':
                new_style['display'] = 'block'
                print("📖 Showing dropdown")
            else:
                new_style['display'] = 'none'
                print("📖 Hiding dropdown")
            return new_style
        return current_style or {'display': 'none'}

    # Handle Connect option
    @app.callback(
        [Output('connect-card', 'style'),
         Output('connect-card', 'children'),
         Output('user-dropdown-menu', 'style', allow_duplicate=True)],
        Input('connect-option', 'n_clicks'),
        [State('connect-card', 'style'),
         State('user-dropdown-menu', 'style')],
        prevent_initial_call=True
    )
    def show_connect_card(n_clicks, connect_style, dropdown_style):
        if n_clicks:
            print("🔗 Showing connect card")
            new_connect_style = connect_style.copy() if connect_style else {}
            new_connect_style['display'] = 'block'
            
            new_dropdown_style = dropdown_style.copy() if dropdown_style else {}
            new_dropdown_style['display'] = 'none'
            
            return new_connect_style, create_connect_card_content(), new_dropdown_style
        return no_update, no_update, no_update

    # Handle Manage Account - Complete workflow
    @app.callback(
        [Output('manage-account-card', 'style'),
         Output('manage-account-card', 'children'),
         Output('user-dropdown-menu', 'style', allow_duplicate=True)],
        [Input('manage-account-option', 'n_clicks'),
         Input({'type': 'manage-btn', 'index': ALL}, 'n_clicks'),
         Input({'type': 'back-btn', 'index': ALL}, 'n_clicks'),
         Input({'type': 'close-btn', 'index': ALL}, 'n_clicks')],
        [State('manage-account-card', 'style'),
         State('user-dropdown-menu', 'style')],
        prevent_initial_call=True
    )
    def handle_manage_account(manage_clicks, manage_btn_clicks, back_btn_clicks, close_btn_clicks, 
                             manage_style, dropdown_style):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update

        trigger_id = ctx.triggered[0]['prop_id']
        print(f"🎯 Manage account trigger: {trigger_id}")

        new_manage_style = manage_style.copy() if manage_style else {}
        new_dropdown_style = dropdown_style.copy() if dropdown_style else {}

        # Handle main manage account option click
        if 'manage-account-option' in trigger_id:
            print("⚙️ Opening manage account card")
            new_manage_style['display'] = 'block'
            new_dropdown_style['display'] = 'none'
            return new_manage_style, create_default_manage_content(), new_dropdown_style

        # Handle close button
        if 'close-btn' in trigger_id:
            print("❌ Closing manage account card")
            new_manage_style['display'] = 'none'
            return new_manage_style, no_update, new_dropdown_style

        # Handle back button
        if 'back-btn' in trigger_id:
            print("⬅️ Back to main manage view")
            return new_manage_style, create_default_manage_content(), new_dropdown_style

        # Handle manage buttons (edit, password, etc.)
        if 'manage-btn' in trigger_id:
            button_data = eval(trigger_id.split('.')[0])
            button_index = button_data['index']
            print(f"🎯 Manage button clicked: {button_index}")

            if button_index == 'edit':
                return new_manage_style, create_edit_profile_form(), new_dropdown_style
            elif button_index == 'password':
                return new_manage_style, create_change_password_form(), new_dropdown_style
            elif button_index == 'accounts':
                return new_manage_style, create_connected_accounts_view(), new_dropdown_style
            elif button_index == 'notifications':
                return new_manage_style, create_notification_settings_view(), new_dropdown_style

        return no_update, no_update, no_update

    # Close connect card
    @app.callback(
        Output('connect-card', 'style', allow_duplicate=True),
        Input({'type': 'close-connect-btn', 'index': ALL}, 'n_clicks'),
        State('connect-card', 'style'),
        prevent_initial_call=True
    )
    def close_connect_card(n_clicks, connect_style):
        if any(n_clicks):
            print("❌ Closing connect card")
            new_style = connect_style.copy() if connect_style else {}
            new_style['display'] = 'none'
            return new_style
        return no_update

    # View Profile handler
    @app.callback(
        Output('page-content', 'children', allow_duplicate=True),
        Input('view-profile-option', 'n_clicks'),
        prevent_initial_call=True
    )
    def show_profile_page(n_clicks):
        if n_clicks:
            print("📊 Showing profile page")
            return create_simple_profile_content()
        return no_update

    # Handle other dropdown actions
    @app.callback(
        Output('user-avatar-button', 'title'),
        Input('sign-out-option', 'n_clicks'),
        prevent_initial_call=True
    )
    def handle_sign_out(n_clicks):
        if n_clicks:
            print("🚪 User signed out")
            return "Signed out"
        return "User Avatar"

    print("✅ Profile controller callbacks registered successfully!")


# Helper functions for creating content
def create_default_manage_content():
    """Create the default manage account content with pattern matching callbacks."""
    return [
        # Header
        html.Div([
            html.H3("Manage Account", style={
                'fontSize': '1.4rem', 'fontWeight': '700', 'color': COLORS['dark'], 'margin': '0'
            }),
            html.Button("×", 
                id={'type': 'close-btn', 'index': 'manage'}, 
                n_clicks=0, 
                style={
                    'position': 'absolute', 'top': '15px', 'right': '15px',
                    'background': 'none', 'border': 'none', 'fontSize': '1.5rem',
                    'cursor': 'pointer', 'color': COLORS['dark']
                }
            )
        ], style={'position': 'relative', 'marginBottom': '20px'}),
        
        # User Info
        html.Div([
            html.Div("N", style={
                'width': '60px', 'height': '60px', 'borderRadius': '50%',
                'backgroundColor': COLORS['primary'], 'color': 'white',
                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                'fontWeight': '600', 'fontSize': '1.5rem', 'margin': '0 auto 15px'
            }),
            html.H4("nom et prenom", style={
                'fontSize': '1.2rem', 'fontWeight': '600', 'color': COLORS['dark'],
                'margin': '0 0 5px 0', 'textAlign': 'center'
            }),
            html.P("nom et prenom@bankdash.com", style={
                'fontSize': '0.9rem', 'color': COLORS['dark'], 'opacity': '0.7',
                'margin': '0 0 20px 0', 'textAlign': 'center'
            })
        ]),
        
        # Menu buttons using pattern matching
        html.Div([
            html.Button([
                html.Span("👤", style={'marginRight': '10px'}),
                html.Span("Edit Profile")
            ], 
            id={'type': 'manage-btn', 'index': 'edit'}, 
            n_clicks=0, 
            style=get_button_style()),
            
            html.Button([
                html.Span("🔒", style={'marginRight': '10px'}),
                html.Span("Change Password")
            ], 
            id={'type': 'manage-btn', 'index': 'password'}, 
            n_clicks=0, 
            style=get_button_style()),
            
            html.Button([
                html.Span("🔗", style={'marginRight': '10px'}),
                html.Span("Connected Accounts")
            ], 
            id={'type': 'manage-btn', 'index': 'accounts'}, 
            n_clicks=0, 
            style=get_button_style()),
            
            html.Button([
                html.Span("🔔", style={'marginRight': '10px'}),
                html.Span("Notification Settings")
            ], 
            id={'type': 'manage-btn', 'index': 'notifications'}, 
            n_clicks=0, 
            style=get_button_style()),
            
            html.Hr(style={'margin': '15px 0'}),
            
            html.Button([
                html.Span("🚪", style={'marginRight': '10px'}),
                html.Span("Sign Out")
            ], style={
                **get_button_style(),
                'color': COLORS['danger'],
                'border': f'1px solid {COLORS["danger"]}'
            })
        ])
    ]


def create_edit_profile_form():
    """Create edit profile form."""
    return [
        html.Div([
            html.Button("← Back", 
                id={'type': 'back-btn', 'index': 'edit'}, 
                n_clicks=0, 
                style={
                    'background': 'none', 'border': 'none', 'color': COLORS['primary'],
                    'cursor': 'pointer', 'fontSize': '0.9rem', 'padding': '0', 'marginBottom': '10px'
                }
            ),
            html.H3("Edit Profile", style={
                'fontSize': '1.4rem', 'fontWeight': '700', 'color': COLORS['dark'], 'margin': '0'
            }),
            html.Button("×", 
                id={'type': 'close-btn', 'index': 'edit'}, 
                n_clicks=0, 
                style={
                    'position': 'absolute', 'top': '15px', 'right': '15px',
                    'background': 'none', 'border': 'none', 'fontSize': '1.5rem',
                    'cursor': 'pointer', 'color': COLORS['dark']
                }
            )
        ], style={'position': 'relative', 'marginBottom': '20px'}),
        
        html.Div([
            html.Label("Full Name", style=get_label_style()),
            dcc.Input(value="nom et prenom", style=get_input_style()),
            
            html.Label("Email", style=get_label_style()),
            dcc.Input(value="nom et prenom@bankdash.com", style=get_input_style()),
            
            html.Label("Phone", style=get_label_style()),
            dcc.Input(value="+216 12 345 678", style=get_input_style(last=True)),
            
            html.Button("Save Changes", style={
                'width': '100%', 'padding': '12px', 'backgroundColor': COLORS['primary'],
                'color': 'white', 'border': 'none', 'borderRadius': '6px',
                'fontSize': '0.95rem', 'fontWeight': '600', 'cursor': 'pointer'
            })
        ])
    ]


def create_change_password_form():
    """Create change password form."""
    return [
        html.Div([
            html.Button("← Back", 
                id={'type': 'back-btn', 'index': 'password'}, 
                n_clicks=0, 
                style={
                    'background': 'none', 'border': 'none', 'color': COLORS['primary'],
                    'cursor': 'pointer', 'fontSize': '0.9rem', 'padding': '0', 'marginBottom': '10px'
                }
            ),
            html.H3("Change Password", style={
                'fontSize': '1.4rem', 'fontWeight': '700', 'color': COLORS['dark'], 'margin': '0'
            }),
            html.Button("×", 
                id={'type': 'close-btn', 'index': 'password'}, 
                n_clicks=0, 
                style={
                    'position': 'absolute', 'top': '15px', 'right': '15px',
                    'background': 'none', 'border': 'none', 'fontSize': '1.5rem',
                    'cursor': 'pointer', 'color': COLORS['dark']
                }
            )
        ], style={'position': 'relative', 'marginBottom': '20px'}),
        
        html.Div([
            html.Label("Current Password", style=get_label_style()),
            dcc.Input(type="password", placeholder="Enter current password", style=get_input_style()),
            
            html.Label("New Password", style=get_label_style()),
            dcc.Input(type="password", placeholder="Enter new password", style=get_input_style()),
            
            html.Label("Confirm New Password", style=get_label_style()),
            dcc.Input(type="password", placeholder="Confirm new password", style=get_input_style(last=True)),
            
            html.Button("Update Password", style={
                'width': '100%', 'padding': '12px', 'backgroundColor': COLORS['primary'],
                'color': 'white', 'border': 'none', 'borderRadius': '6px',
                'fontSize': '0.95rem', 'fontWeight': '600', 'cursor': 'pointer'
            })
        ])
    ]


def create_connected_accounts_view():
    """Create connected accounts view."""
    return [
        html.Div([
            html.Button("← Back", 
                id={'type': 'back-btn', 'index': 'accounts'}, 
                n_clicks=0, 
                style={
                    'background': 'none', 'border': 'none', 'color': COLORS['primary'],
                    'cursor': 'pointer', 'fontSize': '0.9rem', 'padding': '0', 'marginBottom': '10px'
                }
            ),
            html.H3("Connected Accounts", style={
                'fontSize': '1.4rem', 'fontWeight': '700', 'color': COLORS['dark'], 'margin': '0'
            }),
            html.Button("×", 
                id={'type': 'close-btn', 'index': 'accounts'}, 
                n_clicks=0, 
                style={
                    'position': 'absolute', 'top': '15px', 'right': '15px',
                    'background': 'none', 'border': 'none', 'fontSize': '1.5rem',
                    'cursor': 'pointer', 'color': COLORS['dark']
                }
            )
        ], style={'position': 'relative', 'marginBottom': '20px'}),
        
        html.Div([
            create_account_item("🔵", "Facebook", "Connected", True),
            create_account_item("⚫", "GitHub", "Not connected", False),
            create_account_item("🔴", "Google", "Connected", True)
        ])
    ]


def create_notification_settings_view():
    """Create notification settings view."""
    return [
        html.Div([
            html.Button("← Back", 
                id={'type': 'back-btn', 'index': 'notifications'}, 
                n_clicks=0, 
                style={
                    'background': 'none', 'border': 'none', 'color': COLORS['primary'],
                    'cursor': 'pointer', 'fontSize': '0.9rem', 'padding': '0', 'marginBottom': '10px'
                }
            ),
            html.H3("Notification Settings", style={
                'fontSize': '1.4rem', 'fontWeight': '700', 'color': COLORS['dark'], 'margin': '0'
            }),
            html.Button("×", 
                id={'type': 'close-btn', 'index': 'notifications'}, 
                n_clicks=0, 
                style={
                    'position': 'absolute', 'top': '15px', 'right': '15px',
                    'background': 'none', 'border': 'none', 'fontSize': '1.5rem',
                    'cursor': 'pointer', 'color': COLORS['dark']
                }
            )
        ], style={'position': 'relative', 'marginBottom': '20px'}),
        
        html.Div([
            html.H4("Email Notifications", style=get_heading_style()),
            dcc.Checklist(
                options=[
                    {"label": " Account activity", "value": "account"},
                    {"label": " Security alerts", "value": "security"},
                    {"label": " Marketing updates", "value": "marketing"},
                ],
                value=["account", "security"],
                style={'marginBottom': '20px'}
            ),
            
            html.H4("Push Notifications", style=get_heading_style()),
            dcc.Checklist(
                options=[
                    {"label": " Real-time alerts", "value": "realtime"},
                    {"label": " Daily summaries", "value": "daily"},
                ],
                value=["realtime"],
                style={'marginBottom': '20px'}
            ),
            
            html.Button("Save Preferences", style={
                'width': '100%', 'padding': '12px', 'backgroundColor': COLORS['primary'],
                'color': 'white', 'border': 'none', 'borderRadius': '6px',
                'fontSize': '0.95rem', 'fontWeight': '600', 'cursor': 'pointer'
            })
        ])
    ]


def create_connect_card_content():
    """Create connect card content."""
    return [
        html.Div([
            html.H3("Connect Your Account", style={
                'fontSize': '1.4rem', 'fontWeight': '700', 'color': COLORS['dark'], 'margin': '0'
            }),
            html.Button("×", 
                id={'type': 'close-connect-btn', 'index': 'main'}, 
                n_clicks=0, 
                style={
                    'position': 'absolute', 'top': '15px', 'right': '15px',
                    'background': 'none', 'border': 'none', 'fontSize': '1.5rem',
                    'cursor': 'pointer', 'color': COLORS['dark']
                }
            )
        ], style={'position': 'relative', 'marginBottom': '20px'}),
        
        html.Div([
            html.Label("Email:", style=get_label_style()),
            dcc.Input(type="email", placeholder="Enter your email", style=get_input_style()),
            
            html.Label("Password:", style=get_label_style()),
            dcc.Input(type="password", placeholder="Enter your password", style=get_input_style()),
            
            html.Button("Sign In", style={
                'width': '100%', 'padding': '12px', 'backgroundColor': COLORS['primary'],
                'color': 'white', 'border': 'none', 'borderRadius': '5px',
                'fontSize': '1rem', 'fontWeight': '600', 'cursor': 'pointer', 'marginBottom': '20px'
            }),
            
            html.Hr(style={'margin': '20px 0'}),
            html.H4("Or continue with:", style={'textAlign': 'center', 'margin': '20px 0 15px 0'}),
            
            create_social_button("🔵", "Facebook", COLORS['primary']),
            create_social_button("⚫", "GitHub", COLORS['dark']),
            create_social_button("🔴", "Google", COLORS['danger'])
        ])
    ]


def create_simple_profile_content():
    """Create the full profile page content."""
    return html.Div([
        html.H1("👤 User Profile", style={
            'fontSize': '2.5rem', 'color': COLORS['primary'], 
            'textAlign': 'center', 'marginBottom': '30px'
        }),
        
        html.Div([
            html.Div("N", style={
                'width': '150px', 'height': '150px', 'borderRadius': '50%',
                'backgroundColor': COLORS['primary'], 'color': 'white',
                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                'fontSize': '4rem', 'fontWeight': '700', 'margin': '0 auto 30px',
                'boxShadow': '0 10px 30px rgba(30, 64, 175, 0.3)'
            })
        ]),
        
        html.Div([
            html.H2("nom et prenom", style={
                'textAlign': 'center', 'color': COLORS['dark'], 'marginBottom': '10px'
            }),
            html.P("Senior Banking Analyst", style={
                'textAlign': 'center', 'fontSize': '1.2rem', 
                'color': COLORS['primary'], 'marginBottom': '20px'
            }),
            html.P("📧 nom et prenom@bankdash.com | 📞 +216 12 345 678", style={
                'textAlign': 'center', 'opacity': '0.8'
            })
        ], style={'marginBottom': '40px'}),
        
        html.Div([
            create_info_section("📋 Personal Information", [
                "📧 Email: nom et prenom@bankdash.com",
                "📞 Phone: +216 12 345 678",
                "📍 Location: Tunis, Tunisia",
                "🏢 Department: Risk Analysis"
            ]),
            create_info_section("📊 Account Statistics", [
                "📈 Account Age: 2.5 Years",
                "💰 Total Transactions: 1,247",
                "🔒 Security Score: 98%",
                "⭐ Loyalty Points: 15,670"
            ])
        ], style={'maxWidth': '800px', 'margin': '0 auto'}),
        
        html.Div([
            html.H2("✅ Profile Loaded Successfully!", style={
                'color': COLORS['success'], 'textAlign': 'center', 'marginTop': '40px'
            })
        ])
    ], style={'padding': '40px', 'backgroundColor': COLORS['light'], 'minHeight': '100vh'})


# Utility functions for consistent styling
def get_button_style():
    """Get consistent button style."""
    return {
        'width': '100%', 'padding': '12px', 'margin': '5px 0',
        'backgroundColor': 'transparent', 'border': f'1px solid {COLORS["hover"]}',
        'borderRadius': '8px', 'cursor': 'pointer', 'fontSize': '0.95rem',
        'display': 'flex', 'alignItems': 'center', 'justifyContent': 'flex-start',
        'transition': 'all 0.2s ease'
    }


def get_label_style():
    """Get consistent label style."""
    return {
        'fontSize': '0.9rem', 'fontWeight': '600', 'color': COLORS['dark'], 
        'marginBottom': '5px', 'display': 'block'
    }


def get_input_style(last=False):
    """Get consistent input style."""
    return {
        'width': '100%', 'padding': '10px', 'border': f'1px solid {COLORS["hover"]}',
        'borderRadius': '6px', 'fontSize': '0.9rem', 
        'marginBottom': '20px' if last else '15px'
    }


def get_heading_style():
    """Get consistent heading style."""
    return {
        'fontSize': '1rem', 'fontWeight': '600', 'color': COLORS['dark'], 
        'marginBottom': '10px'
    }


def create_account_item(icon, name, status, connected):
    """Create a connected account item."""
    return html.Div([
        html.Div([
            html.Span(icon, style={'fontSize': '1.5rem', 'marginRight': '12px'}),
            html.Div([
                html.Div(name, style={'fontWeight': '600', 'fontSize': '0.95rem'}),
                html.Div(status, style={
                    'fontSize': '0.8rem', 
                    'color': COLORS['success'] if connected else COLORS['dark'],
                    'opacity': '1' if connected else '0.6'
                })
            ])
        ], style={'display': 'flex', 'alignItems': 'center', 'flex': '1'}),
        html.Button(
            "Disconnect" if connected else "Connect", 
            style={
                'padding': '6px 12px', 
                'backgroundColor': COLORS['danger'] if connected else COLORS['primary'], 
                'color': 'white', 'border': 'none', 'borderRadius': '4px', 
                'fontSize': '0.8rem', 'cursor': 'pointer'
            }
        )
    ], style={
        'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 
        'padding': '15px', 'border': f'1px solid {COLORS["hover"]}', 
        'borderRadius': '8px', 'marginBottom': '10px'
    })


def create_social_button(icon, name, color):
    """Create a social login button."""
    return html.Button([
        html.Span(icon, style={'marginRight': '10px', 'fontSize': '1.1rem'}),
        html.Span(f"Continue with {name}")
    ], style={
        'width': '100%', 'padding': '10px', 'margin': '5px 0',
        'backgroundColor': 'white', 'color': color, 
        'border': f'2px solid {color}', 'borderRadius': '5px', 
        'cursor': 'pointer', 'display': 'flex', 'alignItems': 'center', 
        'justifyContent': 'center'
    })


def create_info_section(title, items):
    """Create an information section."""
    return html.Div([
        html.H3(title, style={'color': COLORS['dark'], 'marginBottom': '20px'}),
        html.Div([
            html.P(item) for item in items
        ])
    ], style={
        'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '15px',
        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)', 'marginBottom': '20px'
    })