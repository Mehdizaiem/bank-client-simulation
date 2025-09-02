"""
Geographic Callbacks for Regional Analysis using Real Data
"""
from dash import Input, Output, State, html,no_update
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from services.geographic_service import GeographicService
from config.colors import COLORS

def register_geographic_callbacks(app):
    """Register geographic analysis callbacks"""
    
    geo_service = GeographicService()
    
    @app.callback(
        Output('simulation-region', 'options'),
        Input('simulation-region', 'id')  # Trigger on page load
    )
    def populate_region_dropdown(_):
        """Populate region dropdown with actual data from your files"""
        try:
            available_regions = geo_service.get_available_regions()
            if available_regions:
                return [{'label': region, 'value': region.lower()} for region in available_regions]
            else:
                return [{'label': 'No regions found in your data', 'value': 'none', 'disabled': True}]
        except Exception as e:
            return [{'label': f'Error loading regions: {str(e)}', 'value': 'error', 'disabled': True}]
    
    @app.callback(
        Output('segment-analysis-results', 'children'),
        [Input('simulation-region', 'value'),
         Input('client-segment', 'value')]
    )
    def update_segment_analysis(region, segment):
        """Update segment analysis based on real data"""
        if not region or not segment:
            return html.P("Please select both region and client segment to see analysis", 
                         style={'textAlign': 'center', 'color': COLORS['secondary']})
        
        try:
            # Get filtered data
            analysis_data = geo_service.filter_by_region_and_segment(region, segment)
            
            if analysis_data.get('error'):
                return html.Div([
                    html.H4("Data Analysis Error", style={'color': '#ef4444'}),
                    html.P(analysis_data['error'], style={'color': COLORS['secondary']})
                ])
            
            # Create comprehensive analysis display
            return create_segment_analysis_display(analysis_data)
            
        except Exception as e:
            return html.Div([
                html.H4("Analysis Error", style={'color': '#ef4444'}),
                html.P(f"Error during analysis: {str(e)}", style={'color': COLORS['secondary']})
            ])

    @app.callback(
        [Output('geographic-simulation-results', 'children'),
         Output('market-opportunities-list', 'children'),
         Output('risk-factors-list', 'children'),
         Output('recommendations-list', 'children')],
        [Input('regional-simulation-btn', 'n_clicks')],
        [State('simulation-region', 'value'),
         State('client-segment', 'value'),
         State('scenario-type', 'value'),
         State('impact-intensity', 'value'),
         State('simulation-duration', 'value'),
         State('simulation-budget', 'value')]
    )
    def run_regional_simulation(n_clicks, region, segment, scenario, intensity, duration, budget):
        """Run regional simulation using real data"""
        if not n_clicks or not all([region, segment, scenario]):
            return no_update, no_update, no_update, no_update
        
        try:
            # Run simulation
            sim_results = geo_service.simulate_regional_scenario(
                region, segment, scenario, intensity, duration, budget
            )
            
            if not sim_results.get('success'):
                error_display = html.Div([
                    html.H4("Simulation Error", style={'color': '#ef4444'}),
                    html.P(sim_results.get('error', 'Unknown error'), 
                          style={'color': COLORS['secondary']})
                ])
                return error_display, [], [], []
            
            # Create results display
            results_display = create_simulation_results_display(sim_results)
            
            # Extract insights
            opportunities = create_opportunities_list(sim_results)
            risks = create_risk_factors_list(sim_results) 
            recommendations = create_recommendations_list(sim_results)
            
            return results_display, opportunities, risks, recommendations
            
        except Exception as e:
            error_display = html.Div([
                html.H4("Simulation Error", style={'color': '#ef4444'}),
                html.P(f"Error running simulation: {str(e)}", 
                      style={'color': COLORS['secondary']})
            ])
            return error_display, [], [], []

    @app.callback(
        Output('tunisia-choropleth-map', 'figure'),
        [Input('map-layer', 'value'),
         Input('map-overlays', 'value')]
    )
    def update_tunisia_map(selected_layer, overlays):
        """Update Tunisia choropleth map with real data"""
        try:
            # Get map data from real client distribution
            map_data = geo_service.get_tunisia_choropleth_data(selected_layer)
            
            if map_data.get('error'):
                # Return empty map with error message
                fig = go.Figure()
                fig.add_annotation(
                    text=f"Map Error: {map_data['error']}",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=16, color="red")
                )
                fig.update_layout(
                    title="Tunisia Banking Map - Error Loading Data",
                    height=600
                )
                return fig
            
            # Create choropleth map
            fig = create_tunisia_choropleth(map_data, selected_layer)
            
            # Add overlays if requested
            if overlays:
                fig = add_map_overlays(fig, overlays)
            
            return fig
            
        except Exception as e:
            # Return error map
            fig = go.Figure()
            fig.add_annotation(
                text=f"Map Error: {str(e)}",
                xref="paper", yref="paper", 
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(
                title="Tunisia Banking Map - Error",
                height=600
            )
            return fig

    @app.callback(
        [Output('regional-comparison-table', 'children'),
         Output('regional-performance-radar', 'figure'),
         Output('regional-growth-trends', 'figure')],
        [Input('compare-regions-btn', 'n_clicks')]
    )
    def update_regional_comparison(n_clicks):
        """Update regional comparison using real data"""
        if not n_clicks:
            return no_update, no_update, no_update
        
        try:
            # Get comparison data
            comparison_data = geo_service.get_regional_comparison_data()
            
            if comparison_data.get('error'):
                error_msg = html.Div([
                    html.H4("Comparison Error", style={'color': '#ef4444'}),
                    html.P(comparison_data['error'], style={'color': COLORS['secondary']})
                ])
                empty_fig = go.Figure()
                return error_msg, empty_fig, empty_fig
            
            # Create comparison table
            table = create_regional_comparison_table(comparison_data['comparison_data'])
            
            # Create radar chart
            radar_fig = create_regional_radar_chart(comparison_data['comparison_data'])
            
            # Create trends chart
            trends_fig = create_regional_trends_chart(comparison_data['comparison_data'])
            
            return table, radar_fig, trends_fig
            
        except Exception as e:
            error_msg = html.Div([
                html.H4("Comparison Error", style={'color': '#ef4444'}),
                html.P(f"Error: {str(e)}", style={'color': COLORS['secondary']})
            ])
            empty_fig = go.Figure()
            return error_msg, empty_fig, empty_fig


def create_segment_analysis_display(analysis_data):
    """Create comprehensive segment analysis display"""
    stats = analysis_data.get('statistics', {})
    insights = analysis_data.get('insights', [])
    total_agents = analysis_data.get('total_agents', 0)
    region_info = analysis_data.get('region_info', {})
    segment_info = analysis_data.get('segment_info', {})
    
    return html.Div([
        # Header with key metrics
        html.Div([
            html.H4(f"Analysis: {analysis_data['region'].title()} - {analysis_data['segment'].title()} Segment", 
                   style={'marginBottom': '20px', 'color': COLORS['dark']}),
            
            # Key metrics cards
            html.Div([
                create_analysis_card("Total Clients", f"{total_agents:,}", "Based on real data", COLORS['primary']),
                create_analysis_card("Region Info", f"{region_info.get('name', 'N/A')}", "Selected region", COLORS['success']),
                create_analysis_card("Data Quality", "Real Data", f"{len(stats)} metrics available", COLORS['accent']),
            ], style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
                'gap': '15px',
                'marginBottom': '25px'
            })
        ]),
        
        # Demographics section
        create_demographics_section(stats.get('demographics', {})),
        
        # Financial metrics section  
        create_financial_section(stats.get('financial', {})),
        
        # Behavioral patterns section
        create_behavioral_section(stats.get('behavioral', {})),
        
        # Insights section
        create_insights_section(insights),
        
        # Segment profile
        create_segment_profile_section(segment_info)
    ])

