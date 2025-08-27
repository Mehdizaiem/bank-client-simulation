"""
components/header.py — header shell (page title stays owned by navigation)
Drop this into src/visualisation/components/header.py
"""
from dash import html, dcc
from config.colors import COLORS


def create_top_header():
    return html.Div([
        html.Header([
            html.Div([
                # Title (navigation callbacks may update this elsewhere)
                html.Div([
                    html.H1(id="page-title", children="Dashboard Overview", style={
                        "fontSize": "1.8rem", "fontWeight": "700", "color": COLORS["dark"], "margin": "0",
                    })
                ], style={"flex": "1"}),

                # Right side (search + auth area) — will be replaced by auth callbacks
                html.Div(id="header-user-section", children=[
                    html.Div([
                        dcc.Input(
                            id="global-search",
                            placeholder="Search simulations, scenarios...",
                            style={
                                "padding": "10px 15px",
                                "border": f'1px solid {COLORS["hover"]}',
                                "borderRadius": "25px",
                                "width": "300px",
                                "fontSize": "0.9rem",
                                "outline": "none",
                            },
                        )
                    ], style={"marginRight": "20px"}),

                    html.Button(
                        "Sign In",
                        id="login-button",
                        n_clicks=0,
                        type="button",  # important to prevent default submit behavior
                        style={
                            "padding": "10px 20px", "backgroundColor": COLORS["primary"], "color": "white",
                            "border": "none", "borderRadius": "25px", "cursor": "pointer",
                            "fontSize": "0.9rem", "fontWeight": "600", "marginRight": "15px",
                        },
                    ),

                    html.Div("N", style={
                        "width": "40px", "height": "40px", "borderRadius": "50%", "backgroundColor": COLORS["primary"],
                        "color": "white", "display": "flex", "alignItems": "center", "justifyContent": "center",
                        "fontWeight": "600", "fontSize": "1.1rem", "cursor": "pointer",
                    }),
                ], style={"display": "flex", "alignItems": "center"}),
            ], style={
                "display": "flex", "alignItems": "center", "justifyContent": "space-between", "padding": "15px 25px",
            }),
        ], style={
            "backgroundColor": "white", "borderBottom": f'1px solid {COLORS["hover"]}',
            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)", "position": "relative", "zIndex": "999",
        }),
    ])
