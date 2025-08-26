"""
Chart components and callback functions for Bank Client Simulation Platform
"""
import plotly.graph_objs as go
import plotly.express as px
from dash import html, dcc, Input, Output, State
from config.colors import COLORS, CHART_COLORS
from services.data_service import DataService


def create_chart_container(chart_id, title, width="48%", height="400px"):
    """Create a standardized chart container."""
    return html.Div([
        html.H4(title, style={
            'color': COLORS['dark'], 
            'marginBottom': '15px', 
            'fontSize': '1.1rem',
            'fontWeight': '600',
            'textAlign': 'center'
        }),
        dcc.Graph(
            id=chart_id, 
            config={
                'displayModeBar': False, 
                'staticPlot': False
            },
            style={'height': '300px'}
        )
    ], style={
        'width': width, 
        'padding': '20px', 
        'backgroundColor': 'white', 
        'borderRadius': '12px', 
        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
        'border': f'1px solid {COLORS["hover"]}',
        'margin': '10px',
        'minHeight': height,
        'display': 'flex',
        'flexDirection': 'column'
    })


def create_simulation_charts():
    """Create simulation-specific charts layout."""
    return html.Div([
        # Row 1: Agent Behavior + Market Response
        html.Div([
            create_chart_container("agent-behavior-chart", "Agent Behavior Patterns"),
            create_chart_container("market-response-chart", "Market Response Simulation")
        ], style={
            'display': 'flex', 
            'gap': '20px', 
            'marginBottom': '30px',
            'justifyContent': 'space-between',
            'alignItems': 'stretch'
        }),

        # Row 2: Geographic Distribution + Scenario Results
        html.Div([
            create_chart_container("tunisia-heatmap-chart", "Client Distribution Heatmap"),
            create_chart_container("scenario-impact-chart", "Scenario Impact Analysis")
        ], style={
            'display': 'flex', 
            'gap': '20px',
            'justifyContent': 'space-between',
            'alignItems': 'stretch'
        })
    ], style={
        'width': '100%',
        'maxWidth': '1400px',
        'margin': '0 auto'
    })


def create_economic_charts():
    """Create economic analysis charts layout."""
    return html.Div([
        # Row 1: Economic trends and Client Response
        html.Div([
            create_chart_container("economic-scenario-impact", "Economic Scenario Impact"),
            create_chart_container("client-economic-response", "Client Behavior Response")
        ], style={
            'display': 'flex', 
            'gap': '20px', 
            'marginBottom': '30px',
            'justifyContent': 'space-between',
            'alignItems': 'stretch'
        }),

        # Row 2: Regional Impact and Portfolio Effects
        html.Div([
            create_chart_container("regional-economic-impact", "Regional Economic Impact"),
            create_chart_container("portfolio-risk-analysis", "Portfolio Risk Analysis")
        ], style={
            'display': 'flex', 
            'gap': '20px',
            'justifyContent': 'space-between',
            'alignItems': 'stretch'
        })
    ], style={
        'width': '100%',
        'maxWidth': '1400px',
        'margin': '0 auto'
    })


def create_geographic_charts():
    """Create geographic analysis charts layout."""
    return html.Div([
        # Row 1: Branch Impact Simulation
        html.Div([
            create_chart_container("branch-impact-simulation", "Branch Strategy Impact Simulation"),
            create_chart_container("client-migration-chart", "Client Migration Patterns")
        ], style={
            'display': 'flex', 
            'gap': '20px', 
            'marginBottom': '30px',
            'justifyContent': 'space-between',
            'alignItems': 'stretch'
        }),

        # Row 2: Market Share and Competitive Analysis
        html.Div([
            create_chart_container("market-share-governorate", "Market Share by Governorate"),
            create_chart_container("competitive-positioning", "Competitive Positioning")
        ], style={
            'display': 'flex', 
            'gap': '20px',
            'justifyContent': 'space-between',
            'alignItems': 'stretch'
        })
    ], style={
        'width': '100%',
        'maxWidth': '1400px',
        'margin': '0 auto'
    })


def get_standard_chart_layout(title, xaxis_title, yaxis_title, height=300, width=None):
    """Get standardized chart layout configuration."""
    return {
        'title': {
            'text': title,
            'x': 0.5,
            'font': {'size': 14, 'color': COLORS['dark']}
        },
        'xaxis': {
            'title': xaxis_title,
            'fixedrange': True,
            'showgrid': True,
            'gridcolor': '#f0f0f0'
        },
        'yaxis': {
            'title': yaxis_title,
            'fixedrange': True,
            'showgrid': True,
            'gridcolor': '#f0f0f0'
        },
        'height': height,
        'width': width,
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',
        'margin': dict(l=60, r=30, t=60, b=60),
        'font': dict(size=11, color=COLORS['dark']),
        'showlegend': True,
        'legend': dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    }


