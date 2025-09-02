"""
components/header.py – Compact header with working user dropdown (single CSS file)
"""
from dash import html, dcc
from config.colors import COLORS

def create_top_header():
    return html.Div([
        html.Header([
            html.Div([
                # Left (reserved for title/crumbs if you add later)
                html.Div([], style={"flex": "2"}),

                # Right (search + auth area)
                html.Div(id="header-user-section", children=[
                    # Search
                    html.Div([
                        dcc.Input(
                            id="global-search",
                            placeholder="Search…",
                            style={
                                "padding": "6px 12px",
                                "border": "1px solid var(--hover-color)",
                                "borderRadius": "20px",
                                "width": "250px",
                                "fontSize": "0.85rem",
                                "outline": "none",
                                "backgroundColor": "var(--card-bg)",
                                "color": "var(--text-color)",
                            },
                        )
                    ], style={"marginRight": "12px"}),

                    # Sign-in button
                    html.Button(
                        "Sign In",
                        id="login-button",
                        n_clicks=0,
                        type="button",
                        style={
                            "padding": "6px 16px",
                            "backgroundColor": "var(--accent-color)",
                            "color": "white",
                            "border": "none",
                            "borderRadius": "20px",
                            "cursor": "pointer",
                            "fontSize": "0.85rem",
                            "fontWeight": "600",
                            "marginRight": "10px",
                        },
                    ),

                    # Avatar + dropdown (menu is hidden by default; callback toggles it)
                    html.Div([
                        html.Button(
                            "N",  # replace with an <img> if you have avatar URLs
                            id="user-menu-toggle",
                            n_clicks=0,
                            style={
                                "width": "32px",
                                "height": "32px",
                                "borderRadius": "50%",
                                "backgroundColor": "var(--accent-color)",
                                "color": "white",
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "fontWeight": "600",
                                "fontSize": "0.9rem",
                                "cursor": "pointer",
                                "border": "none"
                            }
                        ),

                        # Dropdown menu
                        html.Div(
                            id="user-menu",
                            className="menu-card",  # styled in layout.css
                            style={
                                "display": "none",
                                "position": "absolute",
                                "right": "0",
                                "top": "44px",
                                "zIndex": 3000
                            },
                            children=[
                                html.Div([
                                    html.Div("Nesrine", style={"fontWeight": "700"}),
                                    html.A("nesrinelouati62@gmail.com",
                                           href="mailto:nesrinelouati62@gmail.com",
                                           style={"fontSize": ".9rem", "opacity": .9})
                                ], style={"padding": "8px 10px", "marginBottom": 6}),
                                html.Hr(style={"border": "1px solid #eef2f7", "margin": "6px 0"}),
                                html.Button([html.I(className="fas fa-user"), "View Profile"],
                                            id="menu-profile-btn",
                                            style={"background": "transparent", "border": "none"}),
                                html.Button([html.I(className="fas fa-cog"), "Settings"],
                                            id="menu-settings-btn",
                                            style={"background": "transparent", "border": "none"}),
                                html.Button([html.I(className="fas fa-sign-out-alt"), "Sign Out"],
                                            id="menu-signout-btn",
                                            style={"color": "#EF4444", "background": "transparent", "border": "none"}),
                            ]
                        )
                    ], style={"position": "relative"})
                ], style={"display": "flex", "alignItems": "center"}),
            ], style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
                "padding": "10px 20px",
            }),
        ], style={
            "backgroundColor": "var(--card-bg)",
            "borderBottom": "1px solid var(--hover-color)",
            "boxShadow": "0 1px 3px rgba(0,0,0,0.05)",
            "position": "relative",
            "zIndex": "999",
            "height": "50px",
        }),
    ])
