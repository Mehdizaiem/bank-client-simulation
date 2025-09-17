"""
components/header.py – Fixed header with consistent auth callback structure
Replace your header.py with this version
"""
from dash import html, dcc
from config.colors import COLORS

def create_top_header():
    return html.Div([
        html.Header([
            html.Div([
                # Left (reserved for title/crumbs if you add later)
                html.Div([], style={"flex": "2"}),

                # Right (search + auth area) - This will be replaced by auth callbacks
                html.Div(id="header-user-section", children=[
                    # Default content (will be replaced by auth callback)
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
                        style={
                            "padding": "10px 20px", 
                            "backgroundColor": COLORS["primary"], 
                            "color": "white",
                            "border": "none", 
                            "borderRadius": "25px", 
                            "cursor": "pointer",
                            "fontSize": "0.9rem", 
                            "fontWeight": "600",
                            "marginRight": "10px",
                        },
                    ),

                    html.Div("N", style={
                        "width": "35px", 
                        "height": "35px", 
                        "borderRadius": "50%", 
                        "backgroundColor": COLORS["secondary"],
                        "color": "white", 
                        "display": "flex", 
                        "alignItems": "center", 
                        "justifyContent": "center",
                        "fontWeight": "600",
                        "fontSize": "0.9rem",
                    }),
                ], style={"display": "flex", "alignItems": "center"}),
            ], style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
                "padding": "10px 20px",
            }),
        ], style={
            "backgroundColor": "var(--card-bg, white)",
            "borderBottom": f"1px solid {COLORS['hover']}",
            "boxShadow": "0 1px 3px rgba(0,0,0,0.05)",
            "position": "relative",
            "zIndex": "999",
            "height": "60px",
        }),
    ])