def create_analysis_card(title, value, subtitle, color):
    """Create analysis metric card"""
    return html.Div([
        html.H5(title, style={'fontSize': '1rem', 'fontWeight': '600', 'marginBottom': '8px'}),
        html.Div(value, style={'fontSize': '1.6rem', 'fontWeight': '700', 'color': color, 'marginBottom': '4px'}),
        html.Div(subtitle, style={'fontSize': '0.85rem', 'color': COLORS['secondary']})
    ], style={
        'backgroundColor': 'white',
        'padding': '18px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.06)',
        'textAlign': 'center',
        'border': f'2px solid {color}20'
    })

def create_demographics_section(demo_stats):
    """Create demographics analysis section"""
    if not demo_stats:
        return html.Div()
    
    age_stats = demo_stats.get('age', {})
    
    return html.Div([
        html.H5("Demographics Analysis", style={'fontSize': '1.2rem', 'fontWeight': '600', 'marginBottom': '15px'}),
        html.Div([
            html.Div([
                html.Strong("Age Distribution:"),
                html.Ul([
                    html.Li(f"Average Age: {age_stats.get('mean', 0):.1f} years"),
                    html.Li(f"Age Range: {age_stats.get('min', 0)} - {age_stats.get('max', 0)} years"),
                    html.Li(f"Age Standard Deviation: {age_stats.get('std', 0):.1f} years")
                ])
            ])
        ])
    ], style={
        'backgroundColor': '#f8fafc',
        'padding': '20px',
        'borderRadius': '10px',
        'marginBottom': '20px'
    })