# ==================== CHART CALLBACK FUNCTIONS ====================

def register_home_chart_callbacks(app):
    """Register all home page chart callbacks."""
    
    @app.callback(
        Output('agent-behavior-chart', 'figure'),
        [Input('sim-client-filter', 'value'),
         Input('sim-region-filter', 'value')]
    )
    def update_agent_behavior_chart(client_filter, region_filter):
        """Update agent behavior patterns chart."""
        time_steps, behavior_data = DataService.get_agent_behavior_data(client_filter, region_filter)
        
        fig = go.Figure()
        colors = [COLORS['primary'], COLORS['success'], COLORS['warning'], COLORS['danger']]
        
        for i, (behavior, values) in enumerate(behavior_data.items()):
            fig.add_trace(go.Scatter(
                x=time_steps,
                y=values,
                mode='lines+markers',
                name=behavior,
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=8)
            ))
        
        layout = get_standard_chart_layout(
            "AI Agent Behavior Patterns Over Time",
            "Time Period",
            "Behavior Index"
        )
        layout.update({
            'yaxis': dict(range=[0, 100], fixedrange=True, showgrid=True, gridcolor='#f0f0f0'),
            'xaxis': dict(fixedrange=True, showgrid=True, gridcolor='#f0f0f0'),
            'hovermode': 'x unified',
            'plot_bgcolor': 'white',
            'paper_bgcolor': 'white'
        })
        
        fig.update_layout(layout)
        return fig

    @app.callback(
        Output('market-response-chart', 'figure'),
        Input('sim-client-filter', 'value')
    )
    def update_market_response_chart(client_filter):
        """Update market response simulation chart."""
        events, responses = DataService.get_market_response_data()
        
        fig = go.Figure(data=[
            go.Bar(
                x=events,
                y=responses,
                marker_color=COLORS['secondary'],
                text=[f"{r:.1f}x" for r in responses],
                textposition='auto'
            )
        ])
        
        layout = get_standard_chart_layout(
            "Market Response to Events",
            "Event Type",
            "Response Multiplier"
        )
        layout.update({
            'yaxis': dict(range=[0, 3], fixedrange=True),
            'xaxis': dict(fixedrange=True)
        })
        
        fig.update_layout(layout)
        return fig

    @app.callback(
        Output('tunisia-heatmap-chart', 'figure'),
        [Input('sim-region-filter', 'value')]
    )
    def update_tunisia_heatmap(region_filter):
        """Update Tunisia client distribution heatmap."""
        governorates, agent_counts = DataService.get_agent_distribution_data(region_filter)
        
        fig = go.Figure(data=[
            go.Bar(
                x=governorates,
                y=agent_counts,
                marker_color=COLORS['accent'],
                text=[f"{count:,}" for count in agent_counts],
                textposition='auto'
            )
        ])
        
        layout = get_standard_chart_layout(
            "Client Distribution by Governorate",
            "Governorate",
            "Number of Clients"
        )
        layout.update({
            'yaxis': dict(range=[0, 6000], fixedrange=True),
            'xaxis': dict(fixedrange=True, tickangle=-45),
            'margin': dict(l=50, r=30, t=50, b=80)
        })
        
        fig.update_layout(layout)
        return fig

    @app.callback(
        Output('scenario-impact-chart', 'figure'),
        Input('sim-client-filter', 'value')
    )
    def update_scenario_impact_chart(client_filter):
        """Update scenario impact analysis chart."""
        scenarios, impacts = DataService.get_scenario_impact_data()
        
        colors = [COLORS['success'] if impact > 0 else COLORS['danger'] for impact in impacts]
        
        fig = go.Figure(data=[
            go.Bar(
                x=scenarios,
                y=impacts,
                marker_color=colors,
                text=[f"{impact:+.1f}%" for impact in impacts],
                textposition='auto'
            )
        ])
        
        layout = get_standard_chart_layout(
            "Scenario Impact Analysis",
            "Scenario Type",
            "Impact (%)"
        )
        layout.update({
            'yaxis': dict(range=[-20, 30], fixedrange=True),
            'xaxis': dict(fixedrange=True, tickangle=-45),
            'margin': dict(l=50, r=30, t=50, b=80)
        })
        
        fig.update_layout(layout)
        return fig


