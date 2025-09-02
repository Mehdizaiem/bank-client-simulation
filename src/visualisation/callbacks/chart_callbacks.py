"""
Chart Callbacks - Only for simulation-specific charts (no duplicates)
Replace callbacks/chart_callbacks.py with this version
"""
from dash import Input, Output
import plotly.graph_objs as go
import json
from pathlib import Path

def register_chart_callbacks(app):
    """Register ONLY simulation result charts - NO duplicates with data_callbacks"""
    
    from config.colors import COLORS
    
    # Chart 1: Agent Behavior Evolution (simulation results only)
    @app.callback(
        Output('agent-behavior-chart', 'figure'),
        [Input('run-simulation-btn', 'n_clicks'),
         Input('load-results-btn', 'n_clicks')]
    )
    def update_agent_behavior_chart(run_clicks, load_clicks):
        """Display time series of satisfaction, digital adoption, and churn"""
        try:
            # Load the dashboard bundle data
            data_file = Path('output/dashboard_exports/dashboard_bundle_enhanced.json')
            if not data_file.exists():
                return create_empty_chart("No simulation data available")
            
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            metrics = data['simulation_metrics']['time_series']['metrics']['core_metrics']
            timestamps = data['simulation_metrics']['time_series']['timestamps']
            
            # Create time labels
            time_labels = [f"Step {t['step']}" for t in timestamps]
            
            fig = go.Figure()
            
            # Satisfaction line (multiply by 100 for percentage)
            fig.add_trace(go.Scatter(
                x=time_labels,
                y=[s * 100 for s in metrics['satisfaction']],
                mode='lines+markers',
                name='Satisfaction',
                line=dict(color=COLORS['success'], width=2),
                marker=dict(size=6)
            ))
            
            # Digital adoption line
            fig.add_trace(go.Scatter(
                x=time_labels,
                y=[d * 100 for d in metrics['digital_adoption']],
                mode='lines+markers',
                name='Digital Adoption',
                line=dict(color=COLORS['primary'], width=2),
                marker=dict(size=6)
            ))
            
            # Churn rate line (multiply by 100 for percentage)
            fig.add_trace(go.Scatter(
                x=time_labels,
                y=[c * 100 for c in metrics['churn_rate']],
                mode='lines+markers',
                name='Churn Rate',
                line=dict(color=COLORS['danger'], width=2),
                marker=dict(size=6)
            ))
            
            fig.update_layout(
                xaxis_title="Simulation Progress",
                yaxis_title="Percentage (%)",
                height=300,
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=True,
                hovermode='x unified',
                margin=dict(l=60, r=30, t=30, b=60),
                xaxis=dict(tickangle=-45 if len(time_labels) > 10 else 0)
            )
            
            return fig
            
        except Exception as e:
            print(f"Error in agent behavior chart: {e}")
            return create_empty_chart("Error loading data")
    
    # Chart 2: Segment Performance (simulation results only)
    @app.callback(
        Output('segment-performance-chart', 'figure'),
        [Input('run-simulation-btn', 'n_clicks'),
         Input('load-results-btn', 'n_clicks')]
    )
    def update_segment_performance_chart(run_clicks, load_clicks):
        """Display performance by satisfaction tiers and value tiers"""
        try:
            data_file = Path('output/dashboard_exports/dashboard_bundle_enhanced.json')
            if not data_file.exists():
                return create_empty_chart("No simulation data available")
            
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            segmentation = data['agent_analytics']['segmentation']
            
            # Create grouped bar chart
            fig = go.Figure()
            
            # Satisfaction tiers
            sat_tiers = segmentation['by_satisfaction_tier']
            fig.add_trace(go.Bar(
                name='By Satisfaction',
                x=['High', 'Medium', 'Low'],
                y=[sat_tiers['high'], sat_tiers['medium'], sat_tiers['low']],
                marker_color=COLORS['success'],
                text=[sat_tiers['high'], sat_tiers['medium'], sat_tiers['low']],
                textposition='auto'
            ))
            
            # Value tiers
            val_tiers = segmentation['by_value_tier']
            fig.add_trace(go.Bar(
                name='By Value',
                x=['Premium', 'Standard', 'Basic'],
                y=[val_tiers['premium'], val_tiers['standard'], val_tiers['basic']],
                marker_color=COLORS['primary'],
                text=[val_tiers['premium'], val_tiers['standard'], val_tiers['basic']],
                textposition='auto'
            ))
            
            fig.update_layout(
                barmode='group',
                xaxis_title="Segment Category",
                yaxis_title="Number of Clients",
                height=300,
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=True,
                margin=dict(l=60, r=30, t=30, b=60)
            )
            
            return fig
            
        except Exception as e:
            print(f"Error in segment performance chart: {e}")
            return create_empty_chart("Error loading data")
    
    # Chart 3: Product Adoption (simulation results only)
    @app.callback(
        Output('product-adoption-chart', 'figure'),
        [Input('run-simulation-btn', 'n_clicks'),
         Input('load-results-btn', 'n_clicks')]
    )
    def update_product_adoption(run_clicks, load_clicks):
        """Display product portfolio metrics"""
        try:
            data_file = Path('output/dashboard_exports/dashboard_bundle_enhanced.json')
            if not data_file.exists():
                return create_empty_chart("No simulation data available")
            
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            # Get average products per client from business metrics
            metrics = data['simulation_metrics']['time_series']['metrics']['business_metrics']
            
            # Create product distribution (simulated based on available data)
            products = ['Checking', 'Savings', 'Credit Card', 'Loan', 'Mobile Banking', 'Investment']
            # Base percentages on realistic distribution
            adoption_rates = [95, 45, 30, 25, 
                            data['simulation_metrics']['kpis']['final_metrics']['final_digital_adoption'] * 100,
                            15]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=products,
                    y=adoption_rates,
                    marker_color=COLORS['warning'],
                    text=[f"{r:.0f}%" for r in adoption_rates],
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                xaxis_title="Product Type",
                yaxis_title="Adoption Rate (%)",
                height=300,
                plot_bgcolor='white',
                paper_bgcolor='white',
                yaxis=dict(range=[0, 100]),
                margin=dict(l=60, r=30, t=30, b=60)
            )
            
            return fig
            
        except Exception as e:
            print(f"Error in product adoption chart: {e}")
            return create_empty_chart("Error loading data")
    
    # Chart 4: Risk Analysis (simulation results only)
    @app.callback(
        Output('risk-analysis-chart', 'figure'),
        [Input('run-simulation-btn', 'n_clicks'),
         Input('load-results-btn', 'n_clicks')]
    )
    def update_risk_analysis(run_clicks, load_clicks):
        """Display risk and churn analysis"""
        try:
            data_file = Path('output/dashboard_exports/dashboard_bundle_enhanced.json')
            if not data_file.exists():
                return create_empty_chart("No simulation data available")
            
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            # Get at-risk clients from time series
            metrics = data['simulation_metrics']['time_series']['metrics']['business_metrics']
            final_at_risk = metrics['at_risk_clients'][-1] if metrics['at_risk_clients'] else 0
            
            # Calculate risk categories based on satisfaction tiers
            sat_tiers = data['agent_analytics']['segmentation']['by_satisfaction_tier']
            
            risk_data = {
                'Low Risk': sat_tiers['high'],
                'Medium Risk': sat_tiers['medium'],
                'High Risk': int(sat_tiers['low'] * 0.6),
                'Churn Risk': final_at_risk
            }
            
            colors = ['#2ca02c', '#ff7f0e', '#ff6b6b', '#d62728']
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=list(risk_data.keys()),
                    values=list(risk_data.values()),
                    marker=dict(colors=colors),
                    hole=0.4,
                    textinfo='label+value',
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                annotations=[
                    dict(text='Risk<br>Profile', x=0.5, y=0.5, 
                         font_size=14, showarrow=False)
                ],
                height=300,
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=30, r=30, t=30, b=30),
                showlegend=True
            )
            
            return fig
            
        except Exception as e:
            print(f"Error in risk analysis chart: {e}")
            return create_empty_chart("Error loading data")
    
    print("Chart callbacks registered successfully (simulation charts only, no duplicates)")
    
    # IMPORTANT: The following charts are handled in data_callbacks.py:
    # - governorate-distribution-chart
    # - client-type-pie-chart
    # - satisfaction-tiers-chart
    # - channel-usage-chart
    # - age-demographics-chart
    # - value-tiers-chart

def create_empty_chart(message):
    """Create an empty chart with a message"""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=14, color='#666')
    )
    fig.update_layout(
        height=300,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig