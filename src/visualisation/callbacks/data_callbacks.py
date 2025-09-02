"""
Updated data_callbacks.py - Uses training data for the six charts
These charts remain independent of simulation results
"""
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from dash import Input, Output
from components.cards import create_metric_card
from config.colors import COLORS

def load_training_data():
    """Load training data for the six charts - independent of simulation"""
    data = {}
    
    # Load training data from correct path
    try:
        retail_path = Path('data/ctgan/training_data/retail_training_data_20250807_154910.csv')
        if retail_path.exists():
            data['retail_training'] = pd.read_csv(retail_path)
            print(f"Loaded retail training: {len(data['retail_training'])} rows")
        else:
            data['retail_training'] = None
    except Exception as e:
        print(f"Error loading retail training: {e}")
        data['retail_training'] = None
        
    try:
        corporate_path = Path('data/ctgan/training_data/corporate_training_data_20250807_155356.csv')
        if corporate_path.exists():
            data['corporate_training'] = pd.read_csv(corporate_path)
            print(f"Loaded corporate training: {len(data['corporate_training'])} rows")
        else:
            data['corporate_training'] = None
    except Exception as e:
        print(f"Error loading corporate training: {e}")
        data['corporate_training'] = None
    
    return data

def load_simulation_data():
    """Load simulation data for KPI cards - updates after simulation"""
    try:
        bundle_path = Path('output/dashboard_exports/dashboard_bundle_enhanced.json')
        if bundle_path.exists():
            with open(bundle_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading simulation data: {e}")
    return None

def register_data_callbacks(app):
    """Register data callbacks - charts use training data, KPIs use simulation data"""
    
    @app.callback(
        Output('data-source-info', 'children'),
        [Input('data-refresh-token', 'data'),
         Input('url', 'pathname')]
    )
    def update_overview_data(refresh_token, pathname):
        """Update overview data"""
        try:
            sim_data = load_simulation_data()
            training_data = load_training_data()
            
            # Data source info only
            if sim_data:
                total_agents = sim_data.get('quick_stats', {}).get('headline_numbers', {}).get('total_clients', 1000)
                active_agents = sim_data.get('quick_stats', {}).get('headline_numbers', {}).get('active_clients', 1000) 
                data_source_text = f"{total_agents:,} Total Clients ({active_agents:,} Active) - Live Simulation Data"
            elif training_data['retail_training'] is not None:
                retail_count = len(training_data['retail_training'])
                corporate_count = len(training_data['corporate_training']) if training_data['corporate_training'] is not None else 0
                total_training = retail_count + corporate_count
                data_source_text = f"{total_training:,} Training Records - {retail_count:,} Retail + {corporate_count:,} Corporate"
            else:
                data_source_text = "Sample data for demonstration"
            
            return data_source_text
            
        except Exception as e:
            print(f"Error in update_overview_data: {e}")
            return "Error loading data"

    def create_default_kpi_cards(data_type):
        """Create default KPI cards"""
        return [
            create_metric_card('ðŸ‘¥', 'Total Clients', '1,000', data_type, COLORS['primary']),
            create_metric_card('ðŸ˜Š', 'Satisfaction', '62.0%', data_type, COLORS['success']),
            create_metric_card('ðŸ“±', 'Digital Adoption', '46.9%', data_type, COLORS['warning']),
            create_metric_card('ðŸ”„', 'Retention Rate', '100.0%', data_type, COLORS['accent'])
        ]
    
    @app.callback(
        Output('governorate-distribution-chart', 'figure'),
        [Input('url', 'pathname')]  # Only load once - independent of simulation
    )
    def update_governorate_chart(pathname):
        """Update governorate distribution chart from training data"""
        try:
            training_data = load_training_data()
            
            if training_data['retail_training'] is not None:
                retail_df = training_data['retail_training']
                
                # Map governorate numbers to names (adjust based on your data)
                gov_mapping = {0: 'Tunis', 1: 'Sfax', 2: 'Sousse', 3: 'Ariana', 4: 'Bizerte', 
                              5: 'Nabeul', 6: 'Monastir', 7: 'Ben Arous', 8: 'Kairouan'}
                
                if 'governorate' in retail_df.columns:
                    gov_counts = retail_df['governorate'].value_counts()
                    
                    # Create governorate data with proper names
                    gov_data = []
                    for gov_num, count in gov_counts.items():
                        gov_name = gov_mapping.get(gov_num, f'Region {gov_num}')
                        gov_data.append({'governorate': gov_name, 'clients': count})
                    
                    gov_df = pd.DataFrame(gov_data).sort_values('clients', ascending=True)
                    
                    fig = px.bar(
                        gov_df, 
                        x='clients', 
                        y='governorate',
                        orientation='h',
                        title="Client Distribution by Governorate (Training Data)",
                        labels={'clients': 'Number of Clients', 'governorate': 'Governorate'},
                        color='clients',
                        color_continuous_scale='blues'
                    )
                    
                    fig.update_layout(
                        height=350,
                        showlegend=False,
                        font=dict(size=12),
                        plot_bgcolor='white',
                        paper_bgcolor='white'
                    )
                    
                    return fig
        except Exception as e:
            print(f"Error in governorate chart: {e}")
        
        # Fallback data
        sample_gov_data = [
            {'governorate': 'Tunis', 'clients': 311},
            {'governorate': 'Sfax', 'clients': 139},
            {'governorate': 'Sousse', 'clients': 107},
            {'governorate': 'Ariana', 'clients': 91},
            {'governorate': 'Bizerte', 'clients': 50}
        ]
        
        fig = px.bar(
            sample_gov_data, 
            x='clients', 
            y='governorate',
            orientation='h',
            title="Client Distribution by Governorate (Sample Data)",
            labels={'clients': 'Number of Clients', 'governorate': 'Governorate'},
            color='clients',
            color_continuous_scale='blues'
        )
        
        fig.update_layout(height=350, showlegend=False, font=dict(size=12), 
                         plot_bgcolor='white', paper_bgcolor='white')
        return fig
    
    @app.callback(
        Output('client-type-pie-chart', 'figure'),
        [Input('url', 'pathname')]
    )
    def update_client_type_chart(pathname):
        """Update client type pie chart from training data"""
        try:
            training_data = load_training_data()
            
            retail_count = len(training_data['retail_training']) if training_data['retail_training'] is not None else 0
            corporate_count = len(training_data['corporate_training']) if training_data['corporate_training'] is not None else 0
            
            if retail_count > 0 or corporate_count > 0:
                fig = px.pie(
                    values=[retail_count, corporate_count],
                    names=['Retail', 'Corporate'],
                    title="Client Segment Distribution (Training Data)",
                    color_discrete_sequence=[COLORS['primary'], COLORS['success']]
                )
                
                fig.update_traces(textinfo='percent+label', textfont_size=12)
                fig.update_layout(height=350, font=dict(size=12), 
                                 plot_bgcolor='white', paper_bgcolor='white')
                return fig
        except Exception as e:
            print(f"Error in client type chart: {e}")
        
        # Fallback
        fig = px.pie(
            values=[800, 200],
            names=['Retail', 'Corporate'],
            title="Client Segment Distribution (Sample Data)",
            color_discrete_sequence=[COLORS['primary'], COLORS['success']]
        )
        fig.update_traces(textinfo='percent+label', textfont_size=12)
        fig.update_layout(height=350, font=dict(size=12), plot_bgcolor='white', paper_bgcolor='white')
        return fig
    
    @app.callback(
        Output('satisfaction-tiers-chart', 'figure'),
        [Input('url', 'pathname')]
    )
    def update_satisfaction_chart(pathname):
        """Update satisfaction tiers chart from training data"""
        try:
            training_data = load_training_data()
            
            if training_data['retail_training'] is not None and 'satisfaction_score' in training_data['retail_training'].columns:
                retail_df = training_data['retail_training']
                satisfaction_scores = retail_df['satisfaction_score']
                
                # Create satisfaction tiers
                high_sat = len(satisfaction_scores[satisfaction_scores > 1.0])  # Normalized scores
                medium_sat = len(satisfaction_scores[(satisfaction_scores >= 0.0) & (satisfaction_scores <= 1.0)])
                low_sat = len(satisfaction_scores[satisfaction_scores < 0.0])
                
                satisfaction_data = [
                    {'tier': 'High', 'clients': high_sat},
                    {'tier': 'Medium', 'clients': medium_sat},
                    {'tier': 'Low', 'clients': low_sat}
                ]
                
                color_map = {'Low': '#ef4444', 'Medium': COLORS['warning'], 'High': COLORS['success']}
                
                fig = px.bar(
                    satisfaction_data,
                    x='tier',
                    y='clients',
                    title="Customer Satisfaction Distribution (Training Data)",
                    labels={'clients': 'Number of Clients', 'tier': 'Satisfaction Level'},
                    color='tier',
                    color_discrete_map=color_map
                )
                
                fig.update_layout(height=350, showlegend=False, font=dict(size=12),
                                 plot_bgcolor='white', paper_bgcolor='white')
                return fig
        except Exception as e:
            print(f"Error in satisfaction chart: {e}")
        
        # Fallback
        sample_satisfaction = [
            {'tier': 'High', 'clients': 168},
            {'tier': 'Medium', 'clients': 824},
            {'tier': 'Low', 'clients': 8}
        ]
        color_map = {'Low': '#ef4444', 'Medium': COLORS['warning'], 'High': COLORS['success']}
        
        fig = px.bar(
            sample_satisfaction,
            x='tier',
            y='clients',
            title="Customer Satisfaction Distribution (Sample Data)",
            color='tier',
            color_discrete_map=color_map
        )
        fig.update_layout(height=350, showlegend=False, font=dict(size=12),
                         plot_bgcolor='white', paper_bgcolor='white')
        return fig
    
    
    @app.callback(
        Output('channel-usage-chart', 'figure'),
        [Input('url', 'pathname')]
    )
    def update_channel_chart(pathname):
        #Update channel usage chart from training data
        try:
            training_data = load_training_data()
            
            if training_data['retail_training'] is not None and 'preferred_channel' in training_data['retail_training'].columns:
                retail_df = training_data['retail_training']
                channel_counts = retail_df['preferred_channel'].value_counts()
                
                # Map channel numbers to names
                channel_mapping = {0: 'Branch', 1: 'Digital', 2: 'Mobile', 3: 'Phone'}
                
                channel_data = []
                for channel_num, count in channel_counts.items():
                    channel_name = channel_mapping.get(channel_num, f'Channel {channel_num}')
                    percentage = (count / len(retail_df)) * 100
                    channel_data.append({'name': channel_name, 'value': percentage})
                
                fig = px.pie(
                    values=[d['value'] for d in channel_data],
                    names=[d['name'] for d in channel_data],
                    title="Channel Usage Distribution (Training Data)",
                    color_discrete_sequence=[COLORS['secondary'], COLORS['primary'], COLORS['warning'], COLORS['accent']]
                )
                
                fig.update_traces(textinfo='percent+label', textfont_size=12)
                fig.update_layout(height=350, font=dict(size=12), plot_bgcolor='white', paper_bgcolor='white')
                return fig
        except Exception as e:
            print(f"Error in channel chart: {e}")
        
        # Fallback
        fig = px.pie(
            values=[53.0, 47.0],
            names=['Branch', 'Digital'],
            title="Channel Usage Distribution (Sample Data)",
            color_discrete_sequence=[COLORS['secondary'], COLORS['primary']]
        )
        fig.update_traces(textinfo='percent+label', textfont_size=12)
        fig.update_layout(height=350, font=dict(size=12), plot_bgcolor='white', paper_bgcolor='white')
        return fig
   
    @app.callback(
        Output('age-demographics-chart', 'figure'),
        [Input('url', 'pathname')]
    )
    def update_age_demographics_chart(pathname):
        """Update age demographics chart from training data"""
        try:
            training_data = load_training_data()
            
            if (training_data['retail_training'] is not None and 
                'age_group' in training_data['retail_training'].columns and
                'digital_adoption' in training_data['retail_training'].columns):
                
                retail_df = training_data['retail_training']
                
                # Group by age and calculate statistics
                age_stats = retail_df.groupby('age_group').agg({
                    'client_id': 'count',
                    'digital_adoption': 'mean'
                }).reset_index()
                
                age_stats.columns = ['age_group', 'total_clients', 'avg_digital_adoption']
                age_stats['digital_clients'] = (age_stats['total_clients'] * age_stats['avg_digital_adoption']).astype(int)
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='Total Clients',
                    x=age_stats['age_group'],
                    y=age_stats['total_clients'],
                    marker_color=COLORS['secondary']
                ))
                
                fig.add_trace(go.Bar(
                    name='Digital Users',
                    x=age_stats['age_group'],
                    y=age_stats['digital_clients'],
                    marker_color=COLORS['warning']
                ))
                
                fig.update_layout(
                    title="Age Demographics vs Digital Adoption (Training Data)",
                    xaxis_title="Age Group",
                    yaxis_title="Number of Clients",
                    barmode='group',
                    height=350,
                    font=dict(size=12),
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
                
                return fig
        except Exception as e:
            print(f"Error in age demographics chart: {e}")
        
        # Fallback
        age_groups = ['18-25', '26-35', '36-45', '46-55', '55+']
        total_clients = [120, 280, 320, 180, 100]
        digital_clients = [102, 202, 186, 76, 25]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Total Clients', x=age_groups, y=total_clients, marker_color=COLORS['secondary']))
        fig.add_trace(go.Bar(name='Digital Users', x=age_groups, y=digital_clients, marker_color=COLORS['warning']))
        
        fig.update_layout(
            title="Age Demographics vs Digital Adoption (Sample Data)",
            xaxis_title="Age Group", yaxis_title="Number of Clients", barmode='group',
            height=350, font=dict(size=12), plot_bgcolor='white', paper_bgcolor='white'
        )
        return fig
    
    @app.callback(
        Output('value-tiers-chart', 'figure'),
        [Input('url', 'pathname')]
    )
    def update_value_tiers_chart(pathname):
        """Update value segmentation chart from training data"""
        try:
            training_data = load_training_data()
            
            if training_data['retail_training'] is not None and 'income_quintile' in training_data['retail_training'].columns:
                retail_df = training_data['retail_training']
                quintile_counts = retail_df['income_quintile'].value_counts()
                
                # Map quintiles to value tiers
                tier_mapping = {'Q1': 'Basic', 'Q2': 'Basic', 'Q3': 'Standard', 'Q4': 'Standard', 'Q5': 'Premium'}
                
                tier_counts = {}
                for quintile, count in quintile_counts.items():
                    tier = tier_mapping.get(quintile, 'Standard')
                    tier_counts[tier] = tier_counts.get(tier, 0) + count
                
                value_data = [{'tier': k, 'clients': v} for k, v in tier_counts.items()]
                
                color_map = {'Basic': COLORS['secondary'], 'Standard': COLORS['primary'], 'Premium': COLORS['accent']}
                
                fig = px.bar(
                    value_data,
                    x='tier',
                    y='clients',
                    title="Value Tier Distribution (Training Data)",
                    labels={'clients': 'Number of Clients', 'tier': 'Value Tier'},
                    color='tier',
                    color_discrete_map=color_map
                )
                
                fig.update_layout(height=350, showlegend=False, font=dict(size=12),
                                 plot_bgcolor='white', paper_bgcolor='white')
                return fig
        except Exception as e:
            print(f"Error in value tiers chart: {e}")
        
        # Fallback
        sample_value_data = [
            {'tier': 'Basic', 'clients': 755},
            {'tier': 'Standard', 'clients': 131},
            {'tier': 'Premium', 'clients': 114}
        ]
        color_map = {'Basic': COLORS['secondary'], 'Standard': COLORS['primary'], 'Premium': COLORS['accent']}
        
        fig = px.bar(
            sample_value_data, x='tier', y='clients',
            title="Value Tier Distribution (Sample Data)",
            color='tier', color_discrete_map=color_map
        )
        fig.update_layout(height=350, showlegend=False, font=dict(size=12),
                         plot_bgcolor='white', paper_bgcolor='white')
        return fig
    
    @app.callback(
        Output('retail-ratio-display', 'children'),
        [Input('retail-ratio-slider', 'value')]
    )
    def update_retail_ratio_display(value):
        """Update the retail ratio display"""
        try:
            retail_pct = int(value * 100)
            corporate_pct = 100 - retail_pct
            return f"Retail: {retail_pct}% | Corporate: {corporate_pct}%"
        except Exception as e:
            print(f"Error updating retail ratio display: {e}")
            return "Retail: 80% | Corporate: 20%"