def register_economic_chart_callbacks(app):
    """Register all economic page chart callbacks."""
    
    @app.callback(
        Output('economic-scenario-impact', 'figure'),
        [Input('economic-sim-btn', 'n_clicks')],
        [State('economic-event-type', 'value'),
         State('economic-severity', 'value'),
         State('economic-time-horizon', 'value')]
    )
    def update_economic_scenario_impact(n_clicks, event_type, severity, time_horizon):
        """Update economic scenario impact chart."""
        time_data, scenario_impact = DataService.get_economic_scenario_data(event_type, severity, time_horizon)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_data,
            y=scenario_impact,
            mode='lines+markers',
            name='Economic Impact',
            line=dict(color=COLORS['primary'], width=3),
            marker=dict(size=10)
        ))
        
        layout = get_standard_chart_layout(
            f"Economic Scenario: {event_type.title()} Impact",
            "Time Period",
            "Impact Index (Base = 100)",
            height=280
        )
        layout.update({
            'yaxis': dict(range=[70, 130]),
            'width': None
        })
        
        fig.update_layout(layout)
        return fig

    @app.callback(
        Output('client-economic-response', 'figure'),
        [Input('economic-sim-btn', 'n_clicks')],
        [State('economic-event-type', 'value')]
    )
    def update_client_economic_response(n_clicks, event_type):
        """Update client economic response chart."""
        segments, responses = DataService.get_client_economic_response_data(event_type)
        
        colors = [COLORS['success'] if r > 1.0 else COLORS['danger'] for r in responses]
        
        fig = go.Figure(data=[
            go.Bar(
                x=segments,
                y=responses,
                marker_color=colors,
                text=[f"{r:.2f}x" for r in responses],
                textposition='auto'
            )
        ])
        
        layout = get_standard_chart_layout(
            "Client Segment Response to Economic Event",
            "Client Segment",
            "Response Factor",
            height=280
        )
        layout.update({
            'yaxis': dict(range=[0.5, 1.5]),
            'width': None
        })
        
        fig.update_layout(layout)
        return fig

    @app.callback(
        Output('regional-economic-impact', 'figure'),
        [Input('economic-sim-btn', 'n_clicks')],
        [State('economic-event-type', 'value')]
    )
    def update_regional_economic_impact(n_clicks, event_type):
        """Update regional economic impact chart."""
        regions, impacts = DataService.get_regional_economic_impact_data(event_type)
        
        fig = go.Figure(data=[
            go.Bar(
                x=regions,
                y=impacts,
                marker_color=COLORS['secondary'],
                text=[f"{impact:.2f}" for impact in impacts],
                textposition='auto'
            )
        ])
        
        layout = get_standard_chart_layout(
            "Regional Economic Impact",
            "Region",
            "Impact Factor",
            height=280
        )
        layout.update({
            'yaxis': dict(range=[0.5, 1.5]),
            'xaxis': dict(tickangle=-45),
            'margin': dict(l=50, r=30, t=50, b=80),
            'width': None
        })
        
        fig.update_layout(layout)
        return fig

    @app.callback(
        Output('portfolio-risk-analysis', 'figure'),
        [Input('economic-sim-btn', 'n_clicks')],
        [State('economic-event-type', 'value')]
    )
    def update_portfolio_risk_analysis(n_clicks, event_type):
        """Update portfolio risk analysis chart."""
        risk_categories, risk_levels = DataService.get_portfolio_risk_data(event_type)
        
        fig = go.Figure(data=[
            go.Scatterpolar(
                r=risk_levels,
                theta=risk_categories,
                fill='toself',
                name='Risk Level',
                line=dict(color=COLORS['danger'])
            )
        ])
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 2]
                )),
            title="Portfolio Risk Assessment",
            height=280,
            width=None,
            margin=dict(l=50, r=30, t=50, b=40),
            font=dict(size=11)
        )
        
        return fig


def register_geographic_chart_callbacks(app):
    """Register all geographic page chart callbacks."""
    
    @app.callback(
        Output('tunisia-interactive-map', 'figure'),
        [Input('map-view-type', 'value'),
         Input('map-overlays', 'value')]
    )
    def update_tunisia_map(view_type, overlays):
        """Update interactive Tunisia map."""
        map_data = DataService.get_tunisia_map_data(view_type)
        
        fig = go.Figure(data=go.Scatter(
            x=[i for i in range(len(map_data['governorates']))],
            y=map_data['values'],
            mode='markers',
            marker=dict(
                size=[v/100 for v in map_data['values']],
                color=map_data['values'],
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title=map_data['metric'])
            ),
            text=map_data['governorates'],
            textposition="middle center"
        ))
        
        fig.update_layout(
            title=f"Tunisia Map - {map_data['metric']}",
            xaxis_title="Geographic Distribution",
            yaxis_title=map_data['metric'],
            height=350,
            width=None,
            plot_bgcolor='white',
            margin=dict(l=50, r=30, t=50, b=40),
            font=dict(size=11),
            yaxis=dict(range=[0, max(map_data['values']) * 1.1])
        )
        
        return fig


def register_all_chart_callbacks(app):
    """Register all chart callbacks with the app."""
    register_home_chart_callbacks(app)
    register_economic_chart_callbacks(app)
    register_geographic_chart_callbacks(app)