def create_financial_section(financial_stats):
    """Create financial analysis section"""
    if not financial_stats:
        return html.Div()
    
    income_stats = financial_stats.get('income', {})
    
    return html.Div([
        html.H5("Financial Profile", style={'fontSize': '1.2rem', 'fontWeight': '600', 'marginBottom': '15px'}),
        html.Div([
            html.Div([
                html.Strong("Income Analysis:"),
                html.Ul([
                    html.Li(f"Average Income: {income_stats.get('mean', 0):,.0f} TND"),
                    html.Li(f"Median Income: {income_stats.get('median', 0):,.0f} TND"),
                    html.Li(f"Total Portfolio Value: {income_stats.get('total', 0):,.0f} TND"),
                    html.Li(f"Income Variability: {income_stats.get('std', 0):,.0f} TND (std dev)")
                ])
            ])
        ])
    ], style={
        'backgroundColor': '#f0fdf4',
        'padding': '20px',
        'borderRadius': '10px',
        'marginBottom': '20px'
    })

def create_behavioral_section(behavioral_stats):
    """Create behavioral patterns section"""
    if not behavioral_stats:
        return html.Div()
    
    channel_dist = behavioral_stats.get('channel_distribution', {})
    client_type_dist = behavioral_stats.get('client_type_distribution', {})
    
    return html.Div([
        html.H5("Behavioral Patterns", style={'fontSize': '1.2rem', 'fontWeight': '600', 'marginBottom': '15px'}),
        html.Div([
            html.Div([
                html.Strong("Channel Preferences:"),
                html.Ul([html.Li(f"{channel}: {count} clients") for channel, count in channel_dist.items()])
            ], style={'flex': '1', 'marginRight': '20px'}),
            html.Div([
                html.Strong("Client Types:"),
                html.Ul([html.Li(f"{client_type}: {count} clients") for client_type, count in client_type_dist.items()])
            ], style={'flex': '1'})
        ], style={'display': 'flex'})
    ], style={
        'backgroundColor': '#fef3c7',
        'padding': '20px',
        'borderRadius': '10px',
        'marginBottom': '20px'
    })

