"""
Chart service for creating and configuring Plotly charts
"""
import plotly.graph_objs as go
import plotly.express as px
from config.colors import COLORS, CHART_COLORS
from config.settings import DASHBOARD_CONFIG


class ChartService:
    """Service class for creating various types of charts."""
    
    @staticmethod
    def create_client_growth_chart(months, clients):
        """Create client growth chart."""
        return ChartService.create_line_chart(
            months, clients,
            "Client Growth Over Time",
            "Month",
            "Number of Clients"
        )
    
    @staticmethod
    def create_revenue_chart(months, revenue):
        """Create monthly revenue chart."""
        return ChartService.create_bar_chart(
            months, revenue,
            "Monthly Revenue (€K)"
        )
    
    @staticmethod
    def create_segmentation_chart(segments, sizes):
        """Create client segmentation chart."""
        return ChartService.create_pie_chart(
            segments, sizes,
            "Client Segmentation"
        )
    
    @staticmethod
    def create_governorate_chart(governorates, counts):
        """Create governorate distribution chart."""
        return ChartService.create_choropleth_bar(
            governorates, counts,
            "Clients by Governorate"
        )
    
    @staticmethod
    def create_branch_distribution_chart(branch_types, branch_counts):
        """Create branch distribution chart."""
        return ChartService.create_pie_chart(
            branch_types, branch_counts,
            "Branch Type Distribution"
        )
    def create_line_chart(x_data, y_data, title, x_title, y_title, color=None):
        """Create a line chart."""
        color = color or CHART_COLORS['line_primary']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data,
            mode='lines+markers',
            name=title,
            line=dict(color=color, width=4),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_title,
            yaxis_title=y_title,
            template='plotly_white',
            height=DASHBOARD_CONFIG['chart_height']
        )
        
        return fig
    
    @staticmethod
    def create_bar_chart(x_data, y_data, title, color=None):
        """Create a bar chart."""
        color = color or CHART_COLORS['bar_primary']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x_data,
            y=y_data,
            name=title,
            marker_color=color
        ))
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            height=DASHBOARD_CONFIG['chart_height']
        )
        
        return fig
    
    @staticmethod
    def create_pie_chart(labels, values, title, hole=0.4):
        """Create a pie chart."""
        fig = go.Figure(go.Pie(
            labels=labels,
            values=values,
            hole=hole,
            marker=dict(colors=CHART_COLORS['pie_colors'])
        ))
        
        fig.update_layout(
            title=title,
            height=DASHBOARD_CONFIG['chart_height'],
            showlegend=True,
            template='plotly_white'
        )
        
        return fig
    
    @staticmethod
    def create_choropleth_bar(x_data, y_data, title):
        """Create a bar chart that simulates a choropleth map."""
        fig = px.bar(
            x=x_data,
            y=y_data,
            title=title,
            color=y_data,
            color_continuous_scale=CHART_COLORS['map_scale']
        )
        
        fig.update_layout(
            template='plotly_white',
            height=DASHBOARD_CONFIG['chart_height'],
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_economic_trends_chart(x_data, y_data):
        """Create economic trends chart."""
        return ChartService.create_line_chart(
            x_data, y_data, 
            "Economic Trends Over Time", 
            "Month", 
            "Economic Index"
        )
    
    @staticmethod
    def create_market_indicators_chart(indicators, values):
        """Create market indicators chart."""
        fig = px.bar(
            x=indicators,
            y=values,
            title="Key Market Indicators",
            color=values,
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        return fig
    
   # @staticmetho