def create_insights_section(insights):
    """Create insights section"""
    if not insights:
        return html.Div()
    
    insight_items = []
    for insight in insights:
        icon_map = {
            'info': 'Info',
            'opportunity': 'Opportunity',
            'strength': 'Strength',
            'challenge': 'Challenge',
            'alert': 'Alert',
            'strategy': 'Strategy',
            'consideration': 'Note'
        }
        
        icon = icon_map.get(insight.get('type', 'info'), 'Info')
        category = insight.get('category', 'General')
        message = insight.get('message', '')
        
        insight_items.append(
            html.Div([
                html.Span(f"[{icon}] ", style={'fontSize': '1rem', 'marginRight': '8px', 'fontWeight': 'bold'}),
                html.Strong(f"{category}: ", style={'marginRight': '8px'}),
                html.Span(message)
            ], style={
                'padding': '12px',
                'backgroundColor': 'white',
                'borderRadius': '8px',
                'marginBottom': '8px',
                'borderLeft': f'4px solid {COLORS["primary"]}'
            })
        )
    
    return html.Div([
        html.H5("Key Insights from Data Analysis", style={'fontSize': '1.2rem', 'fontWeight': '600', 'marginBottom': '15px'}),
        html.Div(insight_items)
    ], style={
        'backgroundColor': '#f1f5f9',
        'padding': '20px',
        'borderRadius': '10px',
        'marginBottom': '20px'
    })

def create_segment_profile_section(segment_info):
    """Create segment profile section"""
    if not segment_info:
        return html.Div()
    
    return html.Div([
        html.H5("Segment Profile", style={'fontSize': '1.2rem', 'fontWeight': '600', 'marginBottom': '15px'}),
        html.P(segment_info.get('profile', 'No profile available'))
    ], style={
        'backgroundColor': '#e0f2fe',
        'padding': '20px',
        'borderRadius': '10px'
    })

def create_simulation_results_display(sim_results):
    """Create simulation results display"""
    projected = sim_results.get('projected_results', {})
    baseline = sim_results.get('baseline', {})
    
    return html.Div([
        html.H4("Regional Simulation Results", style={'marginBottom': '20px'}),
        
        # Key metrics
        html.Div([
            create_result_metric_card("ROI Projection", f"{projected.get('estimated_roi', 0):.1f}%", 
                                    "Return on Investment", COLORS['success']),
            create_result_metric_card("Satisfaction Impact", f"+{projected.get('satisfaction_improvement', 0):.1%}", 
                                    "Improvement Expected", COLORS['primary']),
            create_result_metric_card("Affected Clients", f"{projected.get('affected_clients', 0):,}", 
                                    "Total Reach", COLORS['accent']),
            create_result_metric_card("Implementation", f"{projected.get('implementation_timeline', 0)} months", 
                                    "Timeline", COLORS['warning'])
        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
            'gap': '15px',
            'marginBottom': '25px'
        }),
        
        # Budget utilization
        html.Div([
            html.H5("Budget Analysis", style={'marginBottom': '15px'}),
            html.P(f"Total Budget: {projected.get('budget_utilization', 0):,} TND"),
            html.P(f"Cost per Client: {projected.get('budget_utilization', 0) / max(projected.get('affected_clients', 1), 1):.0f} TND")
        ], style={
            'backgroundColor': '#f8fafc',
            'padding': '20px',
            'borderRadius': '10px'
        })
    ])

def create_result_metric_card(title, value, subtitle, color):
    """Create result metric card"""
    return html.Div([
        html.H6(title, style={'fontSize': '0.9rem', 'fontWeight': '600', 'marginBottom': '8px'}),
        html.Div(value, style={'fontSize': '1.4rem', 'fontWeight': '700', 'color': color, 'marginBottom': '4px'}),
        html.Div(subtitle, style={'fontSize': '0.8rem', 'color': COLORS['secondary']})
    ], style={
        'backgroundColor': 'white',
        'padding': '16px',
        'borderRadius': '8px',
        'textAlign': 'center',
        'border': f'2px solid {color}20'
    })

def create_opportunities_list(sim_results):
    """Create opportunities list from simulation results"""
    opportunities = []
    
    projected = sim_results.get('projected_results', {})
    roi = projected.get('estimated_roi', 0)
    
    if roi > 15:
        opportunities.append(
            html.Li("High ROI potential - strong business case for implementation")
        )
    
    if projected.get('satisfaction_improvement', 0) > 0.1:
        opportunities.append(
            html.Li("Significant satisfaction improvement expected")
        )
    
    # Add scenario-specific opportunities
    scenario = sim_results.get('scenario', '')
    if scenario == 'digital_push':
        opportunities.append(html.Li("Digital transformation opportunity in underserved segment"))
    elif scenario == 'branch_expansion':
        opportunities.append(html.Li("Market expansion potential in target region"))
    
    return opportunities if opportunities else [html.Li("No specific opportunities identified")]

def create_risk_factors_list(sim_results):
    """Create risk factors list"""
    risks = []
    
    projected = sim_results.get('projected_results', {})
    risk_factors = projected.get('risk_factors', [])
    
    for risk in risk_factors:
        risks.append(html.Li(risk))
    
    # Add ROI-based risks
    roi = projected.get('estimated_roi', 0)
    if roi < 0:
        risks.append(html.Li("Negative ROI projection - high financial risk"))
    elif roi < 5:
        risks.append(html.Li("Low ROI margin - sensitivity to market changes"))
    
    return risks if risks else [html.Li("No specific risks identified")]

def create_recommendations_list(sim_results):
    """Create recommendations list"""
    recommendations = sim_results.get('recommendations', [])
    
    rec_items = []
    for rec in recommendations:
        rec_items.append(html.Li(rec))
    
    return rec_items if rec_items else [html.Li("No specific recommendations available")]

def create_tunisia_choropleth(map_data, layer):
    """Create Tunisia choropleth map using real data only"""
    governorates = map_data.get('governorates', [])
    values = map_data.get('values', [])
    
    if not governorates or not values:
        # Return empty map with message
        fig = go.Figure()
        fig.add_annotation(
            text="No real data available for map visualization",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title=f"Tunisia Banking Map - {get_layer_title(layer)} (No Data)",
            height=600,
            showlegend=False
        )
        return fig
    
    # Create horizontal bar chart since we don't have GeoJSON coordinates
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=governorates,
        x=values,
        orientation='h',
        marker=dict(
            color=values,
            colorscale='Viridis',
            colorbar=dict(title=get_layer_title(layer))
        ),
        hovertemplate='<b>%{y}</b><br>' + 
                     f'{get_layer_title(layer)}: %{{x}}<br>' +
                     '<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Tunisia Banking Data - {get_layer_title(layer)} (Real Data)",
        xaxis_title=get_layer_title(layer),
        yaxis_title="Governorate",
        height=600,
        margin=dict(l=150)  # More space for governorate names
    )
    
    return fig

def get_layer_title(layer):
    """Get display title for map layer"""
    titles = {
        'client_density': 'Client Count',
        'revenue': 'Average Income (TND)',
        'digital_adoption': 'Digital Adoption (%)',
        'penetration': 'Client Count',
        'satisfaction': 'Satisfaction Score'
    }
    return titles.get(layer, layer.title())

def add_map_overlays(fig, overlays):
    """Add overlay layers to the map"""
    # This would add markers for branches, ATMs, etc.
    # For now, return the figure as-is since we need real location data
    return fig

def create_regional_comparison_table(comparison_data):
    """Create regional comparison table"""
    if not comparison_data:
        return html.Div("No comparison data available")
    
    # Create table headers
    headers = [
        html.Th("Governorate", style={'padding': '12px', 'fontWeight': 'bold'}),
        html.Th("Clients", style={'padding': '12px', 'fontWeight': 'bold', 'textAlign': 'center'}),
        html.Th("Avg Income", style={'padding': '12px', 'fontWeight': 'bold', 'textAlign': 'center'}),
        html.Th("Digital Rate", style={'padding': '12px', 'fontWeight': 'bold', 'textAlign': 'center'}),
        html.Th("Satisfaction", style={'padding': '12px', 'fontWeight': 'bold', 'textAlign': 'center'})
    ]
    
    # Create table rows
    rows = []
    for data in comparison_data:
        avg_income = data.get('avg_income', 0)
        digital_rate = data.get('digital_adoption_rate', 0)
        satisfaction = data.get('avg_satisfaction', 0)
        
        rows.append(html.Tr([
            html.Td(data['governorate'], style={'padding': '10px'}),
            html.Td(f"{data['client_count']:,}", style={'padding': '10px', 'textAlign': 'center'}),
            html.Td(f"{avg_income:.0f} TND" if avg_income > 0 else "N/A", style={'padding': '10px', 'textAlign': 'center'}),
            html.Td(f"{digital_rate:.1f}%" if digital_rate > 0 else "N/A", style={'padding': '10px', 'textAlign': 'center'}),
            html.Td(f"{satisfaction:.2f}" if satisfaction > 0 else "N/A", style={'padding': '10px', 'textAlign': 'center'})
        ]))
    
    return html.Table([
        html.Thead([html.Tr(headers)]),
        html.Tbody(rows)
    ], style={
        'width': '100%',
        'borderCollapse': 'collapse',
        'backgroundColor': 'white',
        'border': '1px solid #e2e8f0'
    })

def create_regional_radar_chart(comparison_data):
    """Create radar chart for regional performance"""
    if not comparison_data:
        return go.Figure()
    
    fig = go.Figure()
    
    # Select top 5 regions by client count
    top_regions = sorted(comparison_data, key=lambda x: x['client_count'], reverse=True)[:5]
    
    categories = ['Client Count', 'Avg Income', 'Digital Adoption', 'Satisfaction']
    
    for region in top_regions:
        # Scale values appropriately
        client_count = region['client_count']
        avg_income = region.get('avg_income', 0)
        digital_rate = region.get('digital_adoption_rate', 0)
        satisfaction = region.get('avg_satisfaction', 0)
        
        values = [
            min(client_count / 10, 100),  # Scale client count
            min(avg_income / 100, 100) if avg_income > 0 else 0,   # Scale income
            digital_rate if digital_rate > 0 else 0,
            satisfaction * 100 if satisfaction > 0 else 0
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=region['governorate']
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title="Regional Performance Comparison",
        height=400
    )
    
    return fig

def create_regional_trends_chart(comparison_data):
    """Create trends chart for regional analysis"""
    if not comparison_data:
        return go.Figure()
    
    # Sort by client count
    sorted_data = sorted(comparison_data, key=lambda x: x['client_count'], reverse=True)[:10]
    
    governorates = [d['governorate'] for d in sorted_data]
    client_counts = [d['client_count'] for d in sorted_data]
    digital_rates = [d.get('digital_adoption_rate', 0) for d in sorted_data]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add client count bars
    fig.add_trace(
        go.Bar(x=governorates, y=client_counts, name="Client Count", 
               marker_color=COLORS['primary']),
        secondary_y=False,
    )
    
    # Add digital adoption line if data available
    if any(rate > 0 for rate in digital_rates):
        fig.add_trace(
            go.Scatter(x=governorates, y=digital_rates, mode='lines+markers',
                      name="Digital Adoption %", line=dict(color=COLORS['success'])),
            secondary_y=True,
        )
    
    fig.update_xaxes(title_text="Governorate")
    fig.update_yaxes(title_text="Number of Clients", secondary_y=False)
    fig.update_yaxes(title_text="Digital Adoption Rate (%)", secondary_y=True)
    
    fig.update_layout(
        title="Regional Client Distribution and Digital Adoption",
        height=400
    )
    
    return fig